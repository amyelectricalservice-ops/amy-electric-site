# AMY Electric Website Improvement Plan

**Date:** September 10, 2026  
**Baseline:** Lighthouse Performance 90 (homepage), 86 (EV page)

---

## Executive Summary

The site is technically strong with excellent schema markup and content. The main areas for improvement are:
1. **Cumulative Layout Shift (CLS)** — 0.124 on homepage (above 0.1 threshold)
2. **Largest Contentful Paint (LCP)** — 3.4s on service pages (above 2.5s threshold)
3. **Backlink profile** — Zero referring domains

---

## Priority 1: Fix CLS (Cumulative Layout Shift)

**Current:** 0.124 (needs improvement)  
**Target:** < 0.1

### Root Cause
Web font loading causes layout shifts. The hero section shifts when BarlowCondensed-700.woff2 and BarlowCondensed-800.woff2 load.

### Fix
Add `font-display: optional` to font-face declarations, or use `size-adjust` in font fallbacks.

**Files to modify:**
- `css/src/01-variables.css` (or wherever @font-face is defined)

**Implementation:**
```css
@font-face {
  font-family: 'Barlow Condensed';
  src: url('fonts/BarlowCondensed-700.woff2') format('woff2');
  font-display: optional; /* Prevents layout shift */
}
```

**Alternative:** Add explicit width/height to hero image container and use CSS `aspect-ratio`.

---

## Priority 2: Improve LCP on Service Pages

**Current:** 3.4s (EV charger page)  
**Target:** < 2.5s

### Root Cause
Hero image loads late on service pages. The `<link rel="preload" as="image">` is present but the image may be render-blocked by CSS.

### Fix
1. Ensure hero image preload has `fetchpriority="high"`
2. Move hero image preload before CSS link in `<head>`
3. Consider inlining critical CSS for above-the-fold content

**Files to modify:**
- All service page HTML files

**Check:** Verify `<link rel="preload" as="image" href="img/ev-charger.jpg" fetchpriority="high">` is in `<head>` before any `<link rel="stylesheet">`.

---

## Priority 3: Build Backlinks

**Current:** 0 referring domains  
**Target:** 10+ referring domains in 90 days

### Action Items
1. **Google Business Profile** — Claim and complete with website link
2. **Directory submissions:**
   - BBB (Better Business Bureau)
   - Angi (formerly Angie's List)
   - HomeAdvisor
   - Houzz
   - Thumbtack
   - California CSLB contractor directory
   - Yelp (already listed — verify link)
3. **Industry outreach:**
   - Tesla authorized installer directory
   - ChargePoint partner page
   - Local electrical supply shops
4. **Local citations:**
   - LA Chamber of Commerce
   - Winnetka Chamber of Commerce
   - Neighborhood council websites

### Outreach Template
> Hi [Name], I'm Amy from AMY Electric, a licensed C-10 electrical contractor in Los Angeles. We specialize in EV charger installation and panel upgrades. I noticed your [directory/resource page] and wanted to ask if you'd be willing to list us as a recommended contractor. Our license #981578 is verifiable at cslb.ca.gov. Happy to provide any information you need.

---

## Priority 4: Differentiate City Pages

**Current:** 16 city pages with identical templates  
**Risk:** Google may treat as thin/duplicate content

### Fix
Add 2-3 unique sentences to each city page mentioning:
- A local landmark or neighborhood
- A specific project type common in that area
- Local permit requirements or utilities

**Example for Sherman Oaks:**
> "Sherman Oaks homes, especially those built in the 1960s-1980s along the hillsides, often need panel upgrades to support modern electrical loads. We've completed over 30 panel upgrades in Sherman Oaks, working with LADWP for service upgrades on both hillside and flatland properties."

---

## Priority 5: Add Review Schema to Service Pages

**Current:** Only homepage has aggregateRating  
**Target:** All service pages

### Fix
Add to each service page's Electrician/LocalBusiness schema:
```json
"aggregateRating": {
  "@type": "AggregateRating",
  "ratingValue": "4.9",
  "reviewCount": "87",
  "bestRating": "5",
  "worstRating": "1"
}
```

---

## Priority 6: Blog Content for High-Intent Keywords

### New Blog Posts to Create

| Title | Target Keyword | Search Intent |
|-------|---------------|---------------|
| "Tesla Wall Connector Installation: What LA Homeowners Need to Know in 2026" | tesla charger installation near me | High intent |
| "200 Amp Panel Upgrade Cost in Los Angeles: 2026 Price Guide" | 200 amp panel upgrade cost LA | Research |
| "California EV Charger Rebates 2026: LADWP, CALeVIP, and Federal Credits" | ev charger rebate california 2026 | Informational |
| "Panel Upgrade vs. Rewiring: Which Does Your LA Home Need?" | panel upgrade vs rewiring | Comparison |
| "Signs Your Federal Pacific or Zinsco Panel Needs Replacement" | federal pacific panel replacement | Problem-aware |

---

## Timeline

| Week | Task | Expected Impact |
|------|------|-----------------|
| 1 | Fix CLS (font-display: optional) | Performance 90→95+ |
| 1 | Verify LCP preload ordering | LCP 3.4s→2.5s |
| 2 | Submit to 5 directories | 5 backlinks |
| 2 | Add review schema to service pages | Rich snippets |
| 3 | Publish 2 new blog posts | Informational traffic |
| 3 | Differentiate 5 city pages | Local rankings |
| 4 | Outreach to 3 suppliers | 3 more backlinks |
| 4 | Publish rebates guide | High-intent traffic |

---

## Monitoring

- **Weekly:** Run Lighthouse on homepage + 1 service page
- **Monthly:** Check Google Search Console for coverage errors and query growth
- **Quarterly:** Audit backlink profile with Ahrefs or Moz
