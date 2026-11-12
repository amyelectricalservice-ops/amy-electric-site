#!/usr/bin/env node
/* AMY Electric — EspoCRM sync agent.
 *
 * The Worker stores every lead in D1. EspoCRM runs on the LAN, so the edge
 * cannot reach it; this agent drains the queue from the local network:
 *
 *   D1 (Cloudflare)  →  GET /api/admin/leads?crm=pending
 *                    →  EspoCRM REST (Contact + Lead + Task + Opportunity)
 *                    →  POST /api/admin/lead/:id/crm  (mark synced)
 *
 * Idempotent: reuses an existing Contact by email/phone, an open Lead by
 * email/phone, and an existing follow-up Task by parent+name.
 *
 * Config (never committed):
 *   ~/.amy-electric/espocrm.env     ESPOCRM_BASE_URL, ESPOCRM_USERNAME, ESPOCRM_PASSWORD
 *   ~/.amy-electric/admin-token.txt ADMIN_TOKEN for the site admin API
 *
 * Usage:
 *   node scripts/espocrm-sync.mjs                # drain once
 *   node scripts/espocrm-sync.mjs --dry-run      # show what would happen
 *   node scripts/espocrm-sync.mjs --loop 300     # poll every 5 minutes
 *   node scripts/espocrm-sync.mjs --limit 50 --site https://...
 *
 * Cron (every 5 minutes, write the schedule as  0,5,10,...  to avoid closing
 * this comment):
 *   cd /home/amram/WEBSITE && /usr/bin/node scripts/espocrm-sync.mjs >> ~/.amy-electric/sync.log 2>&1
 */
import { readFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import process from 'node:process';
import { syncLeadToEspo, espocrmConfigured } from '../crm-espocrm.js';

const HOME = homedir();
const ESPO_ENV = join(HOME, '.amy-electric', 'espocrm.env');
const TOKEN_FILE = join(HOME, '.amy-electric', 'admin-token.txt');
const DEFAULT_SITE = 'https://amy-electric-site.a-m-y-electricalservice.workers.dev';

function parseEnvFile(path) {
  if (!existsSync(path)) return {};
  const out = {};
  for (const line of readFileSync(path, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m) out[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  return out;
}

function arg(name, fallback = '') {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
const has = (name) => process.argv.includes(`--${name}`);

const espoEnv = { ...parseEnvFile(ESPO_ENV), ...process.env };
const adminToken = process.env.ADMIN_TOKEN
  || (existsSync(TOKEN_FILE) ? readFileSync(TOKEN_FILE, 'utf8').trim() : '');
const site = arg('site', process.env.SITE_URL || DEFAULT_SITE).replace(/\/+$/, '');
const limit = Math.max(1, Math.min(200, Number(arg('limit', '100')) || 100));
const dryRun = has('dry-run');
const loop = Number(arg('loop', '0')) || 0;

if (!espocrmConfigured(espoEnv)) {
  console.error('EspoCRM is not configured. Expected', ESPO_ENV, 'with ESPOCRM_BASE_URL + ESPOCRM_USERNAME/PASSWORD (or ESPOCRM_API_KEY).');
  process.exit(2);
}
if (!adminToken) {
  console.error('No admin token. Put it in', TOKEN_FILE, '(mode 600) or set ADMIN_TOKEN.');
  process.exit(2);
}

async function admin(path, init = {}) {
  const res = await fetch(`${site}${path}`, {
    ...init,
    headers: { Authorization: `Bearer ${adminToken}`, 'Content-Type': 'application/json', ...(init.headers || {}) },
  });
  const text = await res.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = { raw: text.slice(0, 300) }; }
  if (!res.ok) throw new Error(`${path} → ${res.status} ${JSON.stringify(body).slice(0, 200)}`);
  return body;
}

async function drain() {
  const { leads } = await admin(`/api/admin/leads?crm=pending&limit=${limit}`);
  if (!leads || !leads.length) {
    console.log(new Date().toISOString(), 'no pending leads');
    return { synced: 0, failed: 0, total: 0 };
  }
  let synced = 0;
  let failed = 0;
  for (const lead of leads) {
    const label = `${lead.id} [${lead.score}] ${lead.segment}/${lead.urgency} ${lead.service || 'electrical'}`;
    if (dryRun) {
      console.log('would sync', label);
      continue;
    }
    const result = await syncLeadToEspo(espoEnv, lead);
    if (result.ok) {
      await admin(`/api/admin/lead/${encodeURIComponent(lead.id)}/crm`, {
        method: 'POST',
        body: JSON.stringify({
          crm_status: 'synced',
          provider: 'espocrm',
          contact_id: result.contactId || '',
          deal_id: result.opportunityId || '',
          task_id: result.taskId || '',
        }),
      });
      synced += 1;
      console.log('synced', label, '→', result.leadId || '');
    } else {
      failed += 1;
      const error = `${result.reason || 'error'}${result.detail ? `: ${JSON.stringify(result.detail).slice(0, 200)}` : ''}`;
      await admin(`/api/admin/lead/${encodeURIComponent(lead.id)}/crm`, {
        method: 'POST',
        body: JSON.stringify({ crm_status: 'failed', provider: 'espocrm', error }),
      }).catch(() => {});
      console.error('failed', label, '→', error);
    }
  }
  console.log(new Date().toISOString(), `done: ${synced} synced, ${failed} failed`);
  return { synced, failed, total: leads.length };
}

if (loop > 0) {
  console.log(`Polling every ${loop}s. Ctrl-C to stop.`);
  // Sequential by design: EspoCRM is a single small instance.
  const tick = async () => {
    try { await drain(); } catch (err) { console.error('drain failed:', err.message); }
    setTimeout(tick, loop * 1000);
  };
  tick();
} else {
  drain().catch((err) => { console.error(err.message); process.exit(1); });
}
