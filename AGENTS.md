# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site (vanilla, no framework, no site build step) for an LA electrical contractor, hosted on Cloudflare **Workers + Assets** (`run_worker_first: true`) — not Pages. Production is **one Worker**, `amy-electric-site`, which declares the single `amyelectric.com/*` zone route in `wrangler.jsonc`. Push to `main` auto-deploys via `.github/workflows/deploy.yml`; manual is `wrangler deploy --config wrangler.jsonc`. Root `package.json` is tooling-only (`cf` + `wrangler`).

- **Business**: AMY Electric · C-10 #981578 · EVITP #4051604 · (818) 302-5614 · info@amyelectric.com · Greater Los Angeles

## Current state (verified 2026-10-23)

- **315 production pages**, **307 sitemap URLs**, 0 audit issues, schema valid, 0 price-drift flags.
  - Sitemap delta is deliberate: `404.html`, `seo-audit-report.html`, 3 noindex cities, 3 retired redirect sources.
- **112** `city-*.html` (3 deliberately `noindex`: edith-norman, el-sobrante, health-campadre); **64** geo service pages (24 EV + 24 panel + 16 rewiring); **62** blog HTML files; **387** gallery photos × 4 variants = 1548 files in `img/gallery/`.
- **CSS**: `css/src/01..12-*.css` → `scripts/build-css.py` → `css/style.min.css`. **JS**: `js/src/01..08-*.js` → `scripts/build-js.py` → `js/site.min.js`. Never edit built files.
- **Estimate engine**: `05-estimate-data.js` (mirrors `scripts/estimate-schema.sql`) + `06-estimate-engine.js` + `07-estimate-lead.js`. Permit handling is explicit per service (`included`/`separate`/`unpublished`) — never infer from `permitId`. `js/estimator.min.js` is the legacy EV bundle the homepage loads; parity asserted by `test-estimator.mjs`.
- **Booking** (`book.html` only): vendored flatpickr 4.6.13 in `js/vendor/` + `css/vendor/`; `js/book.js` slot rules (Sun closed, weekday 8–4, Sat 8–12, min tomorrow, max +60d). flatpickr-on-a-div needs `appendTo`.
- **Root `package.json` is `"type": "module"`**: standalone browser scripts cannot be `require()`d (returns `{}`) — load via `vm` sandbox (see `test-estimator.mjs` `loadStandalone`) and JSON-round-trip cross-realm arrays before `deepEqual`.

## Known factual-consistency debt (fix before adding content)

`AMY Electric Website SEO Audit and Improvement Plan.md` (owner, 2026-10-22) documents conflicts that are **still live**. Verified against the tree on 2026-10-23:

| Debt | Evidence |
| --- | --- |
| Federal 30C credit still presented as current | 256 `30C`/`2032` matches across ~20 pages, incl. `ev-charger-installation.html`, `tesla-charger-installation.html`, `blog/ev-charger-installation-cost-la.html`, `blog/ladwp-ev-charger-rebate-guide-2026.html` |
| LADWP rebate amount contradicts across pages | `$500 in rebate` (34), `$1,000 — with local utility rebate` (32), `$1,000 base rebate`, `$200` |
| Duplicate blog slugs compete | `blog/ev-charger-installation-cost-la.html` + `-cost-los-angeles.html`; `blog/whole-home-rewiring-cost-la.html` + `-cost-los-angeles.html` |
| Internal links point at `/index`, canonical is `/` | 186 `href="/index"` |
| `service-areas.html` template bug | literal `%d` in "All %d Service Areas" |
| Three testimonial sets disagree on names/cities | homepage, `reviews.html`, `testimonials.html` |

Rules that follow from this:
- **Do not propagate any of these numbers into new content.** A new page must not repeat an unverified rebate, 30C, experience-years, or project-count figure.
- The audit's *external* facts (LADWP amount, 30C end date, workers'-comp status) came from search-result excerpts, not fetched pages. Fetched verification is required before citing any of them.
- `reviewCount` stays **87** (canonical in `scripts/site_data.py`, 336 occurrences). Bumping it is owner-supplied only.
- Experience, project counts, insurance wording, and the founder name (Amy/"her" vs Amram/"he") need an owner decision, not an agent guess.

## Gotchas (read before touching)

- **HTML cache**: `worker.js` sends `public, max-age=300, s-maxage=60, stale-while-revalidate=600`. Do NOT "fix" to `max-age=0` — the zone edge strips `ETag`/`Content-Length` from Worker HTML, so repeat visits would re-download full HTML.
- **Geo personalization**: `/` + `/index.html` only; on `request.cf.city` match the response goes `private, no-store`. Target list = `GEO_TARGET_AREAS` in `worker.js` (20 LA neighborhoods; expand list AND `scripts/test-worker-geo.mjs`, which asserts length 20). Consumer `js/src/08-geo-personalize.js` must ship with any worker change.
- **RUM**: beacon injected by `worker.js`, endpoint must stay `"send": {"to": "/cdn-cgi/rum"}`. Never diagnose from `workers.dev` (no `cdn-cgi` pipeline → 404 by design) or curl. Verify with a real browser on apex, or dashboard `events.rumPageloadEvents`.
- **Live checks**: use the `workers.dev` host (real status codes); apex serves bot challenges (expect 403). `.html` URLs 301 to extensionless — curl needs `-L`.
- **`functions/` is dead** (Pages leftover). Sibling Workers (`amy-electric-estimator`, `-photos`, `-portfolio`) are out of scope.
- **Zone routes belong to the site Worker.** An `amy-electric-seo` wrapper was retired 2026-10-18; if it reappears it is wrong. Check with `python3 scripts/audit-cloudflare-routes.py`.
- **Images**: `worker.js serveImage()` negotiates WebP + `?w=` snapping (tests: `test-worker-images.mjs`). IMAGES binding is fallback-only. AVIF measured and parked.
- **Gallery LCP**: position-0 image gets `eager` + `fetchpriority="high"` + preload via `scripts/update-gallery.py` (idempotent — regenerate, don't hand-edit). Don't trim ItemList JSON-LD.
- **Rocket Loader is OFF** (zone setting) — it rewrites script order and threatens flatpickr + the estimate engine. Don't re-enable. Also: Polish lossy, minify off, Brotli on, HTTP/2+3, Early Hints, Speed Brain, Smart Tiered Cache, Mirage off, SSL strict, HSTS via `_headers`.
- **`.topbar` lives in 3 places**: `css/src/02-header.css`, built `style.min.css`, inline critical `<style>` in 161 HTML files (`/*topbar-responsive-fix*/`) + `scripts/generate-city-pages.py`.
- **`.nav-book` follows the same 3-place rule** (`/*nav-book*/` marker); anchor before `nav-cta`. Only show ≤680px inside `nav.open` — desktop nav wraps 3 rows.
- **Mobile touch targets (44×44, ≤767px)**: sized in `css/src/10-responsive.css`; `scripts/sync-mobile-touch-css.py` mirrors the `/*touch-targets*/` block into inline critical CSS. Prose links are deliberately excluded (WCAG 2.5.8 inline exception) — do NOT add `p a` / `.faq-a a` rules.
- **Quote form radio group**: `<label id="request-type-label">` + `role="radiogroup" aria-labelledby` on 238 pages (`scripts/fix-radiogroup-labels.py`). Never re-add `<label for="request_type">` — that id does not exist.

## Content rules

- Shared nav/footer: update every `.html` file. Phone as `tel:18183025614`. Every page: JSON-LD, OG, Twitter Cards. Images: `loading="lazy"`, `decoding="async"`, `alt`, dimensions.
- **Price canonicals only**: NEMA $350–$600, Tesla $500–$1,200, hardwired $500–$1,200. `audit-price-drift.py` is non-blocking by design; `--strict` gates. Blind spots needing human sweeps: CSS-grid comparison tables, prose pricing a charger without naming one, ranges near "no service".
- **Utility correctness**: only City-of-LA pages may claim LADWP; Alhambra, Bellflower, Carson, Santa Clarita are SCE (`SCE_CITIES` in `scripts/generate-city-pages.py`). `grep -rl 'coordinate with SCE' city-*.html` must return only those four.
- **Photos**: raw in `/home/amram/Pictures/Electric Work/` → `scripts/process-photos.py` → `img/gallery/` (`PHOTOS_SRC`/`GALLERY_OUT` override, worktree-safe); then `scripts/redact-photos.py`. Blur/crop street numbers, names, faces (unless consenting team), LADWP account numbers.
- **Blog conventions**: scaffold from 2–3 current posts; title ≤60 chars; FAQPage JSON-LD only for visible on-page pairs (exact text); BreadcrumbList per existing posts; HowTo only where visible step content exists.

## Pre-push gate (in order)

1. `python3 scripts/schema-tool.py validate`
2. `python3 scripts/audit-price-drift.py --strict`
3. `python3 scripts/audit-site.py` (expect 315 pages, 0 issues)
4. `node --test scripts/test-*.mjs` (only if JS/prices/worker touched)
5. Rebuild CSS/JS + `git diff --exit-code` on minified output (only when CSS/JS sources changed)
6. `npx wrangler deploy --dry-run`

Never run `scripts/sync-faq-schema.py --apply` (rewrites answers, verified 2026-10-12). After push: rebase over `[skip ci]` lastmod commits, watch Deploy green, spot-check on `workers.dev`, `bash scripts/notify-indexnow.sh` if the workflow didn't.

## Agents & skills

- **`.opencode/agents/amramseo.md`** — the AMY content writer/publisher (Amram). Publishes static HTML on `content/*` branches with PRs; scope is explainer blogs, cost guides, owner-supplied case studies, and AMY_ESTIMATE docs. Its `permission:` block asks before `git push` and `wrangler deploy`.
- **`.opencode/agents/seo.md`** — SEO orchestrator (`seo`, mode `all`) writing into `seo-workspace/`. Uses the legacy `permission:` map; this opencode build (1.18.33) silently ignores the V2 `permissions:` list — a new agent with only `permissions:` gets no gating.
- Only the `cloudflare` MCP server is connected. All SEO data tools degrade to `websearch`/`webfetch` — label output `[directional: web]`. Prefer repo auditors over skill prose.
- Skill routing: market view → `competitive-landscape`; one domain → `competitor-analysis`; new page → `seo-content-brief`; single page → `seo-page`; tech/crawl → `seo-technical`; sitemap → `seo-sitemap`; images → `seo-images`; prose cleanup → `deslop`.

## Remaining work (owner-sized)

- [ ] **Fix the factual debt above** — highest impact: 30C removal, one LADWP rebate figure (fetched), one testimonial set, `/index` → `/`, one Reviews URL, one emergency URL, `%d` fix.
- [ ] **Merge duplicate blog slugs** (EV cost, rewiring cost) with 301s in `_redirects`.
- [ ] **GBP posts, every other day**: `gbp-posting-calendar.md` (30 posts, 2026-10-21→12-18) from `gbp-posts-document.txt`. ~5 min each, no agent needed.
- [ ] **GBP auto-posting agent**: code shipped (`gbp-agent.js` + 16:00 UTC cron + `GBP-AGENT.md`). PENDING OWNER: Google OAuth credentials + location ID as Worker secrets (5 `wrangler secret put`s), dry-run, go live.
- [ ] **Hero photo**: replace the "LA CITY ELECTRIC" shirt with a real AMY tech shot (owner-supplied, via photo pipeline).
- [ ] **Case studies**: all four are illustrative; replace with real projects + photos, permission first.
- [ ] **PageSpeed field check**: pagespeed.web.dev on homepage vs CrUX targets (<2.5s LCP / <200ms INP / <0.1 CLS / 90+ mobile).
- [ ] **`areaServed` unification**: blocked on owner-supplied per-city county/ZIP data (112 pages in 3 valid shapes — don't invent data).
- [ ] **Live form + RUM**: owner submits a real test lead; checks beacon in a real browser. Agent won't fake-submit.
- [ ] **Yelp/CALeVIP/GBP cleanup**: address spelling, service area, hours, review count.
- [ ] **Hygiene**: bump `reviewCount` as Google reviews grow; human sweep of EV pages for prose/grid prices.
