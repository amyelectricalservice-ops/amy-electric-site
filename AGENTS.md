# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor hosted on Cloudflare Workers + Assets. Pushes to `main` auto-deploy via `.github/workflows/deploy.yml` (schema/sitemap validation, then `wrangler deploy`); Workers Builds is **not** connected. Manual deploy also works with `wrangler deploy --config wrangler.jsonc`. No build system and no package manager, but GitHub Actions runs on every push to `main` (`.github/workflows/audit.yml`): JSON-LD validation via `scripts/schema-tool.py`, CSS/JS build reproducibility, and sitemap integrity.

- **Business name**: AMY Electric
- **License**: C-10 #981578 (verify at [CSLB](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578)), EVITP #4051604
- **Phone**: (818) 302-5614
- **Email**: info@amyelectric.com
- **Service area**: Greater Los Angeles (16 city pages, 62+ ZIP codes)

## Current state

- **312 production HTML pages** (per `scripts/audit-site.py`; 307 URLs in `sitemap.xml`, delta is deliberate noindex/404 exclusions):
  - Homepage: `index.html`
  - 246 root-level + 61 `blog/` HTML files on disk
  - **112 `city-*.html` files** (16 core cities + neighborhood pages) with FAQPage + BreadcrumbList + Electrician schema — note: 3 (`city-edith-norman`, `city-el-sobrante`, `city-health-campadre`) are deliberately `noindex` (commit `2255643`) and excluded from the sitemap
  - **48 geo service pages** (24 `ev-charger-installation-{city}.html` + 24 `panel-upgrade-{city}.html`) with FAQPage (7 Qs each) + BreadcrumbList + Electrician schema
  - 60 blog posts + index with BlogPosting + FAQPage + BreadcrumbList
  - Special pages include `testimonials.html`, `gallery.html` (310 photos), `privacy-policy.html`, `service-areas.html`
  - (Older revisions of this file said "76 pages / 16 city / 32 geo / 33 blog" — superseded by the counts above, verified 2026-10-08)
- **4 service pages** have HowTo schema (panel-upgrade, ev-charger-installation, generator-transfer-switch, whole-home-rewiring)
- **CSS** at `css/style.min.css` (production, ~30KB) — source modules in `css/src/01-*.css` through `css/src/12-*.css`, built via `scripts/build-css.py`
- **JS** at `js/site.min.js` (production) — source modules in `js/src/01-*.js` through `js/src/06-*.js`, built via `scripts/build-js.py` — plus `js/estimator.min.js` (~8.4KB) legacy EV-only bundle for the homepage quote estimator. `05-estimate-data.js` holds priced service/material/adder tables (every value sourced from site content; mirrors `scripts/estimate-schema.sql` 1:1) and `06-estimate-engine.js` is the pure calculation layer (`window.AMY_ESTIMATE.calcEstimate`), tested by `node --test scripts/test-estimate-engine.mjs` (14 tests: math, FK integrity, JS/SQL parity)
- **`favicon.svg`** — navy background with gold "AE" lightning bolt
- **`robots.txt`** — allows /, explicitly allows 8 AI search crawlers, blocks 3 training crawlers, RSL link, Sitemap
- **`_redirects`** — Cloudflare Pages HTTPS + www canonicalization
- **`sitemap.xml`** — all 76+ pages with `<lastmod>`, priorities (1.0 home, 0.9 high-value services, 0.8 services, 0.7 cities, 0.6 special/blog)
- **`gbp-posts-document.txt`** — 30 Google Business Profile post ideas
- **`*~`** and **`.antigravitycli/`** are in `.gitignore`

## What to know

- **Hosting**: Cloudflare **Workers + Assets** (`wrangler deploy`, `run_worker_first: true`) — not Pages. Minify is off in the dashboard because `scripts/build-css.py` / `build-js.py` already ship minified output; Polish is lossy (WebP)
- **HTML caching** (set by `HTML_CACHE_CONTROL` in `worker.js`): `public, max-age=300, s-maxage=60, stale-while-revalidate=600`. **Do not "fix" this back to `max-age=0, must-revalidate`.** The original audit added a SHA-256 `ETag` + `If-None-Match` → 304 path, and it works — but only on `workers.dev`: the zone edge **strips both `ETag` and `Content-Length` from Worker-built HTML** while leaving them on ASSETS responses (favicon/CSS/JS keep theirs). With no validator ever reaching the browser, `max-age=0, must-revalidate` meant a full ~21 KB HTML re-download on *every* repeat visit. The `max-age` + `stale-while-revalidate` pair is the validator-independent fix; `s-maxage=60` keeps the edge revalidating so a deploy never lingers. Verify with `curl -D - https://amyelectric.com/ | grep -i cache-control`.
- **No dev server** — open HTML files directly in a browser to preview
- **All pages share the same nav bar** and footer — when updating shared layout, update every `.html` file
- **No framework** — vanilla HTML
- **Images**: 5 original JPEGs in `img/`. 30 real project photos in `img/gallery/` (1200w WebP + 1200w JPEG + 400w WebP per photo). WebP conversion handled by Cloudflare Polish.
- **Analytics**: Cloudflare Web Analytics (RUM). Site token `f960270c37b54f689d72991f9503b718`; the beacon is injected by `worker.js` (`RUM_BEACON`) because auto-install does not reach Worker-served HTML — not by `site.js`, which has no analytics code. **The config must keep `"send": {"to": "/cdn-cgi/rum"}`**: without it the beacon posts cross-origin to `cloudflareinsights.com/cdn-cgi/rum`, which answers 404 (no CORS header) and silently drops every event — that bug zeroed RUM from 10-01 to 10-04 while traffic looked normal. Same-origin `/cdn-cgi/rum` returns 204 and lands events; verify with `events.rumPageloadEvents` if in doubt. The GA deferred loader was removed.
- **Contact forms**:
  - Homepage: Two-tier — `quick-form` (3 fields: name, phone, service) by default, `estimate-form` (7 fields) in expandable `<details>` toggle
  - POST to `/api/contact` — handled by `worker.js` → `contact-handler.js` (honeypot `website` field + `_timestamp` time-trap reject anything submitted in under 3s). `functions/` is leftover Pages Functions and is **not** deployed; `wrangler.jsonc` never references it
- **Sticky call bar**: Mobile-only gold bar fixed to bottom on all production pages (hidden ≥768px; audit verifies 0 missing)
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

Run these checks in Google Search Console and Google Analytics:

1. **Search Console → Coverage**: Check for new 404 or 500 errors
2. **Search Console → Sitemaps**: Verify sitemap submitted and fresh
3. **Search Console → Performance**: Review top queries and CTR for service pages
4. **GA4 → Realtime**: Verify tracking is firing (after GA4 activation)
5. **GA4 → Events**: Check `phone_click`, `cta_click`, `form_submit` events
6. **GA4 → Conversions**: Monitor form submission conversion rate
7. **Manual spot-check**: Open 3 random service pages + 1 city page in browser
8. **Schema validation**: https://search.google.com/test/rich-results test homepage
9. **Mobile test**: Chrome DevTools mobile emulator on 3 pages
10. **PageSpeed Insights**: Run https://pagespeed.web.dev/audit on homepage weekly

## Performance Targets

- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1
- Mobile PageSpeed score: 90+

Achieved via: minified CSS/JS, lazy-loaded images, preload hints, HTTPS redirects, Cloudflare edge caching.

## Important Notes

- **Deployment**: automatic on push to `main` via `.github/workflows/deploy.yml` (validates, then `wrangler deploy` with `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` repo secrets). Workers Builds is **not** connected. Manual deploy also works via `wrangler deploy --config wrangler.jsonc` against the zone-owning account (`a08528fe…`). The `_headers` file must use proper path-prefixed format for Workers + Assets (each block starts with a URL path like `/*` or `/css/*`). See `DEPLOYMENT-AMY-ELECTRIC.md`.
- **IndexNow**: Key at `/16076f14-4d06-4581-b281-38a7a89804ca.txt`. Notify after each deploy by running `bash scripts/notify-indexnow.sh` or via `curl` to `https://api.indexnow.org/indexnow`.
- **New files this session**: `blog/california-electrical-code-changes-2026.html`, `blog/ladwp-ev-charger-rebate-guide-2026.html`
- **Gallery**: `gallery.html` (273KB, 309 photos) — first 36 items HTML, 273 JS-lazy via "Show More". Inline CSS → `css/src/12-gallery.css`. `scripts/update-gallery.py` is idempotent.
- **Schema improvements this session**: FAQPage (4→7 Qs) + BreadcrumbList on all 32 geo pages; BreadcrumbList on 7 root pages + 31 blog posts; HowTo schema on 4 service pages; PriceRange/offers on 11 service pages; homepage FAQ expanded 4→15 Qs
