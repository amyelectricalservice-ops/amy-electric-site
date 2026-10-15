# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site (vanilla, no framework, no site build step) for an LA electrical contractor, hosted on Cloudflare **Workers + Assets** (`run_worker_first: true`) — not Pages. Push to `main` auto-deploys via `.github/workflows/deploy.yml` (validates, then `wrangler deploy`); Workers Builds is connected but non-deploying. Manual: `wrangler deploy --config wrangler.jsonc`. Root `package.json` is tooling-only (`cf`+`wrangler` devDeps); `wrangler.jsonc` is the live config, `cloudflare.config.ts` mirrors it, `cf build` is validation-only. CI on every push (`audit.yml`): JSON-LD validation, CSS/JS reproducibility, sitemap integrity.

- **Business**: AMY Electric · C-10 #981578 · EVITP #4051604 · (818) 302-5614 · info@amyelectric.com · Greater Los Angeles

## Current state

- **314 production HTML pages** (`scripts/audit-site.py`); **309 URLs in `sitemap.xml`** (delta is deliberate noindex/404 exclusions: `404.html`, `seo-audit-report.html`, 3 noindex cities). No `<priority>`/`<changefreq>`. `index`/`blog/index`/`case-studies/index` map to directory URLs. Changed pages get `<lastmod>` bumps via `scripts/refresh-sitemap-lastmod.py` (commits `[skip ci]` back to `main` — expect rebase-before-push).
- 112 `city-*.html` (16 core + neighborhoods; 3 deliberately `noindex`: `city-edith-norman`, `city-el-sobrante`, `city-health-campadre`), 48 geo service pages (24 EV + 24 panel), 60 blog posts, `testimonials.html`, `gallery.html` (310 photos), `privacy-policy.html`, `service-areas.html`.
- **CSS**: source `css/src/01-*.css`–`12-*.css`, built via `scripts/build-css.py` → `css/style.min.css`. **JS**: source `js/src/01-*.js`–`08-*.js` via `scripts/build-js.py` → `js/site.min.js`. Never edit built files.
- Estimate engine: `05-estimate-data.js` (canonical priced tables, mirrors `scripts/estimate-schema.sql` 1:1) + `06-estimate-engine.js` (`window.AMY_ESTIMATE.calcEstimate`) + `07-estimate-lead.js` (attaches indicative range to quote-form leads; `/api/contact` allowlists it, drops invalid without failing the lead). Permit handling is explicit per service (`included`/`separate`/`unpublished`) — never infer from `permitId`. `js/estimator.js` is standalone; `js/estimator.min.js` is the legacy EV bundle the homepage actually loads — parity between the three is asserted by `test-estimator.mjs`, no build step links them.
- Booking widget (`book.html` only): open-source flatpickr 4.6.13 (MIT, (c) 2017 Gregory Petrosyan) vendored version-pinned at `js/vendor/flatpickr-4.6.13.min.js` + `css/vendor/flatpickr-dark-4.6.13.css` — never hand-edit vendored files (contrast/a11y overrides live in book.html `/*book-widget*/` CSS). `js/book.js` is standalone (pure slot rules: Sun closed, weekday 4 windows 8–4, Sat 2 windows 8–12, min tomorrow, max +60d; `window.AMY_BOOK`, tested by `test-book.mjs`). flatpickr-on-a-div needs `appendTo` or the calendar lands at body level.
- Root `package.json` is `"type": "module"`: standalone browser scripts CANNOT be `require()`d in tests (returns `{}`) — load via `vm` sandbox with `{module:{exports:{}}}` (see `test-estimator.mjs` `loadStandalone`), and JSON-round-trip any cross-realm arrays before strict `deepEqual`.
- `js/webmcp.js` loads via conditional inline injector on 99 root pages only when `navigator.modelContext` exists — never a render-blocking `defer` tag (cost 300ms lab TBT; verified 88→98 perf 2026-10-14). Blog pages omit it.
- `testimonials.html` stays published but canonicals to `/reviews`, with a `/testimonials → /reviews` 301 in `_redirects`. All 929 old `testimonials` hrefs repointed 2026-10-14.

## Gotchas (read before touching)

- **HTML cache**: `worker.js` sends `public, max-age=300, s-maxage=60, stale-while-revalidate=600`. Do NOT "fix" back to `max-age=0, must-revalidate` — the zone edge strips `ETag`/`Content-Length` from Worker HTML (ASSETS responses keep theirs), so without max-age every repeat visit re-downloads full HTML.
- **Geo personalization**: `/` + `/index.html` only; on `request.cf.city` match the response goes `private, no-store` (edge can't Vary on `cf.city`). Consumer `js/src/08-geo-personalize.js` must ship with any worker change. Tests: `test-worker-geo.mjs` (12) + `test-geo-personalize.mjs` (4).
- **RUM**: beacon injected by `worker.js`, endpoint must stay `"send": {"to": "/cdn-cgi/rum"}`. Never diagnose RUM from `workers.dev` (no `cdn-cgi` pipeline → 404 by design) or curl (404s on non-beacon POSTs) — both are artifacts, not outages. Verify with a real browser on apex or dashboard `events.rumPageloadEvents`.
- **Live checks**: use the `workers.dev` host (real status codes); apex serves bot challenges to agents (expect 403). `.html` URLs 301 to extensionless — curl needs `-L`.
- **`functions/` is dead** (Pages leftover, never referenced). Sibling Workers (`amy-electric-estimator`, `-photos`, `-portfolio`) are out of scope — do not touch.
- **Images**: 366 gallery photos (310 + 56 Google Photos exports, 2026-10-15) × 4 variants (1200w WebP + 1200w JPEG + 800w WebP + 400w WebP) in `img/gallery/`; `worker.js serveImage()` negotiates WebP + `?w=` snapping (tests: `test-worker-images.mjs`, 15). IMAGES binding is fallback-only — zero billing path active. AVIF measured and parked (needs subscription or pre-generated variants).
- **Gallery LCP is done**: position-0 image gets `eager` + `fetchpriority="high"` + preload via `scripts/update-gallery.py` (idempotent — regenerate, don't hand-edit). Lab 80% has zero flagged opportunities; don't trim ItemList JSON-LD (SEO value).
- **Rocket Loader is OFF** (zone setting, disabled 2026-10-15 via `cf`): it rewrites script execution order and threatens the flatpickr booking widget + estimate engine; the site ships its own defer/idle-load strategy. Do not re-enable. Other zone settings verified same day: Polish lossy, minify off (bundles pre-minified), Brotli on, HTTP/2+3 on, Early Hints on, Speed Brain on, Smart Tiered Cache on, Mirage off, SSL strict, HSTS via `_headers`.
- **`.topbar` lives in 3 places**: `css/src/02-header.css`, built `style.min.css`, inline critical `<style>` in 161 HTML files (`/*topbar-responsive-fix*/` marker) + `generate-city-pages.py` template. Keep in sync; ≤480px stacks, phone link never wraps.
- **`.nav-book` (hamburger-only "📅 Book Online", 305 pages) follows the same 3-place rule**: `css/src/02-header.css` + `css/src/10-responsive.css` (≤680px `nav.open` gate — desktop nav wraps 3 rows, never show it there), inline `/*nav-book*/` marker, `generate-city-pages.py` template. Anchor goes before `nav-cta` (`book` root, `../book` blog); 4 pages without a nav-cta anchor are out of scope.

## Content rules

- Shared nav/footer: update every `.html` file. Phone as `tel:18183025614`. Every page: JSON-LD, OG, Twitter Cards. Images: `loading="lazy"`, `decoding="async"`, `alt`, dimensions.
- `reviewCount` canonical = `BUSINESS["aggregateRating"]["reviewCount"]` in `scripts/site_data.py` (87 as of 2026-10-14; 333 occurrences, zero drift). Validator fails with `REVIEWCOUNT_DRIFT` on mismatch; sweep one-liner is in the site_data.py comment.
- Price canonicals (leads are quoted from these): NEMA $350–$600, Tesla $500–$1,200, hardwired $500–$1,200. `audit-price-drift.py` is non-blocking by design; `--strict` to gate. Blind spots needing human sweeps: CSS-grid comparison tables, prose pricing a charger without naming one, ranges near no service phrase.
- Utility correctness: only City-of-LA pages may claim LADWP; Alhambra/Bellflower/Carson/Santa Clarita are SCE (`SCE_CITIES` in `generate-city-pages.py`). `grep -rl 'coordinate with SCE' city-*.html` must return only those four.
- Photos: raw in `/home/amram/Pictures/Electric Work/` → `process-photos.py` + manifest → `img/gallery/`; `redact-photos.py` after (face blur / text blackout). Privacy rule: crop/blur/redact street numbers, names, faces (unless consenting team), LADWP account numbers — check equipment labels, meter faces, stickers, notes.

## Pre-push gate (in order)

`schema-tool.py validate` → `audit-price-drift.py` (`--strict` to gate) → `audit-site.py` (314 pages, 0 issues) → `node --test scripts/test-*.mjs` if JS/prices/worker touched → rebuild CSS/JS + `git diff --exit-code` on minified output → `wrangler deploy --dry-run`. Never run `sync-faq-schema.py --apply` (rewrites answers, verified 2026-10-12). Then push (rebase over `[skip ci]` lastmod if needed), watch Deploy workflow green, spot-check live on `workers.dev`, `bash scripts/notify-indexnow.sh` if workflow didn't.

## Skills

Repo-local `.agents/skills/`, global `~/.claude/skills/` for the rest. Route: market view → `competitive-landscape`; one domain → `competitor-analysis`; new page → `seo-content-brief`; single page → `seo-page`; tech/crawl → `seo-technical`; sitemap → `seo-sitemap`; images → `seo-images`. Only the `cloudflare` MCP server is connected — all SEO data tools degrade to `websearch`/`webfetch` (directional only, label as such). Prefer repo auditors over skill prose.

## Remaining work (owner-sized; code side is shipped)

- [ ] **GBP posts, every other day** (highest ROI): `gbp-posting-calendar.md` — 30 posts, 2026-10-21→2026-12-18, copy-paste from `gbp-posts-document.txt`. ~5 min each, no agent needed.
- [ ] **GBP auto-posting agent**: CODE SHIPPED 2026-10-14 (`gbp-agent.js` + daily 16:00 UTC cron + `GBP-AGENT.md`). PENDING OWNER: Google Cloud OAuth credentials + location ID as Worker secrets (5 `wrangler secret put`s), dry-run, go live. Until then the calendar stays manual.
- [ ] **Hero photo**: replace "LA CITY ELECTRIC" shirt with a real AMY tech shot; agent swaps via photo pipeline when supplied.
- [ ] **PageSpeed field check**: run pagespeed.web.dev on homepage, compare CrUX LCP/INP/CLS to targets (<2.5s / <200ms / <0.1 / 90+ mobile).
- [ ] **Phase 3 — `/book` page**: SHIPPED 2026-10-14 with open-source booking (flatpickr 4.6.13 MIT date picker + `js/book.js` slot widget posting `request_type: booking-request` to `/api/contact`; slots are REQUESTS confirmed by text — no double-booking protection, never promise guaranteed booking). 112 "📅 Book Online" buttons repointed `index#estimator` → `book`; 203 sticky-bar Estimate buttons repointed (`index#estimate` → `book`, `../index#estimate` → `../book`; same-page `#estimate` anchors and `#estimator` widget links left alone). Possible follow-up: nav-menu + sticky-bar "Book" placement (visual call, held).
- [ ] **`areaServed` unification**: blocked on owner-supplied per-city county/ZIP/Wikipedia data (112 pages currently in 3 valid shapes — don't unify by inventing data).
- [ ] **Live form + RUM**: owner submits a real test lead; checks beacon in dashboard with a real browser. Agent won't fake-submit.
- [ ] **Hygiene**: bump canonical `reviewCount` as Google reviews grow; human sweep of EV pages for prose/grid prices.
- [ ] **Brand mentions**: YouTube/Reddit/Wikipedia presence — real-world effort, not code.
