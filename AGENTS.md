# AMY Electric Website — Agent Instructions

## Project

Static HTML marketing site for an LA electrical contractor. No build system, no package manager, no CI, no tests.

- **Business name**: AMY Electric
- **License**: C-10 #1125186, EVITP #4051604
- **Phone**: (818) 302-5614
- **Service area**: Greater Los Angeles

## Current state

- **Pages live in repo root** — 7 pages: `index.html`, `ev-charger-installation.html`, `panel-upgrade.html`, `electrical-repair.html`, `commercial-electrical.html`, `lighting-installation.html`, `city-los-angeles.html`
- **CSS** at `css/styles.css`
- **`main.txt`** is a planning document for a future `amyelectric/` subdirectory layout — do not treat it as current structure
- **`*~`** and **`.antigravitycli/`** are in `.gitignore`

## What to know

- **No dev server** — open HTML files directly in a browser to preview
- **All pages share the same nav bar** (from `index.html`) and footer — when updating shared layout, update every `.html` file
- **No framework** — vanilla HTML
- **No staging** — changes are ready to deploy as static files as-is
- **Images** in `img/` are 1024×1024 JPEGs at quality 85

## File conventions

- Each service page: `<section class="page-hero">`, service grid with `<div class="grid-3">`, FAQ section, and a CTA section
- All internal links use relative paths to `.html` files (e.g. `href="panel-upgrade.html"`)
- Phone number uses `tel:18183025614` throughout
- Every page includes JSON-LD structured data (LocalBusiness + FAQ schemas) and Open Graph / Twitter meta tags
- Form inputs use `id` and `aria-label` attributes for accessibility
- Navigation links and footer links use stable `id` attributes throughout
- Service images are 800×800 in `<img>` tags, with `width`/`height` and `alt` text
