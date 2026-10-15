/**
 * GBP auto-posting agent (Cloudflare Worker scheduled handler helper).
 *
 * Stateless cadence: post index derives from the calendar start date, so no
 * KV/state is needed. The cron fires DAILY; the handler only posts when the
 * date matches the every-other-day calendar (dayDiff % 2 === 0), which keeps
 * exact calendar dates across 31-day months (a step-value cron would drift).
 *
 * Secrets (wrangler secret put): GBP_CLIENT_ID, GBP_CLIENT_SECRET,
 * GBP_REFRESH_TOKEN, GBP_ACCOUNT_ID, GBP_LOCATION_ID.
 * Set GBP_DRY_RUN=1 to build + log the payload without posting.
 *
 * Pure functions (pickPostIndex, buildLocalPost) are tested by
 * node --test scripts/test-gbp-agent.mjs.
 */
import POSTS from './scripts/gbp-posts.json' with { type: 'json' };

export const CALENDAR_START = '2026-10-21'; // must match gbp-posting-calendar.md
export const CADENCE_DAYS = 2;
export const BOOK_URL = 'https://amyelectric.com/book';

function dayDiff(a, b) {
  const ms = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate())
           - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
  return Math.round(ms / 86400000);
}

function parseDay(s) {
  const [y, m, d] = s.split('-').map(Number);
  // Local midnight (NOT UTC): dayDiff reads both dates through local
  // calendar parts, so constructing in UTC would shift a day behind in
  // negative-offset timezones. The Worker runs UTC, matching calendar dates.
  return new Date(y, m - 1, d);
}

/** True when `now` is a posting day; false → handler exits quietly. */
export function isPostingDay(now = new Date()) {
  return dayDiff(parseDay(CALENDAR_START), now) % CADENCE_DAYS === 0;
}

/** 0-based post index for `now`; wraps the 30-post rotation indefinitely. */
export function pickPostIndex(now = new Date()) {
  const diff = dayDiff(parseDay(CALENDAR_START), now);
  if (diff < 0 || diff % CADENCE_DAYS !== 0) return -1;
  return Math.floor(diff / CADENCE_DAYS) % POSTS.length;
}

export function getPost(index) {
  return POSTS[index] || null;
}

/** LocalPost body for accounts.locations.localPosts.create. */
export function buildLocalPost(post) {
  return {
    languageCode: 'en-US',
    summary: `${post.title}\n${post.body}`,
    topicType: 'STANDARD',
    callToAction: { actionType: 'LEARN_MORE', url: BOOK_URL },
  };
}

function missingSecrets(env) {
  return ['GBP_CLIENT_ID', 'GBP_CLIENT_SECRET', 'GBP_REFRESH_TOKEN',
          'GBP_ACCOUNT_ID', 'GBP_LOCATION_ID']
    .filter((k) => !env[k]);
}

async function refreshAccessToken(env) {
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: env.GBP_CLIENT_ID,
      client_secret: env.GBP_CLIENT_SECRET,
      refresh_token: env.GBP_REFRESH_TOKEN,
      grant_type: 'refresh_token',
    }),
  });
  if (!res.ok) throw new Error(`oauth refresh failed: ${res.status}`);
  const data = await res.json();
  if (!data.access_token) throw new Error('oauth refresh returned no token');
  return data.access_token;
}

async function createLocalPost(env, accessToken, payload) {
  const parent = `accounts/${env.GBP_ACCOUNT_ID}/locations/${env.GBP_LOCATION_ID}`;
  const res = await fetch(
    `https://mybusiness.googleapis.com/v4/${parent}/localPosts`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    }
  );
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`localPosts.create failed: ${res.status} ${text.slice(0, 300)}`);
  }
  return res.json();
}

/** Entry point for the Worker scheduled handler. Never throws. */
export async function handleScheduled(env, now = new Date()) {
  const missing = missingSecrets(env);
  if (missing.length) {
    console.log(JSON.stringify({ type: 'gbp_agent', status: 'skipped_no_secrets', missing }));
    return { status: 'skipped_no_secrets', missing };
  }
  if (!isPostingDay(now)) {
    return { status: 'skipped_not_posting_day', date: now.toISOString().slice(0, 10) };
  }
  const index = pickPostIndex(now);
  const post = getPost(index);
  if (!post) return { status: 'error', message: 'no post for index ' + index };
  const payload = buildLocalPost(post);
  if (env.GBP_DRY_RUN === '1') {
    console.log(JSON.stringify({
      type: 'gbp_agent', status: 'dry_run', post: post.n, city: post.city,
      summaryChars: payload.summary.length,
    }));
    return { status: 'dry_run', post: post.n, city: post.city };
  }
  try {
    const token = await refreshAccessToken(env);
    const created = await createLocalPost(env, token, payload);
    console.log(JSON.stringify({
      type: 'gbp_agent', status: 'posted', post: post.n, city: post.city,
      name: created.name || '',
    }));
    return { status: 'posted', post: post.n, city: post.city, name: created.name || '' };
  } catch (err) {
    console.log(JSON.stringify({ type: 'gbp_agent', status: 'error', post: post.n, message: String(err).slice(0, 300) }));
    return { status: 'error', post: post.n, message: String(err).slice(0, 300) };
  }
}
