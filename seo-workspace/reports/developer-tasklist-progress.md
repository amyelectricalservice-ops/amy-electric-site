# AMY Electric developer task list — progress by task ID

Branch: `feat/espocrm` (EspoCRM) / `feat/lead-gen-phase1` (original platform) · Staging: `https://amy-electric-site-staging.a-m-y-electricalservice.workers.dev`
Last updated: 2026-11-12

Legend:
- **DONE** — implemented and demonstrated (test or live check named)
- **CODE** — code shipped and tested, but the task is not finished until an owner credential/account step is completed
- **SPEC** — deliverable is a plan/spec; nothing was created in a third-party account
- **BLOCKED** — missing information or access; cannot proceed safely

---

## Website and conversion

| ID | Status | What was actually done / evidence |
|---|---|---|
| AE-001 | **DONE** | Removed the literal placeholder `Keep the existing Quick Quote form component here.` and the duplicate empty section from `contact.html`. Every form posts to `/api/contact` (JSON + FormData). Tested locally and on staging: accepted lead persisted, 400 on invalid phone. |
| AE-002 | **DONE** | Homepage H1 rewritten to an outcome promise ("Licensed Electrician in Los Angeles — Upfront Pricing. Permits Handled."); three CTAs reduced to call / 60-second price / book. Playwright: 1 H1, 0 horizontal overflow at 390 px. |
| AE-003 | **DONE** | Already present, verified: gold topbar with `tel:`, header "Call Now", hero call button, mobile sticky bar (call / text / quick quote). 11 `tel:18183025614` links on the homepage. |
| AE-004 | **DONE** | New `residential-electrician.html`: services, canonical price table, process, reviews, 12 city links, FAQ, upload-enabled form, `Electrician` + `Service` + `BreadcrumbList` + `FAQPage` schema. Linked from home nav, services page and commercial page; added to sitemap. |
| AE-005 | **DONE** | `commercial-electrical.html` already existed; added a residential cross-link and verified page/schema. |
| AE-006 | **DONE** | Photo + PDF uploads: magic-byte validation (JPEG/PNG/WebP/HEIC/PDF), 10 MB/file, 5 files, private R2 keys, SHA-256, 20 uploads/hour/IP. Tested locally and on staging (upload → lead → authenticated download roundtrip byte-identical). |
| AE-007 | **DONE** | Quick form is 3 required fields + optional uploads; the detailed form stays collapsed in `<details>`. Mobile Playwright run: 0 overflow, no console/page errors (RUM 405 is a known local/workers.dev artifact). |
| AE-008 | **DONE** | The priced estimator (`05-estimate-data` + `06-estimate-engine` + `07-estimate-lead`) was already live with indicative ranges and permit handling. Verified parity tests (101/101), and estimates now attach to the stored lead. |
| AE-009 | **DONE** | Homepage trust bar links to CSLB verification and reviews; contact page has a "Credentials you can verify" block (active status, issue/expiry, bond); new page carries the same. Claims corrected where CSLB contradicted them (see AE-010). |
| AE-010 | **DONE** | Verified live on CSLB 2026-11-12: **C-10 #981578 current and active**, issued 2013-03-02, expires 2027-03-31, bond $25,000 (American Contractors Indemnity), workers' comp **exempt** (no employees). Removed first-person workers'-comp claims (89 files) and "15+ years" (341 files → "over a decade"). |

## CRM integration

| ID | Status | What was actually done / evidence |
|---|---|---|
| AE-011 | **DONE** | **EspoCRM** (FOSS, GPLv3) integrated: `crm-espocrm.js` + `scripts/espocrm-sync.mjs` create Contact → Lead → Task (+ Opportunity for commercial). Tested against the running instance. HubSpot remains an optional fallback. |
| AE-012 | **DONE** | Residential and commercial leads are separated by `segment`; commercial also creates an EspoCRM Opportunity at stage *Prospecting*, residential stays a Lead. |
| AE-013 | **DONE** | Every accepted lead creates/reuses a Contact, creates a Lead, and creates a follow-up Task (idempotent by parent+name). Tested end-to-end. |
| AE-014 | **DONE** | `leads` table stores project type, city, phone, email, source page, referrer, all UTMs, gclid/fbclid, IP hash, user agent. Verified on staging. |
| AE-015 | **DONE** | Deterministic 0–100 score with reasons (urgency, segment, service weight, completeness, paid click, local area code). Tested; staging commercial lead scored 68. |
| AE-016 | **CODE** | New-lead visibility comes from EspoCRM (task assigned to the configured user) plus the daily overdue digest. EspoCRM's own email notifications need its outbound mail configured; the admin desk is the guaranteed fallback. |
| AE-017 | **DONE** | Task per lead in EspoCRM with due date (emergency +15 min, same-day +2 h, otherwise next day), High priority for emergency. Daily overdue digest still runs. |
| AE-018 | **DONE** | 30-day de-dupe on normalised phone then email; duplicate is stored for attribution, flagged `duplicate_of`, and no second deal is created. Tested twice locally. |
| AE-019 | **DONE** | Private R2 bucket `amy-electric-leads`; no public URL; downloads require the admin token. Uploads validated and hashed. |
| AE-020 | **DONE** | Forms tested desktop + mobile (local, staging, production); EspoCRM ingestion tested from the real lead pipeline. |

## SEO and Google marketing

| ID | Status | What was actually done / evidence |
|---|---|---|
| AE-021 | **CODE** | Worker injects the GA4 tag into every HTML response when `GA4_ID` is set (no 342-file edit). CSP updated. Needs the GA4 measurement ID as a secret. |
| AE-022 | **CODE** | Worker injects `<meta name="google-site-verification">` when `GSC_VERIFICATION` is set. Needs the token from Search Console (or DNS verification). |
| AE-023 | **CODE** | Google Ads gtag config + conversion firing on a *successful* lead only (`GADS_ID` + `GADS_CONVERSION_LABEL`). |
| AE-024 | **DONE** | First-party `phone_click` / `cta_click` / `form_submit` / `lead_accepted` events already post to `/api/events`; `lead_accepted` is now fired from a wrapped `fetch` so every form path counts once, and it forwards to GA4/Ads when configured. |
| AE-025 | **SPEC** | GBP post copy v2 (`gbp-posts-document-v2.txt`, 30 posts) and the posting calendar; auto-posting agent still needs Google OAuth secrets. |
| AE-026 | **DONE** | EV page already strong; left intact (prices canonical, schema valid). |
| AE-027 | **DONE** | Panel page already strong; left intact. |
| AE-028 | **DONE** | Commercial page kept, cross-linked to residential, schema valid. |
| AE-029 | **CODE** | City pages exist (112). Unique-content deepening is an editorial task; no pages were rewritten in this pass. |
| AE-030 | **DONE** | `schema-tool.py validate` passes, `audit-site.py` 342 pages / 0 issues, sitemap 322 URLs, canonical checks pass. |

## Lead acquisition

| ID | Status | What was actually done / evidence |
|---|---|---|
| AE-031 | **SPEC** | `seo-workspace/ads/google-ads-campaign-plan.md` — EV campaign: ad groups, keywords, RSAs, negatives, budget, conversion actions. |
| AE-032 | **SPEC** | Same doc — panel-upgrade campaign (200A, hazard panels, capacity). |
| AE-033 | **SPEC** | Same doc — residential campaign (repairs, rewiring, lighting). |
| AE-034 | **SPEC** | Same doc — commercial campaign (TI, fleet, 3-phase). |
| AE-035 | **SPEC** | `seo-workspace/ads/lsa-eligibility.md` — requirements, gaps, budget, screening. |
| AE-036 | **DONE** | `prospects` table + `POST /api/admin/prospects` + `scripts/prospect-import.py` (tested locally; upsert and merge verified). |
| AE-037 | **DONE** | `scripts/permit-monitor.py` pulls LADBS submitted electrical permits, filters to service-area ZIPs, scores them, writes CSV, and can push to the prospect table. Tested: 22 scored opportunities from 7 days. |
| AE-038 | **DONE** | `ad_spend` + `jobs` tables, admin endpoints, and report math (CPL, CPQL, close rate). Tested locally: $35 spend / 3 leads → $12 CPL, $18 CPQL. |

## AI and reporting

| ID | Status | What was actually done / evidence |
|---|---|---|
| AE-039 | **CODE** | `POST /api/admin/qualify` runs Workers AI (`@cf/meta/llama-3.1-8b-instruct`) with a strict JSON contract, falling back to the deterministic scorer. Fallback tested; AI path needs a live account check. |
| AE-040 | **DONE** | Commercial detection (keywords + service) drives segment, score weight and pipeline selection. Tested. |
| AE-041 | **BLOCKED** | "Estimate Pro" is not defined anywhere in the repo and no API/account details were supplied. Need endpoints/auth before wiring. |
| AE-042 | **DONE** | `draftEstimate()` produces a range + lines + assumptions from the submitted project; `POST /api/admin/draft-estimate` tested (panel lead → $2,500–$4,500 + permit line). |
| AE-043 | **CODE** | Follow-up timestamps stored per lead, HubSpot task created, daily cron digest. Delivery channel needs `HUBSPOT_TOKEN` or `LEAD_NOTIFY_WEBHOOK`. |
| AE-044 | **DONE** | `/admin` (token or Basic auth) shows 30-day totals, commercial/emergency counts, avg score, won, and the latest 40 leads. 401 without token, 200 with token (local + staging). |
| AE-045 | **CODE** | `jobs` table + `POST /api/admin/jobs` + revenue in the report. No owner UI for data entry yet (API + CSV only). |
| AE-046 | **DONE** | `GET /api/admin/report?days=7` returns the weekly marketing report; the Monday cron sends the same shape. Tested locally. |
| AE-047 | **DONE** | Rule-based recommendations (spend missing, low commercial share, low emergency share, low avg score, low close rate) included in the report. AI enrichment is available but not required. |
| AE-048 | **CODE** | `scripts/security-check.sh` (headers, admin auth, upload rejection, contact method) passes on staging; `scripts/backup-d1.sh` exports/gzips/rotates both D1 databases outside the repo. Security test must be re-run against production after deploy. |

---

## Verified in this pass

- `schema-tool.py validate` — all pages pass
- `audit-price-drift.py --strict` — 0 flagged
- `audit-site.py` — 342 pages, 0 issues
- `audit-skills.py` — 29/29 locked
- `node --test scripts/test-*.mjs` — **101/101**
- `bash scripts/lint.sh` — OK
- `wrangler deploy --dry-run` — bindings present
- Playwright (390 px): `/`, `/contact`, `/residential-electrician`, `/commercial-electrical`, `/services`, `/panel-upgrade`, `/book` → 200, 0 overflow, 1 H1, valid JSON-LD
- Staging: health bindings, admin 401/200, lead persisted with score/segment, upload→download byte-identical, `security-check.sh` all pass

## Outstanding owner actions (in order)

1. **EspoCRM**: confirm the `amy-site` user role and the assigned user in `~/.amy-electric/espocrm.env`; install the 5-minute cron for `scripts/espocrm-sync.mjs`; configure EspoCRM outbound email if you want notification emails (HubSpot is no longer required).
2. **GA4 + Ads + Search Console**: create the GA4 property, then set `GA4_ID`, `GADS_ID`, `GADS_CONVERSION_LABEL`, `GSC_VERIFICATION` as Worker secrets. Update the two conversion actions in Google Ads to match `lead_accepted` and `phone_click`.
3. **Email notifications**: confirm whether Cloudflare Email Routing / a send binding is available for `info@amyelectric.com`; otherwise set `LEAD_NOTIFY_WEBHOOK` to a Slack/Zapier endpoint so overdue-lead digests are delivered.
4. **Launch the four Ads campaigns** from the spec after the conversion tags show as recording.
5. **LSA application** (account + background check + COI).
6. **Estimate Pro**: provide the product's API/base URL and auth so AE-041 can be wired.
7. **Insurance wording**: confirm the general-liability carrier/limits; if confirmed, the "certificate of insurance on request" copy can name the coverage.
8. **Google reviews**: bump `reviewCount` in `scripts/site_data.py` when the count changes (validator enforces zero drift).

## Known limitations

- Lead uploads are accepted before the lead exists; unlinked uploads are deleted after 7 days by the daily cron.
- The admin dashboard is intentionally minimal (read-only list + CSV + JSON report). Status changes go through `POST /api/admin/lead/:id`.
- Workers AI is not exercised in local dev; the rules fallback always runs, so qualification never blocks a lead.
- No owner UI exists yet for `jobs`/`ad_spend`; they are API/CSV-driven until the dashboard grows.
- The staging Worker is intentionally route-less; delete it after the production release (`npx wrangler delete --name amy-electric-site-staging`).
