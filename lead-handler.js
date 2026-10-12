/* AMY Electric — lead wizard CRM handler (lead-handler.js).
 *
 * POST /api/lead — same-origin proxy in front of the external CRM/invoicing
 * webhook. The browser NEVER sees the webhook URL: it lives in the
 * CRM_WEBHOOK_URL worker secret (wrangler secret put CRM_WEBHOOK_URL).
 *
 * Flow (CRM-first, /api/contact as fallback):
 *   1. Validate honeypot + timestamp trap (same contract as contact-handler.js).
 *   2. Allowlist + validate contact + engineering params.
 *   3. POST JSON payload to CRM_WEBHOOK_URL (awaited, 8s timeout).
 *      - CRM 2xx → return { success: true, crm: 'ok' }.
 *      - CRM unreachable/non-2xx/unconfigured → forward the payload to the
 *        internal lead email path via handleContact-equivalent fields and
 *        return { success: true, crm: 'fallback' } so the UI can note it.
 *   4. Validation failures → 400 { success: false, message } (inline errors).
 */

import { handleContact } from './contact-handler.js';

function badRequest(message) {
  return new Response(JSON.stringify({ success: false, message }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' },
  });
}

function okResponse(crm, estimateLabel) {
  return new Response(JSON.stringify({ success: true, crm, estimate: estimateLabel || '' }), {
    headers: { 'Content-Type': 'application/json' },
  });
}

export async function handleLead(request, env) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', Allow: 'POST' },
    });
  }

  let raw;
  try {
    const contentType = request.headers.get('Content-Type') || '';
    raw = contentType.includes('application/json')
      ? await request.json()
      : Object.fromEntries(await request.formData());
  } catch {
    return badRequest('Could not read your submission. Please try again.');
  }

  const str = (v) => (typeof v === 'string' ? v.trim() : '');

  /* Spam traps (same contract as /api/contact). */
  if (str(raw.website) !== '') {
    return okResponse('fallback', '');
  }
  if (raw._timestamp) {
    const elapsed = Date.now() - new Date(raw._timestamp).getTime();
    if (Number.isFinite(elapsed) && elapsed < 3000) {
      return okResponse('fallback', '');
    }
  }

  /* Contact (required: name, email, phone). */
  const contact = {
    name: str(raw.name).slice(0, 100),
    email: str(raw.email).slice(0, 254),
    phone: str(raw.phone).slice(0, 25),
    city: str(raw.city).slice(0, 100),
  };
  if (contact.name.length < 2) return badRequest('Please enter your name (at least 2 characters).');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact.email)) {
    return badRequest('Please enter a valid email address.');
  }
  const digits = contact.phone.replace(/\D/g, '');
  if (!/^[\d\s()+.-]{7,25}$/.test(contact.phone) || digits.length < 7 || digits.length > 15) {
    return badRequest('Please enter a valid phone number with at least 7 digits.');
  }

  /* Engineering params (wizard spec). */
  let spec = null;
  if (typeof raw.spec === 'string' && raw.spec) {
    try { spec = JSON.parse(raw.spec); } catch { spec = { raw: raw.spec.slice(0, 2000) }; }
  } else if (raw.spec && typeof raw.spec === 'object') {
    spec = raw.spec;
  }
  const serviceId = str(raw.serviceId || (spec && spec.serviceId) || raw.service).slice(0, 60);
  if (!serviceId) return badRequest('Please choose a project type first.');

  const estimate = {
    label: str(raw.estimateLabel).slice(0, 60),
    low: Number(raw.estimateLow) || null,
    high: Number(raw.estimateHigh) || null,
    lines: Array.isArray(raw.lines) ? raw.lines.slice(0, 20) : [],
    exclusions: Array.isArray(raw.exclusions) ? raw.exclusions.slice(0, 20) : [],
  };

  const payload = {
    source: 'amyelectric.com-lead-wizard',
    submittedAt: new Date().toISOString(),
    geoCity: str(raw.geoCity).slice(0, 100),
    contact,
    project: { serviceId, spec },
    estimate,
  };

  /* CRM-first: awaited POST with timeout. Secret never leaves the edge. */
  const webhook = env.CRM_WEBHOOK_URL || '';
  if (webhook) {
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 8000);
      const res = await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: ctrl.signal,
      });
      clearTimeout(timer);
      if (res.ok) return okResponse('ok', estimate.label);
    } catch {
      /* fall through to internal fallback */
    }
  }

  /* Fallback: reuse the internal lead pipeline (/api/contact path). */
  const fd = new FormData();
  fd.set('name', contact.name);
  fd.set('phone', contact.phone);
  fd.set('email', contact.email);
  fd.set('city', contact.city);
  fd.set('service', serviceId);
  fd.set('website', '');
  fd.set('_timestamp', new Date(Date.now() - 10000).toISOString());
  fd.set('message', 'Lead wizard (' + payload.geoCity + '): ' + serviceId +
    ' — estimate ' + estimate.label + ' — spec ' + JSON.stringify(spec));
  const fbReq = new Request('https://amyelectric.com/api/contact', { method: 'POST', body: fd });
  await handleContact(fbReq, env, () => {});
  return okResponse('fallback', estimate.label);
}
