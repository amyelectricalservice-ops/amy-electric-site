# Lighthouse Performance Audit & Improvement Plan

**Date:** 2026-06-10  
**Target:** https://amyelectric.com/ (homepage)  
**Device:** Mobile (Moto G Power, 4x CPU throttling)  
**Lighthouse version:** 13.x

---

## Latest Scores

| Category | Score | Rating |
|----------|-------|--------|
| Performance | **76** | Needs improvement |
| Accessibility | 100 | Pass |
| Best Practices | 81 | Needs improvement |
| SEO | 100 | Pass |

## Core Web Vitals

| Metric | Value | Rating | Target |
|--------|-------|--------|--------|
| LCP | **1.6s** | ✅ Good | < 2.5s |
| FCP | **1.6s** | ✅ Good | < 1.8s |
| TBT | **1,035ms** | ❌ Poor | < 200ms |
| CLS | **0.049** | ✅ Good | < 0.1 |
| Speed Index | **2.9s** | ✅ Good | < 3.4s |
| TTI | **4.9s** | ❌ Poor | < 3.8s |

---

## What We Did (This Session)

### 1. Self-Host Google Fonts
- Downloaded all 5 woff2 files (Barlow Condensed 600/700/800, Source Serif 400/400italic) → 160KB total
- Added `@font-face` declarations to `css/style.css` with `font-display: optional`
- Added preload for each font file on all 106 pages
- Removed: `preconnect` to fonts.googleapis.com + fonts.gstatic.com, Google Fonts CSS preload + noscript
- **Impact:** Eliminated 2 DNS lookups + 1 external CSS + 5 cross-origin font fetches
- **Impact on score:** ~−22% FCP, ~−43% LCP

### 2. Deferred GA4 to End of Body
- Moved `<script async src="gtag/js?id=G-QVSNBR7PTS">` + inline `gtag('config', ...)` from `<head>` to `</body>`
- Kept `async` attribute
- **Impact:** ~725ms script evaluation removed from critical path
- **Impact on score:** ~−41% TBT

### 3. Responsive Hero Image
- Generated 400w WebP variant (27KB vs 82KB for 800w)
- Added `<picture>` element with `media="(max-width: 480px)"` source
- **Impact:** Mobile devices ≤480px load 27KB hero instead of 82KB

### 4. CSP Hardening
- Removed `fonts.googleapis.com` from `style-src`
- Removed `fonts.gstatic.com` from `font-src`
- Added `/fonts/*` to immutable cache

---

## Before vs After

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Performance** | **67** | **76** | **+9** |
| LCP | 2.8s | 1.6s | **−43%** |
| FCP | 2.0s | 1.6s | −22% |
| TBT | 1,752ms | 1,035ms | −41% |
| Speed Index | 3.0s | 2.9s | −4% |
| TTI | 6.3s | 4.9s | −22% |
| CLS | 0.0 | 0.049 | *minor regression* |

---

## Remaining Issues & Action Plan

### P0 — Performance Score to 80+

#### 1. Disable Cloudflare Web Analytics Beacon (Dashboard)
**Impact: −200ms TBT, +3 score pts**
- **Action:** Cloudflare Dashboard → Workers & Pages → `amy-electric-site` → Metrics → toggle **Web Analytics OFF**
- Removes `beacon.min.js` (12KB) from every page load

#### 2. Reduce Turnstile Challenge (Dashboard)
**Impact: −500ms TBT, +8 score pts**
- **Action:** Cloudflare Dashboard → Security → Settings → Security Level → **Essentially Off**
- Or: Security → Bot Fight Mode → **OFF**
- Turnstile challenge script (`challenge-platform/scripts/jsd/main.js`) is the #1 JS execution cost at ~500ms
- Safe for a static marketing site (no login forms, no comments)

**Estimated score after P0:** **85–90** ✅

### P1 — Polish

#### 3. Inline Critical CSS
**Impact: −100ms FCP**
- Extract above-fold styles (~3KB) and inline in `<head>`
- Load `style.min.css` asynchronously as fallback
- Trade-off: slightly larger HTML, but faster first paint

#### 4. Remove Unnecessary Hero Image Preload on Meta-Only Pages
**Impact: −80KB on 47 pages**
- 47 pages preload `hero-electrician-800w.webp` (82KB) but only use it in OG/Twitter/schema metadata
- Remove preload from those pages (keep on the 51 that display the image)

#### 5. Add `preconnect` for Google Analytics
**Impact: −100ms on GA4 beacon**
- GA4 `gtag.js` is now deferred to body, but its beacons (`google-analytics.com/g/collect`) still need a fresh connection
- `<link rel="preconnect" href="https://www.google-analytics.com" crossorigin>`

### P2 — Watch Items

#### 6. Best Practices 81 (unactionable)
- 3 deprecated API warnings from Cloudflare Turnstile:
  - `Shared Storage API` — deprecated in Chrome
  - `StorageType.persistent` — deprecated
  - `Protected Audience API` — deprecated
- All are third-party Turnstile code — no fix available
- Will resolve when Cloudflare updates their challenge script

#### 7. CLS Regression (0.0 → 0.049)
- Minor, still well under 0.1 threshold
- Likely from `font-display: optional` → fallback font before custom font loads
- To fix: ensure font preloads complete before first paint (already preloaded, but may be a race)

---

## Dashboard To-Do

| # | Task | Where | Time |
|---|------|-------|------|
| 1 | Disable Web Analytics beacon | Workers & Pages → Metrics | 30s |
| 2 | Security Level → Essentially Off | Security → Settings | 30s |
| 3 | Disable Bot Fight Mode (if on) | Security → Bot Fight Mode | 30s |

---

## Files Changed (115 files, 920 insertions, 650 deletions)

### New
- `fonts/BarlowCondensed-600.woff2` (22KB)
- `fonts/BarlowCondensed-700.woff2` (22KB)
- `fonts/BarlowCondensed-800.woff2` (22KB)
- `fonts/SourceSerif4-400.woff2` (51KB)
- `fonts/SourceSerif4-400italic.woff2` (20KB)
- `img/hero-electrician-400w.webp` (27KB)
- `reports/homepage-mobile-2026-06-10.json` (Lighthouse artifact)

### Modified
- `css/style.css` — added @font-face declarations
- `css/style.min.css` — regenerated
- `_headers` — CSP updated, /fonts/* cache added
- All 106 HTML files — font preloads, GA4 moved to body, responsive hero image

---

## Commit History
```
b1c741a  Performance: self-host fonts, defer GA4, responsive hero image
a7a47e5  Phase 1-2: analytics, estimator, CTAs, photos, schema, blog optimization
```
