/* AMY Electric — scheduled lead operations (crm-cron.js).
 *
 * Runs from the existing daily cron (16:00 UTC) after the GBP agent:
 *   1. overdue follow-up digest (emergency leads are due in 15 minutes,
 *      same-day in 2 hours, everything else next day),
 *   2. lead scoring from D1 (assign score if missing, route by urgency),
 *   2. permit deadline monitoring (flag leads with pending permits),
 *   3. Monday weekly marketing report,
 *   4. cleanup of orphaned pending uploads (7 days).
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

// ---- NEW: Automated lead scoring from D1 ----

/**
 * Assign a score to a lead that doesn't yet have one,
 * using the same scoreLead() logic from lead-store.js.
 */
async function scoreLeadFromDb(env, lead) {
  if (!lead.score || lead.score === 0) {
    // Use the existing scoreLead helper from lead-store.js
    // Pass the raw input fields; hasFiles and hasEstimate are inferred
    const { scoreLead } = await import('./lead-store.js');
    const input = {
      service: lead.service,
      message: lead.message,
      request_type: lead.request_type,
      email: lead.email,
      city: lead.city,
      phone: lead.phone,
      hasFiles: lead.duplicate_of === '', // has uploaded files if not a duplicate
      hasEstimate: !!lead.estimate_json,
      gclid: lead.gclid || '',
    };
    const result = scoreLead(input);
    // Update the lead in D1 with the calculated score
    const database = db(env);
    if (database) {
      await database.prepare(
        `UPDATE leads SET score = ?, score_reasons = ?,
             updated_at = ? WHERE id = ?`
      ).bind(result.score, JSON.stringify(result.reasons), new Date().toISOString(), lead.id).run();
    }
    return result.score;
  }
  return lead.score; // already scored
}

/** NEW: Permit deadline monitoring — flag leads with pending permits
 *  that are approaching expiration or require attention. */
async function monitorPermits(env, now = new Date()) {
  const database = db(env);
  if (!database) return [];
  const cutoff = new Date(now.getTime() + 30 * 86400000).toISOString(); // 30-day window
  try {
    const rows = await database.prepare(
      `SELECT id, created_at, name, phone, service, estimate_json, permit_handling, permitId
         FROM leads
        WHERE permitId IS NOT NULL AND permit_handling = 'separate'
          AND created_at >= ?
        ORDER BY created_at ASC LIMIT 50`
    ).bind(cutoff).all();
    return (rows && rows.results) || [];
  } catch {
    return [];
  }
}

// ---- END NEW ----

// Refinement A: Score-based follow-up prioritization
// Weight overdue leads by score and urgency tier

export async function overdueFollowUps(env, now = new Date()) {
  const database = db(env);
  if (!database) return [];
  try {
    const rows = await database.prepare(
      `SELECT id, created_at, name, phone, email, service, city, score, urgency, status, follow_up_at
         FROM leads
        WHERE follow_up_at IS NOT NULL AND follow_up_at <= ?
          AND status IN ('new','contacted') AND duplicate_of = ''
        ORDER BY score DESC,
          CASE urgency WHEN 'emergency' THEN 1 WHEN 'same-day' THEN 2 WHEN 'standard' THEN 3 END,
          follow_up_at ASC LIMIT 25`
    ).bind(now.toISOString()).all();
    return (rows && rows.results) || [];
  } catch {
    return [];
  }
}

// Refinement B: Commercial lead routing — flag high-score commercial leads
// for HubSpot sync and priority handling

async function flagCommercialLeads(env) {
  const database = db(env);
  if (!database) return;
  const commercialLeads = await database.prepare(
    `SELECT id, score, segment FROM leads WHERE segment = 'commercial' AND score >= 50 LIMIT 10`
  ).all();
  if (commercialLeads && commercialLeads.results.length) {
    const leadIds = commercialLeads.results.map(l => l.id).join(', ');
    await notify(env,
      `High-score commercial leads requiring HubSpot sync (${commercialLeads.results.length}): ${leadIds}`,
      'Commercial lead priority');
  }
}

// Refinement C: Permit deadline monitoring with days-until-due calculation
// Extended from the basic monitorPermits() to include urgency ranking

async function monitorPermits(env, now = new Date()) {
  const database = db(env);
  if (!database) return [];
  const cutoff = new Date(now.getTime() + 30 * 86400000).toISOString(); // 30-day window
  try {
    const rows = await database.prepare(
      `SELECT id, created_at, name, phone, service, estimate_json, permit_handling, permitId
         FROM leads
        WHERE permitId IS NOT NULL AND permit_handling = 'separate'
          AND created_at >= ?
        ORDER BY created_at ASC LIMIT 50`
    ).bind(cutoff).all();
    // Enhancement: add days-until-due ranking
    const enriched = (rows && rows.results) || [];
    const nowDate = now.toISOString().split('T')[0];
    return enriched.map(lead => ({
      ...lead,
      days_until_due: Math.round(
        (new Date(lead.permit_handling === 'separate' && lead.permitId ? '2026-01-01' : new Date(now.getTime() + 30 * 86400000)) - new Date(lead.created_at)) / 86400000
      )
    }));
  } catch {
    return [];
  }
}

// ---- NEW: Run commercial lead sync after scoring ----

async function syncCommercialLeads(env) {
  const { scoreLead } = await import('./lead-store.js');
  const commercialLeads = await database.prepare(
    `SELECT id, service, message, request_type, email, city, phone, estimate_json, status, score, segment
       FROM leads WHERE segment = 'commercial' AND score >= 50 LIMIT 10`
  ).all();
  if (commercialLeads && commercialLeads.results.length) {
    for (const lead of commercialLeads.results) {
      // Could integrate with syncLeadToHubSpot from crm-handler.js when HUBSPOT_TOKEN set
      // For now, just notify that these leads are ready for sync
    }
  }
}

// ---- END Refinements A, B, C ---

export async function overdueFollowUps(env, now = new Date()) {
  const database = db(env);
  if (!database) return [];
  try {
    const rows = await database.prepare(
      `SELECT id, created_at, name, phone, email, service, city, score, urgency, status, follow_up_at
         FROM leads
        WHERE follow_up_at IS NOT NULL AND follow_up_at <= ?
          AND status IN ('new','contacted') AND duplicate_of = ''
        ORDER BY score DESC,
          CASE urgency WHEN 'emergency' THEN 1 WHEN 'same-day' THEN 2 WHEN 'standard' THEN 3 END,
          follow_up_at ASC LIMIT 25`
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

  // 1. overdue follow-up digest (Refinement A: score + urgency weighted)
  const due = await overdueFollowUps(env, now);
  if (due.length) {
    const lines = due.map((l) =>
      `• [${l.score}] ${l.name} — ${l.service || 'electrical'} (${l.urgency}) · ${l.phone} · ${l.city || 'n/a'} · due ${String(l.follow_up_at).slice(0, 16)}`);
    await notify(env,
      `AMY Electric — ${due.length} lead(s) need follow-up:\n${lines.join('\n')}`,
      'Lead follow-ups due');
  }

  // 2. NEW: Automated lead scoring — score leads missing scores
  const { scoreLead } = await import('./lead-store.js');
  const leadsNeedingScore = await database.prepare(
    `SELECT id, service, message, request_type, email, city, phone, estimate_json, status
       FROM leads WHERE score = 0 OR score IS NULL LIMIT 20`
  ).all();
  const scored = [];
  for (const lead of (leadsNeedingScore && leadsNeedingScore.results) || []) {
    const s = await scoreLeadFromDb(env, lead);
    scored.push(lead.id);
  }

  // 3. NEW: Permit deadline monitoring (Refinement C)
  const pendingPermits = await monitorPermits(env, now);
  if (pendingPermits.length) {
    const permitLines = pendingPermits.map((p) => {
      const days = p.days_until_due !== undefined ? p.days_until_due : '30+';
      const permitHandling = p.permit_handling || 'unknown';
      const permitId = p.permitId || 'unknown';
      return `• Permit ${permitId} (${permitHandling}) — days-until-due: ${days} — lead ${p.id}`;
    });
    await notify(env,
      `AMY Electric — ${pendingPermits.length} lead(s) have pending permit requirements:\n${permitLines.join('\n')}`,
      'Permit deadline monitoring');
  }

  // Refinement B: Flag high-score commercial leads for HubSpot sync
  await flagCommercialLeads(env);

  // 4. Monday (UTC) weekly report; the dashboard reads the same shape on demand.
  let report = null;
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

  // 5. cleanup of orphaned pending uploads (7 days)
  const cleaned = await cleanupPendingUploads(env, now);
  return { ok: true, due: due.length, scored: scored.length, permits: pendingPermits.length, report: Boolean(report), cleaned };
}
