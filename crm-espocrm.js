/* AMY Electric — EspoCRM integration (crm-espocrm.js).
 *
 * FOSS CRM: EspoCRM (GPLv3) at ESPOCRM_BASE_URL (default http://localhost:8081).
 * Auth: Basic with a dedicated non-admin user (ESPOCRM_USERNAME/ESPOCRM_PASSWORD)
 * or an API key (ESPOCRM_API_KEY) when the instance exposes one.
 *
 * Two callers:
 *   1. worker.js — only when ESPOCRM_BASE_URL is a publicly reachable URL.
 *   2. scripts/espocrm-sync.mjs — the normal path while the CRM is on the LAN.
 *
 * Entity mapping:
 *   Contact      one per person (found by email, then phone)
 *   Lead         one per inquiry, status New, source Web Site, score in description
 *   Task         follow-up, parent = Lead, priority High for emergency/same-day
 *   Opportunity  commercial inquiries only, stage Prospecting
 */

function baseUrl(env) {
  return String((env && env.ESPOCRM_BASE_URL) || '').replace(/\/+$/, '');
}

function authHeaders(env) {
  // Basic is the reliable path on EspoCRM 10 (the per-user apiKey field is
  // read-only via the API). Prefer explicit credentials when both exist.
  const user = (env && env.ESPOCRM_USERNAME) || '';
  const pass = (env && env.ESPOCRM_PASSWORD) || '';
  if (user) return { Authorization: `Basic ${btoa(`${user}:${pass}`)}` };
  if (env && env.ESPOCRM_API_KEY) return { 'X-Api-Key': env.ESPOCRM_API_KEY };
  return {};
}

export function espocrmConfigured(env) {
  if (!baseUrl(env)) return false;
  return Boolean(env.ESPOCRM_API_KEY || env.ESPOCRM_USERNAME);
}

async function espocrm(env, path, init = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...authHeaders(env),
    ...(init.headers || {}),
  };
  const res = await fetch(`${baseUrl(env)}/api/v1${path}`, { ...init, headers });
  const text = await res.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = { raw: text.slice(0, 500) }; }
  return { ok: res.ok, status: res.status, body };
}

/** E.164 is the only phone format EspoCRM accepts. */
export function toE164(raw) {
  const s = String(raw || '').trim();
  if (s.startsWith('+')) {
    const digits = s.replace(/\D/g, '');
    return digits.length >= 8 && digits.length <= 15 ? `+${digits}` : '';
  }
  const digits = s.replace(/\D/g, '');
  if (digits.length === 10) return `+1${digits}`;
  if (digits.length === 11 && digits.startsWith('1')) return `+${digits}`;
  if (digits.length >= 8 && digits.length <= 15) return `+${digits}`;
  return '';
}

export function splitName(raw) {
  const parts = String(raw || '').trim().split(/\s+/).filter(Boolean);
  return {
    firstName: parts[0] || '',
    lastName: parts.slice(1).join(' ') || parts[0] || 'Lead',
  };
}

function esc(value) {
  return String(value == null ? '' : value);
}

export function leadDescription(lead) {
  const lines = [
    `Score ${lead.score}/100 · ${lead.segment} · ${lead.urgency}`,
    lead.service ? `Service: ${lead.service}` : '',
    lead.city ? `City: ${lead.city}` : '',
    lead.message ? `Message: ${lead.message}` : '',
    lead.estimate_json ? `Indicative estimate: ${lead.estimate_json}` : '',
    `Source: ${lead.source_page || 'unknown'}${lead.utm_source ? ` · utm_source=${lead.utm_source}` : ''}${lead.utm_campaign ? ` · utm_campaign=${lead.utm_campaign}` : ''}${lead.gclid ? ` · gclid=${lead.gclid}` : ''}`,
    `Website lead id: ${lead.id}`,
  ];
  return lines.filter(Boolean).join('\n').slice(0, 6000);
}

async function findContact(env, lead) {
  const queries = [];
  if (lead.email_norm) {
    queries.push(`where[0][type]=equals&where[0][attribute]=emailAddress&where[0][value]=${encodeURIComponent(lead.email_norm)}`);
  }
  const phone = toE164(lead.phone);
  if (phone) {
    queries.push(`where[0][type]=equals&where[0][attribute]=phoneNumber&where[0][value]=${encodeURIComponent(phone)}`);
  }
  for (const q of queries) {
    const res = await espocrm(env, `/Contact?maxSize=1&select=id,name,emailAddress,phoneNumber&${q}`);
    if (res.ok && res.body && Array.isArray(res.body.list) && res.body.list.length) {
      return res.body.list[0].id;
    }
  }
  return null;
}

async function findLead(env, lead) {
  if (lead.crm_lead_id) return lead.crm_lead_id;
  const phone = toE164(lead.phone);
  const filters = [];
  if (lead.email_norm) {
    filters.push(`where[0][type]=equals&where[0][attribute]=emailAddress&where[0][value]=${encodeURIComponent(lead.email_norm)}`);
  } else if (phone) {
    filters.push(`where[0][type]=equals&where[0][attribute]=phoneNumber&where[0][value]=${encodeURIComponent(phone)}`);
  }
  if (!filters.length) return null;
  const res = await espocrm(env, `/Lead?maxSize=1&orderBy=createdAt&order=desc&select=id,name,status&${filters[0]}`);
  if (res.ok && res.body && Array.isArray(res.body.list) && res.body.list.length) {
    const row = res.body.list[0];
    if (row.status !== 'Dead' && row.status !== 'Converted') return row.id;
  }
  return null;
}

function taskDue(urgency) {
  const d = new Date();
  if (urgency === 'emergency') d.setMinutes(d.getMinutes() + 15);
  else if (urgency === 'same-day') d.setHours(d.getHours() + 2);
  else d.setDate(d.getDate() + 1);
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())} ${p(d.getUTCHours())}:${p(d.getUTCMinutes())}:00`;
}

function estimateAmount(lead) {
  if (!lead.estimate_json) return null;
  try {
    const e = JSON.parse(lead.estimate_json);
    const low = Number(e.rangeLow);
    const high = Number(e.rangeHigh);
    if (!Number.isFinite(low) || !Number.isFinite(high)) return null;
    return Math.round((low + high) / 2);
  } catch {
    return null;
  }
}

/**
 * Create (or reuse) Contact → Lead → Task, plus Opportunity for commercial.
 * Never throws: returns { ok, reason, ids } so the caller can record status.
 */
export async function syncLeadToEspo(env, lead) {
  if (!espocrmConfigured(env)) return { ok: false, reason: 'not-configured' };
  if (lead.duplicate_of) return { ok: false, reason: 'duplicate' };

  try {
    const { firstName, lastName } = splitName(lead.name);
    const phone = toE164(lead.phone);

    let contactId = await findContact(env, lead);
    if (!contactId) {
      const created = await espocrm(env, '/Contact', {
        method: 'POST',
        body: JSON.stringify({
          firstName,
          lastName,
          emailAddress: lead.email_norm || undefined,
          phoneNumber: phone || undefined,
          addressCity: lead.city || undefined,
          description: `Created from amyelectric.com (lead ${lead.id})`,
        }),
      });
      if (!created.ok) {
        return { ok: false, reason: `contact ${created.status}`, detail: created.body };
      }
      contactId = created.body.id;
    }

    let leadId = await findLead(env, lead);
    if (!leadId) {
      const created = await espocrm(env, '/Lead', {
        method: 'POST',
        body: JSON.stringify({
          firstName,
          lastName,
          emailAddress: lead.email_norm || undefined,
          phoneNumber: phone || undefined,
          status: 'New',
          source: 'Web Site',
          addressCity: lead.city || undefined,
          website: lead.source_page ? `https://amyelectric.com${lead.source_page}` : undefined,
          assignedUserId: env.ESPOCRM_ASSIGNED_USER_ID || undefined,
          description: leadDescription(lead),
        }),
      });
      if (!created.ok) {
        return { ok: false, reason: `lead ${created.status}`, detail: created.body, contactId };
      }
      leadId = created.body.id;
    }

    const taskName = `Follow up: ${lead.name || 'website lead'} — ${lead.service || 'electrical'}`;
    // Idempotency: a retry after a failed D1 write must not create a second task.
    let taskId = '';
    const existingTask = await espocrm(env, `/Task?maxSize=1&select=id&where[0][type]=equals&where[0][attribute]=parentId&where[0][value]=${encodeURIComponent(leadId)}&where[1][type]=equals&where[1][attribute]=name&where[1][value]=${encodeURIComponent(taskName)}`);
    if (existingTask.ok && existingTask.body && Array.isArray(existingTask.body.list) && existingTask.body.list.length) {
      taskId = existingTask.body.list[0].id;
    }
    const task = taskId ? { ok: true, body: { id: taskId } } : await espocrm(env, '/Task', {
      method: 'POST',
      body: JSON.stringify({
        name: taskName,
        status: 'Not Started',
        priority: lead.urgency === 'emergency' ? 'High' : 'Normal',
        dateEnd: taskDue(lead.urgency),
        parentType: 'Lead',
        parentId: leadId,
        assignedUserId: env.ESPOCRM_ASSIGNED_USER_ID || undefined,
        description: `Score ${lead.score}/100\nPhone: ${esc(lead.phone)}\nCity: ${esc(lead.city)}\n${lead.message ? `Message: ${esc(lead.message)}` : ''}`.slice(0, 4000),
      }),
    });
    taskId = task.ok ? task.body.id : taskId;

    let opportunityId = '';
    if (lead.segment === 'commercial') {
      const amount = estimateAmount(lead);
      const close = new Date();
      close.setDate(close.getDate() + 30);
      const opp = await espocrm(env, '/Opportunity', {
        method: 'POST',
        body: JSON.stringify({
          name: `Commercial — ${lead.service || 'electrical'} — ${lead.name || 'website lead'}`,
          stage: 'Prospecting',
          // EspoCRM requires amount; 0 means "not yet priced".
          amount: amount == null ? 0 : amount,
          amountCurrency: 'USD',
          closeDate: close.toISOString().slice(0, 10),
          contactId,
          assignedUserId: env.ESPOCRM_ASSIGNED_USER_ID || undefined,
          description: leadDescription(lead),
        }),
      });
      if (opp.ok) {
        opportunityId = opp.body.id;
      } else {
        console.warn('EspoCRM opportunity failed:', opp.status, JSON.stringify(opp.body).slice(0, 200));
      }
    }

    return { ok: true, contactId, leadId, opportunityId, taskId };
  } catch (err) {
    return { ok: false, reason: 'exception', detail: String(err && err.message).slice(0, 300) };
  }
}
