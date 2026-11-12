/* AMY Electric — wraps /api/contact with persistence + CRM sync.
 *
 * The public handler (contact-handler.js) stays dependency-free and keeps its
 * exact response contract. This wrapper reads a clone of the request, lets the
 * original handler validate/send, and only when the lead was accepted does it:
 *   1. classify + score + de-duplicate the lead (lead-store.js),
 *   2. link any pre-uploaded photos/plans (private R2 objects),
 *   3. sync to EspoCRM (or HubSpot, or the legacy webhook, whichever is configured),
 *   4. log a funnel event.
 *
 * Persistence failures never change the visitor's response.
 */

import { handleContact } from './contact-handler.js';
import { buildLead, persistLead, linkFiles, recordEvent, markCrm } from './lead-store.js';
import { syncLeadToHubSpot, syncLeadToWebhook, aiQualify } from './crm-handler.js';
import { syncLeadToEspo, espocrmConfigured } from './crm-espocrm.js';

const str = (v) => (typeof v === 'string' ? v.trim() : '');

function fileIds(raw) {
  const value = raw.files;
  if (!value) return [];
  try {
    const parsed = typeof value === 'string' ? JSON.parse(value) : value;
    return Array.isArray(parsed) ? parsed.filter((x) => typeof x === 'string').slice(0, 5) : [];
  } catch {
    return [];
  }
}

function attribution(raw, request) {
  const url = new URL(request.url);
  const q = url.searchParams;
  return {
    source_page: str(raw.source_page).slice(0, 200) || url.pathname,
    referrer: str(raw.referrer).slice(0, 300) || request.headers.get('Referer') || '',
    utm_source: (str(raw.utm_source) || q.get('utm_source') || '').slice(0, 100),
    utm_medium: (str(raw.utm_medium) || q.get('utm_medium') || '').slice(0, 100),
    utm_campaign: (str(raw.utm_campaign) || q.get('utm_campaign') || '').slice(0, 120),
    utm_term: (str(raw.utm_term) || q.get('utm_term') || '').slice(0, 120),
    utm_content: (str(raw.utm_content) || q.get('utm_content') || '').slice(0, 120),
    gclid: (str(raw.gclid) || q.get('gclid') || '').slice(0, 200),
    fbclid: (str(raw.fbclid) || q.get('fbclid') || '').slice(0, 200),
    ip: request.headers.get('CF-Connecting-IP') || '',
    user_agent: request.headers.get('User-Agent') || '',
  };
}

export async function handleContactEnriched(request, env, waitUntil) {
  if (request.method !== 'POST') return handleContact(request, env, waitUntil);

  const contentType = request.headers.get('Content-Type') || '';
  let raw = null;
  try {
    const clone = request.clone();
    raw = contentType.includes('application/json')
      ? await clone.json()
      : Object.fromEntries(await clone.formData());
  } catch {
    raw = null;
  }

  const ids = raw ? fileIds(raw) : [];
  const extra = ids.length
    ? { lines: [`Attachments: ${ids.length} photo/plan file(s) — open the lead desk to download.`] }
    : null;

  const response = await handleContact(request, env, waitUntil, extra);
  if (!response || !response.ok || !raw) return response;

  // Spam traps: the handler returns success without sending. Do not persist.
  if (str(raw.website) !== '') return response;
  if (raw._timestamp) {
    const elapsed = Date.now() - new Date(raw._timestamp).getTime();
    if (Number.isFinite(elapsed) && elapsed < 3000) return response;
  }

  const meta = attribution(raw, request);
  const task = (async () => {
    try {
      const lead = await buildLead({
        name: str(raw.name).slice(0, 100),
        phone: str(raw.phone).slice(0, 25),
        email: str(raw.email).slice(0, 254),
        service: str(raw.service).slice(0, 50),
        city: str(raw.city).slice(0, 100),
        message: str(raw.message).slice(0, 5000),
        request_type: str(raw.request_type).slice(0, 50),
        estimate: str(raw.estimate).slice(0, 2000),
        hasFiles: ids.length > 0,
        hasEstimate: Boolean(str(raw.estimate)),
      }, meta);

      // Optional Workers AI re-scoring (env.AI_QUALIFY = '1').
      if (env.AI_QUALIFY === '1' && env.AI) {
        const ai = await aiQualify(env, lead);
        if (ai && ai.source === 'workers-ai') {
          lead.score = ai.score;
          lead.segment = ai.segment;
          lead.urgency = ai.urgency;
          lead.score_reasons = JSON.stringify(ai.reasons || []);
        }
      }

      const stored = await persistLead(env, lead);
      if (!stored) return;

      if (ids.length) {
        await linkFiles(env, str(raw.upload_token), lead.id, ids);
      }

      await recordEvent(env, 'lead_created', {
        leadId: lead.id,
        label: lead.service,
        page: lead.source_page,
        meta: { score: lead.score, segment: lead.segment, urgency: lead.urgency, files: ids.length },
      });

      if (lead.duplicate_of) {
        await recordEvent(env, 'lead_duplicate', { leadId: lead.id, label: lead.duplicate_of, page: lead.source_page });
        return;
      }

      // Provider order: EspoCRM (FOSS) → HubSpot → generic webhook.
      // EspoCRM on the LAN is not reachable from the edge, so when it is not
      // configured here the lead stays 'skipped' and scripts/espocrm-sync.mjs
      // delivers it from the local network instead.
      let crm = { ok: false, reason: 'not-configured' };
      if (espocrmConfigured(env)) {
        crm = await syncLeadToEspo(env, lead);
        if (crm.ok) {
          await markCrm(env, lead.id, {
            status: 'synced', contactId: crm.contactId, dealId: crm.opportunityId,
            taskId: crm.taskId, provider: 'espocrm',
          });
        } else {
          await markCrm(env, lead.id, { status: 'failed', error: crm.reason, provider: 'espocrm' });
        }
      } else if (env.HUBSPOT_TOKEN) {
        crm = await syncLeadToHubSpot(env, lead);
      } else if (env.CRM_WEBHOOK_URL) {
        crm = await syncLeadToWebhook(env, lead);
        if (crm.ok) await markCrm(env, lead.id, { status: 'synced', provider: 'webhook' });
      }
      if (!crm.ok && !espocrmConfigured(env) && !env.HUBSPOT_TOKEN && !env.CRM_WEBHOOK_URL) {
        await markCrm(env, lead.id, { status: 'skipped', provider: '' });
      }
    } catch (err) {
      console.warn('lead enrichment failed:', err && err.message);
    }
  })();

  if (typeof waitUntil === 'function') {
    waitUntil(task);
  } else {
    // In tests without a context: bound the wait so a hung sync can't stall.
    await Promise.race([task, new Promise((resolve) => setTimeout(resolve, 50))]);
  }
  return response;
}
