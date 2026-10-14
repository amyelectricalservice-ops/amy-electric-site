# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor hosted on Cloudflare Workers + Assets. Pushes to `main` auto-deploy via `.github/workflows/deploy.yml` (schema/sitemap validation, then `wrangler deploy`); Workers Builds is connected but non-deploying (green since the 2026-10-14 `open-seo` gitlink fix; empty build/deploy commands, workflow remains the deploy path). Manual deploy also works with `wrangler deploy --config wrangler.jsonc`. No site build step; a tooling-only root `package.json` (private, `cf`+`wrangler` devDeps) supports the `cf`-migrated config (`cloudflare.config.ts`, `wrangler.config.ts` — `wrangler.jsonc` still live). GitHub Actions runs on every push to `main` (`.github/workflows/audit.yml`): JSON-LD validation via `scripts/schema-tool.py`, CSS/JS build reproducibility, and sitemap integrity.

- **Business name**: AMY Electric
- **License**: C-10 #981578 (verify at [CSLB](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578)), EVITP #4051604
- **Phone**: (818) 302-5614
- **Email**: info@amyelectric.com
- **Service area**: Greater Los Angeles (16 city pages, 62+ ZIP codes)

## Current state

- **313 production HTML pages** (per `scripts/audit-site.py`; 308 URLs in `sitemap.xml`, delta is deliberate noindex/404 exclusions):
  - Homepage: `index.html`
  - 246 root-level + 61 `blog/` HTML files on disk
  - **112 `city-*.html` files** (16 core cities + neighborhood pages) with FAQPage + BreadcrumbList + Electrician schema — note: 3 (`city-edith-norman`, `city-el-sobrante`, `city-health-campadre`) are deliberately `noindex` (commit `2255643`) and excluded from the sitemap
  - **48 geo service pages** (24 `ev-charger-installation-{city}.html` + 24 `panel-upgrade-{city}.html`) with FAQPage (7 Qs each) + BreadcrumbList + Electrician schema
  - 60 blog posts + index with BlogPosting + FAQPage + BreadcrumbList
  - Special pages include `testimonials.html`, `gallery.html` (310 photos), `privacy-policy.html`, `service-areas.html`
  - (Older revisions of this file said "76 pages / 16 city / 32 geo / 33 blog" — superseded by the counts above, verified 2026-10-08)
- **4 service pages** have HowTo schema (`ev-charger-installation`, `panel-upgrade`, `generator-transfer-switch`, `whole-home-rewiring`; added 2026-10-12 — the prior claim of 4 was wrong, zero pages had it). Steps mirror visible page content (assessment → LADWP coordination → install → inspection)
- **CSS** at `css/style.min.css` (production, ~30KB) — source modules in `css/src/01-*.css` through `css/src/12-*.css`, built via `scripts/build-css.py`
- **JS** at `js/site.min.js` (production) — source modules in `js/src/01-*.js` through `js/src/08-*.js`, built via `scripts/build-js.py` — plus `js/estimator.min.js` (~8.4KB) legacy EV-only bundle for the homepage quote estimator. `05-estimate-data.js` holds priced service/material/adder tables (every value sourced from site content; mirrors `scripts/estimate-schema.sql` 1:1) and `06-estimate-engine.js` is the pure calculation layer (`window.AMY_ESTIMATE.calcEstimate`), tested by `node --test scripts/test-estimate-engine.mjs` (16 tests: math, FK integrity, permit handling, JS/SQL parity). Permit treatment is explicit per service via `permitHandling` (`included` / `separate` / `unpublished`) — never inferred from `permitId` alone, because NULL means both "inside the base range" (200A panel) and "never published" (rewiring). `07-estimate-lead.js` attaches an indicative range to quote-form leads as a hidden `estimate` field (mappable services only; assumptions labeled; permit note derived from `permitHandling`; `/api/contact` accepts it via `contact-handler.js` allowlist, invalid payloads dropped without failing the lead), tested by `node --test scripts/test-estimate-lead.mjs` (6) + `test-contact-estimate.mjs` (4). `js/estimator.js` is a standalone (unbundled) project estimator — `estimateProject({projectType, serviceAmperage, linearDistance})` returns price range + material/labor lines + permit flag as JSON, tested by `node --test scripts/test-estimator.mjs` (12 tests incl. parity with the bundled engine data **and** with the shipped `js/estimator.min.js` price table — that widget file is what the homepage actually loads and no build step derives one from the other, so the parity test is what catches drift)
- **`favicon.svg`** — navy background with gold "AE" lightning bolt
- **`robots.txt`** — allows /, explicitly allows 8 AI search crawlers, blocks 3 training crawlers, RSL link, Sitemap
- **`_redirects`** — Cloudflare Pages HTTPS + www canonicalization
- **`sitemap.xml`** — 307 URLs with `<lastmod>` (no `<priority>`/`<changefreq>` — Google ignores both). Deliberate exclusions: `404.html`, `seo-audit-report.html` (both `noindex`), 3 noindex cities. `index`/`blog/index`/`case-studies/index` map to directory URLs (`/`, `/blog/`, `/case-studies/`). Deploys bump `<lastmod>` only for changed pages via `scripts/refresh-sitemap-lastmod.py` (commits `[skip ci]` back to `main`)
- **`gbp-posts-document.txt`** — 30 Google Business Profile post ideas
- **`*~`** and **`.antigravitycli/`** are in `.gitignore`

## What to know

- **Hosting**: Cloudflare **Workers + Assets** (`wrangler deploy`, `run_worker_first: true`) — not Pages. Minify is off in the dashboard because `scripts/build-css.py` / `build-js.py` already ship minified output; Polish is lossy (WebP)
- **HTML caching** (set by `HTML_CACHE_CONTROL` in `worker.js`): `public, max-age=300, s-maxage=60, stale-while-revalidate=600`. **Do not "fix" this back to `max-age=0, must-revalidate`.** The original audit added a SHA-256 `ETag` + `If-None-Match` → 304 path, and it works — but only on `workers.dev`: the zone edge **strips both `ETag` and `Content-Length` from Worker-built HTML** while leaving them on ASSETS responses (favicon/CSS/JS keep theirs). With no validator ever reaching the browser, `max-age=0, must-revalidate` meant a full ~21 KB HTML re-download on *every* repeat visit. The `max-age` + `stale-while-revalidate` pair is the validator-independent fix; `s-maxage=60` keeps the edge revalidating so a deploy never lingers. Verify with `curl -D - https://amyelectric.com/ | grep -i cache-control`.
- **Geo personalization** (`GEO_TARGET_AREAS` in `worker.js`: Northridge, Winnetka, Canoga Park): on `/` + `/index.html` only, a `request.cf.city` match injects `data-service-city` on `<header>` and `window.AMY_GEO` for the frontend, and the response goes out `private, no-store` — the edge cannot Vary on `cf.city`, so a shared-cache policy would leak one visitor's city to others. The visible consumer is `js/src/08-geo-personalize.js`, which rewrites the hero eyebrow to the matched city (same node → no CLS) — it must ship with the worker change, otherwise matched visitors pay the no-store cache opt-out for a page that looks identical. Tested by `node --test scripts/test-worker-geo.mjs` (12 tests with stubbed edge requests) + `scripts/test-geo-personalize.mjs` (4). Non-matches and all other pages keep the shared policy above.
- **No dev server** — open HTML files directly in a browser to preview
- **All pages share the same nav bar** and footer — when updating shared layout, update every `.html` file
- **No framework** — vanilla HTML
- **Images**: 5 original JPEGs in `img/`. 30 real project photos in `img/gallery/` (1200w WebP + 1200w JPEG + 400w WebP per photo). WebP conversion handled by Cloudflare Polish. `worker.js` `serveImage()` also negotiates WebP at the edge (Accept: image/webp|avif on `/img/*.jpg|png` serves the sibling `.webp`, `?w=`/`?width=` snaps to 400/800/1200 variants, optional `IMAGES` binding in `wrangler.jsonc` transforms arbitrary widths with `format:auto` + `caches.default`), tested by `node --test scripts/test-worker-images.mjs` (15 tests). Served from self so CSP `img-src` needs no change. Live 2026-10-14: byte-exact static fallback serves prod (no active Images transform path — zero billing risk). AVIF measured same day (ffmpeg libaom crf30: hero 43KB vs WebP 83KB vs JPEG 100KB) but parked: needs an active Images subscription or pre-generated `.avif` variants, unjustified while WebP/LCP is healthy. `cloudflare.config.ts` mirrors `wrangler.jsonc` (compat date, IMAGES binding, log sampling); `wrangler.jsonc` stays the live deploy config, `cf build` is validation-only.
- **Analytics**: Cloudflare Web Analytics (RUM). Site token `f960270c37b54f689d72991f9503b718` (site provisioned + enabled since 2026-05-22); the beacon is injected by `worker.js` (`RUM_BEACON`) because auto-install does not reach Worker-served HTML — not by `site.js`, which has no analytics code. **The config must keep `"send": {"to": "/cdn-cgi/rum"}`**: it is the correct same-origin endpoint on apex (real-browser POST returns 204, verified 2026-10-13). **Do not diagnose RUM from `workers.dev` or curl**: `workers.dev` has no `cdn-cgi` edge pipeline so its `/cdn-cgi/rum` 404s by design, and curl POSTs 404 on apex too (endpoint only accepts real beacon payloads) — both are measurement artifacts, not outages (this exact mistake burned a session on 2026-10-12/13). Verify only with a real browser on apex, or `events.rumPageloadEvents` in the dashboard. The GA deferred loader was removed.
- **Contact forms**:
  - Homepage: Two-tier — `quick-form` (3 fields: name, phone, service) by default, `estimate-form` (7 fields) in expandable `<details>` toggle
  - POST to `/api/contact` — handled by `worker.js` → `contact-handler.js` (honeypot `website` field + `_timestamp` time-trap reject anything submitted in under 3s). `functions/` is leftover Pages Functions and is **not** deployed; `wrangler.jsonc` never references it
- **Sticky call bar**: Mobile-only gold bar fixed to bottom on all production pages (hidden ≥768px; audit verifies 0 missing)
- **Published price drift**: `python3 scripts/audit-price-drift.py` diffs the EV charger prices printed on pages against the canonical ranges in `js/src/05-estimate-data.js` (the values leads are actually quoted). Pages are hand-written, so they drift. The owner applied a **"use the higher price" pass on 2026-10-12**: every published range sitting *below* canonical on either bound was raised to canonical, anything already at or above it was left alone, and permit lines were never touched. That took 16 flagged pairs to **0**. Canonical today is NEMA **$350–$600**, Tesla **$500–$1,200** (unchanged — it was already the highest same-scope figure), hardwired **$500–$1,200**; `js/estimator.js` and the shipped `js/estimator.min.js` carry matching rows and `scripts/test-estimator.mjs` asserts parity, so raising a canonical without the widgets fails CI. Ranges that are genuinely a *different* scope are documented in `ALT_SCOPES` with the reason printed in the report rather than silently accepted — e.g. the LA cost-breakdown table prices the circuit and permit on their own rows, so its `$1,200–$2,500` Tesla row is not comparable to the all-in `$500–$1,200`. Also catches `$350$550`-style prices with a missing separator (fixed 3 on `ev-charger-hardwired-vs-plug-in.html`, which published them straight into live FAQ schema). Runs in CI as a **non-blocking** report — correcting copy is an owner decision, not a build failure; pass `--strict` to gate on it. Prices come from two independent passes, because one alone was not enough: proximity (first range within 160 chars of a service phrase, stopping at a row boundary) and a table-structure pass, where a charger named in a `<th>` claims its column and one named in a row's label cell claims that row's price. The table pass matches a bare charger name — safe only inside a label cell — so `Hardwired` must sit beside an EV word or it prices hardwired smoke/CO detectors as chargers. It stops at a row boundary, so a neighbouring column can never be swallowed. **Both passes still miss two shapes**: a CSS-grid comparison table with no `<table>` around it, and prose that prices a charger without naming one ("a typical Level 2 installation costing $500-$900"). Those need a human sweep of the EV pages — that gap is how ten below-canonical prices shipped while this script reported 0.
- **Photo pipeline**: Raw photos in `/home/amram/Pictures/Electric Work/` → `scripts/process-photos.py` + `scripts/photo-manifest.csv` → `img/gallery/`. Each photo outputs 1200w WebP + 1200w JPEG + 400w WebP. EXIF stripped, 4:3 crop, orientation fixed. To add new photos: edit manifest and run `python3 scripts/process-photos.py`.
- **Privacy redactions**: `scripts/redact-photos.py` applies in-place edits to published photos. Supports Gaussian face blur (`blur_box`) and black-box text redaction (`blackout_box`). Run after `process-photos.py` for photos containing faces or identifiable text/numbers.
- **Custom crop per photo**: Add `custom_crop` column to `photo-manifest.csv` with source-pixel coordinates `x1,y1,x2,y2`. Used when a center 4:3 crop doesn't exclude privacy-sensitive content (e.g., meter face with account numbers). Example: `"0,0,3024,2268"` for a portrait photo cropped to top 56%.
- **Privacy rule**: Any published photo with visible street number/address, customer name, identifiable face (unless confirmed as consenting team member), or LADWP account number must be cropped/blurred/redacted before deployment. Review every photo before publishing — addresses can appear on equipment labels, meter faces, stickers, and handwritten notes.

## File conventions

- All HTML files reference `css/style.min.css` and `js/site.min.js`
- Each service page: `<section class="page-hero">`, service grid, FAQ using `<details>`, FAQPage JSON-LD, CTA section
- Each city page: Electrician JSON-LD with `areaServed` (City + DefinedRegion/postalCode), Local Knowledge section, FAQ
- Phone number uses `tel:18183025614` throughout
- Every page has JSON-LD (Electrician/Service/FAQPage/BlogPosting), Open Graph, Twitter Cards
- All images have `loading="lazy"`, `decoding="async"`, and `alt` text
- All pages have `<link rel="preload" as="style" href="css/style.min.css">`

## Weekly Audit Checklist

Run these checks in Google Search Console and Cloudflare Web Analytics:

1. **Search Console → Coverage**: Check for new 404 or 500 errors
2. **Search Console → Sitemaps**: Verify sitemap submitted and fresh
3. **Search Console → Performance**: Review top queries and CTR for service pages
4. **RUM (not GA4 — GA was removed)**: Cloudflare Web Analytics dashboard, spot-check beacon 204s if traffic looks off (see Analytics note above)
5. **Contact funnel**: test `/api/contact` from homepage quick-form; check honeypot/time-trap still rejecting spam
6. **Manual spot-check**: Open 3 random service pages + 1 city page in browser
7. **Schema validation**: https://search.google.com/test/rich-results test homepage
8. **Mobile test**: Chrome DevTools mobile emulator on 3 pages
9. **PageSpeed Insights**: Run https://pagespeed.web.dev/audit on homepage weekly

## Auditing with skills

Repo-local skills (`.agents/skills/`): `competitive-landscape`, `competitor-analysis`, `keyword-clustering`, `keyword-research`, `link-prospecting`, `seo-coach`, `seo-project-setup`, `web-perf`. Global `~/.claude/skills/` adds the rest (`seo-audit`, `seo-page`, `seo-technical`, `seo-sitemap`, `seo-schema`, `seo-content`, `seo-local`, `seo-geo`, `seo-images`, …). Route by intent:

- Market view across rivals → `competitive-landscape`; one-domain deep dive → `competitor-analysis`; new page plan → `seo-content-brief` (+ `keyword-clustering`); single-page check → `seo-page`; tech/crawl → `seo-technical`; sitemap → `seo-sitemap`; images → `seo-images`
- **MCP caveat (verified): only the `cloudflare` MCP server is connected.** All OpenSEO data tools (`research_keywords`, `get_serp_results`, `get_domain_overview`, `get_ranked_keywords`, backlinks, local SERP) are unavailable, as is the Chrome DevTools MCP behind `web-perf`. Data-driven skills still work but degrade to `websearch`/`webfetch` fallback: directional only, no traffic/backlink estimates — always label results as such
- Prefer the repo's own executable auditors over skill prose — they encode owner decisions CI enforces. Run in this order: `python3 scripts/schema-tool.py validate` → `python3 scripts/sync-faq-schema.py` (dry-run only: its mismatch report false-positives on pages whose schema is verified in sync, and `--apply` rewrites answers by swallowing whole pages — verified 2026-10-12, reverted) → `python3 scripts/audit-price-drift.py --strict` (0 flagged; non-blocking in CI by design) → `python3 scripts/audit-site.py` (expect 312 pages, 0 issues) → `node --test scripts/test-estimate-*.mjs scripts/test-estimator.mjs` if JS/prices touched → `scripts/build-css.py` + `scripts/build-js.py` + `git diff --exit-code` on minified output if sources changed
- Known guardrail gaps (do not trust a green report blindly): price-drift misses pages whose ranges sit near no service phrase (e.g. `ev-charger-vs-panel-upgrade.html` shipped `$350–$900` vs canonical `$350–$1,200` while reporting 0 — fixed 2026-10-12); misses CSS-grid comparison tables and prose that prices a charger without naming one
- Utility correctness is a recurring content bug: only `$CITY is inside the City of Los Angeles$` pages may claim LADWP coordination (Alhambra/Bellflower/Carson/Santa Clarita are genuinely SCE — verified). `grep -rl 'coordinate with SCE' city-*.html` must return only those four
- Live verification that works from CI/sandbox: `workers.dev` host (`https://amy-electric-site.a-m-y-electricalservice.workers.dev/...`) returns real status codes; `amyelectric.com` serves bot challenges to non-browser agents (expect 403, not failure)

## Performance Targets

- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1
- Mobile PageSpeed score: 90+

Achieved via: minified CSS/JS, lazy-loaded images, preload hints, HTTPS redirects, Cloudflare edge caching.

## Important Notes

- **Deployment**: automatic on push to `main` via `.github/workflows/deploy.yml` (validates, then `wrangler deploy` with `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` repo secrets). Workers Builds is connected but non-deploying (workflow remains the deploy path). Manual deploy also works via `wrangler deploy --config wrangler.jsonc` against the zone-owning account (`a08528fe…`). CLI rule: use the `cf` CLI for Cloudflare interactions unless the project has a Wrangler configuration file — this repo has `wrangler.jsonc`, so `wrangler` stays the deploy tool and `cf` is validation-only (`cf build`). The `_headers` file must use proper path-prefixed format for Workers + Assets (each block starts with a URL path like `/*` or `/css/*`). See `DEPLOYMENT-AMY-ELECTRIC.md`.
- **IndexNow**: Key at `/16076f14-4d06-4581-b281-38a7a89804ca.txt`. Notify after each deploy by running `bash scripts/notify-indexnow.sh` or via `curl` to `https://api.indexnow.org/indexnow`.
- **DNS** (zone `amyelectric.com`, 8 records as of 2026-10-14): apex A `192.0.2.1` + www CNAME (both proxied, Worker-served), Email Routing MX/SPF/DKIM, Google site-verification TXT. `estimator.amyelectric.com` detached 2026-10-14 (was the custom domain of the `amy-electric-estimator` Worker; Worker itself left deployed). Sibling Workers in the account (`amy-electric-estimator`, `-photos`, `-portfolio`) are outside this repo — do not touch without owner direction.
- **New files this session**: `blog/california-electrical-code-changes-2026.html`, `blog/ladwp-ev-charger-rebate-guide-2026.html`
- **Gallery**: `gallery.html` (273KB, 309 photos) — first 36 items HTML, 273 JS-lazy via "Show More". Inline CSS → `css/src/12-gallery.css`. `scripts/update-gallery.py` is idempotent.
- **Schema improvements this session**: FAQPage (4→7 Qs) + BreadcrumbList on all 32 geo pages; BreadcrumbList on 7 root pages + 31 blog posts; HowTo schema on 4 service pages; PriceRange/offers on 11 service pages; homepage FAQ expanded 4→15 Qs
