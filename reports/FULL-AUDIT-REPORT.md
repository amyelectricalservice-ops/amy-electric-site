# Full Website SEO Audit — AMY Electric

**Date**: 2026-06-18
**URL**: https://amyelectric.com/
**Business Type**: Service Area Business (SAB) — Electrical Contractor
**Pages crawled**: 108 active HTML pages
**Tools used**: Local crawl, Lighthouse CLI, schema validation, content analysis, image audit, security header check

---

## Executive Summary

| Metric | Value |
|---|---|
| **SEO Health Score** | **89/100** |
| Business type | Licensed electrical contractor (C-10), Service Area Business |
| Total pages | 108 active (126 files total incl. backups + reports) |
| Total site weight | 6.5 MB (HTML) + ~13 MB (images) |
| Desktop Lighthouse | **98** Performance, **0.000** CLS |
| Mobile Lighthouse | ~77 Performance, **0.000** CLS |
| HTTPS | ✅ Enforced (301 redirect) |
| www canonicalization | ❌ **522 error** — CNAME not configured |
| Schema coverage | 105/108 pages have structured data |
| AI Search Readiness | ✅ llms.txt, SpeakableSpec, 8 AI crawlers allowed |

### Top 5 Critical Issues

1. **www.amyelectric.com returns 522** — DNS CNAME record missing; all authority leaks to non-resolving subdomain
2. **3 blog posts missing BlogPosting + BreadcrumbList schema** — `how-to-choose-electrician-los-angeles`, `signs-you-need-electrical-panel-upgrade`, `smart-home-electrical-upgrades-la` — these are redirect stubs but still need proper schema
3. **Gallery WebP quality too high** — gallery images average only 1-20% compression savings vs JPEG; re-encoding at q80 could save 3-4 MB
4. **Opening hours inconsistency** — homepage shows 24/7 emergency dispatch; city pages show Saturday hours but not 24/7 emergency
5. **Homepage FAQ contains typo** — question 15: `your home?s` should be `your home?`

### Top 5 Quick Wins

1. Fix FAQ typo on index.html (30 seconds)
2. Expand city page FAQ from 3→5+ questions (adds depth for FAQPage rich results)
3. Add Facebook/Nextdoor/BBB to sameAs across all Electrician schemas
4. Add FAQPage schema to testimonials.html
5. Fix smoke-co-detector duplicate title

---

## Technical SEO (Weight: 22%) — Score: 90/100

### Crawlability

| Check | Status | Notes |
|---|---|---|
| robots.txt | ✅ | Well-configured, 8 AI crawlers allowed, 3 training crawlers blocked, RSL referenced, sitemap linked |
| Sitemap.xml | ✅ | 108 URLs, priorities assigned (1.0→0.5), lastmod dates, image:image tags on gallery |
| Canonical tags | ✅ | All pages have self-referencing canonical |
| 404 handling | ✅ | Cloudflare default 404 page |
| Redirects | ✅ | .html stripping via `_redirects`, 3 meta-refresh for consolidated blog pages |
| Internal link structure | ✅ | No broken internal links, proper nav hierarchy |

### Indexability

| Check | Status | Notes |
|---|---|---|
| noindex tags | ✅ | Only on 3 redirect stubs (intentional) |
| robots meta | ✅ | `index, follow` on all live pages |
| Pagination | N/A | No pagination used |
| Duplicate content | ⚠️ Minor | `smoke-co-detector-installation.html` and `blog/smoke-co-detector-installation-la.html` share same title |

### Security

| Check | Status | Notes |
|---|---|---|
| HTTPS | ✅ | 301 redirect from HTTP |
| HSTS | ✅ | `max-age=31536000; includeSubDomains; preload` |
| CSP | ✅ | Comprehensive, includes Turnstile + GTM + Cloudflare Insights |
| X-Frame-Options | ✅ | `DENY` |
| X-Content-Type-Options | ✅ | `nosniff` |
| Permissions-Policy | ✅ | Restrictive (no camera/mic/geo) |
| Referrer-Policy | ✅ | `strict-origin-when-cross-origin` |
| Google Safe Browsing | ✅ | **Not blacklisted** |
| **www subdomain** | ❌ | **522 error** — DNS CNAME missing |

### Core Web Vitals (Lab)

| Metric | Desktop | Mobile | Target |
|---|---|---|---|
| **Performance** | **98** | **~77** | 90+ |
| **LCP** | 1.13s ✅ | 1.4-1.8s ⚠️ | <2.5s |
| **CLS** | **0.000** ✅ | **0.000** ✅ | <0.1 |
| **TBT** | 0.05s ✅ | 0.6-1.0s ⚠️ | <200ms |
| **FCP** | 0.45s ✅ | 1.3-1.4s ✅ | <1.8s |
| **Speed Index** | 0.94s ✅ | 2.3-2.8s ⚠️ | <3.0s |

**Mobile bottleneck**: GA4 gtag.js (66KB, ~500ms evaluation). Removing GA4 or switching to server-side Measurement Protocol would boost mobile score to ~90+.

---

## Content Quality (Weight: 23%) — Score: 85/100

### E-E-A-T Assessment

| Signal | Status | Details |
|---|---|---|
| **Experience** | ✅ Strong | "Since 2012", 2000+ projects, real project photos in gallery |
| **Expertise** | ✅ Strong | C-10 license #981578 (verifiable at CSLB), EVITP #4051604 |
| **Authoritativeness** | ✅ Good | Verifiable license number, citations to DOE/NFPA/NEC/OSHA |
| **Trustworthiness** | ✅ Strong | Upfront pricing, transparent NAP, real reviews with named customers |

### Page-Level Quality

| Page Type | Word Count | Quality | Notes |
|---|---|---|---|
| Homepage | 500+ | Excellent | Comprehensive hero text, 15 FAQs, service grid, testimonials |
| Service pages (15) | 800-1500 | Good | HowTo on 4 pages, FAQ sections, price ranges |
| City pages (16) | 600-1000 | Good | Local knowledge sections, Electrician schema |
| Geo-service pages (32) | 400-800 | Adequate | FAQ sections present, but city-specific unique content is thin |
| Blog posts (31) | 1200-2500 | Good | Author bylines, dates, citations, FAQ sections |
| Emergency pages (5) | 600-1000 | Good | Unique FAQ answers, Electrician schema |

### Issues

| Issue | Severity | Pages |
|---|---|---|
| Duplicate page title | Low | 2 (smoke-co-detector) |
| Thin geo-service content | Medium | 32 pages (template-like, minimal differentiation) |
| Missing author bylines | Low | 2 service pages (ev-charger-installation, panel-upgrade) |
| No external citations | Low | 1 service page |

---

## On-Page SEO (Weight: 20%) — Score: 95/100

| Element | Status | Notes |
|---|---|---|
| Title tags | ✅ 108/108 | Unique, keyword-rich, 50-60 chars |
| Meta descriptions | ✅ 108/108 | Compelling, 150-160 chars, includes CTAs |
| H1 headings | ✅ 108/108 | One per page, descriptive, includes target keyword |
| Heading hierarchy | ✅ | Proper h1→h2→h3 nesting |
| Open Graph tags | ✅ | og:title, og:description, og:image, og:url all present and fixed |
| Twitter Cards | ✅ | summary_large_image on all pages |
| Image alt text | ✅ | 100% coverage, descriptive |
| Internal links | ✅ | Service grid, blog index, footer, breadcrumbs |
| External links (nofollow) | ✅ | 23 external links, appropriate rel attributes |
| Breadcrumb visible markup | ✅ | Present on all non-homepage pages |

---

## Schema & Structured Data (Weight: 10%) — Score: 88/100

### Coverage

| Schema Type | Coverage | Pages |
|---|---|---|
| Electrician | ✅ 97% | 105/108 |
| FAQPage | ✅ 87% | 94/108 |
| BreadcrumbList | ✅ 97% | 105/108 |
| BlogPosting | ✅ 91% | 30/33 |
| HowTo | ✅ 4 pages | panel-upgrade, ev-charger, generator-transfer-switch, whole-home-rewiring |
| SpeakableSpecification | ✅ 100% | 108/108 |
| Service with offers | ✅ 51 pages | 32 geo + 17 root service |
| WebSite + SearchAction | ✅ 1 page | Homepage |
| Organization + Person | ✅ 1 page | Homepage |

### Issues

| Issue | Severity | Details |
|---|---|---|
| **3 blog posts missing BlogPosting + BreadcrumbList** | **High** | `how-to-choose-electrician-los-angeles`, `signs-you-need-electrical-panel-upgrade`, `smart-home-electrical-upgrades-la` — redirect stubs, but schema should match |
| **datePublished/dateModified on Service type** | Low | 15 service pages — not a standard property for Service (Google may ignore) |
| **Electrician schema on 38 pages without @id** | Medium | 32 geo + 5 emergency + privacy — missing entity linkage |
| **FAQ typo in JSON-LD** | Low | Homepage Q15: `home?s` |
| **Breadcrumb text formatting issues** | Low | 3 blog posts — missing spaces in concatenated text |
| **Testimonials page missing FAQPage** | Low | 1 page |
| **Missing Facebook/Nextdoor/BBB in sameAs** | Low | All pages |

---

## Performance & CWV (Weight: 10%) — Score: 82/100

### Strengths
- CLS: **0.000** (perfect) on both desktop and mobile
- Desktop Performance: **98** (excellent)
- Self-hosted fonts (eliminates 5 cross-origin fetches)
- GA4 deferred to end of `<body>` with `defer`
- Lazy loading on 84/86 images
- Responsive hero image via `<picture>` element
- No render-blocking CSS (async load via `onload`)
- No background images (gradients only)
- `font-display: optional`

### Weaknesses
- Mobile Performance: ~77 (bottlenecked by GA4 gtag.js)
- Gallery WebP quality too high: some files only 1% smaller than JPEG
- Only 1 responsive breakpoint for hero images (no 1200w/1600w for retina)
- No AVIF format fallback
- Gallery images use manual selection per page, not programmatic srcset

---

## AI Search Readiness / GEO (Weight: 10%) — Score: 95/100

### Strengths
| Element | Status | Notes |
|---|---|---|
| **llms.txt** | ✅ | Comprehensive: business info, 11 services with costs, 16 cities, 8 LLM prompt suggestions |
| **AI crawler management** | ✅ | 8 AI search crawlers explicitly allowed, 3 training crawlers blocked, RSL referenced |
| **SpeakableSpecification** | ✅ | Every page has cssSelector for voice search |
| **FAQPage depth** | ✅ | 15 questions on homepage (excellent), 7 on geo pages |
| **Quick Answer sections** | ✅ | 102 pages with `.quick-answer` sections |
| **Brand mention signals** | ✅ | sameAs links to Yelp + Google Maps, review schema, aggregate rating |
| **Schema.org markup** | ✅ | Multiple types for entity extraction |

### Weaknesses
- No brand mentions on Facebook/Nextdoor/BBB in sameAs
- Testimonials page lacks FAQPage

---

## Images (Weight: 5%) — Score: 85/100

### Inventory

| Location | JPG | WebP | SVG | Total | Size |
|---|---|---|---|---|---|
| `img/` | 18 | 19 | 0 | 37 | ~3.1 MB |
| `img/gallery/` | 30 | 60 | 0 | 90 | ~9.9 MB |
| Root | 0 | 0 | 1 | 1 | 2 KB |
| **Total** | **48** | **79** | **1** | **128** | **~13 MB** |

### Strengths
- **100% alt text** coverage
- **100% WebP** coverage (both native and JPEG)
- **Lazy loading** on all gallery and service images
- **Explicit dimensions** on all images (width/height attributes)
- **CLS prevention**: inline `aspect-ratio: 4/3` with navy placeholder background
- **No PNGs** anywhere (excellent modern format adoption)
- **SVG favicon** (lightweight, scalable)

### Weaknesses
- **Gallery WebP quality too high** — some images only 1-20% smaller than JPEG. Batch re-encode at quality 80-85 could save 3-4 MB
- **Single hero breakpoint** (480px + 800w default) — no 1200w or 1600w for retina displays
- **No AVIF support** — could save additional 30% over WebP
- **Gallery page loads 30 images** — 1200w JPEG batch ~4.8 MB

---

## Local SEO

| Element | Score | Notes |
|---|---|---|
| NAP Consistency | 🟢 95% | Minor Winnetka vs LA chip in footer |
| Local Schema (Electrician) | 🟢 95% | Full PostalAddress + GeoCoordinates + openingHours |
| GBP sameAs | 🟡 70% | Yelp + Google Maps only; missing Facebook, Nextdoor, BBB |
| Review Schema | 🟢 100% | 4.9/5 from 87 reviews, 3 individual Review items |
| Area Served | 🟢 100% | 16 cities with ZIP codes in DefinedRegion |
| Opening Hours | 🟡 80% | Homepage has 24/7 emergency; city pages drop this |

---

## SEO Health Score Calculation

| Category | Weight | Score | Weighted |
|---|---|---|---|
| Technical SEO | 22% | 90 | 19.8 |
| Content Quality | 23% | 85 | 19.6 |
| On-Page SEO | 20% | 95 | 19.0 |
| Schema / Structured Data | 10% | 88 | 8.8 |
| Performance (CWV) | 10% | 82 | 8.2 |
| AI Search Readiness | 10% | 95 | 9.5 |
| Images | 5% | 85 | 4.3 |
| **Total** | **100%** | | **89.2 / 100** |

---

## Disclaimers

- **CrUX field data**: Not available (PSI API quota exceeded). Desktop/mobile scores are lab-based via Lighthouse CLI.
- **Backlink profile**: Not audited — no Ahrefs, SEMrush, or Moz API credentials available. Common Crawl domain-level metrics not fetched.
- **Search Console data**: Not available — no API credentials configured. Manual GSC check recommended.
- **Live SERP positions**: Not checked — no DataForSEO MCP tools available.
- **Screenshots**: Not captured — Playwright not available in CLI environment.
