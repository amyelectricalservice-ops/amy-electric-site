/* AMY Electric — lead store, scoring and de-duplication (lead-store.js).
 *
 * Pure-ish helpers around the D1 `leads` / `lead_files` / `lead_events`
 * tables (scripts/lead-schema.sql). Everything degrades gracefully: if the
 * DB binding is missing (node --test, preview) the functions return null and
 * the caller keeps its existing email-only behaviour.
 */

function DB(env) {
  return (env && (env.CRM_DB || env.DB)) || null;
}

const COMMERCIAL_RE = /\b(commercial|tenant improvement|restaurant|retail|office|warehouse|industrial|3-phase|three phase|400a|property management|hoa|multi-family|multifamily|fleet)\b/i;
const EMERGENCY_RE = /\b(sparking|smoking|burning|burn smell|fire|shock(ed|ing)?|exposed wire|water leak|no power|power outage|live wire|melted|scorch(ed|ing)?|overheat(ed|ing)?|hot panel|panel is hot|buzzing|(feels?|is|getting|very|really)\s+hot)\b/i;
const SAME_DAY_RE = /\b(same[- ]day|today|asap|urgent|emergency|right away|immediately)\b/i;
const PLANNING_RE = /\b(quote|estimate|planning|remodel|renovation|next month|future|budget)\b/i;

const LOCAL_AREA_CODES = new Set(['818', '747', '310', '213', '424', '323', '626', '661', '805']);

const SERVICE_WEIGHT = {
  'commercial': 15,
  'panel-upgrade': 15,
  'rewiring': 12,
  'ev-charger': 12,
  'tesla-charger': 12,
  'generator': 10,
  'electrical-repair': 10,
  'licensed-electrician': 8,
  'safety-inspection': 7,
  'dedicated-circuit': 7,
  'lighting': 5,
  'smart-home': 5,
  'ceiling-fan': 3,
  'outlet-switch': 4,
  'smoke-co': 4,
  'surge-protection': 4,
};

export function uid(prefix) {
  const rand = crypto.randomUUID().replace(/-/g, '');
  return `${prefix}_${rand.slice(0, 20)}`;
}

export async function sha256Hex(value) {
  const data = new TextEncoder().encode(String(value ?? ''));
  const digest = await crypto.subtle.digest('SHA-256', data);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function normalizePhone(raw) {
  const digits = String(raw || '').replace(/\D/g, '');
  if (digits.length === 11 && digits.startsWith('1')) return digits.slice(1);
  return digits;
}

export function normalizeEmail(raw) {
  return String(raw || '').trim().toLowerCase();
}

/** Deterministic 0-100 score + segment/urgency classification. */
export function scoreLead(input) {
  const reasons = [];
  let score = 20;

  const text = `${input.service || ''} ${input.message || ''} ${input.request_type || ''}`;
  const commercial = COMMERCIAL_RE.test(text) || String(input.service || '') === 'commercial';
  const segment = commercial ? 'commercial' : 'residential';

  let urgency = 'standard';
  if (EMERGENCY_RE.test(text)) {
    urgency = 'emergency';
    score += 30;
    reasons.push('emergency language +30');
  } else if (SAME_DAY_RE.test(text)) {
    urgency = 'same-day';
    score += 20;
    reasons.push('same-day intent +20');
  } else if (PLANNING_RE.test(text)) {
    urgency = 'planning';
    score -= 5;
    reasons.push('planning-stage language -5');
  }

  if (commercial) {
    score += 15;
    reasons.push('commercial segment +15');
  }

  const serviceWeight = SERVICE_WEIGHT[String(input.service || '')] || 0;
  if (serviceWeight) {
    score += serviceWeight;
    reasons.push(`service ${input.service} +${serviceWeight}`);
  }

  if (input.email) { score += 5; reasons.push('email provided +5'); }
  if ((input.message || '').trim().length >= 80) { score += 6; reasons.push('detailed message +6'); }
  if ((input.city || '').trim()) { score += 4; reasons.push('city provided +4'); }
  if (input.hasFiles) { score += 6; reasons.push('photos/plans attached +6'); }
  if (input.hasEstimate) { score += 6; reasons.push('estimate captured +6'); }
  if (input.gclid) { score += 8; reasons.push('paid click (gclid) +8'); }

  const phoneNorm = normalizePhone(input.phone);
  if (phoneNorm.length === 10 && LOCAL_AREA_CODES.has(phoneNorm.slice(0, 3))) {
    score += 3;
    reasons.push('local area code +3');
  }

  score = Math.max(0, Math.min(100, Math.round(score)));
  return { score, segment, urgency, reasons };
}

/**
 * Build the persisted lead record from validated form data + request meta.
 * `raw` fields are already trimmed/allowlisted by the caller.
 */
export async function buildLead(raw, meta = {}) {
  const scored = scoreLead({
    service: raw.service,
    message: raw.message,
    request_type: raw.request_type,
    email: raw.email,
    city: raw.city,
    phone: raw.phone,
    hasFiles: raw.hasFiles,
    hasEstimate: raw.hasEstimate,
    gclid: meta.gclid,
  });

  const phoneNorm = normalizePhone(raw.phone);
  const emailNorm = normalizeEmail(raw.email);

  return {
    id: uid('lead'),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    name: raw.name || '',
    phone: raw.phone || '',
    phone_norm: phoneNorm,
    email: emailNorm,
    email_norm: emailNorm,
    city: raw.city || '',
    service: raw.service || '',
    request_type: raw.request_type || '',
    message: raw.message || '',
    estimate_json: raw.estimate || '',
    segment: scored.segment,
    urgency: scored.urgency,
    score: scored.score,
    score_reasons: JSON.stringify(scored.reasons),
    source_page: meta.source_page || '',
    referrer: meta.referrer || '',
    utm_source: meta.utm_source || '',
    utm_medium: meta.utm_medium || '',
    utm_campaign: meta.utm_campaign || '',
    utm_term: meta.utm_term || '',
    utm_content: meta.utm_content || '',
    gclid: meta.gclid || '',
    fbclid: meta.fbclid || '',
    status: 'new',
    crm_provider: meta.crm_provider || '',
    crm_status: 'pending',
    dedupe_key: phoneNorm || emailNorm,
    duplicate_of: '',
    ip_hash: await sha256Hex(`${meta.ip || ''}|amy-leads`),
    user_agent: (meta.user_agent || '').slice(0, 300),
    turnstile_ok: meta.turnstile_ok ? 1 : 0,
    follow_up_at: scored.urgency === 'emergency'
      ? new Date(Date.now() + 15 * 60000).toISOString()
      : scored.urgency === 'same-day'
        ? new Date(Date.now() + 2 * 3600000).toISOString()
        : new Date(Date.now() + 24 * 3600000).toISOString(),
  };
}

/** Existing lead from the last `days` days with the same phone/email. */
export async function findDuplicate(env, lead, days = 30) {
  if (!env || !DB(env)) return null;
  const since = new Date(Date.now() - days * 86400000).toISOString();
  try {
    if (lead.phone_norm) {
      const row = await DB(env).prepare(
        `SELECT id, created_at FROM leads
          WHERE phone_norm = ? AND created_at >= ? AND duplicate_of = ''
          ORDER BY created_at DESC LIMIT 1`
      ).bind(lead.phone_norm, since).first();
      if (row) return row;
    }
    if (lead.email_norm) {
      const row = await DB(env).prepare(
        `SELECT id, created_at FROM leads
          WHERE email_norm = ? AND created_at >= ? AND duplicate_of = ''
          ORDER BY created_at DESC LIMIT 1`
      ).bind(lead.email_norm, since).first();
      if (row) return row;
    }
  } catch {
    return null;
  }
  return null;
}

/** Insert the lead. Returns { id, duplicateOf } or null when D1 is absent. */
export async function persistLead(env, lead) {
  if (!env || !DB(env)) return null;

  const dup = await findDuplicate(env, lead);
  if (dup) {
    lead.duplicate_of = dup.id;
    lead.status = 'duplicate';
    lead.crm_status = 'skipped';
  }

  try {
    await DB(env).prepare(
      `INSERT INTO leads (
        id, created_at, updated_at, name, phone, phone_norm, email, email_norm, city,
        service, request_type, message, estimate_json, segment, urgency, score,
        score_reasons, source_page, referrer, utm_source, utm_medium, utm_campaign,
        utm_term, utm_content, gclid, fbclid, status, crm_provider, crm_status,
        dedupe_key, duplicate_of, ip_hash, user_agent, turnstile_ok, follow_up_at
      ) VALUES (
        ?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?,?,?,
        ?,?,?,?,?,?,
        ?,?,?,?,?,?,?,
        ?,?,?,?,?,?
      )`
    ).bind(
      lead.id, lead.created_at, lead.updated_at, lead.name, lead.phone, lead.phone_norm,
      lead.email, lead.email_norm, lead.city,
      lead.service, lead.request_type, lead.message, lead.estimate_json, lead.segment,
      lead.urgency, lead.score,
      lead.score_reasons, lead.source_page, lead.referrer, lead.utm_source, lead.utm_medium,
      lead.utm_campaign,
      lead.utm_term, lead.utm_content, lead.gclid, lead.fbclid, lead.status,
      lead.crm_provider, lead.crm_status,
      lead.dedupe_key, lead.duplicate_of, lead.ip_hash, lead.user_agent, lead.turnstile_ok,
      lead.follow_up_at || null
    ).run();
    return { id: lead.id, duplicateOf: lead.duplicate_of || null };
  } catch (err) {
    console.warn('lead persist failed:', err && err.message);
    return null;
  }
}

/** Attach previously uploaded files to a lead (upload token authorises it). */
export async function linkFiles(env, uploadToken, leadId, fileIds) {
  if (!env || !DB(env) || !uploadToken || !Array.isArray(fileIds) || !fileIds.length) return 0;
  const ids = fileIds.filter((id) => typeof id === 'string' && /^file_[a-f0-9]{8,40}$/.test(id)).slice(0, 6);
  if (!ids.length) return 0;
  let linked = 0;
  for (const id of ids) {
    try {
      const res = await DB(env).prepare(
        `UPDATE lead_files SET lead_id = ?, status = 'linked'
          WHERE id = ? AND upload_token = ? AND status = 'pending'`
      ).bind(leadId, id, uploadToken).run();
      if (res && res.meta && res.meta.changes) linked += res.meta.changes;
    } catch {
      /* continue: one bad id must not lose the lead */
    }
  }
  return linked;
}

export async function recordEvent(env, event, { leadId = null, label = '', page = '', meta = null } = {}) {
  if (!env || !DB(env)) return;
  try {
    await DB(env).prepare(
      `INSERT INTO lead_events (id, lead_id, event, label, page, meta, created_at)
       VALUES (?,?,?,?,?,?,?)`
    ).bind(uid('evt'), leadId, String(event).slice(0, 60), String(label).slice(0, 200),
      String(page).slice(0, 200), meta ? JSON.stringify(meta).slice(0, 2000) : '', new Date().toISOString()).run();
  } catch {
    /* analytics must never break a request */
  }
}

export async function markCrm(env, leadId, { status, contactId, dealId, taskId, error, provider }) {
  if (!env || !DB(env)) return;
  try {
    await DB(env).prepare(
      `UPDATE leads SET crm_status = ?, crm_contact_id = COALESCE(?, crm_contact_id),
        crm_deal_id = COALESCE(?, crm_deal_id), crm_task_id = COALESCE(?, crm_task_id),
        crm_error = ?, crm_provider = COALESCE(?, crm_provider), updated_at = ?
       WHERE id = ?`
    ).bind(status, contactId || null, dealId || null, taskId || null,
      (error || '').slice(0, 500), provider || null, new Date().toISOString(), leadId).run();
  } catch {
    /* non-fatal */
  }
}

/** Aggregate counts for the dashboard / weekly report. */
export async function leadStats(env, days = 30) {
  if (!env || !DB(env)) return null;
  const since = new Date(Date.now() - days * 86400000).toISOString();
  const one = async (sql, ...args) => {
    try {
      const row = await DB(env).prepare(sql).bind(...args).first();
      return row || {};
    } catch {
      return {};
    }
  };
  const totals = await one(
    `SELECT COUNT(*) AS total,
            SUM(CASE WHEN segment = 'commercial' THEN 1 ELSE 0 END) AS commercial,
            SUM(CASE WHEN urgency = 'emergency' THEN 1 ELSE 0 END) AS emergency,
            SUM(CASE WHEN status IN ('quoted','won') THEN 1 ELSE 0 END) AS quoted,
            SUM(CASE WHEN status = 'won' THEN 1 ELSE 0 END) AS won,
            AVG(score) AS avg_score
       FROM leads WHERE created_at >= ? AND status != 'duplicate'`, since);
  const spend = await one(
    `SELECT SUM(spend_cents) AS spend_cents, SUM(clicks) AS clicks,
            SUM(impressions) AS impressions, SUM(qualified) AS qualified
       FROM ad_spend WHERE day >= ?`, since.slice(0, 10));
  const revenue = await one(
    `SELECT SUM(revenue_cents) AS revenue_cents, COUNT(*) AS jobs
       FROM jobs WHERE created_at >= ? AND status = 'completed'`, since);
  return { days, totals, spend, revenue };
}
