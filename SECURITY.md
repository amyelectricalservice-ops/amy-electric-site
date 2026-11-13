# Security policy

This repository is the marketing website for AMY Electric (amyelectric.com),
a licensed C-10 electrical contractor. The site is static HTML served by a
Cloudflare Worker; the only dynamic surface is the lead-capture API.

## Reporting a vulnerability

Email **info@amyelectric.com** with a subject starting `SECURITY:`.

Please include what you found, the URL or file involved, and a short
reproduction. A reply normally comes within a few business days.

Please do **not** open a public issue, and do not include live customer data
(names, phone numbers, addresses, photos) in a report.

## Scope

In scope:

- `worker.js` and the `/api/*` endpoints (lead intake, uploads, admin API).
- The static site under this repository.
- Cloudflare configuration committed here (`wrangler.jsonc`,
  `cloudflare.config.ts`, `_headers`, `_redirects`).

Out of scope:

- Denial-of-service and volumetric testing.
- Spam or bulk submissions to the contact form.
- Automated scanner output without a demonstrated impact.
- Findings that depend on a compromised device, browser extension, or the
  reporter's own Cloudflare/GitHub account.

## What we do not offer

There is no bug bounty and no payment for reports. Credit is given on request.

## Handling

Reports are triaged, reproduced, fixed, and deployed through the normal CI
path. Anything that touches customer data is treated as urgent. This site does
not store payment card data.
