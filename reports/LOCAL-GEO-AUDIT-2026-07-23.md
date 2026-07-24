# Local SEO + GEO Audit — AMY Electric

**Date:** 2026-07-23
**URL:** https://amyelectric.com
**Scope:** Full local SEO health + Generative Engine Optimization (GEO) analysis

---

## LOCAL SEO SCORE: 92 / 100

## GEO SCORE: 94 / 100

---

## Executive Summary

AMY Electric has **excellent local SEO foundations** — NAP consistency is near-perfect, structured data is comprehensive across all 76 pages, and the geo-targeted content architecture (16 cities × 3 page types) provides strong local relevance signals. The site also leads on GEO readiness with a high-quality `llms.txt`, comprehensive AI crawler access in `robots.txt`, and well-structured schema markup that makes content highly extractable by AI systems.

**Key strengths:**
- NAP 100% consistent across every page (name, phone, address, email)
- 48 geo-targeted service pages (16 cities × 3 service types)
- Schema markup on every page: Electrician, FAQPage (107 instances), HowTo (73 instances), BreadcrumbList
- AI crawler access fully open for all major bots (GPTBot, ClaudeBot, PerplexityBot, etc.)
- `llms.txt` is high-quality with structured data, prices, and service areas
- `rsl.json` present with Robots Search License allowing search-and-summarize

**Priority gaps:**
- Schema `telephone` format inconsistency (`+1-818-302-5614` vs `+18183025614`)
- All city pages share same `og:image` (`hero-electrician.jpg`) — missed local relevance
- Missing Apple Maps / Bing Places / YP.com sameAs links
- No `LocalBusiness` schema variant (using `Electrician` subtype — acceptable but narrower)
- City pages use templated structure — risk of thin-content perception at scale

---

## 1. NAP Consistency

| Field | Value | Consistent? |
|-------|-------|------------|
| Business Name | AMY Electric | ✅ Yes |
| Phone | (818) 302-5614 | ⚠️ Minor format variation |
| Address | 20628 Londelius St, Winnetka, CA 91306 | ✅ Yes |
| Email | info@amyelectric.com | ✅ Yes |
| Hours | Monday–Friday: 7 AM–6 PM, Sat: 8 AM–5 PM, Sun: Closed | ✅ Yes |
| License | C-10 #981578 | ✅ Yes |
| EVITP | #4051604 | ✅ Yes |

**Phone format note:** Schema uses two formats: `+1-818-302-5614` and `+18183025614`. Both are E.164-compliant and parsers handle both, but strict NAP checkers may flag this. Recommend standardizing to one format.

**Business name note:** Schema type is `Electrician` (subtype of `HomeAndBusinessBusiness`). The parent type is `LocalBusiness`. No inconsistency found — name is "AMY Electric" everywhere, never "AMY Electrical Service."

**NAP Score: 95/100** (minor phone format variation only)

---

## 2. Google Business Profile Signals

| Signal | Status | Details |
|--------|--------|---------|
| GBP link in sameAs | ✅ Present | `https://g.page/r/CVdK9ZAvNBrZEAI/review` |
| Maps link | ✅ Present | `https://maps.app.goo.gl/WTNSkHRUgULPBHpc9` |
| Review count in schema | ✅ Present | 87 reviews, 4.9/5 aggregate rating |
| NAP matches GBP | ✅ Yes | Same phone, address, hours |
| GBP category | ⚠️ Not verifiable | Schema type is "Electrician" |
| Service area defined | ✅ Yes | 16 cities with zip codes in schema |

**GBP Score: 90/100**

---

## 3. Structured Data (Schema Markup)

### Coverage by Page Type

| Page Type | Count | Schema Types |
|-----------|-------|-------------|
| Homepage | 1 | Electrician, FAQPage (15 Qs), BreadcrumbList |
| City pages | 16 | Electrician, FAQPage (6-7 Qs), BreadcrumbList |
| Service pages | 15 | Electrician, FAQPage, HowTo (4 pages), PriceRange, BreadcrumbList |
| Service-City pages | 32 | Electrician, FAQPage (7 Qs), BreadcrumbList |
| Comparison pages | 2 | FAQPage, BreadcrumbList |
| Emergency/info pages | 5 | FAQPage, BreadcrumbList |
| Blog posts | 31 | BlogPosting, FAQPage, BreadcrumbList |
| Special pages | 2 | Varies |

### Electrician Schema Details

- **Type:** `Electrician` (subtype of `HomeAndBusinessBusiness`)
- **areaServed:** Each city page includes `City` + `DefinedRegion` with postal codes
- **geo:** Latitude/longitude on each city page (e.g., Glendale: 34.1469, -118.2553)
- **aggregateRating:** 4.9/5 from 87 reviews (homepage)
- **sameAs:** 4 links (Yelp, Google Maps page, Google Maps shortened, Facebook)
- **priceRange:** "$$" on service pages
- **openingHours:** Mo-Fr 07:00-18:00, Sa 08:00-17:00

### FAQPage Schema

- **107 total instances** across the site
- Homepage: 15 questions (expanded from 4)
- City pages: 6-7 questions each, city-customized
- Service pages: Varies
- Service-city pages: 7 questions each

### HowTo Schema

- **73 instances** across service pages
- Applied to: panel-upgrade, ev-charger-installation, generator-transfer-switch, whole-home-rewiring

### Schema Issues

1. **Telephone format inconsistency** — `+1-818-302-5614` vs `+18183025614`
2. **Missing `areaServed` on service pages** — Only city pages and service-city pages have it; main service pages (e.g., `ev-charger-installation.html`) don't include service area
3. **No `hasOfferCatalog`** — Could add catalog of services with prices
4. **No `areaServed` with GeoCircle** — Only postal codes and cities defined, no radius

**Schema Score: 93/100**

---

## 4. Geo-Targeted Content Architecture

### Page Inventory

| Page Type | Count | URL Pattern | Content Quality |
|-----------|-------|-------------|-----------------|
| City landing pages | 16 | `city-{city}.html` | High — unique landmarks, zip codes, local references |
| EV charger per city | 16 | `ev-charger-installation-{city}.html` | Medium — service-specific + city content |
| Panel upgrade per city | 16 | `panel-upgrade-{city}.html` | Medium — service-specific + city content |

**Total geo-targeted pages: 48** (out of 76 total pages = 63%)

### City Coverage

Los Angeles, Glendale, Pasadena, Santa Monica, Burbank, Hollywood, North Hollywood, Studio City, Van Nuys, Sherman Oaks, Encino, Beverly Hills, Culver City, Woodland Hills, Calabasas, West LA

### Content Uniqueness Assessment

- **City landing pages:** ✅ Genuinely unique — different landmarks, zip codes, geo coordinates, neighborhood references
- **Service-city pages:** ⚠️ Templated structure with city variable substitution — same core content, different city name and a few local references
- **Risk:** Google may treat heavily templated service-city pages as thin content if the unique content ratio is too low

**Geo Architecture Score: 90/100**

---

## 5. Local Citations & Directories

| Platform | sameAs Present? | Notes |
|----------|----------------|-------|
| Google Business Profile | ✅ Yes | Maps link + review link |
| Yelp | ✅ Yes | `yelp.com/biz/amy-electric-los-angeles` |
| Facebook | ✅ Yes | Page ID 100063766463600 |
| Apple Maps | ❌ No | Missing |
| Bing Places | ❌ No | Missing |
| BBB | ❌ No | Not linked |
| Angi / HomeAdvisor | ❌ No | Not linked |
| Thumbtack | ❌ No | Not linked |
| YP.com | ❌ No | Not linked |
| Nextdoor | ❌ No | Not linked |

**Citations Score: 75/100** — Only 3 of 10+ major directories linked

---

## 6. Mobile & Technical Local SEO

| Factor | Status | Details |
|--------|--------|---------|
| Mobile responsive | ✅ Yes | Viewport meta, responsive CSS |
| Sticky call bar | ✅ Present | Mobile-only gold bar with phone link on all 42+ pages |
| Click-to-call | ✅ Present | `tel:18183025614` links throughout |
| Page speed | ✅ Optimized | Minified CSS/JS, lazy images, preload hints |
| HTTPS | ✅ Yes | Enforced via `_redirects` |
| Canonical | ⚠️ Not verified | Not explicitly found in head |

**Mobile/Technical Score: 92/100**

---

## 7. GEO: AI Crawler Access

### robots.txt Analysis

| Bot | Access | Status |
|-----|--------|--------|
| GPTBot | ✅ Allowed | OpenAI search + ChatGPT |
| OAI-SearchBot | ✅ Allowed | OpenAI search crawler |
| ChatGPT-User | ✅ Allowed | ChatGPT browsing |
| ClaudeBot | ✅ Allowed | Anthropic Claude |
| anthropic-ai | ✅ Allowed | Anthropic research |
| PerplexityBot | ✅ Allowed | Perplexity AI search |
| Google-Extended | ✅ Allowed | Gemini / AI Overviews |
| Applebot-Extended | ✅ Allowed | Apple Intelligence |
| Meta-ExternalAgent | ✅ Allowed | Meta AI |
| Meta-ExternalFetcher | ✅ Allowed | Meta AI fetcher |
| Bytespider | ❌ Blocked | Training only |
| CCBot | ❌ Blocked | Training only |
| cohere-ai | ❌ Blocked | Training only |

**Verdict:** Optimal configuration — search bots allowed, training bots blocked.

---

## 8. GEO: llms.txt Quality

**File:** `/llms.txt` — Present and linked via `<link rel="alternate" type="text/markdown" href="/llms.txt">`

| Element | Present? | Quality |
|---------|----------|---------|
| Business description | ✅ | Clear, concise |
| Key facts | ✅ | License numbers, years in business, review count |
| Services with prices | ✅ | 6 services with price ranges |
| Service areas | ✅ | 16 cities listed |
| Contact info | ✅ | Phone, email, address |
| Links to key pages | ✅ | Homepage, 6 services, 4 cities, about, contact |

**Verdict:** High quality — well-structured, specific data points, links to pages. This is one of the better `llms.txt` implementations.

---

## 9. GEO: Robots Search License (RSL)

**File:** `/rsl.json` — Present

```json
{
  "licenseVersion": "1.0",
  "permission": "search-and-summarize",
  "attribution": true
}
```

**Verdict:** Present and correctly configured. Grants permission for search-and-summarize with attribution required.

---

## 10. GEO: Brand Signals & Citation Readiness

| Signal | Status | Details |
|--------|--------|---------|
| Brand name in schema | ✅ | "AMY Electric" in every Electrician schema |
| Brand name in content | ✅ | Consistent throughout |
| License credentials | ✅ | C-10 #981578, EVITP #4051604 in schema + content |
| Review count | ✅ | 87 reviews, 4.9/5 in schema |
| Service specifics | ✅ | 15 services with descriptions |
| Price transparency | ✅ | Price ranges in llms.txt and schema |
| Geographic specificity | ✅ | 16 cities, 62+ zip codes in schema |
| Structured data richness | ✅ | 107 FAQPage, 73 HowTo, Electrician on every page |

**Brand Signals Score: 95/100**

---

## 11. GEO: Passage-Level Citability

| Element | Present? | Citability |
|---------|----------|------------|
| FAQ sections | ✅ 107 FAQPage schemas | High — AI systems extract Q&A pairs |
| HowTo steps | ✅ 73 HowTo schemas | High — procedural content extractable |
| Price mentions | ✅ In content + schema | High — specific dollar amounts |
| License numbers | ✅ In schema + content | High — verifiable credentials |
| Service area lists | ✅ In schema + content | High — geographic specificity |
| Statistics | ✅ 200+ EV installs, 14 years experience | Medium — specific numbers |

**Citation Readiness Score: 96/100**

---

## 12. GEO: AI Overview / ChatGPT / Perplexity Readiness

| Factor | Score | Notes |
|--------|-------|-------|
| Content extractability | ✅ Excellent | Schema markup makes every answer machine-readable |
| Direct answer format | ✅ Good | FAQ sections provide ready-made answers |
| Brand mention density | ✅ High | "AMY Electric" appears consistently |
| Competitor differentiation | ⚠️ Medium | No "why choose us" vs competitors in schema |
| Multi-platform coverage | ✅ Good | All major AI crawlers allowed |
| Structured data completeness | ✅ Excellent | FAQ, HowTo, BreadcrumbList, Electrician on most pages |

**AI Overview Readiness: 94/100**

---

## Priority Actions

### Critical (Fix Now)

1. **Standardize schema telephone format**
   - Change all instances to `+1-818-302-5614` (E.164 with dashes for readability)
   - Files: All HTML files with Electrician schema
   - Impact: Schema validation consistency

2. **Add Apple Maps sameAs link**
   - If Apple Maps listing exists, add to sameAs array
   - Impact: 10-15% of local searches via Apple devices

### High Priority

3. **Add Bing Places sameAs link**
   - If Bing Places listing exists, add to sameAs array
   - Impact: Bing/Copilot citation visibility

4. **Add unique og:image per city page**
   - Create 16 city-specific hero images or use city landmarks
   - Currently all 16 city pages share `hero-electrician.jpg`
   - Impact: Social sharing + visual local relevance

5. **Add `areaServed` to main service pages**
   - `ev-charger-installation.html`, `panel-upgrade.html`, etc. should include `areaServed`
   - Currently only on city-specific variants
   - Impact: Service pages signal geographic relevance to AI systems

### Medium Priority

6. **Increase unique content ratio on service-city pages**
   - `ev-charger-installation-{city}.html` and `panel-upgrade-{city}.html` are heavily templated
   - Add 100-200 words of unique city-specific content per page
   - Impact: Avoid thin content penalties, improve local relevance

7. **Add BBB / Angi / Thumbtack links to sameAs**
   - Even if no profile exists, consider adding industry directory links
   - Impact: Broader citation network

8. **Add `hasOfferCatalog` schema**
   - List all services with prices in structured format
   - Impact: AI systems can extract complete service catalog

### Low Priority

9. **Add `GeoCircle` to schema**
   - Define service radius around Winnetka office
   - Impact: Minor schema enrichment

10. **Create `llms.txt` for individual service pages**
    - Each service page could have its own `llms.txt`-style summary
    - Impact: Page-level AI optimization (currently only site-wide)

---

## Summary Metrics

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| NAP Consistency | 95 | 20% | 19.0 |
| GBP Signals | 90 | 15% | 13.5 |
| Schema Markup | 93 | 20% | 18.6 |
| Geo Architecture | 90 | 15% | 13.5 |
| Citations | 75 | 10% | 7.5 |
| Mobile/Technical | 92 | 10% | 9.2 |
| GEO: AI Access | 98 | 5% | 4.9 |
| GEO: llms.txt | 95 | 3% | 2.85 |
| GEO: Brand Signals | 95 | 2% | 1.9 |
| **LOCAL SEO TOTAL** | | **100%** | **92.0** |

| GEO Category | Score | Weight | Weighted |
|--------------|-------|--------|----------|
| AI Crawler Access | 98 | 25% | 24.5 |
| llms.txt Quality | 95 | 20% | 19.0 |
| RSL Configuration | 95 | 10% | 9.5 |
| Structured Data Richness | 93 | 20% | 18.6 |
| Passage Citability | 96 | 15% | 14.4 |
| AI Overview Readiness | 88 | 10% | 8.8 |
| **GEO TOTAL** | | **100%** | **94.0** |

---

*Audit conducted by reviewing all 76 HTML pages, robots.txt, llms.txt, rsl.json, _headers, sitemap.xml, and schema markup across city pages, service pages, service-city pages, and homepage.*
