# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor — vanilla HTML/CSS/JS, **no framework and no site build step** — served by Cloudflare **Workers + Assets** from one Worker, `amy-electric-site`, which owns the zone route `amyelectric.com/*` in `wrangler.jsonc`. No Pages project, no proxy Worker in front of it.

Business: AMY Electric · C-10 #981578 · EVITP #4051604 · (818) 302-5614 · info@amyelectric.com · Greater Los Angeles. Repo: `amyelectricalservice-ops/amy-electric-site`.

Push to `main` → `.github/workflows/deploy.yml` (node tests → JSON-LD + sitemap parity → `wrangler deploy`), plus `.github/workflows/audit.yml` (site audit + bundle-freshness diff + sitemap integrity) and `.github/workflows/cloudflare-routes.yml`. Manual: `wrangler deploy --config wrangler.jsonc`. `package.json` is tooling-only (`cf` + `wrangler` devDeps, no scripts); `wrangler.jsonc` is the live config, `cloudflare.config.ts` mirrors it — never run `cf dev/build/deploy` in this repo.

**Be sceptical of plans written for a different stack.** AI-generated roadmaps for this site routinely propose `/electrician/[city-slug]` routes, `data/cities.ts`, `workers/lead-automation.ts`, `public/sitemap.xml`, n8n workflows, or a Durable Object CRM. None of that exists. Real equivalents:

| proposed | actual |
|---|---|
| `/electrician/[city-slug]`, `data/cities.ts` | flat `city-*.html` files + `scripts/generate-city-pages.py` |
| `workers/lead-automation.ts`, n8n | root handler modules wired in `worker.js` + D1 `CRM_DB` |
| `public/sitemap.xml` | `sitemap.xml` at the repo root |
| Durable Object / SQLite dashboard | D1 + the Worker-rendered `/admin` page |

## Baseline (re-measured 2026-11-19, branch `fix/red-main-and-backlog`)

The gate below is green: `schema-tool.py validate` passes, `audit-site.py` reports 0 issues over 371 pages, `audit-skills.py` passes, 133 tests pass, `sync-nav.py --check` is clean. The two things that were red on `44e79257` — the `contact-handler.js` regression that 400'd every form submission, and the four `electrician-*` pages/`case-studies` links that failed the audit — are fixed. Re-measure before claiming a green baseline on a later HEAD.

Not fixed, because they are owner-blocked rather than code bugs: no `EMAIL` binding (notification mail is silently dropped), no GA4/GSC/Ads secrets (every event is a no-op), and no capability-sheet PDF.

## Current state

- **371 production HTML pages** (`python3 scripts/audit-site.py`); **328 URLs in `sitemap.xml`**. The delta is deliberate noindex/redirect-source exclusions — never "fix" it by adding them. No `<priority>`/`<changefreq>`. `index` → `/`, `blog/index` → `/blog/`. Changed pages get `<lastmod>` via `scripts/refresh-sitemap-lastmod.py`, which commits `[skip ci]` back to `main` — expect a rebase before you push.
- 112 `city-*.html` (3 deliberately `noindex`: `city-edith-norman`, `city-el-sobrante`, `city-health-campadre`), **65** geo service pages (24 EV + 24 panel + **17** rewiring), 92 `blog/*.html`, `testimonials.html`, `gallery.html`, `privacy-policy.html`, `service-areas.html`, `contractors-commercial.html` (B2B lander), and 8 `case-studies/*.html`.
- The four `electrician-{burbank,glendale,santa-monica,sherman-oaks}.html` pages are **aliases**, like the three older `electrician-*` pages: `noindex, follow` with a canonical to the matching `city-*` page. They exist for the exact-match query, not as indexable duplicates. Do not "fix" their sitemap absence.
- CSS source `css/src/00-*.css`–`12-*.css` → `scripts/build-css.py` → `css/style.min.css`. Site JS source `js/src/01..03, 05..08` (there is **no `04`**) → `scripts/build-js.py` → `js/site.min.js`. Never edit a `.min.` file.

## Commands (pre-push gate, in this order)

```bash
python3 scripts/schema-tool.py validate        # in CI
python3 scripts/audit-site.py                  # in CI; 371 pages, 0 issues
python3 scripts/audit-skills.py                # in CI
python3 scripts/sync-nav.py --check            # in CI; one canonical header
node --test scripts/test-*.mjs                 # in CI; 133 tests
bash scripts/lint.sh                           # ruff + node --check; no rewrites, exits non-zero on findings (--fix for safe ruff fixes)
python3 scripts/build-css.py && python3 scripts/build-js.py \
  && python3 scripts/build-estimator.py && python3 scripts/build-leadform.py
git diff --exit-code css/style.min.css js/site.min.js js/estimator.min.js \
  js/lead-estimator.js js/lead-estimator.min.js css/lead-form.min.css
python3 scripts/audit-price-drift.py            # report-only by design; --strict to gate
wrangler deploy --dry-run
```

Then push, rebase over the `[skip ci]` lastmod commit, watch Deploy go green, spot-check live, and run `bash scripts/notify-indexnow.sh` if the workflow didn't.

Never run `sync-faq-schema.py --apply` — it rewrites answer text (verified 2026-10-12).

**Nav is generated from one source: `scripts/sync-nav.py`.** It renders the canonical 7-item menu plus the "More" panel, computes the `../` prefix from each file's depth, and is idempotent; `--check` runs in CI so a hand-edited header fails the build. When you add a page that belongs in the menu, add it to `MORE_COL_1`/`MORE_COL_2` and re-run the script — do not hand-edit 371 files.

`scripts/inject-layout.py` is **retired** and now exits 1 with an explanation. It injected root-relative partials, replaced the first `<nav>` it found (the breadcrumb on some pages), stripped `class="main-nav"` and the "More" panel, and would have regressed ~367 pages. The `partials/` directory it read was deleted with it. Do not resurrect either.

## Lead platform

`POST /api/contact` → `contact-enrich.js` wraps `contact-handler.js` (validation + notification, dependency-free), and only on an accepted lead does it classify/score/dedupe, link uploads, sync CRM and log a funnel event. **Persistence failures never change the visitor's response** — keep it that way.

| module | owns |
|---|---|
| `lead-store.js` | D1 `leads` / `lead_files` / `lead_events` (schema `scripts/lead-schema.sql`), scoring regexes (`COMMERCIAL_RE`, emergency/same-day), dedupe window, phone/email normalisation. Returns null with no DB binding, so `node --test` needs no D1. |
| `lead-handler.js` | `/api/lead` proxy to the `CRM_WEBHOOK_URL` secret (URL never reaches the browser), falls back to `/api/contact` |
| `crm-handler.js` | `/api/admin/*`, the `/admin` HTML page, private R2 uploads via `/api/lead-files` (magic-byte validated, capped, random key) |
| `crm-espocrm.js` | EspoCRM mapping: Contact per person, Lead per inquiry, Task follow-up (High for emergency/same-day), Opportunity for commercial only |
| `crm-cron.js` | overdue follow-up digest, Monday weekly report, orphaned-upload cleanup |
| `gbp-agent.js` | Google Business Profile posting; `GBP_DRY_RUN=1` gates live posting, credentials are `GBP_*` secrets |
| `estimator-handler.js` / `photo-handler.js` | `/estimator*` app, and the legacy `/api/photos*` admin endpoints |

- One cron, `0 16 * * *`: `gbp-agent.js` first, then `runLeadCron`.
- `contact-handler.js` now contains **its own D1 insert** (the `44e79257` regression) that duplicates `lead-store.js`'s job with placeholder scoring. The live path is `contact-enrich.js` → `lead-store.js`; fix the duplication by restoring the deleted helpers, not by extending the inline insert.
- CRM provider order: **EspoCRM → HubSpot → legacy webhook**. The Worker cannot reach a LAN EspoCRM, so the normal path is pull-based — `scripts/espocrm-sync.mjs` drains `/api/admin/leads?crm=pending` from a local 5-minute cron.
- **`/admin` is generated inside `crm-handler.js`** (search `AMY Electric — Leads`). It takes `Authorization: Bearer` or `?token=`. `admin/dashboard.html` is **dead code**: `admin/` is in `.assetsignore`, `/admin/dashboard` 404s, nothing links to it.
- Worker endpoints beyond pages: `/api/contact`, `/api/lead`, `/api/lead-files`, `/api/events`, `/api/health`, `/api/admin/*`, `/estimator*`, plus an agent-facing surface generated in `worker.js` — `/openapi.json`, `/a2a`, `/.well-known/{openid-configuration,agent.json,api-catalog,mcp/server-card.json,agent-skills/index.json}`, `/llms.txt`, `/llms-full.txt`. Changing the contact schema means updating that spec too.

## Three estimator stacks — pick the right source

| surface | source | build → output |
|---|---|---|
| homepage + `get-quote.html` widget | `js/estimator-widget.js` | `scripts/build-estimator.py` → `js/estimator.min.js` |
| `get-quote.html` wizard | `js/src/05-estimate-data.js` + `06-estimate-engine.js` + `js/wizard.js` | `scripts/build-leadform.py` → `js/lead-estimator.min.js` (+ `css/lead-form.min.css`) |
| every page | `js/src/05/06/07` | `scripts/build-js.py` → `js/site.min.js` (07 attaches the indicative range to quote-form leads) |

`build-leadform.py` enforces budgets (JS ≤ 24 KB — the current bundle is 23,973 bytes, so it is nearly at the limit — CSS ≤ 14 KB). `js/estimator.js` is legacy and loaded by no page. Prices in `05-estimate-data.js` are canonical and mirrored 1:1 in `scripts/estimate-schema.sql`; `test-estimator.mjs` asserts every row. Permit handling is explicit per service (`included` / `separate` / `unpublished`) — never infer it from `permitId`.

## Gotchas

- **`.assetsignore` is the public surface.** ASSETS serves the repo root, so any file not listed is downloadable. Two leaks were live (2026-11-14 root Worker modules; 2026-11-15 `.claude/`, `data/`, `markdown/`, `wrangler.staging.jsonc`, internal docs). `scripts/test-assets-ignore.mjs` now fails CI if *any* tracked file outside the public allowlist (`img/ blog/ css/ js/ fonts/ case-studies/ .well-known/` + root `*.html` + a short list incl. `SECURITY.md` and the IndexNow key files) would be served. New root Worker module → add it to `.assetsignore` **and** keep that test green.
- **Internal docs live in `docs/`, not the repo root** — `docs/ops/`, `docs/seo/`, `docs/audits/`. Only `AGENTS.md`, `README.md`, `SECURITY.md`, `GEMINI.md` stay at the root, and `docs/` is assets-ignored as a whole.
- **HTML cache**: `worker.js` sends `public, max-age=300, s-maxage=60, stale-while-revalidate=600`. Do not "fix" it back to `max-age=0, must-revalidate` — the zone edge strips `ETag`/`Content-Length` from Worker HTML, so every repeat visit would re-download the page. `_headers` gives `/css/*` and `/js/*` `max-age=3600, s-maxage=3600` because the bundles are not fingerprinted.
- **Geo personalization**: `/` and `/index.html` only; matched `request.cf.city` makes the response `private, no-store`. `GEO_TARGET_AREAS` in `worker.js` is 20 City-of-LA neighborhoods — grow the list, `test-worker-geo.mjs` and `js/src/08-geo-personalize.js` together.
- **RUM**: the beacon must stay `"send": {"to": "/cdn-cgi/rum"}`. Never diagnose it from `workers.dev` (no `cdn-cgi` pipeline → 404 by design) or curl — both are artifacts.
- **Live checks**: use the `workers.dev` host for real status codes (`https://amy-electric-site.a-m-y-electricalservice.workers.dev`); apex serves Bot Fight Mode challenges to agents (expect 403, and CI treats that as "edge up"). `.html` URLs 301 to extensionless (`_redirects` `/*.html /:splat 301`), so curl needs `-L`.
- **The account has three Workers; only one is in this repo.** `wrangler deploy` publishes only the routes it declares and never deletes another script's route, so an unmanaged Worker can silently shadow a path — a stray `seo-sitemap` Worker served a fake 5-URL sitemap to Google for three days in 2026-10.

  | Worker | in repo | surface | note |
  |---|---|---|---|
  | `amy-electric-site` | yes | `amyelectric.com/*` | everything below |
  | `amyelectric-lead-automation` | **no** | `amyelectric.com/api/leads` only | owner-managed; all site forms post to `/api/contact`, `/api/lead`, `/api/lead-files`, `/api/events` |
  | `amyelectric-marketing-agent` | **no** | workers.dev only, no zone route | owner-managed Durable Object app; `/dashboard` returns 401 |

  Do not delete the two out-of-repo Workers and do not "adopt" their routes into `wrangler.jsonc`. `scripts/audit-cloudflare-routes.py` allowlists the lead-automation route via `EXPECTED_OTHER_WORKERS`.
- **Images**: 545 gallery photos × 4 variants (1200w WebP + 1200w JPEG + 800w/400w WebP) in `img/gallery/`; `worker.js serveImage()` negotiates WebP and snaps `?w=`. `IMAGES` is fallback-only. Gallery LCP is solved — position-0 gets `eager` + `fetchpriority="high"` + preload via `scripts/update-gallery.py`; regenerate, don't hand-edit, and don't trim the ItemList JSON-LD.
- **Edge schema**: `injectSchema()` adds a default `Electrician` block only to HTML that lacks `Electrician`/`LocalBusiness` text. Adding schema to a page that already has it does not double-inject; adding an `Electrician` block by hand does risk drift.
- **Shared CSS lives in 3 places**: `.topbar`, `.nav-book` and the "MOBILE TOUCH TARGETS" block (`css/src/10-responsive.css`) are duplicated into each page's inline critical CSS (277 pages carry `/*topbar-responsive-fix*/`) and into `scripts/generate-city-pages.py`. `scripts/sync-mobile-touch-css.py` mirrors the touch block idempotently — without it the header resizes after first paint and costs CLS. Prose links inside a sentence are deliberately exempt (WCAG 2.5.8 inline exception); do not add rules for `p a`.
- **Quote form radio group**: `<div class="radio-group" role="radiogroup" aria-labelledby="request-type-label">` (252 pages). Never re-add `<label for="request_type">` — no element has that id, so it names nothing and renders a duplicate label.
- **`/estimator*` is a prefix route**, not a file: every path starting with `/estimator` is proxied to the estimator app, so `/estimator-bundle.js` returns that app's HTML rather than the file. Never name a page or asset `estimator-*`.
- **`js/webmcp.js`** is injected by a conditional inline snippet on 116 pages, only when `navigator.modelContext` exists. Never make it a plain `defer` tag (it cost 300 ms lab TBT), and don't add it to blog pages.
- **Zone settings that must not change**: Rocket Loader off (it reorders script execution and breaks the booking widget and estimate engine), minify off (bundles pre-minified), Polish lossy, Brotli on, SSL strict, HSTS via `_headers`.
- `testimonials.html` stays published but canonicals to `/reviews` (`_redirects` 301s it too).
- `go.mod` + `cmd/build/main.go` are an **unused Go minifier**; all real builds are Python. `functions/`, `seo-worker/` and `estimator-app/` no longer exist — don't recreate them from old notes.
- `package.json` is `"type": "module"`, so CommonJS-style standalone browser scripts cannot be `require()`d (it returns `{}`). Load them through a `vm` sandbox with `{module:{exports:{}}}` (see `loadStandalone` in `test-estimator.mjs`) and JSON-round-trip cross-realm arrays before strict `deepEqual`.

## Content rules

- `reviewCount` canonical = `BUSINESS["aggregateRating"]["reviewCount"]` in `scripts/site_data.py` (**87**, 479 occurrences). The validator fails with `REVIEWCOUNT_DRIFT`; the sweep one-liner is in that file's comment. (A stray 24 lives in the assets-ignored `amyelectric-site/` copy — not drift.)
- **Price canonicals — do not "standardise" them to a backlog's rounder numbers.** NEMA 14-50 $350–$600, Tesla Wall Connector $500–$1,200, hardwired $500–$1,200; panel upgrades quote $2,500–$4,500 on the main pages. The source of truth is `js/src/05-estimate-data.js` mirrored into `scripts/estimate-schema.sql`, asserted row-by-row by `test-estimator.mjs`. Changing a range means changing the data file, the SQL, the page copy and the test together. `audit-price-drift.py` cannot see CSS-grid comparison tables or prose that prices a charger without naming one — those need a human sweep.
- Utility correctness: only City-of-LA pages may claim LADWP. `SCE_CITIES` in `generate-city-pages.py` = alhambra, bellflower, carson, santa-clarita; `grep -rl 'coordinate with SCE' city-*.html` must return only those four.
- **Federal energy credits: all expired.** Per the IRS FAQ on Public Law 119-21 (2025-07-04): §25C and §25D ended for property placed in service / expenditures after 2025-12-31; §25E and §30D ended for vehicles acquired after 2025-09-30; §30C ended for property placed in service after 2026-06-30; §179D ended for construction beginning after 2026-06-30. Never present any of them as currently available — a historical mention must say when it ended. `scripts/test-tax-claims.mjs` scans production pages and JS source and fails CI on an unqualified claim. Editorial rewrite, not regex.
- Photos: raw in `/home/amram/Pictures/Electric Work/` → `process-photos.py` → manifest → `img/gallery/` (`SRC`/`OUT` are repo-relative and overridable via `PHOTOS_SRC`/`GALLERY_OUT` so worktrees stay isolated), then `redact-photos.py`. Redact street numbers, names, faces (unless consenting team), LADWP account numbers — check equipment labels, meter faces, stickers and notes.
- Every page: JSON-LD, OG, Twitter Cards, `tel:18183025614`, images with `loading="lazy"`, `decoding="async"`, `alt` and dimensions.

## Backlog reality check (P0–P3 plans)

A recurring roadmap asks for price standardisation, CSLB copy fixes, LADWP/ADU authority pages, a 3-way inquiry form, a `/contractors-commercial` page, schema/review work and GA4 conversion events. Check before building:

- **Already shipped**: `/ev-charger-installation-los-angeles`, `adu-electrical.html`, `ladwp-electrical-guide.html`, 65 geo service pages, commercial pages, `meter spot` (6 pages), CALeVIP (5), EVITP (385), load calculations (113). Contact and quote forms already collect `city`, optional file uploads, and the server already captures UTM/gclid/fbclid in `contact-enrich.js:attribution()`.
- **Genuinely missing**: any `/contractors-commercial` (or B2B) page; Charge Up LA copy (0 pages); a capability-sheet PDF.
- **Traps**: the inquiry selector is `name="request_type"` with existing values `service` / `estimate` — `lead-store.js` scores `commercial` / `emergency` from regex over `service`+`message`+`request_type`, so new option values must be added to those regexes or B2B leads score as residential. GA4 events already exist with different names (`phone_click`, `form_submit`, `quote_submit`, `estimate_sent`, …) in `js/src/02-analytics.js`; rename only with the dashboards in mind. The GA4/GSC IDs are Worker secrets that are not set, so every event is a no-op today.
- **Owner-blocked, don't invent workarounds**: email delivery (`contact-handler.js` prefers `env.EMAIL`, then MailChannels — no `EMAIL` binding is declared and both errors are swallowed, so notification mail is dropped; never promise email in visitor copy), GA4/GSC/Ads IDs, GBP API/review replies, Estimate Pro, Ads/LSA, and any edge→LAN EspoCRM call (it runs at `localhost:8081`; keep integrations pull-based).

## Working in this repo

- **Trust `origin/main`, not the working tree.** A stale local checkout can be dozens of commits behind and missing whole modules. When a file "doesn't exist", check `git show origin/main:<path>` first.
- Branch + PR, never push to `main`. If `gh pr create` 404s, the default `gh` account is not a collaborator: `gh auth switch --user amyelectricalservice-ops`.
- **Editing this file is CI-checked.** `scripts/audit-skills.py` treats every backticked lowercase-kebab token in `AGENTS.md` and `.opencode/agents/*.md` as a skill id and fails unless it resolves to a real `SKILL.md` or sits on its allowlist. Backtick full filenames (`file.js`, `page.html`) or paths instead of bare slugs, and extend the allowlist in that script when you introduce a new prose token.
- Project subagents live in `.opencode/agents/` (`gbp`, `seo`, `geo-linking`, `web-perf`) and plans in `.opencode/plans/`.
- Dependabot PRs get no repository secrets, so preview/route jobs skip `dependabot[bot]`.
- `cf` CLI is authenticated separately from `wrangler`. `cf d1 list` reports `num_tables: 0` for every database — `cf d1 get <id>` shows the truth.
- SEO work lands in `seo-workspace/` (reports, keywords, GSC CSVs). Repo skills live in `.agents/skills/` (hash-pinned in `skills-lock.json`) with `.claude/skills/*` symlinked — validate with `python3 scripts/audit-skills.py` (29 skills). Only the `cloudflare` MCP server is connected; when a skill assumes OpenSEO/DataForSEO, degrade to GSC CSVs `[gsc: file]` → web `[directional: web]` → repo auditors, and never report a number you did not measure.
- `accessibility-audit/`, `audit/`, `reports/` are generated artifacts (assets-ignored). Don't hand-edit them.
