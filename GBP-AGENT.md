# GBP Auto-Posting Agent — Setup

The Worker posts `gbp-posting-calendar.md` to your Google Business Profile
every other day, automatically. Code is fully shipped and tested; what
remains is Google-side credentials only you can create (OAuth must be
granted by the Google account that manages the business listing).

## How it works

- Cron fires **daily at 16:00 UTC** (9am PDT / 8am PST). The handler posts
  only on calendar dates (stateless: post index derives from 2026-10-21).
- Each post goes out as a `STANDARD` local post with a **Learn more → /book**
  button (drives the booking funnel).
- Rotation wraps after post 30 and repeats indefinitely.
- Everything is logged (`type: gbp_agent`) to Workers Logs.

## Setup (owner, ~20 min + Google approval wait)

1. **Google Cloud project**: create one at console.cloud.google.com, enable
   the **Business Profile APIs** (My Business Account Management + Business
   Information + Local Post endpoints). Note: Google may require an API
   access approval request — file it early, it can take days.
2. **OAuth client**: APIs & Services → Credentials → Create OAuth client ID
   (Desktop app is simplest). Note the client ID + secret.
3. **Refresh token** (easiest path — OAuth 2.0 Playground):
   - Go to developers.google.com/oauthplayground, click the gear → check
     "Use your own OAuth credentials", enter the client ID + secret.
   - Select scope `https://www.googleapis.com/auth/business.manage` →
     Authorize with the Google account that manages the GBP listing →
     Exchange tokens. Copy the **refresh token**.
4. **Account + location IDs** (with a fresh access token from step 3):
   ```
   curl -H "Authorization: Bearer ACCESS_TOKEN" \
     https://mybusinessaccountmanagement.googleapis.com/v1/accounts
   curl -H "Authorization: Bearer ACCESS_TOKEN" \
     https://mybusinessbusinessinformation.googleapis.com/v1/accounts/{accountId}/locations
   ```
   Copy the numeric `accountId` and `locationId` (`locations/{id}`).
5. **Store secrets** (never commit these):
   ```
   wrangler secret put GBP_CLIENT_ID
   wrangler secret put GBP_CLIENT_SECRET
   wrangler secret put GBP_REFRESH_TOKEN
   wrangler secret put GBP_ACCOUNT_ID
   wrangler secret put GBP_LOCATION_ID
   wrangler secret put GBP_DRY_RUN   # value: 1 (remove when going live)
   ```
6. **Dry-run first**: deploy, then watch logs on the next posting day
   (`npx wrangler tail` — expect `status: dry_run` with the right post #).
   Then `wrangler secret delete GBP_DRY_RUN`, redeploy, and confirm a real
   post lands on the profile.
7. **Local trigger test** (optional): `npx wrangler dev --test-scheduled`
   fires cron handlers on demand against `.dev.vars` secrets.

## Caveats

- POST 1 says "$50 off ... this month" — refresh time-sensitive copy in
  `gbp-posts-document.txt` + `python3 scripts/build-gbp-posts.py` before its
  rotation date returns, or it will post stale offers.
- Text-only posts v1. Upgrade path: attach a rotating gallery photo via the
  media upload endpoint (needs `accounts.locations.media` scope + code).
- Paid third-party APIs (post in 5 min, no Google approval) exist if the
  approval stalls — owner's call, not implemented here.
