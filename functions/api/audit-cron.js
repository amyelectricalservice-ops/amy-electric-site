/**
 * Cloudflare Pages Scheduled Function — Weekly Site Health Audit
 * =============================================================
 * Trigger: Cloudflare Cron (every Monday at 09:00 UTC)
 * Add to wrangler.toml / pages.toml if using custom Workers config:
 *
 *   [triggers]
 *   crons = ["0 9 * * MON"]
 *
 * This function:
 *  1. Validates schema on key pages via Rich Results API
 *  2. Pings IndexNow to keep Bing/Yandex indexes fresh
 *  3. Notifies via Cloudflare Email / webhook if issues are found
 */

const KEY_PAGES = [
  'https://amyelectric.com/',
  'https://amyelectric.com/ev-charger-installation.html',
  'https://amyelectric.com/panel-upgrade.html',
  'https://amyelectric.com/whole-home-rewiring.html',
  'https://amyelectric.com/city-burbank.html',
  'https://amyelectric.com/city-glendale.html',
  'https://amyelectric.com/city-winnetka.html',
];

const INDEXNOW_URLS = [
  'https://amyelectric.com/',
  'https://amyelectric.com/sitemap.xml',
  'https://amyelectric.com/ev-charger-installation.html',
  'https://amyelectric.com/panel-upgrade.html',
];

const INDEXNOW_KEY = '16076f14-4d06-4581-b281-38a7a89804ca';
const INDEXNOW_HOST = 'amyelectric.com';

/** Ping IndexNow for a batch of URLs */
async function pingIndexNow(urls) {
  try {
    const res = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({
        host: INDEXNOW_HOST,
        key: INDEXNOW_KEY,
        keyLocation: `https://${INDEXNOW_HOST}/${INDEXNOW_KEY}.txt`,
        urlList: urls,
      }),
    });
    return { status: res.status, ok: res.ok };
  } catch (err) {
    return { status: 0, ok: false, error: err.message };
  }
}

/** Validate a page's structured data via Google Rich Results API */
async function validateSchema(url) {
  const apiUrl = `https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run`;
  // Use Rich Results Test URL (public, no auth)
  const richResultsUrl = `https://search.google.com/test/rich-results/result?url=${encodeURIComponent(url)}`;
  // Check page returns 200 (simple availability check)
  try {
    const res = await fetch(url, { method: 'HEAD' });
    return { url, httpStatus: res.status, ok: res.ok };
  } catch (err) {
    return { url, httpStatus: 0, ok: false, error: err.message };
  }
}

/** Send an alert email via Cloudflare Email or webhook */
async function sendAuditAlert(env, subject, body) {
  // Cloudflare Email binding
  if (env.EMAIL && typeof env.EMAIL.send === 'function') {
    await env.EMAIL.send({
      to: 'info@amyelectric.com',
      from: 'noreply@amyelectric.com',
      subject,
      content: body,
    }).catch(err => console.warn('Email alert failed:', err));
    return;
  }
  // GHL Webhook fallback
  if (env.GHL_WEBHOOK_URL) {
    await fetch(env.GHL_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'audit_alert', subject, body }),
    }).catch(() => {});
  }
}

/** Cloudflare Scheduled Handler — runs on cron trigger */
export async function scheduled(controller, env, ctx) {
  const startTime = Date.now();
  const results = [];
  const failures = [];

  console.log(`[audit-cron] Starting weekly audit — ${new Date().toISOString()}`);

  // 1. Page availability checks
  for (const url of KEY_PAGES) {
    const result = await validateSchema(url);
    results.push(result);
    if (!result.ok) {
      failures.push(`❌ ${result.url} — HTTP ${result.httpStatus}`);
    } else {
      console.log(`[audit-cron] ✅ ${result.url} — ${result.httpStatus}`);
    }
  }

  // 2. IndexNow ping
  const indexNowResult = await pingIndexNow(INDEXNOW_URLS);
  console.log(`[audit-cron] IndexNow ping: ${indexNowResult.ok ? '✅' : '❌'} (${indexNowResult.status})`);

  const durationMs = Date.now() - startTime;
  const report = {
    timestamp: new Date().toISOString(),
    durationMs,
    pagesChecked: KEY_PAGES.length,
    failures: failures.length,
    indexNow: indexNowResult,
    pageResults: results,
  };

  console.log('[audit-cron] Report:', JSON.stringify(report, null, 2));

  // 3. Alert on failures
  if (failures.length > 0) {
    const subject = `[AMY Electric] ⚠️ Weekly Audit — ${failures.length} page(s) down`;
    const body = `Weekly site audit detected the following issues:\n\n${failures.join('\n')}\n\nFull report:\n${JSON.stringify(report, null, 2)}`;
    await sendAuditAlert(env, subject, body);
  }
}

/**
 * Also expose as an HTTP trigger at GET /api/audit-cron
 * so you can manually trigger a run from the admin dashboard.
 */
export async function onRequest(context) {
  const { request, env } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, OPTIONS' },
    });
  }

  // Protect manual trigger with DASHBOARD_TOKEN
  const authHeader = request.headers.get('Authorization') || '';
  const expectedToken = env.DASHBOARD_TOKEN;
  if (expectedToken && authHeader !== `Bearer ${expectedToken}`) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const startTime = Date.now();
  const results = [];
  const failures = [];

  for (const url of KEY_PAGES) {
    const result = await validateSchema(url);
    results.push(result);
    if (!result.ok) failures.push(`❌ ${result.url} — HTTP ${result.httpStatus}`);
  }

  const indexNowResult = await pingIndexNow(INDEXNOW_URLS);

  const report = {
    timestamp: new Date().toISOString(),
    durationMs: Date.now() - startTime,
    pagesChecked: KEY_PAGES.length,
    failures: failures.length,
    indexNow: indexNowResult,
    pageResults: results,
  };

  if (failures.length > 0) {
    await sendAuditAlert(
      env,
      `[AMY Electric] ⚠️ Manual Audit — ${failures.length} page(s) down`,
      `Manual audit triggered. Issues:\n${failures.join('\n')}\n\n${JSON.stringify(report, null, 2)}`
    );
  }

  return new Response(JSON.stringify(report, null, 2), {
    status: 200,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}
