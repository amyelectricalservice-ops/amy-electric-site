# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor hosted on Cloudflare Pages. No build system, no package manager, no CI, no tests.

- **Business name**: AMY Electric
- **License**: C-10 #981578 (verify at [CSLB](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578)), EVITP #4051604
- **Phone**: (818) 302-5614
- **Email**: info@amyelectric.com
- **Service area**: Greater Los Angeles (12 city pages, 62+ ZIP codes)

## Current state

- **42 HTML pages total**:
  - Homepage: `index.html`
  - **15 service pages**: `ev-charger-installation.html`, `panel-upgrade.html`, `electrical-repair.html`, `commercial-electrical.html`, `lighting-installation.html`, `tesla-charger-installation.html`, `whole-home-rewiring.html`, `surge-protection.html`, `outlet-switch-installation.html`, `ceiling-fan-installation.html`, `smoke-co-detector-installation.html`, `generator-transfer-switch.html`, `dedicated-circuits.html`, `smart-home-electrical.html`, `electrical-safety-inspections.html`
  - **12 location pages**: `city-los-angeles.html`, `city-sherman-oaks.html`, `city-burbank.html`, `city-glendale.html`, `city-pasadena.html`, `city-studio-city.html`, `city-north-hollywood.html`, `city-hollywood.html`, `city-beverly-hills.html`, `city-west-la.html`, `city-encino.html`, `city-santa-monica.html`
  - **2 special pages**: `testimonials.html`, `gallery.html`
  - **12 blog pages** in `blog/`: 10 posts + `blog/index.html`
- **CSS** at `css/style.min.css` (production, 17KB) — original at `css/style.css`
- **JS** at `js/site.min.js` (production, 2.3KB) — original at `js/site.js`
- **`favicon.svg`** — navy background with gold "AE" lightning bolt
- **`robots.txt`** — allows /, disallows /amyelectric-site/ and /~*
- **`_redirects`** — Cloudflare Pages HTTPS + www canonicalization
- **`sitemap.xml`** — all 42 pages with `<lastmod>`, priorities (1.0 home, 0.9 high-value services, 0.8 services, 0.7 cities, 0.6 special/blog)
- **`gbp-posts-document.txt`** — 30 Google Business Profile post ideas
- **`*~`** and **`.antigravitycli/`** are in `.gitignore`

## What to know

- **Hosting**: Cloudflare Pages — enable Auto-Minify (HTML/CSS/JS) and Polish (WebP) in dashboard
- **No dev server** — open HTML files directly in a browser to preview
- **All pages share the same nav bar** and footer — when updating shared layout, update every `.html` file
- **No framework** — vanilla HTML
- **Images**: 5 original JPEGs in `img/`. WebP conversion handled by Cloudflare Polish.
- **Analytics placeholder**: All pages have commented-out GA4/GTM code. Activate by replacing `G-XXXXXXXXXX` and `GTM-XXXXXXX` placeholders.
- **Contact forms**:
  - Homepage: Two-tier — `quick-form` (3 fields: name, phone, service) by default, `estimate-form` (7 fields) in expandable `<details>` toggle
  - Replace `action="https://formspree.io/f/your-form-id"` with real endpoint
- **Sticky call bar**: Mobile-only gold bar fixed to bottom on all 42 pages (hidden ≥768px)

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
