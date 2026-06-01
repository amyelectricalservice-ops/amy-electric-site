# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor. No build system, no package manager, no CI, no tests.

- **Business name**: AMY Electric
- **License**: C-10 #981578 (verify at [CSLB](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578)), EVITP #4051604
- **Phone**: (818) 302-5614
- **Email**: info@amyelectric.com
- **Service area**: Greater Los Angeles

## Current state

- **30+ pages live in repo root**:
  - Homepage: `index.html`
  - **15 service pages**: `ev-charger-installation.html`, `panel-upgrade.html`, `electrical-repair.html`, `commercial-electrical.html`, `lighting-installation.html`, `tesla-charger-installation.html`, `whole-home-rewiring.html`, `surge-protection.html`, `outlet-switch-installation.html`, `ceiling-fan-installation.html`, `smoke-co-detector-installation.html`, `generator-transfer-switch.html`, `dedicated-circuits.html`, `smart-home-electrical.html`, `electrical-safety-inspections.html`
  - **11 location pages**: `city-los-angeles.html`, `city-sherman-oaks.html`, `city-burbank.html`, `city-glendale.html`, `city-pasadena.html`, `city-studio-city.html`, `city-north-hollywood.html`, `city-hollywood.html`, `city-beverly-hills.html`, `city-west-la.html`, `city-encino.html`
  - **2 special pages**: `testimonials.html`, `gallery.html`
  - **10 blog posts** in `blog/`: `ev-charging-benefits.html`, `panel-upgrade-signs.html`, `ev-charging-los-angeles.html`, `la-electrical-safety-tips.html`, `ceiling-fan-installation-la.html`, `commercial-electrical-la.html`, `choosing-electrician-la.html`, `whole-home-rewiring-guide.html`, `gfci-afci-protection-la.html`, `smart-home-electrical-upgrades.html`, `la-electrical-code-requirements.html`, plus `blog/index.html` index
- **CSS** at `css/style.css` (navy `#0b1628` + gold `#f5a623` theme)
- **JS** at `js/site.js` (mobile nav, form handling, mailto fallback)
- **`favicon.svg`** — navy background with gold "AE" lightning bolt
- **`robots.txt`** — allows /, disallows /amyelectric-site/ and /~*, references sitemap
- **`sitemap.xml`** — all 30+ pages with priorities (1.0 home, 0.9 high-value services, 0.8 services, 0.7 cities, 0.6 special/blog)
- **`gbp-posts-document.txt`** — 30 Google Business Profile post ideas
- **`*~`** and **`.antigravitycli/`** are in `.gitignore`

## What to know

- **No dev server** — open HTML files directly in a browser to preview
- **All pages share the same nav bar** and footer — when updating shared layout, update every `.html` file (use grep)
- **No framework** — vanilla HTML
- **No staging** — changes are ready to deploy as static files as-is
- **Images** in `img/` are 5 original JPEGs (~244KB each): `commercial.jpg`, `ev-charger.jpg`, `hero-electrician.jpg`, `lighting.jpg`, `panel-upgrade.jpg`
- **Custom contact form** in `index.html` with mailto: fallback (subject: "Service Request - {name}" or "Free Estimate Request - {name}"). Replace `action="https://formspree.io/f/your-form-id"` with real endpoint for production.
- **Form fields**: request_type (radio), name, phone, email, city, service (dropdown), message

## File conventions

- Each service page: `<section class="page-hero">`, service grid with `<div class="grid-3">`, FAQ section using `<details>`, CTA section, related services, and trust bar
- All internal links use relative paths to `.html` files (e.g. `href="panel-upgrade.html"`)
- Phone number uses `tel:18183025614` throughout
- Every page includes JSON-LD structured data (LocalBusiness + FAQ + BreadcrumbList + Service or Electrician schemas) and Open Graph / Twitter meta tags
- Form inputs use `id` and `aria-label` attributes for accessibility
- Navigation links and footer links are duplicated across all pages (manual update required)
- Service images are 800×800 in `<img>` tags, with `width`/`height` and `alt` text
- Favicon link is included on all pages
- Hero image on `index.html` has `loading="lazy"`; other images should use lazy loading
- Preload hints (hero image, style, font) are on `index.html`, `ev-charger-installation.html`, `panel-upgrade.html`
