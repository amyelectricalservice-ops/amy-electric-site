/* AMY Electric — lead files, CRM sync and the admin API (crm-handler.js).
 *
 * Routes wired in worker.js:
 *   POST /api/lead-files        project photos / PDF plans (multipart, private R2)
 *   GET  /api/admin/stats       aggregate funnel numbers
 *   GET  /api/admin/leads       recent leads (JSON)
 *   GET  /api/admin/leads.csv   CSV export
 *   POST /api/admin/lead/:id    status / owner / follow-up update
 *   POST /api/admin/spend       record ad spend
 *   POST /api/admin/jobs        record a quoted/booked job
 *   GET  /api/admin/report      weekly marketing report (+ recommendations)
 *   GET  /api/admin/file/:id    authenticated download of an uploaded file
 *   GET  /admin                 management dashboard (HTML, token protected)
 *
 * Uploads are validated by magic bytes, capped, hashed, stored under a random
 * key in a private bucket, and only downloadable with the admin token.
 */

import {
  buildLead, persistLead, linkFiles, recordEvent, markCrm,
  leadStats, sha256Hex, normalizePhone, normalizeEmail, scoreLead, uid,
} from './lead-store.js';

function R2(env) {
  return (env && (env.LEAD_FILES || env.BUCKET)) || null;
}

function DB(env) {
  return (env && (env.CRM_DB || env.DB)) || null;
}

const MAX_FILE_BYTES = 10 * 1024 * 1024;      // 10 MB per file
const MAX_FILES_PER_LEAD = 5;
const MAX_UPLOADS_PER_HOUR = 20;

const ALLOWED_TYPES = {
  'application/pdf': [0x25, 0x50, 0x44, 0x46],
  'image/jpeg': [0xff, 0xd8, 0xff],
  'image/png': [0x89, 0x50, 0x4e, 0x47],
};

function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extra },
  });
}

function bearer(request) {
  const h = request.headers.get('Authorization') || '';
  return h.startsWith('Bearer ') ? h.slice(7).trim() : '';
}

function timingSafeEqual(a, b) {
  const x = String(a || '');
  const y = String(b || '');
  if (x.length !== y.length) return false;
  let out = 0;
  for (let i = 0; i < x.length; i += 1) out |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return out === 0;
}

export function isAdmin(request, env) {
  const token = bearer(request) || new URL(request.url).searchParams.get('token') || '';
  if (!env.ADMIN_TOKEN) return false;
  if (timingSafeEqual(token, env.ADMIN_TOKEN)) return true;
  const basic = request.headers.get('Authorization') || '';
  if (basic.startsWith('Basic ') && env.ADMIN_USER) {
    try {
      const decoded = atob(basic.slice(6));
      const idx = decoded.indexOf(':');
      const user = decoded.slice(0, idx);
      const pass = decoded.slice(idx + 1);
      return timingSafeEqual(user, env.ADMIN_USER) && timingSafeEqual(pass, env.ADMIN_PASS || '');
    } catch {
      return false;
    }
  }
  return false;
}

function sniffType(bytes) {
  if (bytes[0] === 0x25 && bytes[1] === 0x50 && bytes[2] === 0x44 && bytes[3] === 0x46) return 'application/pdf';
  if (bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) return 'image/jpeg';
  if (bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47) return 'image/png';
  // RIFF....WEBP
  if (bytes[0] === 0x52 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x46
      && bytes[8] === 0x57 && bytes[9] === 0x45 && bytes[10] === 0x42 && bytes[11] === 0x50) return 'image/webp';
  // ISO-BMFF ftyp box: HEIC/HEIF brands
  if (bytes[4] === 0x66 && bytes[5] === 0x74 && bytes[6] === 0x79 && bytes[7] === 0x70) return 'image/heic';
  return '';
}

function safeName(name) {
  const base = String(name || 'file')
    .replace(/[\\/]+/g, '-')
    .replace(/[\x00-\x1f\x7f]+/g, '')
    .replace(/[^A-Za-z0-9._ ()-]+/g, '_')
    .replace(/^\.+/, '')
    .trim()
    .slice(-120);
  return base || 'file';
}

/** Logged-in upload: one file per request; client loops up to 5 times. */
export async function handleLeadFiles(request, env, ctx) {
  if (request.method !== 'POST') return json({ success: false, message: 'Method not allowed' }, 405);
  if (!R2(env)) return json({ success: false, message: 'File uploads are not configured.' }, 503);

  const ip = request.headers.get('CF-Connecting-IP') || '';
  const ipHash = await sha256Hex(`${ip}|amy-lead-files`);

  if (DB(env)) {
    try {
      const since = new Date(Date.now() - 3600000).toISOString();
      const row = await DB(env).prepare(
        'SELECT COUNT(*) AS n FROM lead_files WHERE ip_hash = ? AND created_at >= ?'
      ).bind(ipHash, since).first();
      if (row && Number(row.n) >= MAX_UPLOADS_PER_HOUR) {
        return json({ success: false, message: 'Too many uploads. Please call (818) 302-5614.' }, 429);
      }
    } catch { /* rate limiting is best-effort */ }
  }

  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ success: false, message: 'Could not read the upload.' }, 400);
  }

  const file = form.get('file');
  if (!file || typeof file === 'string' || typeof file.arrayBuffer !== 'function') {
    return json({ success: false, message: 'No file received.' }, 400);
  }
  if (file.size > MAX_FILE_BYTES) {
    return json({ success: false, message: 'Each file must be 10 MB or smaller.' }, 413);
  }
  if (file.size === 0) {
    return json({ success: false, message: 'That file is empty.' }, 400);
  }

  const buf = new Uint8Array(await file.arrayBuffer());
  const sniffed = sniffType(buf);
  if (!sniffed) {
    return json({ success: false, message: 'Please upload a JPG, PNG, WebP, HEIC or PDF file.' }, 415);
  }
  const declared = String(file.type || '').toLowerCase();
  // Trust the bytes, not the browser: allow a declared/actual mismatch only
  // inside the image family (HEIC is frequently mislabelled).
  if (declared && !declared.startsWith('image/') && declared !== 'application/pdf') {
    return json({ success: false, message: 'Unsupported file type.' }, 415);
  }
  if (declared === 'application/pdf' && sniffed !== 'application/pdf') {
    return json({ success: false, message: 'That file is not a valid PDF.' }, 415);
  }

  const token = String(form.get('upload_token') || '');
  if (!/^[a-zA-Z0-9-]{16,64}$/.test(token)) {
    return json({ success: false, message: 'Upload session expired — please reload the page.' }, 400);
  }

  const id = uid('file');
  const sha = await sha256Hex(buf);
  const now = new Date();
  const key = `leads/${now.toISOString().slice(0, 10)}/${token}/${id}-${safeName(file.name)}`;

  try {
    await R2(env).put(key, buf, {
      httpMetadata: { contentType: sniffed, cacheControl: 'private, no-store' },
      customMetadata: { sha256: sha, original: safeName(file.name) },
    });
  } catch (err) {
    console.warn('R2 put failed:', err && err.message);
    return json({ success: false, message: 'Upload failed. Please try again or call us.' }, 500);
  }

  if (DB(env)) {
    try {
      await DB(env).prepare(
        `INSERT INTO lead_files (id, upload_token, created_at, r2_key, filename, content_type, bytes, sha256, status, ip_hash)
         VALUES (?,?,?,?,?,?,?,?, 'pending', ?)`
      ).bind(id, token, now.toISOString(), key, safeName(file.name), sniffed, buf.length, sha, ipHash).run();
    } catch (err) {
      console.warn('lead_files insert failed:', err && err.message);
      // The object is orphaned but unreachable without an admin token.
      return json({ success: false, message: 'Upload could not be recorded. Please retry.' }, 500);
    }
  }

  return json({
    success: true,
    upload_token: token,
    file: { id, name: safeName(file.name), size: buf.length, type: sniffed },
  });
}

/* ---------------------------------------------------------------- HubSpot */

async function hubspot(env, path, init = {}) {
  const res = await fetch(`https://api.hubapi.com${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${env.HUBSPOT_TOKEN}`,
      'Content-Type': 'application/json',
      ...(init.headers || {}),
    },
  });
  const text = await res.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = { raw: text.slice(0, 500) }; }
  return { ok: res.ok, status: res.status, body };
}

function splitName(name) {
  const parts = String(name || '').trim().split(/\s+/);
  return { firstname: parts[0] || '', lastname: parts.slice(1).join(' ') || '' };
}

function followUpIso(urgency) {
  const now = Date.now();
  if (urgency === 'emergency') return new Date(now + 15 * 60000).toISOString();
  if (urgency === 'same-day') return new Date(now + 2 * 3600000).toISOString();
  const d = new Date(now + 24 * 3600000);
  d.setUTCHours(17, 0, 0, 0); // 9am Pacific during DST
  return d.toISOString();
}

async function findHubSpotContact(env, lead) {
  const filters = [];
  if (lead.email_norm) filters.push({ propertyName: 'email', operator: 'EQ', value: lead.email_norm });
  if (lead.phone_norm) filters.push({ propertyName: 'phone', operator: 'EQ', value: lead.phone });
  if (!filters.length) return null;
  const res = await hubspot(env, '/crm/v3/objects/contacts/search', {
    method: 'POST',
    body: JSON.stringify({ filterGroups: filters.slice(0, 1).map((f) => ({ filters: [f] })), limit: 1 }),
  });
  if (res.ok && res.body && Array.isArray(res.body.results) && res.body.results.length) {
    return res.body.results[0].id;
  }
  return null;
}

/** Best-effort HubSpot sync. Never throws; records the outcome in D1. */
export async function syncLeadToHubSpot(env, lead) {
  if (!env.HUBSPOT_TOKEN) return { ok: false, reason: 'not-configured' };
  if (lead.duplicate_of) return { ok: false, reason: 'duplicate' };

  try {
    const { firstname, lastname } = splitName(lead.name);
    let contactId = await findHubSpotContact(env, lead);

    if (!contactId) {
      const created = await hubspot(env, '/crm/v3/objects/contacts', {
        method: 'POST',
        body: JSON.stringify({
          properties: {
            email: lead.email_norm || undefined,
            phone: lead.phone || undefined,
            firstname,
            lastname,
            city: lead.city || undefined,
            lifecyclestage: 'lead',
            hs_lead_status: 'NEW',
            website: lead.source_page ? `https://amyelectric.com${lead.source_page}` : undefined,
          },
        }),
      });
      if (!created.ok) {
        return { ok: false, reason: `contact ${created.status}`, detail: created.body };
      }
      contactId = created.body.id;
    }

    const pipeline = lead.segment === 'commercial'
      ? (env.HUBSPOT_PIPELINE_COMMERCIAL || 'default')
      : (env.HUBSPOT_PIPELINE_RESIDENTIAL || 'default');
    const stage = lead.segment === 'commercial'
      ? (env.HUBSPOT_STAGE_COMMERCIAL || 'appointmentscheduled')
      : (env.HUBSPOT_STAGE_RESIDENTIAL || 'appointmentscheduled');

    const deal = await hubspot(env, '/crm/v3/objects/deals', {
      method: 'POST',
      body: JSON.stringify({
        properties: {
          dealname: `${lead.segment === 'commercial' ? 'Commercial' : 'Residential'} — ${lead.service || 'Electrical'} — ${lead.name}`,
          pipeline,
          dealstage: stage,
          description: [
            `Score ${lead.score}/100 (${lead.urgency})`,
            `Service: ${lead.service || 'unspecified'}`,
            `City: ${lead.city || 'unspecified'}`,
            lead.message ? `Message: ${lead.message}` : '',
            lead.estimate_json ? `Indicative estimate: ${lead.estimate_json}` : '',
            lead.gclid ? `Google Ads click: ${lead.gclid}` : '',
          ].filter(Boolean).join('\n').slice(0, 60000),
        },
      }),
    });

    let dealId = '';
    if (deal.ok) {
      dealId = deal.body.id;
      await hubspot(env, `/crm/v4/objects/deals/${dealId}/associations/default/contacts/${contactId}`, { method: 'PUT' });
    }

    const task = await hubspot(env, '/crm/v3/objects/tasks', {
      method: 'POST',
      body: JSON.stringify({
        properties: {
          hs_task_subject: `Follow up: ${lead.name} — ${lead.service || 'electrical'}`,
          hs_task_body: `Score ${lead.score}/100 · ${lead.urgency}\nPhone: ${lead.phone}\nCity: ${lead.city || 'n/a'}`,
          hs_task_status: 'NOT_STARTED',
          hs_task_type: 'TODO',
          hs_timestamp: followUpIso(lead.urgency),
        },
      }),
    });
    const taskId = task.ok ? task.body.id : '';
    if (taskId) {
      await hubspot(env, `/crm/v4/objects/tasks/${taskId}/associations/default/contacts/${contactId}`, { method: 'PUT' });
    }

    await markCrm(env, lead.id, {
      status: 'synced', contactId, dealId, taskId, provider: 'hubspot',
    });
    return { ok: true, contactId, dealId, taskId };
  } catch (err) {
    await markCrm(env, lead.id, { status: 'failed', error: err && err.message, provider: 'hubspot' });
    return { ok: false, reason: 'exception' };
  }
}

/** Legacy webhook path (GHL / Zapier). Kept so existing automation still runs. */
export async function syncLeadToWebhook(env, lead) {
  if (!env.CRM_WEBHOOK_URL) return { ok: false, reason: 'not-configured' };
  try {
    const res = await fetch(env.CRM_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        source: 'amyelectric.com',
        lead_id: lead.id,
        submittedAt: lead.created_at,
        contact: { name: lead.name, email: lead.email, phone: lead.phone, city: lead.city },
        project: { service: lead.service, request_type: lead.request_type, message: lead.message },
        classification: { segment: lead.segment, urgency: lead.urgency, score: lead.score },
        attribution: {
          source_page: lead.source_page, utm_source: lead.utm_source,
          utm_medium: lead.utm_medium, utm_campaign: lead.utm_campaign, gclid: lead.gclid,
        },
        estimate: lead.estimate_json || null,
      }),
    });
    return { ok: res.ok };
  } catch {
    return { ok: false, reason: 'exception' };
  }
}

/* ------------------------------------------------------------- admin API */

function csvEscape(v) {
  const s = String(v == null ? '' : v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export async function handleAdminApi(request, env) {
  if (!isAdmin(request, env)) return json({ success: false, message: 'Unauthorized' }, 401);
  const url = new URL(request.url);
  const path = url.pathname;

  if (path === '/api/admin/stats') {
    const days = Math.min(365, Math.max(1, Number(url.searchParams.get('days')) || 30));
    return json({ success: true, stats: await leadStats(env, days) });
  }

  if (path === '/api/admin/leads') {
    if (!DB(env)) return json({ success: true, leads: [] });
    const limit = Math.min(200, Math.max(1, Number(url.searchParams.get('limit')) || 50));
    const status = url.searchParams.get('status') || '';
    const crm = url.searchParams.get('crm') || '';
    let rows;
    if (crm === 'pending') {
      // Anything not yet delivered to the CRM, oldest first so the local
      // EspoCRM agent drains the backlog in order.
      rows = await DB(env).prepare(
        `SELECT * FROM leads
          WHERE crm_status IN ('pending','failed','skipped') AND duplicate_of = ''
          ORDER BY created_at ASC LIMIT ?`
      ).bind(limit).all();
    } else if (status) {
      rows = await DB(env).prepare(
        `SELECT * FROM leads WHERE status = ? ORDER BY created_at DESC LIMIT ?`
      ).bind(status, limit).all();
    } else {
      rows = await DB(env).prepare(
        `SELECT * FROM leads ORDER BY created_at DESC LIMIT ?`
      ).bind(limit).all();
    }
    return json({ success: true, leads: (rows && rows.results) || [] });
  }

  if (path === '/api/admin/leads.csv') {
    if (!DB(env)) return new Response('id\n', { headers: { 'Content-Type': 'text/csv' } });
    const rows = await DB(env).prepare(
      `SELECT id, created_at, name, phone, email, city, service, segment, urgency, score,
              status, source_page, utm_source, utm_campaign, crm_status, duplicate_of
         FROM leads ORDER BY created_at DESC LIMIT 5000`
    ).all();
    const cols = ['id', 'created_at', 'name', 'phone', 'email', 'city', 'service', 'segment',
      'urgency', 'score', 'status', 'source_page', 'utm_source', 'utm_campaign', 'crm_status', 'duplicate_of'];
    const lines = [cols.join(',')];
    for (const r of (rows.results || [])) lines.push(cols.map((c) => csvEscape(r[c])).join(','));
    return new Response(lines.join('\n'), {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="amy-leads.csv"',
        'Cache-Control': 'no-store',
      },
    });
  }

  if (path.startsWith('/api/admin/lead/') && request.method === 'POST') {
    if (!DB(env)) return json({ success: false, message: 'No database' }, 503);
    const id = path.slice('/api/admin/lead/'.length);
    let body = {};
    try { body = await request.json(); } catch { body = {}; }
    const allowed = ['status', 'owner', 'follow_up_at'];
    const sets = [];
    const vals = [];
    for (const k of allowed) {
      if (typeof body[k] === 'string') { sets.push(`${k} = ?`); vals.push(body[k].slice(0, 200)); }
    }
    if (!sets.length) return json({ success: false, message: 'Nothing to update' }, 400);
    sets.push('updated_at = ?'); vals.push(new Date().toISOString());
    await DB(env).prepare(`UPDATE leads SET ${sets.join(', ')} WHERE id = ?`).bind(...vals, id).run();
    return json({ success: true });
  }

  if (path.startsWith('/api/admin/lead/') && path.endsWith('/crm') && request.method === 'POST') {
    if (!DB(env)) return json({ success: false, message: 'No database' }, 503);
    const id = path.slice('/api/admin/lead/'.length, -'/crm'.length);
    let b = {};
    try { b = await request.json(); } catch { b = {}; }
    const status = ['synced', 'failed', 'skipped', 'pending'].includes(b.status) ? b.status : 'failed';
    await markCrm(env, id, {
      status,
      contactId: typeof b.contact_id === 'string' ? b.contact_id : '',
      dealId: typeof b.deal_id === 'string' ? b.deal_id : '',
      taskId: typeof b.task_id === 'string' ? b.task_id : '',
      error: typeof b.error === 'string' ? b.error : '',
      provider: typeof b.provider === 'string' ? b.provider : 'espocrm',
    });
    return json({ success: true });
  }

  if (path === '/api/admin/spend' && request.method === 'POST') {
    let b = {};
    try { b = await request.json(); } catch { b = {}; }
    const day = String(b.day || '').slice(0, 10);
    const channel = String(b.channel || '').slice(0, 40);
    const campaign = String(b.campaign || '').slice(0, 120);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day) || !channel || !campaign) {
      return json({ success: false, message: 'day, channel and campaign are required' }, 400);
    }
    await DB(env).prepare(
      `INSERT INTO ad_spend (id, day, channel, campaign, spend_cents, impressions, clicks, leads, qualified, notes, created_at)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)
       ON CONFLICT(day, channel, campaign) DO UPDATE SET
         spend_cents = excluded.spend_cents, impressions = excluded.impressions,
         clicks = excluded.clicks, leads = excluded.leads, qualified = excluded.qualified,
         notes = excluded.notes`
    ).bind(uid('spend'), day, channel, campaign,
      Math.max(0, Math.round(Number(b.spend_cents) || 0)),
      Math.max(0, Math.round(Number(b.impressions) || 0)),
      Math.max(0, Math.round(Number(b.clicks) || 0)),
      Math.max(0, Math.round(Number(b.leads) || 0)),
      Math.max(0, Math.round(Number(b.qualified) || 0)),
      String(b.notes || '').slice(0, 500), new Date().toISOString()).run();
    return json({ success: true });
  }

  if (path === '/api/admin/jobs' && request.method === 'POST') {
    let b = {};
    try { b = await request.json(); } catch { b = {}; }
    if (!b.lead_id && !b.service) return json({ success: false, message: 'lead_id or service required' }, 400);
    const now = new Date().toISOString();
    const id = uid('job');
    await DB(env).prepare(
      `INSERT INTO jobs (id, lead_id, created_at, updated_at, status, service, quoted_cents, revenue_cents, scheduled_at, completed_at, notes)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)`
    ).bind(id, b.lead_id || null, now, now,
      String(b.status || 'quoted').slice(0, 20), String(b.service || '').slice(0, 60),
      Math.max(0, Math.round(Number(b.quoted_cents) || 0)),
      Math.max(0, Math.round(Number(b.revenue_cents) || 0)),
      b.scheduled_at || null, b.completed_at || null, String(b.notes || '').slice(0, 1000)).run();
    return json({ success: true, id });
  }

  if (path === '/api/admin/report') {
    const days = Math.min(180, Math.max(7, Number(url.searchParams.get('days')) || 7));
    return json({ success: true, report: await weeklyReport(env, days) });
  }

  if (path.startsWith('/api/admin/file/')) {
    if (!R2(env)) return json({ success: false, message: 'No storage' }, 503);
    const id = path.slice('/api/admin/file/'.length);
    if (!/^file_[a-f0-9]{8,40}$/.test(id)) return json({ success: false, message: 'Bad id' }, 400);
    const row = await DB(env).prepare('SELECT * FROM lead_files WHERE id = ?').bind(id).first();
    if (!row) return json({ success: false, message: 'Not found' }, 404);
    const obj = await R2(env).get(row.r2_key);
    if (!obj) return json({ success: false, message: 'Object missing' }, 404);
    return new Response(obj.body, {
      headers: {
        'Content-Type': row.content_type,
        'Content-Disposition': `attachment; filename="${String(row.filename).replace(/"/g, '')}"`,
        'Cache-Control': 'private, no-store',
        'X-Content-Type-Options': 'nosniff',
      },
    });
  }

  if (path === '/api/admin/prospects') {
    if (!DB(env)) return json({ success: false, message: 'No database' }, 503);
    if (request.method === 'GET') {
      const rows = await DB(env).prepare(
        'SELECT * FROM prospects ORDER BY score DESC, created_at DESC LIMIT 200'
      ).all();
      return json({ success: true, prospects: (rows && rows.results) || [] });
    }
    if (request.method === 'POST') {
      let b = {};
      try { b = await request.json(); } catch { b = {}; }
      const items = Array.isArray(b.prospects) ? b.prospects.slice(0, 500) : [b];
      const now = new Date().toISOString();
      let saved = 0;
      for (const item of items) {
        const permitRef = String(item.permit_ref || '').slice(0, 80);
        const source = String(item.source || 'manual').slice(0, 40);
        if (!item.company && !item.contact_name && !permitRef) continue;
        try {
          await DB(env).prepare(
            `INSERT INTO prospects (id, created_at, updated_at, company, contact_name, email, phone,
              city, segment, source, permit_ref, project_address, zip, project_type, score, status, notes)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
             ON CONFLICT(source, permit_ref) DO UPDATE SET
               updated_at = excluded.updated_at,
               score = MAX(prospects.score, excluded.score),
               project_type = COALESCE(NULLIF(excluded.project_type,''), prospects.project_type),
               notes = COALESCE(NULLIF(excluded.notes,''), prospects.notes)`
          ).bind(
            uid('pros'), now, now,
            String(item.company || '').slice(0, 160),
            String(item.contact_name || '').slice(0, 120),
            String(item.email || '').slice(0, 160),
            String(item.phone || '').slice(0, 40),
            String(item.city || '').slice(0, 80),
            String(item.segment || 'general-contractor').slice(0, 40),
            source, permitRef,
            String(item.project_address || '').slice(0, 200),
            String(item.zip || '').slice(0, 12),
            String(item.project_type || '').slice(0, 120),
            Math.max(0, Math.min(100, Math.round(Number(item.score) || 0))),
            String(item.status || 'new').slice(0, 20),
            String(item.notes || '').slice(0, 1000),
          ).run();
          saved += 1;
        } catch { /* skip one bad row */ }
      }
      return json({ success: true, saved });
    }
  }

  if (path === '/api/admin/qualify' && request.method === 'POST') {
    let b = {};
    try { b = await request.json(); } catch { b = {}; }
    const result = await aiQualify(env, b);
    return json({ success: true, qualification: result, draft_reply: draftReply({
      name: b.name, service: b.service, urgency: result.urgency,
    }) });
  }

  if (path === '/api/admin/draft-estimate' && request.method === 'POST') {
    let b = {};
    try { b = await request.json(); } catch { b = {}; }
    let lead = b;
    if (b.lead_id && DB(env)) {
      const row = await DB(env).prepare('SELECT * FROM leads WHERE id = ?').bind(b.lead_id).first();
      if (row) lead = row;
    }
    return json({ success: true, estimate: draftEstimate(lead), reply: draftReply(lead) });
  }

  return json({ success: false, message: 'Not found' }, 404);
}

/* -------------------------------------------------------- weekly report */

export async function weeklyReport(env, days = 7) {
  const stats = (await leadStats(env, days)) || {};
  const t = stats.totals || {};
  const spend = stats.spend || {};
  const revenue = stats.revenue || {};
  const total = Number(t.total) || 0;
  const won = Number(t.won) || 0;
  const spendCents = Number(spend.spend_cents) || 0;
  const qualified = Number(spend.qualified) || 0;
  const cpl = total ? Math.round(spendCents / total) : 0;
  const cpql = qualified ? Math.round(spendCents / qualified) : 0;
  const closeRate = total ? Math.round((won / total) * 100) : 0;

  const recommendations = [];
  if (!spendCents) recommendations.push('No ad spend recorded — add rows with POST /api/admin/spend so cost-per-lead is real.');
  if (total && Number(t.commercial) / total < 0.2) recommendations.push('Commercial share is under 20% — review the commercial landing page and Ads campaign targeting.');
  if (total && Number(t.emergency) / total < 0.1) recommendations.push('Few emergency-intent leads — the same-day/emergency pages may need stronger above-the-fold dispatch messaging.');
  if (Number(t.avg_score) && Number(t.avg_score) < 50) recommendations.push('Average lead score is low — tighten form qualification or add a service/urgency question.');
  if (closeRate < 15) recommendations.push('Close rate under 15% — audit follow-up speed (emergency leads should be called within 15 minutes).');
  if (!recommendations.length) recommendations.push('Funnel metrics look healthy for this window — keep monitoring weekly.');

  return {
    window_days: days,
    generated_at: new Date().toISOString(),
    leads: {
      total, commercial: Number(t.commercial) || 0, emergency: Number(t.emergency) || 0,
      quoted: Number(t.quoted) || 0, won, avg_score: Math.round(Number(t.avg_score) || 0),
      close_rate_pct: closeRate,
    },
    media: {
      spend_usd: Math.round(spendCents / 100), clicks: Number(spend.clicks) || 0,
      impressions: Number(spend.impressions) || 0, qualified,
      cost_per_lead_usd: Math.round(cpl / 100), cost_per_qualified_lead_usd: Math.round(cpql / 100),
    },
    revenue: {
      completed_jobs: Number(revenue.jobs) || 0,
      revenue_usd: Math.round((Number(revenue.revenue_cents) || 0) / 100),
    },
    recommendations,
  };
}

/* ------------------------------------------------------------ dashboard */

const DASH_CSS = `
:root{--navy:#0b1628;--navy2:#122040;--gold:#f5a623;--ink:#f4f1eb;--muted:#98a6b8;--line:#1e3055}
*{box-sizing:border-box}body{margin:0;background:var(--navy);color:var(--ink);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{background:var(--navy2);border-bottom:3px solid var(--line);padding:18px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
h1{font-size:20px;margin:0;letter-spacing:.02em}h1 span{color:var(--gold)}
main{max-width:1200px;margin:0 auto;padding:24px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:26px}
.card{background:var(--navy2);border:1px solid var(--line);border-radius:8px;padding:16px}
.card b{display:block;font-size:28px;color:var(--gold);line-height:1.1}
.card span{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
table{width:100%;border-collapse:collapse;background:var(--navy2);border-radius:8px;overflow:hidden;font-size:14px}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);background:#0f1b31}
tr:last-child td{border-bottom:none}
.pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:700;letter-spacing:.04em}
.hi{background:rgba(245,166,35,.18);color:var(--gold)}.mid{background:rgba(61,214,245,.15);color:#3dd6f5}.lo{background:rgba(152,166,184,.15);color:var(--muted)}
a{color:var(--gold)}.muted{color:var(--muted);font-size:13px}
`;

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

export async function handleAdminPage(request, env) {
  if (!isAdmin(request, env)) {
    return new Response('Unauthorized', {
      status: 401,
      headers: { 'WWW-Authenticate': 'Basic realm="AMY Electric admin"' },
    });
  }
  const token = new URL(request.url).searchParams.get('token') || '';
  const qs = token ? `?token=${encodeURIComponent(token)}` : '';
  const stats = (await leadStats(env, 30)) || {};
  const t = stats.totals || {};
  let leads = [];
  if (DB(env)) {
    const rows = await DB(env).prepare(
      'SELECT * FROM leads ORDER BY created_at DESC LIMIT 40'
    ).all();
    leads = rows.results || [];
  }
  const rows = leads.map((l) => {
    const cls = Number(l.score) >= 70 ? 'hi' : Number(l.score) >= 45 ? 'mid' : 'lo';
    return `<tr>
      <td>${esc((l.created_at || '').slice(0, 16).replace('T', ' '))}</td>
      <td>${esc(l.name)}<div class="muted">${esc(l.phone)}</div></td>
      <td>${esc(l.service || '—')}<div class="muted">${esc(l.city || '')}</div></td>
      <td><span class="pill ${cls}">${esc(l.score)}</span></td>
      <td>${esc(l.segment)}<div class="muted">${esc(l.urgency)}</div></td>
      <td>${esc(l.status)}</td>
      <td>${esc(l.crm_status)}</td>
      <td>${esc((l.source_page || '').slice(0, 40))}</td>
    </tr>`;
  }).join('');

  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>AMY Electric — Leads</title>
<style>${DASH_CSS}</style></head><body>
<header><h1>AMY Electric <span>Lead Desk</span></h1>
<div class="muted"><a href="/api/admin/leads.csv${qs}">Download CSV</a> · <a href="/api/admin/report${qs}">Weekly report JSON</a> · 30-day view</div></header>
<main>
<div class="cards">
  <div class="card"><b>${Number(t.total) || 0}</b><span>Leads (30d)</span></div>
  <div class="card"><b>${Number(t.commercial) || 0}</b><span>Commercial</span></div>
  <div class="card"><b>${Number(t.emergency) || 0}</b><span>Emergency</span></div>
  <div class="card"><b>${Math.round(Number(t.avg_score) || 0)}</b><span>Avg score</span></div>
  <div class="card"><b>${Number(t.won) || 0}</b><span>Won</span></div>
</div>
<table><thead><tr><th>When</th><th>Contact</th><th>Project</th><th>Score</th><th>Type</th><th>Status</th><th>CRM</th><th>Source</th></tr></thead>
<tbody>${rows || '<tr><td colspan="8" class="muted">No leads recorded yet.</td></tr>'}</tbody></table>
<p class="muted">Uploaded photos and plans are downloadable from the lead record via the admin API.</p>
</main></body></html>`;
  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow' },
  });
}

/* ---------------------------------------------- AI-assisted qualification */

/** Workers AI classification with a deterministic fallback. */
export async function aiQualify(env, input) {
  const rules = scoreLead({
    service: input.service, message: input.message, request_type: input.request_type,
    email: input.email, city: input.city, phone: input.phone,
  });
  if (!env.AI) return { ...rules, source: 'rules' };
  try {
    const prompt = `You are a lead qualifier for an electrical contractor in Los Angeles.
Return STRICT JSON only: {"segment":"residential|commercial","urgency":"emergency|same-day|standard|planning","score":0-100,"summary":"one sentence"}.
Service: ${input.service || 'unknown'}
City: ${input.city || 'unknown'}
Message: ${String(input.message || '').slice(0, 800)}`;
    const out = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 180,
    });
    const text = String((out && out.response) || '');
    const match = text.match(/\{[\s\S]*\}/);
    if (match) {
      const parsed = JSON.parse(match[0]);
      const score = Math.max(0, Math.min(100, Math.round(Number(parsed.score) || rules.score)));
      return {
        score,
        segment: parsed.segment === 'commercial' ? 'commercial' : 'residential',
        urgency: ['emergency', 'same-day', 'standard', 'planning'].includes(parsed.urgency) ? parsed.urgency : rules.urgency,
        reasons: [String(parsed.summary || 'AI qualification').slice(0, 200)],
        source: 'workers-ai',
      };
    }
  } catch {
    /* fall back to rules */
  }
  return { ...rules, source: 'rules' };
}

/** Draft an estimate skeleton from the submitted project info (AE-042). */
export function draftEstimate(lead) {
  const service = String(lead.service || '');
  const text = `${lead.message || ''}`.toLowerCase();
  const lines = [];
  let low = 0;
  let high = 0;
  if (service.includes('panel')) { lines.push('200A service upgrade (panel, meter, grounding)'); low = 2500; high = 4500; }
  else if (service.includes('ev') || service.includes('tesla')) { lines.push('Level 2 EV charger circuit + install'); low = 350; high = 1200; }
  else if (service.includes('rewir')) { lines.push('Whole-home rewiring (per room / whole house)'); low = 8000; high = 18000; }
  else if (service.includes('repair')) { lines.push('Troubleshooting + repair labor'); low = 150; high = 450; }
  else { lines.push('Electrical service (scope TBD on site)'); low = 150; high = 600; }

  if (/permit|ladbs/.test(text)) lines.push('Permit + inspection coordination (included)');
  if (/drywall|patch|paint/.test(text)) lines.push('Drywall patching excluded unless quoted');
  if (/attic|crawl|conduit/.test(text)) lines.push('Access/conduit conditions to confirm on site');

  return {
    service: service || 'general',
    rangeLow: low,
    rangeHigh: high,
    currency: 'USD',
    lines,
    assumptions: ['Pricing is indicative until an on-site assessment.'],
    permitNote: 'Permits included where required by LADBS; HOA/landlord approvals are the owner\'s responsibility.',
  };
}

/** Draft a customer-facing reply for the lead desk (AE-039). */
export function draftReply(lead) {
  const first = String(lead.name || '').split(' ')[0] || 'there';
  const when = lead.urgency === 'emergency'
    ? 'We are prioritizing your request — a licensed electrician will call you shortly. If anything is sparking, smoking, or hot to the touch, shut the breaker off and call (818) 302-5614 now.'
    : lead.urgency === 'same-day'
      ? 'We can usually reach same-day requests within a few hours when capacity allows.'
      : 'We will follow up within one business day with next steps and a written estimate.';
  return `Hi ${first}, thanks for reaching out to AMY Electric about ${lead.service || 'your electrical project'}. ${when} If you need us sooner, call or text (818) 302-5614. — AMY Electric (C-10 #981578)`;
}

export { MAX_FILE_BYTES, MAX_FILES_PER_LEAD, MAX_UPLOADS_PER_HOUR, normalizePhone, normalizeEmail };
