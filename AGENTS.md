# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor — vanilla HTML/CSS/JS, **no framework and no site build step** — served by Cloudflare **Workers + Assets** from one Worker, `amy-electric-site`, which owns the only zone route (`amyelectric.com/*` in `wrangler.jsonc`). No Pages project, no second proxy Worker.

Business: AMY Electric · C-10 #981578 · EVITP #4051604 · (818) 302-5614 · info@amyelectric.com · Greater Los Angeles.

Push to `main` → `.github/workflows/deploy.yml` (tests → JSON-LD + sitemap parity → `wrangler deploy`). Manual: `wrangler deploy --config wrangler.jsonc`. `package.json` is tooling-only (`cf` + `wrangler` devDeps, no scripts); `wrangler.jsonc` is the live config, `cloudflare.config.ts` mirrors it, `cf build` is validation-only — never run `cf dev/build/deploy` in this repo.

**Be sceptical of plans written for a different stack.** AI-generated roadmaps for this site routinely propose `/electrician/[city-slug]` routes, `data/cities.ts`, `workers/lead-automation.ts`, `public/sitemap.xml`, n8n workflows, or a Durable Object CRM. None of that exists. Real equivalents:

| proposed | actual |
|---|---|
| `/electrician/[city-slug]`, `data/cities.ts` | flat `city-*.html` files + `scripts/generate-city-pages.py` |
| `workers/lead-automation.ts`, n8n | root handler modules wired in `worker.js` + D1 `CRM_DB` |
| `public/sitemap.xml` | `sitemap.xml` at the repo root |
| Durable Object / SQLite dashboard | D1 + the Worker-rendered `/admin` page |

## Current state

- **349 production HTML pages** (`python3 scripts/audit-site.py`); **322 URLs in `sitemap.xml`**. The delta is deliberate noindex/redirect-source exclusions — never "fix" it by adding them. No `<priority>`/`<changefreq>`. `index`, `blog/index`, `case-studies/index` map to directory URLs. Changed pages get `<lastmod>` via `scripts/refresh-sitemap-lastmod.py`, which commits `[skip ci]` back to `main` — expect a rebase before you push.
- 112 `city-*.html` (3 deliberately `noindex`: `city-edith-norman`, `city-el-sobrante`, `city-health-campadre`), 64 geo service pages (24 EV + 24 panel + 16 rewiring), ~91 blog posts, `testimonials.html`, `gallery.html`, `privacy-policy.html`, `service-areas.html`.
- CSS source `css/src/01-*.css`–`12-*.css` → `scripts/build-css.py` → `css/style.min.css`. Site JS source `js/src/01-*.js`–`08-*.js` → `scripts/build-js.py` → `js/site.min.js`. Never edit a `.min.` file.

## Commands (pre-push gate, in this order)

```bash
python3 scripts/schema-tool.py validate
python3 scripts/audit-price-drift.py          # add --strict to gate; non-blocking by design
python3 scripts/audit-site.py                 # 349 pages, 0 issues — NOT in CI, so only you catch regressions
python3 scripts/audit-skills.py
node --test scripts/test-*.mjs                # 122 tests — required if js/, prices or the Worker changed
bash scripts/lint.sh                          # ruff + node --check, report-only (--fix for safe autofixes)
python3 scripts/build-css.py && python3 scripts/build-js.py && python3 scripts/build-estimator.py
git diff --exit-code css/style.min.css js/site.min.js js/estimator.min.js
python3 scripts/build-leadform.py             # NOT in CI — only if js/wizard.js or 05/06 changed
wrangler deploy --dry-run
```

Then push, rebase over the `[skip ci]` lastmod commit, watch the Deploy workflow go green, spot-check live, and run `bash scripts/notify-indexnow.sh` if the workflow didn't.

Never run `sync-faq-schema.py --apply` — it rewrites answer text (verified 2026-10-12).

## Lead platform

`POST /api/contact` → `contact-enrich.js` wraps `contact-handler.js` (validation + email, dependency-free), and only on an accepted lead does it classify/score/dedupe, link uploads, sync CRM and log a funnel event. **Persistence failures never change the visitor's response** — keep it that way.

| module | owns |
|---|---|
| `lead-store.js` | D1 `leads` / `lead_files` / `lead_events` (schema `scripts/lead-schema.sql`), scoring regexes, dedupe window, phone/email normalisation. Returns null with no DB binding, so `node --test` needs no D1. |
| `lead-handler.js` | `/api/lead` proxy to the `CRM_WEBHOOK_URL` secret (URL never reaches the browser), falls back to `/api/contact` |
| `crm-handler.js` | `/api/admin/*`, the `/admin` HTML page, private R2 uploads via `/api/lead-files` (magic-byte validated, capped, random key) |
| `crm-espocrm.js` | EspoCRM mapping: Contact per person, Lead per inquiry, Task follow-up (High for emergency/same-day), Opportunity for commercial only |
| `crm-cron.js` | overdue follow-up digest, Monday weekly report, orphaned-upload cleanup |
| `gbp-agent.js` | Google Business Profile posting; `GBP_DRY_RUN` env gates live posting |

- One cron, `0 16 * * *`: `gbp-agent.js` first, then `runLeadCron`.
- CRM provider order: **EspoCRM → HubSpot → legacy webhook**. The Worker cannot reach a LAN EspoCRM, so the normal path is pull-based — `scripts/espocrm-sync.mjs` drains `/api/admin/leads?crm=pending` from a local 5-minute cron.
- **`/admin` is generated inside `crm-handler.js`** (search `AMY Electric — Leads`). It takes `Authorization: Bearer` or `?token=`. Do not assume it comes from `admin/dashboard.html`.
- `admin/dashboard.html` is **dead code**: `admin/` is in `.assetsignore`, `/admin/dashboard` 404s, nothing links to it. Don't add features there without first wiring it up.

## Three estimator stacks — pick the right source

| surface | source | build → output |
|---|---|---|
| homepage widget | `js/estimator-widget.js` | `scripts/build-estimator.py` → `js/estimator.min.js` |
| `get-quote.html` | `js/src/05-estimate-data.js` + `06-estimate-engine.js` + `js/wizard.js` | `scripts/build-leadform.py` → `js/lead-estimator.min.js` (+ `css/lead-form.min.css`) |
| every page | `js/src/05/06/07` | `scripts/build-js.py` → `js/site.min.js` (07 attaches the indicative range to quote-form leads) |

`js/estimator.js` is legacy and loaded by no page. Prices in `05-estimate-data.js` are canonical and mirrored 1:1 in `scripts/estimate-schema.sql`; `test-estimator.mjs` asserts every row. Permit handling is explicit per service (`included` / `separate` / `unpublished`) — never infer it from `permitId`.

## Gotchas

- **`.assetsignore` is the public surface.** ASSETS serves the repo root, so any file not listed is downloadable. New root Worker module → add it or it is served at `/name.js` (that leak was live until 2026-11-14; `scripts/test-assets-ignore.mjs` now fails CI if a root `.js/.ts/.mjs` is missing). The same file is why `admin/`, `scripts/`, `css/src`, `js/src`, `seo-workspace/` and the stale nested `amyelectric-site/` copy are not public.
- **HTML cache**: `worker.js` sends `public, max-age=300, s-maxage=60, stale-while-revalidate=600`. Do not "fix" it back to `max-age=0, must-revalidate` — the zone edge strips `ETag`/`Content-Length` from Worker HTML, so every repeat visit would re-download the page.
- **Geo personalization**: `/` and `/index.html` only; matched `request.cf.city` makes the response `private, no-store` (the edge cannot vary on `cf.city`). `GEO_TARGET_AREAS` in `worker.js` is 20 City-of-LA neighborhoods — grow the list, `test-worker-geo.mjs` and `js/src/08-geo-personalize.js` together.
- **RUM**: the beacon must stay `"send": {"to": "/cdn-cgi/rum"}`. Never diagnose it from `workers.dev` (no `cdn-cgi` pipeline → 404 by design) or curl — both are artifacts.
- **Live checks**: use the `workers.dev` host for real status codes; apex serves bot challenges to agents (expect 403). `.html` URLs 301 to extensionless, so curl needs `-L`.
- **One Worker only.** `wrangler deploy` publishes only routes it declares and never deletes another script's route, so a stray Worker can silently shadow a path (a fake 5-URL sitemap did exactly that for 3 days). `python3 scripts/audit-cloudflare-routes.py` checks agreement; `.github/workflows/cloudflare-routes.yml` runs it daily.
- **Images**: 545 gallery photos × 4 variants (1200w WebP + 1200w JPEG + 800w/400w WebP) in `img/gallery/`; `worker.js serveImage()` negotiates WebP and snaps `?w=`. `IMAGES` is fallback-only. Gallery LCP is solved — position-0 gets `eager` + `fetchpriority="high"` + preload via `scripts/update-gallery.py`; regenerate, don't hand-edit, and don't trim the ItemList JSON-LD.
- **Edge schema**: `injectSchema()` adds a default `Electrician` block only to HTML that lacks `Electrician`/`LocalBusiness` text. Adding schema to a page that already has it does not double-inject; adding an `Electrician` block by hand does risk drift.
- **Shared CSS lives in 3 places**: `.topbar`, `.nav-book` and the "MOBILE TOUCH TARGETS" block (`css/src/10-responsive.css`) are duplicated into each page's inline critical CSS (264 pages carry `/*topbar-responsive-fix*/`) and into `scripts/generate-city-pages.py`. `scripts/sync-mobile-touch-css.py` mirrors the touch block idempotently — without it the header resizes after first paint and costs CLS. Prose links inside a sentence are deliberately exempt (WCAG 2.5.8 inline exception); do not add rules for `p a`.
- **Quote form radio group**: `<div class="radio-group" role="radiogroup" aria-labelledby="request-type-label">` on 240 pages. Never re-add `<label for="request_type">` — no element has that id, so it names nothing and renders a duplicate label.
- **`/estimator*` is a prefix route**, not a file: `worker.js` sends every path that starts with `/estimator` to the estimator app, so `/estimator-bundle.js` returns that app's HTML rather than a 404 or the file. Never name a page or asset `estimator-*`.
- **`admin/dashboard.html` is dead code.** `admin/` is in `.assetsignore`, `/admin/dashboard` 404s, and nothing links to it. Don't add features there without first wiring it up.
- **`js/webmcp.js`** is injected by a conditional inline snippet on 104 pages, only when `navigator.modelContext` exists. Never make it a plain `defer` tag (it cost 300 ms lab TBT), and don't add it to blog pages.
- **Zone settings that must not change**: Rocket Loader off (it reorders script execution and breaks the booking widget and estimate engine), minify off (bundles pre-minified), Polish lossy, Brotli on, SSL strict, HSTS via `_headers`.
- `testimonials.html` stays published but canonicals to `/reviews` (`_redirects` 301s it too).
- `functions/` and `seo-worker/` no longer exist — don't recreate them from old notes.

## Content rules

- `reviewCount` canonical = `BUSINESS["aggregateRating"]["reviewCount"]` in `scripts/site_data.py` (**87**, 447 occurrences). The validator fails with `REVIEWCOUNT_DRIFT`; the sweep one-liner is in that file's comment. (A stray 24 lives in the stale `amyelectric-site/` copy, which is assets-ignored — don't treat it as drift.)
- Price canonicals: NEMA 14-50 $350–$600, Tesla Wall Connector $500–$1,200, hardwired $500–$1,200. `audit-price-drift.py` cannot see CSS-grid comparison tables or prose that prices a charger without naming one — those need a human sweep.
- Utility correctness: only City-of-LA pages may claim LADWP. `SCE_CITIES` in `generate-city-pages.py` = alhambra, bellflower, carson, santa-clarita; `grep -rl 'coordinate with SCE' city-*.html` must return only those four.
- **26 U.S.C. §30C expired for property placed in service after 2026-06-30.** Do not add 30C claims. ~21 pages still carry them (SCE-territory geo pages, commercial pages, some blog posts) and need editorial rewrite, not regex.
- Photos: raw in `/home/amram/Pictures/Electric Work/` → `process-photos.py` → manifest → `img/gallery/` (`SRC`/`OUT` are repo-relative and overridable via `PHOTOS_SRC`/`GALLERY_OUT` so worktrees stay isolated), then `redact-photos.py`. Redact street numbers, names, faces (unless consenting team), LADWP account numbers — check equipment labels, meter faces, stickers and notes.
- Every page: JSON-LD, OG, Twitter Cards, `tel:18183025614`, images with `loading="lazy"`, `decoding="async"`, `alt` and dimensions. Shared nav/footer changes mean touching every page (or the generator + a sync script).

## Working in this repo

- **Trust `origin/main`, not the working tree.** A stale local checkout can be dozens of commits behind and missing whole modules (the entire lead platform was absent from one that looked current). When a file "doesn't exist", check `git show origin/main:<path>` before concluding anything.
- Branch + PR, never push to `main`. If `gh pr create` 404s, the default `gh` account is not a collaborator: `gh auth switch --user amyelectricalservice-ops`.
- Dependabot PRs get no repository secrets, so preview/route jobs skip `dependabot[bot]`.
- `cf` CLI is authenticated separately from `wrangler`. `cf d1 list` reports `num_tables: 0` for every database — `cf d1 get <id>` shows the truth.
- `package.json` is `"type": "module"`, so CommonJS-style standalone browser scripts cannot be `require()`d (it returns `{}`). Load them through a `vm` sandbox with `{module:{exports:{}}}` (see `loadStandalone` in `test-estimator.mjs`) and JSON-round-trip cross-realm arrays before strict `deepEqual`.
- SEO work lands in `seo-workspace/` (reports, keywords, GSC CSVs). Repo skills live in `.agents/skills/` (hash-pinned in `skills-lock.json`) with `.claude/skills/` symlinked — validate with `python3 scripts/audit-skills.py`. Only the `cloudflare` MCP server is connected; when a skill assumes OpenSEO/DataForSEO, degrade to GSC CSVs `[gsc: file]` → web `[directional: web]` → repo auditors, and never report a number you did not measure.
- `accessibility-audit/` and `audit/` are generated artifacts (assets-ignored). Don't hand-edit them.

## Blocked on the owner — don't invent a workaround

- **Email delivery**: `contact-handler.js` prefers `env.EMAIL`, then MailChannels — but no `EMAIL` binding is declared and both errors are swallowed, so notification mail is effectively dropped until an email sending domain exists. Do not promise email in visitor-facing copy.
- **GA4 / GSC / Google Ads**: IDs and verification tokens are Worker secrets that are not set, so those events are inert. Code paths exist; don't "fix" them without the IDs.
- **Google Business Profile API, review replies, Estimate Pro, Ads/LSA**: blocked on owner-side Google Cloud OAuth, an account, or an undefined product API. Scaffolding for these is speculation, not work.
- **EspoCRM** runs on the LAN at `localhost:8081`; the edge cannot reach it. Keep integrations pull-based.
