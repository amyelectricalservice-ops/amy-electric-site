/* AMY Electric — scheduled lead operations (crm-cron.js).
 *
 * Runs from the existing daily cron (16:00 UTC) after the GBP agent:
 *   1. overdue follow-up digest (emergency leads are due in 15 minutes,
 *      same-day in 2 hours, everything else next day),
 *   2. Monday weekly marketing report,
 *   3. cleanup of orphaned pending uploads (7 days).
 *
 * Delivery uses LEAD_NOTIFY_WEBHOOK (Slack/Zapier/ntfy style JSON POST) when
 * configured; otherwise the digest is written to Workers Logs so nothing is
 * silently dropped. HubSpot is the primary task system once HUBSPOT_TOKEN is
 * set — this is the safety net.
 */

import { weeklyReport } from './crm-handler.js';

function R2(env) {
  return (env && (env.LEAD_FILES || env.BUCKET)) || null;
}

function db(env) {
  return (env && (env.CRM_DB || env.DB)) || null;
}

async function notify(env, text, subject) {
  if (env.LEAD_NOTIFY_WEBHOOK) {
    try {
      await fetch(env.LEAD_NOTIFY_WEBHOOK, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, subject, source: 'amyelectric.com-lead-desk' }),
      });
      return true;
    } catch (err) {
      console.warn('lead notify webhook failed:', err && err.message);
    }
  }
  console.log(JSON.stringify({ type: 'lead_digest', subject, text }));
  return false;
}

export async function overdueFollowUps(env, now = new Date()) {
  const database = db(env);
  if (!database) return [];
  try {
    const rows = await database.prepare(
      `SELECT id, created_at, name, phone, email, service, city, score, urgency, status, follow_up_at
         FROM leads
        WHERE follow_up_at IS NOT NULL AND follow_up_at <= ?
          AND status IN ('new','contacted') AND duplicate_of = ''
        ORDER BY score DESC, follow_up_at ASC LIMIT 25`
    ).bind(now.toISOString()).all();
    return (rows && rows.results) || [];
  } catch {
    return [];
  }
}

export async function cleanupPendingUploads(env, now = new Date()) {
  const database = db(env);
  if (!database || !R2(env)) return 0;
  const cutoff = new Date(now.getTime() - 7 * 86400000).toISOString();
  let deleted = 0;
  try {
    const rows = await database.prepare(
      `SELECT id, r2_key FROM lead_files WHERE status = 'pending' AND created_at <= ? LIMIT 200`
    ).bind(cutoff).all();
    for (const row of (rows && rows.results) || []) {
      try {
        await R2(env).delete(row.r2_key);
        await database.prepare(`UPDATE lead_files SET status = 'deleted' WHERE id = ?`).bind(row.id).run();
        deleted += 1;
      } catch { /* keep going */ }
    }
  } catch {
    return deleted;
  }
  return deleted;
}

export async function runLeadCron(env, now = new Date()) {
  const database = db(env);
  if (!database) return { ok: false, reason: 'no-db' };

  const due = await overdueFollowUps(env, now);
  if (due.length) {
    const lines = due.map((l) =>
      `• [${l.score}] ${l.name} — ${l.service || 'electrical'} (${l.urgency}) · ${l.phone} · ${l.city || 'n/a'} · due ${String(l.follow_up_at).slice(0, 16)}`);
    await notify(env,
      `AMY Electric — ${due.length} lead(s) need follow-up:\n${lines.join('\n')}`,
      'Lead follow-ups due');
  }

  let report = null;
  // Monday (UTC) weekly report; the dashboard reads the same shape on demand.
  if (now.getUTCDay() === 1) {
    report = await weeklyReport(env, 7);
    const m = report.media;
    await notify(env,
      `AMY Electric weekly marketing report\n`
      + `Leads: ${report.leads.total} (${report.leads.commercial} commercial, ${report.leads.emergency} emergency)\n`
      + `Avg score: ${report.leads.avg_score} · close rate ${report.leads.close_rate_pct}%\n`
      + `Spend: $${m.spend_usd} · CPL $${m.cost_per_lead_usd} · CPQL $${m.cost_per_qualified_lead_usd}\n`
      + `Revenue: $${report.revenue.revenue_usd} across ${report.revenue.completed_jobs} completed jobs\n`
      + `Recommendations:\n- ${report.recommendations.join('\n- ')}`,
      'Weekly marketing report');
  }

  const cleaned = await cleanupPendingUploads(env, now);
  return { ok: true, due: due.length, report: Boolean(report), cleaned };
}
