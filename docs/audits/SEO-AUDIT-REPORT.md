# SEO Audit Report — amyelectric.com

**Date:** June 8, 2026 | **Pages:** 106 static HTML | **Host:** Cloudflare Pages

---

## Overall SEO Health Score: **81/100** 

| Category | Score | Weight |
|----------|-------|--------|
| Technical SEO | 80/100 | 22% |
| Content Quality & E-E-A-T | 76/100 | 23% |
| On-Page SEO | 82/100 | 20% |
| Schema / Structured Data | 85/100 | 10% |
| Core Web Vitals / Performance | 85/100 | 10% |
| AI Search Readiness (GEO) | 78/100 | 10% |
| Images | 85/100 | 5% |

---

## 1. Technical SEO — 80/100

| Sub-category | Score |
|---|---|
| Crawlability | 90/100 |
| Indexability | 95/100 |
| Security | 95/100 |
| Mobile | 90/100 |
| Structured Data | 90/100 |
| JS Rendering | 100/100 |
| IndexNow | **0/100** |

### Critical
- **IndexNow not implemented** — Cloudflare Pages supports IndexNow via Cache Rules or API. Submit a key file at `/{key}.txt` and notify Bing/Yandex on publish. This directly improves non-Google indexing speed.

### High
- **www DNS missing** — `www.amyelectric.com` returns NXDOMAIN. Add `www` as a Cloudflare Pages custom domain or CNAME record. Visitors typing `www.` get a connection error.
- **SearchAction schema broken** — `/?q={search_term_string}` has no search handler. Either implement client-side search or remove the SearchAction property.

### Medium
- **BreadcrumbList minimal** — Homepage only has `[{position: 1, name: "Home"}]`. Expand to reflect actual hierarchy.
- **Clean up robots.txt** — Remove `Disallow: /reports/` and `Disallow: /api/` if those paths don't exist.

### Low
- Add `maximum-scale=5` to viewport meta to prevent accidental zoom-lock.
- Remove deprecated `X-XSS-Protection` header (CSP already handles this).

---

## 2. Content Quality & E-E-A-T — 76/100

| Factor | Score |
|--------|-------|
| Experience | 82/100 |
| Expertise | 85/100 |
| Authoritativeness | 68/100 |
| Trustworthiness | 75/100 |

### Critical
- **No privacy policy link in footer** — Significant trust and legal gap. The `/privacy-policy` page exists but isn't linked. Add to all 106 page footers.

### High
- **City pages are thin (~600 words)** — Expand with neighborhood-specific detail (typical wiring era per neighborhood, LADBS district office distinctions, localized permit nuances).
- **Author context weak** — No byline on pages. Add "By AMY Electric Team" with link to founder bio.
- **No HowTo schema** — Service pages have process steps but no HowTo markup. Would improve eligibility for rich results and AI extraction.

### Medium
- No dedicated About page (separate from homepage section) with full name, credentials, education.
- No media/awards mentions. Pursue IEC/ECA membership.
- External credential verification links missing (CSLB license check URL).
- Blog content could expand with more citeable statistics.

### Low
- Internal links from city pages to blog posts referencing those neighborhoods.
- Add BBB/TrustedPros badges if accredited.
- Monitor llms.txt freshness.

---

## 3. Schema / Structured Data — 85/100

### ❌ Errors
1. **BreadcrumbList missing** on `blog/index.html` and `testimonials.html`
2. **panel-upgrade.html** missing `datePublished`, `dateModified`, `hasOfferCatalog` in Service schema
3. **areaServed inconsistent** — `panel-upgrade.html` lists only Los Angeles; `ev-charger-installation.html` lists 7 cities

### ⚠️ Warnings
4. `query-input` property deprecated in SearchAction — remove; use `target.urlTemplate` only
5. Geo coordinates at 3 decimals (~111m precision) — increase to 5 decimals (~1.1m)
6. Founder Person missing `@id`, `jobTitle`, `image`
7. Service schemas missing `@id` for unique identification
8. Blog `BlogPosting.image` uses generic `hero-electrician.jpg` instead of post-specific images
9. Testimonials Electrician schema thin — add geo, openingHours, areaServed

### ✅ Done Well
- All URLs absolute — no relative URLs in any schema
- Gallery: comprehensive ItemList + ImageGallery with 30 photos
- Service pages: every service has unique Service + FAQPage + BreadcrumbList
- City pages: Electrician + FAQPage + BreadcrumbList (all 16)
- Blog posts: BlogPosting with datePublished, dateModified, author, publisher, mainEntityOfPage
- Electrician (homepage): 30+ properties — credentials, reviews, ratings, founder, hours, catalog

---

## 4. Local SEO — 66/100

| Dimension | Score |
|-----------|-------|
| NAP Consistency | 10/15 |
| Local Schema | 20/25 |
| Local On-Page | 13/20 |
| GBP & Reviews | 10/20 |
| Citations | 3/10 |
| Content & Coverage | 10/10 |

### Critical
- **GBP not claimed** — No Google Business Profile means zero Map Pack presence, no review responses, no GBP posts. This alone caps local visibility.

### High
- **Street address not in footer HTML** — Only in schema. Add `20628 Londelius St, Winnetka, CA 91306` to footer text.
- **Geo precision** — Schema has 34.223, -118.582 (3 decimals ≈ 100m). Needs 5+ decimals.
- **Expand sameAs** — Only Yelp. Add Facebook Business Page, BBB profile, Nextdoor.

### Medium
- No Google Maps embed on any page (add to city pages or homepage).
- No citation profile — get listed on BBB, Facebook, Nextdoor, Angi, HomeAdvisor.
- Opening hours inconsistent (homepage vs city pages differ on Saturday).

---

## 5. AI Search / GEO Readiness — 78/100

| Platform | Readiness |
|----------|-----------|
| ChatGPT / OpenAI | 85% |
| Perplexity | 85% |
| Claude / Anthropic | 85% |
| Google AI Overviews | 75% |
| Bing Copilot | 70% |

### High
- **No real author photo** — Replace monogram avatar with professional headshot in "Meet Amy" section and blog bios. High E-E-A-T signal for AI systems.
- **No YouTube channel** — Even 3–5 short videos would unlock multi-modal AI citations.
- **No `rsl.json`** — Add at `/rsl.json` for AI licensing terms.

### Medium
- No Wikipedia/external brand mentions (strongest AI citation signal per Ahrefs).
- No LinkedIn company page (free, quick to set up, AI crawlers index it).
- No brand footprint across YouTube, Reddit, LinkedIn (the 3 strongest AI citation platforms).

### Low
- Optimize paragraph length — audit service page intros to 134–167 word self-contained blocks.
- Expand pricing tables to more service pages.
- Submit to IndexNow for faster Bing/Copilot indexing.

### ✅ Done Well
- Exceptional AI crawler management (9 crawlers explicitly handled — 6 allowed, 3 blocked)
- Model `llms.txt` — key facts, pricing, services, contact, areas
- High factual density (specific costs, timelines, credentials)
- FAQPage schema throughout for AI extraction
- All AI search crawlers allowed; training crawlers blocked

---

## 6. SXO / Search Experience — 78/100

| Page | Score |
|------|-------|
| Homepage | 78/100 |
| EV Charger | 84/100 (strongest) |
| City LA | 73/100 |

### Critical
- **No inline form on service pages** — Every CTA redirects to homepage form, losing context. Add an inline form directly on each service page.

### High
- **Hero image not deployed** — Live homepage is text-only hero. Add the existing `hero-electrician-800w.jpg` with `fetchpriority="high"`. (Fix made locally, needs deployment.)
- **Commercial pages thin** — No commercial case studies, no large-project photos, no commercial client testimonials. Hurts the commercial client persona journey (scored 59/100).

### Medium
- No Google Maps embed on city pages.
- City pages missing links to geo-specific sub-pages (e.g., link to `/ev-charger-installation-los-angeles` from the LA city page).
- Blog posts don't link back to relevant service pages within content body.

### Low
- Add pricing summary on city pages for top 3 services.
- Move detailed form out of `<details>` toggle.

---

## 7. Images — 85/100

### High
- **Gallery 1200w WebP at 285KB** — Could be compressed further. Enable/verify Cloudflare Polish (lossy) for ~30-40% savings.

### Medium
- **Missing hero preload** on some service pages (`lighting-installation`, `commercial-electrical`). Only `ev-charger-installation` and `panel-upgrade` have hero image preload hints.
- **Blog author photos JPEG-only** — Switch to `<picture>` with WebP source (saves ~3KB per author photo).

### Low
- Gallery modal alt text is empty string — set to `alt="Enlarged project photo"`.
- `panel-100a-vs-200a.html` uses direct JPEG `<img>` without WebP `<picture>` wrapper.

### ✅ Done Well
- Alt text excellent — descriptive, unique, includes city/business context, no keyword stuffing
- Lazy loading correct — hero/first gallery image uses `eager` + `fetchpriority="high"`, rest lazy
- All key images have explicit width/height for CLS prevention
- Gallery + service/city pages use `<picture>` with WebP + JPEG sources

---

## Prioritized Action Plan

### Deploy Now (fixes already made locally)

| # | Action | Files | Expected Impact |
|---|--------|-------|-----------------|
| 1 | Deploy to Cloudflare Pages (all fixes below) | — | — |
| 2 | `scrollIntoView` replacing `offsetTop` in estimator.js | `js/estimator.js` | Eliminates 123ms forced reflow |
| 3 | Trimmed inline CSS (~58→48 lines) | `index.html` | Reduces inline CSS parse time ~25% |
| 4 | Hero image with fetchpriority="high" on homepage | `index.html` | Shifts LCP from text badge to visual; improves LCP score |
| 5 | Re-minified CSS/JS | `css/style.min.css`, `js/*.min.js` | Ensures latest changes in production |

### Fix This Week

| # | Priority | Action | Category |
|---|----------|--------|----------|
| 6 | 🔴 Critical | Add privacy policy link to all page footers | E-E-A-T |
| 7 | 🔴 Critical | Implement IndexNow (`/{key}.txt` + API) | Technical |
| 8 | 🔴 Critical | Add inline form on top service pages | SXO |
| 9 | 🔴 High | Fix www DNS in Cloudflare dashboard | Technical |
| 10 | 🔴 High | Fix SearchAction schema (remove or implement search) | Schema |
| 11 | 🔴 High | Add real author photo (replace monogram "A") | GEO/E-E-A-T |
| 12 | 🔴 High | Add street address to footer HTML | Local SEO |

### Fix This Month

| # | Priority | Action | Category |
|---|----------|--------|----------|
| 13 | 🟡 High | Claim/verify Google Business Profile | Local SEO |
| 14 | 🟡 High | Expand city pages to 800+ words with neighborhood detail | Content |
| 15 | 🟡 High | Add HowTo schema to service pages | Schema |
| 16 | 🟡 Medium | Expand BreadcrumbList on all pages | Schema |
| 17 | 🟡 Medium | Improve geo precision to 5 decimals | Local/Schema |
| 18 | 🟡 Medium | Expand sameAs: add Facebook, BBB, Nextdoor | Local/Geo |
| 19 | 🟡 Medium | Create YouTube channel with 3 project walkthrough videos | GEO |
| 20 | 🟡 Medium | Add LinkedIn company page | GEO |
| 21 | 🟡 Medium | Add rsl.json for AI licensing | GEO |

### Backlog

| # | Priority | Action | Category |
|---|----------|--------|----------|
| 22 | 🟢 Low | Enable Cloudflare Polish for image compression | Images |
| 23 | 🟢 Low | Add Google Maps embed to city pages | Local |
| 24 | 🟢 Low | Fix gallery modal alt text | Images |
| 25 | 🟢 Low | Remove deprecated X-XSS-Protection header | Technical |
| 26 | 🟢 Low | Add post-specific images to blog BlogPosting schema | Schema |
| 27 | 🟢 Low | Add `maximum-scale=5` to viewport meta | Technical |

---

## Quick Wins (can fix in < 30 min)

1. Add street address to footer HTML in all 106 files
2. Add privacy policy link to all 106 footers
3. Fix geo precision in homepage and city page schemas
4. Remove deprecated `query-input` from SearchAction schema
5. Add BreadcrumbList to blog index and testimonials
6. Fix panel-upgrade `areaServed` to match EV charger (7 cities)
7. Add `@id` to Service schemas on all 15 service pages
8. Add blog post links to relevant service pages (3-5 blog posts)
9. Deploy the hero image, scrollIntoView fix, and trimmed CSS

---

## Limitations

- PageSpeed API quota exhausted — no live LCP/INP/CLS field data
- DataForSEO not available — no keyword position, backlink or SERP data
- Chrome DevTools MCP not configured — no full performance traces
- GBP visibility (Map Pack position, review velocity) not measurable
- No Search Console access — actual indexed page count, click-through data, query performance unavailable
- No Ahrefs or similar — backlink profile, referring domains, anchor text not analyzed

---

## Previous Audit Comparison

| Metric | Previous (GEO report) | This audit | Change |
|--------|----------------------|------------|--------|
| Technical SEO | 89/100 | 80/100 | -9 (IndexNow gap identified) |
| Content Quality | 75/100 | 76/100 | +1 |
| Local SEO | 82/100 | 66/100 | -16 (deeper GBP/citation analysis) |
| Image SEO | 90/100 | 85/100 | -5 |
| GEO/AEO | 72/100 | 78/100 | +6 (auth photo still missing) |
| Schema | (not scored) | 85/100 | — |
| SXO | 84/100 | 78/100 | -6 |
| **Combined** | **~80/100** | **81/100** | **+1** |

Note: Previous audit used different methodology and didn't score IndexNow, citation presence, or GBP claims — the lower scores reflect deeper analysis, not regression.
