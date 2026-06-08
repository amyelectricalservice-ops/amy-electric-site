# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor hosted on Cloudflare Workers + Assets (auto-deployed via Workers Builds from GitHub main branch). No build system, no package manager, no CI, no tests.

- **Business name**: AMY Electric
- **License**: C-10 #981578 (verify at [CSLB](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578)), EVITP #4051604
- **Phone**: (818) 302-5614
- **Email**: info@amyelectric.com
- **Service area**: Greater Los Angeles (16 city pages, 62+ ZIP codes)

## Current state

- **42 HTML pages total**:
  - Homepage: `index.html`
  - **15 service pages** (`ev-charger-installation.html`, `panel-upgrade.html`, `electrical-repair.html`, `commercial-electrical.html`, `lighting-installation.html`, `tesla-charger-installation.html`, `whole-home-rewiring.html`, `surge-protection.html`, `outlet-switch-installation.html`, `ceiling-fan-installation.html`, `smoke-co-detector-installation.html`, `generator-transfer-switch.html`, `dedicated-circuits.html`, `smart-home-electrical.html`, `electrical-safety-inspections.html`)
  - **16 city pages**: `city-los-angeles.html`, `city-sherman-oaks.html`, `city-burbank.html`, `city-glendale.html`, `city-pasadena.html`, `city-studio-city.html`, `city-north-hollywood.html`, `city-hollywood.html`, `city-beverly-hills.html`, `city-west-la.html`, `city-encino.html`, `city-santa-monica.html`, `city-woodland-hills.html`, `city-van-nuys.html`, `city-calabasas.html`, `city-culver-city.html`
  - **2 special pages**: `testimonials.html`, `gallery.html`
  - **31 blog pages** in `blog/`: 30 posts + `blog/index.html`
  - **2 comparison pages**: `panel-100a-vs-200a.html`, `ev-charger-hardwired-vs-plug-in.html`
  - **16 geo service pages**: `panel-upgrade-{city}.html`, `ev-charger-installation-{city}.html`
  - **1 privacy policy**: `privacy-policy.html`
  - **31 blog pages** in `blog/`: 30 posts + `blog/index.html`
  - **2 comparison pages**: `panel-100a-vs-200a.html`, `ev-charger-hardwired-vs-plug-in.html`
  - **4 geo service pages**: `panel-upgrade-{city}.html` (16), `ev-charger-installation-{city}.html` (16)
  - **1 privacy policy**: `privacy-policy.html`
- **CSS** at `css/style.min.css` (production, 17KB) — original at `css/style.css`
- **JS** at `js/site.min.js` (production, 2.3KB) — original at `js/site.js`
- **`favicon.svg`** — navy background with gold "AE" lightning bolt
- **`robots.txt`** — allows /, explicitly allows 8 AI search crawlers, blocks 3 training crawlers, RSL link, Sitemap
- **`_redirects`** — Cloudflare Pages HTTPS + www canonicalization
- **`sitemap.xml`** — all 42 pages with `<lastmod>`, priorities (1.0 home, 0.9 high-value services, 0.8 services, 0.7 cities, 0.6 special/blog)
- **`gbp-posts-document.txt`** — 30 Google Business Profile post ideas
- **`*~`** and **`.antigravitycli/`** are in `.gitignore`

## What to know

- **Hosting**: Cloudflare Pages — enable Auto-Minify (HTML/CSS/JS) and Polish (WebP) in dashboard
- **No dev server** — open HTML files directly in a browser to preview
- **All pages share the same nav bar** and footer — when updating shared layout, update every `.html` file
- **No framework** — vanilla HTML
- **Images**: 5 original JPEGs in `img/`. 30 real project photos in `img/gallery/` (1200w WebP + 1200w JPEG + 400w WebP per photo). WebP conversion handled by Cloudflare Polish.
- **Analytics**: Cloudflare Web Analytics — one-click enable in dashboard (Workers & Pages → project → Metrics → Enable). Free, privacy-first, auto-injects beacon. No client-side analytics code in `site.js`. The GA deferred loader was removed.
- **Contact forms**:
  - Homepage: Two-tier — `quick-form` (3 fields: name, phone, service) by default, `estimate-form` (7 fields) in expandable `<details>` toggle
  - POST to `/api/contact` (Cloudflare Pages Function) — no form service dependency
- **Sticky call bar**: Mobile-only gold bar fixed to bottom on all 42 pages (hidden ≥768px)
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

- **Deployment**: Workers + Assets via Workers Builds (GitHub → auto-deploy). `npx wrangler deploy` triggered by pushing to `main`. Workers Builds runs in Cloudflare infra — no local API token needed. The `_headers` file must use proper path-prefixed format for Workers + Assets (each block starts with a URL path like `/*` or `/css/*`).
- **IndexNow**: Key at `/16076f14-4d06-4581-b281-38a7a89804ca.txt`. Notify after each deploy by running `bash scripts/notify-indexnow.sh` or via `curl` to `https://api.indexnow.org/indexnow`.
- **New files added this session**: `privacy-policy.html`, `rsl.json`, `js/estimator.js`, `js/estimator.min.js`, `img/author-amy-200w.jpg`, `img/author-amy-200w.webp`, `img/author-amy-400w.jpg`, `img/author-amy-400w.webp`, `GEO-ANALYSIS.md`, `SEO-AUDIT-REPORT.md`, `scripts/notify-indexnow.sh`, `16076f14-4d06-4581-b281-38a7a89804ca.txt`.
