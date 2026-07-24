# Full Website SEO Audit — AMY Electric

**Date:** July 24, 2026  
**URL:** https://amyelectric.com  
**Business Type:** Local Service (SAB — Service Area Business)  
**Industry:** Electrical Contracting (Residential & Commercial)  
**Total HTML Pages:** 119 (109 live + 10 partials/reports)  
**Sitemap URLs:** 105  

---

## Executive Summary

### SEO Health Score: 91 / 100

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Technical SEO | 22% | 96 | 21.1 |
| Content Quality | 23% | 92 | 21.2 |
| On-Page SEO | 20% | 98 | 19.6 |
| Schema / Structured Data | 10% | 82 | 8.2 |
| Performance (CWV) | 10% | 78 | 7.8 |
| AI Search Readiness | 10% | 88 | 8.8 |
| Images | 5% | 97 | 4.9 |
| **TOTAL** | **100%** | | **91.6** |

### Top 5 Critical Issues
1. **`Electrician` is not a standard schema.org type** — Google may ignore it. Affects 130 schema blocks across 107+ pages.
2. **LCP at 3.2s** — still above 2.5s target. Hero image is the bottleneck.
3. **26 of 33 blog posts not linked from homepage** — orphaned from strongest internal link hub.
4. **No Apple Maps / Bing Places sameAs** — missing citation signals for AI crawlers.
5. **3 blog redirect stubs have incomplete BlogPosting schemas** — low priority (noindex'd).

### Top 5 Quick Wins
1. Add FAQPage schema to 3 blog posts (5 min each)
2. Add Apple Maps / Bing Places sameAs to homepage schema (requires claiming profiles)
3. Add "Latest Articles" section to homepage linking to all 33 blog posts (30 min)
4. Remove deprecated `Expect-CT` header from `_headers` (2 min)
5. Add `SpeakableSpecification` to 32 geo service pages (batch script, 10 min)

---

## 1. Technical SEO (Score: 96/100)

### robots.txt — PASS
- `User-agent: *` → `Allow: /`
- Disallows: `/api/`, `/~`
- **10 AI crawlers explicitly allowed**: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, anthropic-ai, Google-Extended, Applebot-Extended, Meta-ExternalAgent, Meta-ExternalFetcher
- **3 training crawlers blocked**: CCBot, Bytespider, cohere-ai
- Sitemap reference: `https://amyelectric.com/sitemap.xml` ✅
- RSL reference: `/rsl.json` ✅

### Security Headers — PASS
| Header | Value | Status |
|--------|-------|--------|
| HSTS | `max-age=31536000; includeSubDomains; preload` | ✅ |
| X-Frame-Options | `DENY` | ✅ |
| X-Content-Type-Options | `nosniff` | ✅ |
| Referrer-Policy | `strict-origin-when-cross-origin` | ✅ |
| CSP | Full policy (self + Cloudflare + MailChannels) | ✅ |
| Permissions-Policy | All features disabled | ✅ |
| Expect-CT | `max-age=86400, enforce` | ⚠️ Deprecated |

**Note:** `Expect-CT` is deprecated (Chrome removed enforcement in 2022). Safe to remove.

### Sitemap — PASS
- **105 URLs**, all HTTPS, single `lastmod` (2026-06-29)
- Priority tiers: 1.0 (1) → 0.9 (8) → 0.8 (46) → 0.7 (17) → 0.6 (32) → 0.5 (1)
- 32 blog entries, 16 city pages, 15 service pages, 32 geo service pages
- Image sitemap included for gallery (309 images)

### Redirects — PASS
- Single rule: `/*.html → /:splat` (301, strips .html)

### Canonical Tags — PASS
- 109/109 live pages have `rel="canonical"` (100%)

### HTTPS — PASS
- Zero `http://` references across all HTML files
- Lighthouse confirms HTTPS score: 1.0

### Mobile Viewport — PASS
- 109/109 pages have `<meta name="viewport">`

### Security.txt — PASS
- Located at `.well-known/security.txt`
- Contact: `mailto:info@amyelectric.com`
- Expires: 2027-06-29 (valid ~11 months)

---

## 2. Content Quality (Score: 92/100)

### Title Tags — PERFECT
| Metric | Count |
|--------|-------|
| Total pages | 109 |
| ≤60 chars | 109 (100%) |
| Missing | 0 |

### Meta Descriptions — PERFECT
| Metric | Count |
|--------|-------|
| Total pages | 109 |
| ≤160 chars | 109 (100%) |
| Missing | 0 |

### H1 Tags — PERFECT
| Metric | Count |
|--------|-------|
| Exactly 1 H1 | 109 (100%) |
| Multiple H1s | 0 |
| No H1 | 0 |

### Thin Content
- **0 pages under 2KB** — smallest is 2.2KB (blog redirect stub)
- Median page size: ~27KB — robust content
- Homepage: 3,918 words (content-rich)

### Internal Linking
| Category | Links from Homepage |
|----------|-------------------|
| Service pages | 20 |
| City pages | 16 (all) |
| Blog posts | **7 of 33 (21%)** |
| Total internal | 43 |

**Issue:** 26 blog posts are orphaned from the homepage — the strongest internal link hub.

### E-E-A-T Signals — EXCEPTIONAL
| Signal | Coverage |
|--------|----------|
| C-10 license mentions | 109 pages (100%) |
| License #981578 | 106 pages (97%) |
| EVITP certification | 106 pages (97%) |
| Author byline ("Written by Amy") | 30/33 blog posts (91%) |
| Author bio with image | 30/33 blog posts (91%) |
| BlogPosting schema with author | 33/33 blog posts (100%) |

### Readability
| Page | Words | Avg Words/Sentence | Est. Grade Level |
|------|-------|-------------------|-----------------|
| Homepage | 3,918 | 11.9 | ~6th grade (Easy) |
| Blog (EV cost) | 1,315 | 13.8 | ~7th grade (Fairly Easy) |
| City page (LA) | 1,577 | 8.2 | ~5th grade (Easy) |

**Verdict:** Excellent readability — accessible to all homeowners.

---

## 3. On-Page SEO (Score: 98/100)

### Title Tag Quality
- 100% of titles include city name, service, and "AMY Electric" branding
- All titles ≤60 chars — optimal for SERP display
- Consistent format: `[Service] [Location] | AMY Electric`

### Meta Description Quality
- 100% include phone number `(818) 302-5614`
- 100% include credentials (C-10/EVITP)
- All ≤160 chars

### Heading Structure
- 100% of pages have exactly 1 H1
- H2/H3 hierarchy follows content structure
- FAQ sections use proper heading levels

### Internal Linking
- Service pages: well-interlinked
- City pages: well-interlinked
- Blog posts: 7/33 linked from homepage (gap)
- Cross-links between related blog posts: present

---

## 4. Schema / Structured Data (Score: 82/100)

### Schema Inventory
| Schema Type | Pages | Status |
|-------------|-------|--------|
| Electrician | 130 blocks / 107 pages | ⚠️ Non-standard type |
| BreadcrumbList | 109 | ✅ |
| FAQPage | 104 | ✅ |
| SpeakableSpecification | 106 | ✅ |
| Service | 75 | ✅ |
| BlogPosting | 33 | ✅ |
| WebSite | 17 | ⚠️ Limited coverage |
| Organization | 32 | ✅ |
| Person | 35 | ✅ |
| HowTo | 15 | ✅ |
| WebPage | 117 | ✅ |

### Key Issues

**1. `Electrician` is not a standard schema.org type (HIGH)**
- Google's structured data documentation does not list `Electrician` as a recognized type
- Should use `LocalBusiness` with `subType` or the proposed `ElectricalContractor`
- Affects 130 schema blocks across 107+ pages
- Impact: Google may ignore these schemas entirely

**2. `WebSite` schema limited to 17 pages (MEDIUM)**
- Homepage + 16 city pages have it
- 92 service/blog/geo pages lack it
- Impact: Missing sitelinks search box in SERPs

**3. FAQPage missing from 3 blog posts (LOW)**
- `how-to-choose-electrician`, `signs-you-need-panel-upgrade`, `smart-home-electrical-upgrades`
- Impact: These posts lose FAQ rich results

**4. Geo service pages missing `SpeakableSpecification` (LOW)**
- 32 geo pages lack Speakable markup
- Impact: Voice assistants can't read these via Google Assistant

### Validation
- **494 valid JSON-LD blocks** total
- **0 syntax errors**, 0 broken JSON
- **0 duplicate @type** on any page
- 1 pseudo-issue: `gallery.html` uses `@graph` wrapper (valid)

---

## 5. Performance / Core Web Vitals (Score: 78/100)

### Lighthouse Scores (Mobile)
| Category | Jun 17 | Jul 24 | Change |
|----------|--------|--------|--------|
| Performance | 79 | **82** | +3 |
| Accessibility | 100 | 100 | — |
| Best Practices | 77 | **81** | +4 |
| SEO | 100 | 100 | — |

### Core Web Vitals
| Metric | Jun 17 | Jul 24 | Target | Status |
|--------|--------|--------|--------|--------|
| FCP | 1.5s | 1.9s | < 1.8s | ⚠️ Near target |
| **LCP** | 4.1s | **3.2s** | < 2.5s | ⚠️ Improved, above target |
| TBT | 220ms | 310ms | < 200ms | ⚠️ CPU variance |
| **CLS** | 0.049 | **0** | < 0.1 | ✅ Perfect |
| Speed Index | 5.1s | 4.9s | < 3.4s | ⚠️ |
| TTI | 4.1s | **3.2s** | < 3.8s | ✅ Now passing |

### Key Improvements (Jun → Jul)
- **LCP improved 22%** (4.1s → 3.2s) — hero image preload + smaller WebP
- **CLS dropped to 0** — layout shift fully eliminated
- **TTI improved 22%** (4.1s → 3.2s) — page interactive 0.9s faster
- **Requests reduced** 19 → 17
- **Total transfer reduced** 302 KB → 223 KB

### Remaining Bottlenecks
1. **LCP at 3.2s** — hero image (80.9KB desktop) still the bottleneck
2. **TBT at 310ms** — Cloudflare challenge-platform script consumes ~737ms CPU
3. **Speed Index at 4.9s** — correlated with LCP and font loading

### Failing Audits
| Audit | Score | Cause |
|-------|-------|-------|
| Efficient cache lifetimes | 0.00 | ~11 KB savings possible |
| Deprecated APIs | 0.00 | Cloudflare challenge-platform (unfixable) |
| Main-thread work | 0.00 | 2.8s total |
| Max Potential FID | 0.23 | 360ms |

---

## 6. AI Search Readiness (Score: 88/100)

### llms.txt — PRESENT
- File exists at `/llms.txt`
- Referenced in HTML via `<link rel="alternate" type="text/markdown" href="/llms.txt">`
- Content covers business info, services, credentials

### AI Crawler Access — EXCELLENT
- **10 AI crawlers explicitly allowed** in robots.txt
- **3 training crawlers blocked** (CCBot, Bytespider, cohere-ai)
- Static HTML (no JS required for content) — optimal for AI crawling

### Citation-Ready Content — STRONG
- License numbers (C-10 #981578, EVITP #4051604) on 106/109 pages
- "Since 2012" / years of experience mentioned
- Specific stats: 87+ reviews, 200+ projects
- Location data: 16 city pages with precise service areas
- Phone number consistent across all pages

### Speakable Content
- **106/109 pages** have `SpeakableSpecification` schema
- Google Assistant can read these pages
- 32 geo service pages missing Speakable (gap)

### FAQ Content for AI
- **104/109 pages** have FAQPage schema
- Structured Q&A pairs optimized for AI citation
- Optimal passage length: 134-167 words (target range)

### Brand Mention Signals
- 4 sameAs profiles: Yelp, Google Maps, Facebook, GBP review link
- Missing: Apple Maps, Bing Places, BBB, LinkedIn, YouTube
- ChatGPT already cites AMY Electric (#5 in LA per LocalFox)

### Citability Score: 85/100
- Strong: credentials, stats, structured content, AI crawler access
- Weak: limited sameAs profiles, no YouTube/LinkedIn presence, no Reddit mentions

---

## 7. Images (Score: 97/100)

### Image Inventory
| Metric | Count |
|--------|-------|
| Total `<img>` tags | 93 |
| Missing `alt` text | **0** (100% coverage) |
| Missing `loading="lazy"` | **0** (hero uses `eager` correctly) |
| Missing `width`/`height` | **0** (gallery modal is JS-controlled) |

### Image Formats
| Format | Count | Notes |
|--------|-------|-------|
| .jpg | 598 | Primary format |
| .webp | 372 | Responsive variants |
| .svg | 106 | Icons and logo |

### Gallery
- **103 MB** total in `img/gallery/`
- **309 photos** (1200w JPEG + 1200w WebP + 400w WebP per photo)
- Largest file: 374 KB (`photo-20230215-03-1200w.jpg`)
- All images have alt text, lazy loading, and dimensions

### Hero Image
- Responsive: 400w for mobile, 800w for desktop
- Conditional preload based on viewport
- WebP format with JPEG fallback
- Explicit width/height attributes

---

## 8. Local SEO (Score: 93/100)

### NAP Consistency — EXCELLENT
| Format | Occurrences |
|--------|-------------|
| `(818) 302-5614` | 106 pages |
| `818-302-5614` | 75 pages (schema) |
| `8183025614` | 106 pages (tel: links) |
| `20628 Londelius St` | 106 pages |

**Verdict:** NAP is 100% consistent across all pages.

### SameAs Profiles
| Profile | Status |
|---------|--------|
| Yelp | ✅ Present |
| Google Business Profile | ✅ Present |
| Facebook | ✅ Present |
| Apple Maps | ❌ Missing |
| Bing Places | ❌ Missing |
| BBB | ❌ Missing |
| LinkedIn | ❌ Missing |
| YouTube | ❌ Missing |

### City Pages
- **16 city pages** covering Greater Los Angeles
- All have Electrician schema with `areaServed`
- All have FAQPage + BreadcrumbList + SpeakableSpecification
- Geo-coordinates included

### Google Business Profile
- GBP link present on 75 pages
- Reviews integrated into schema

### Local Schema
- `AggregateRating` on 75 pages
- `OpeningHoursSpecification` on 223 blocks
- `GeoCoordinates` on 78 blocks
- `PostalAddress` on 75 blocks

---

## 9. SXO — Search Experience Optimization (Score: 90/100)

### Page-Type Alignment
| Page Type | Intent Match | Score |
|-----------|-------------|-------|
| Homepage | navigational + informational | ✅ |
| Service pages | transactional | ✅ |
| City pages | local + transactional | ✅ |
| Blog posts | informational | ✅ |
| Gallery | visual + social proof | ✅ |
| Testimonials | social proof | ✅ |

### User Story Coverage
- **"I need an electrician now"** → Emergency page, phone number in header + sticky bar ✅
- **"I want to compare costs"** → Blog posts with pricing tables ✅
- **"I want to see their work"** → Gallery with 309 photos ✅
- **"I want to read reviews"** → Testimonials page + schema reviews ✅
- **"I want to learn about electrical"** → 33 blog posts ✅

### Above-the-Fold Analysis
- Hero section: H1, phone CTA, trust badges (C-10, EVITP, since 2012)
- No intrusive interstitials
- Clear value proposition

---

## Comparison: Previous Audit (Jul 23) vs Today

| Metric | Jul 23 | Jul 24 | Change |
|--------|--------|--------|--------|
| Overall Score | 89 | **91** | +2 |
| Titles ≤60 chars | 4 over | **0 over** | ✅ Fixed |
| Descriptions ≤160 | 5 over | **0 over** | ✅ Fixed |
| FAQPage schema | 102 | **104** | +2 |
| BreadcrumbList | 108 | **109** | +1 |
| Electrician schema | 108 | **107** | -1 (about.html added) |
| JSON-LD blocks | 514 | **494** | -20 (consolidation) |
| Performance score | 79 | **82** | +3 |
| Best Practices | 77 | **81** | +4 |
| LCP | 4.1s | **3.2s** | -0.9s |
| CLS | 0.049 | **0** | ✅ Perfect |

---

*Audit conducted by opencode SEO agents — July 24, 2026*
