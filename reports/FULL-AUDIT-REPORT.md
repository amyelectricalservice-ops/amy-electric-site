# Full SEO Audit Report — AMY Electric

**Audit Date:** June 18, 2026  
**Site:** https://amyelectric.com  
**Platform:** Static HTML on Cloudflare Workers + Assets  
**Total Pages:** 108 (74 root + 34 blog)

---

## Executive Summary

| Category | Score | Status |
|----------|-------|--------|
| Technical SEO | 7/10 | Strong fundamentals, 2 systemic HTML bugs |
| Content Quality | 7/10 | Service pages excellent; blog thin + 3 duplicate pairs |
| On-Page SEO | 8/10 | All meta tags present, good heading structure |
| Schema & Structured Data | 8/10 | Comprehensive coverage, 2 pages with invalid JSON |
| Performance (CWV) | 7/10 | LCP 1.6s, TBT 1,035ms; Cloudflare edge fast |
| AI Search Readiness | 7/10 | Speakable on 18 pages, llms.txt present, GEO-ready |
| Images | 9/10 | All lazy-loaded, WebP, responsive, alt text present |
| **Overall SEO Health** | **7.6/10** | |

---

## Critical Issues (Fix Immediately)

### 1. `www.amyelectric.com` returns 522 Connection Timed Out
**Impact:** Users typing www domain see error page. No redirect working.  
**Fix:** Add DNS CNAME for www → project, or add DNS-level 301 redirect.

### 2. Broken og:image meta tag — 107 of 108 pages
Missing closing `>` on og:image tag + extra `>>` on og:image:height. Social sharing previews may fail.

### 3. Invalid JSON-LD — 2 comparison pages
Stray comma + duplicate fields on `ev-charger-hardwired-vs-plug-in.html` and `panel-100a-vs-200a.html`. Entire schema blocks silently rejected by Google.

### 4. 3 duplicate blog post pairs
- `panel-upgrade-signs` vs `signs-you-need-electrical-panel-upgrade`
- `smart-home-electrical-upgrades` vs `smart-home-electrical-upgrades-la`
- `how-to-choose-electrician-los-angeles` vs `choosing-electrician-la`

### 5. BreadcrumbList text concatenation — 5 emergency pages
Names like "Emergency Electrician24/7 Service" instead of "Emergency Electrician" — broken rich results.

---

## High-Priority Issues (Fix Within 1 Week)

| # | Issue | Pages | Impact |
|---|-------|-------|--------|
| 1 | Generic og:image on 60+ pages | 60+ | Social shares look identical |
| 2 | 10 blog posts under 1,200 words | 10 | Thin content risk |
| 3 | No FAQ sections on any blog post | 32 | Missing rich results |
| 4 | No author byline on blog posts | 32 | Weak E-E-A-T |
| 5 | Emergency pages missing Electrician schema | 5 | No local rich results |
| 6 | Geo pages missing Service schema | 32 | No service rich results |
| 7 | Only 1 of 15 service pages cites external sources | 14 | Weak AI citation |
| 8 | Blog posts average only 3 internal links | 32 | Poor PageRank flow |
| 9 | Double 301 redirect on .html URLs | 108 | Adds latency per click |
| 10 | City page FAQ answers are city-name-swapped | 16 | Low-value duplication |

---

## Medium-Priority Issues (Fix Within 1 Month)

| # | Issue | Pages | Impact |
|---|-------|-------|--------|
| 1 | SpeakableSchema only on 18/108 pages | 90 | Voice search gap |
| 2 | No Quick Answer sections on city/geo pages | 48 | AI citation gap |
| 3 | No visible publication dates on blog posts | 32 | Freshness signal missing |
| 4 | No /about page for Amy's credentials | Site-wide | E-E-A-T gap |
| 5 | No WebSite/SearchAction schema | Homepage | No sitelinks search box |
| 6 | Emergency page FAQ answers are copy-pasted | 5 | Low-value duplication |
| 7 | City pages missing dateModified | 16 | Freshness signal missing |

---

## What's Working Well

| Area | Status |
|------|--------|
| HTTP → HTTPS redirect | ✅ 301 in place |
| Security headers | ✅ HSTS, CSP, X-Frame-Options all strong |
| Sitemap | ✅ 108 URLs, all HTTPS, valid dates |
| Robots.txt | ✅ AI crawlers allowed, training blocked |
| Canonical tags | ✅ 108/108 present, zero duplicates |
| Schema coverage | ✅ Electrician/Service/FAQPage/BreadcrumbList across site |
| Voice search | ✅ Quick Answer + Speakable on 18 key pages |
| Self-hosted fonts | ✅ 160KB total, immutable cache |
| Cloudflare edge caching | ✅ HIT on warm loads, <0.6s |
| Image optimization | ✅ WebP + lazy load + responsive |
| GA4 tracking | ✅ Present on all pages |
| Contact form | ✅ Working, honeypot + rate limit |
| llms.txt | ✅ AI-friendly site description |
| Price transparency | ✅ 15 service pages with pricing |

---

## Schema Coverage Matrix

| Schema Type | Coverage | Notes |
|-------------|----------|-------|
| Electrician (LocalBusiness) | 86/108 | Missing on emergency (5) + blog index (1) + privacy (1) + 15 blog posts |
| Service | 17/108 | Only on 15 service + 2 comparison pages |
| FAQPage | 94/108 | Missing on 14 pages with no FAQ content |
| BreadcrumbList | 108/108 | ✅ Complete |
| BlogPosting | 33/33 | ✅ All blog posts + index |
| HowTo | 4/108 | panel-upgrade, ev-charger, generator, rewiring |
| SpeakableSpecification | 18/108 | Service (11) + emergency (5) + comparison (2) |
| PriceRange/offers | 15/108 | All 15 root service pages |
| ImageGallery | 1/108 | Gallery page only |

---

## Content Quality Summary

| Page Type | Avg Words | FAQ | Schema | E-E-A-T | Score |
|-----------|-----------|-----|--------|---------|-------|
| Service (root) | 2,352 | 4–6 | 8–10 types | Strong | 87/100 |
| Emergency | 1,579 | 3 | 3 types | Moderate | 72/100 |
| Comparison | 2,884 | 6 | 6–8 types | Strong | 88/100 |
| City | 1,805 | 3 | 10+ types | Strong | 78/100 |
| Geo Service | 2,179 | 7 | 4–5 types | Strong | 75/100 |
| Blog | 1,437 | 0 | 1–2 types | Moderate | 68/100 |

---

## Performance Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| LCP | 1.6s | < 2.5s | ✅ |
| TBT | 1,035ms | < 200ms | ⚠️ |
| CLS | 0.049 | < 0.1 | ✅ |
| FCP | 1.6s | < 1.8s | ✅ |
| Mobile score | 76 | 90+ | ⚠️ |
| Warm cache TTFB | 0.2–0.6s | < 0.5s | ✅ |

---

*Full sub-reports: `schema-technical-audit.md`, `content-quality-audit.md`, `live-site-audit.md`*
