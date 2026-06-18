# Schema & Technical SEO Audit — AMY Electric

**Audit date:** 2026-06-18
**Pages crawled:** 108 (74 root + 34 blog)
**Site:** https://amyelectric.com

---

## Executive Summary

| Category | Status |
|---|---|
| JSON-LD schema | 108/108 pages have schema — 2 pages have **invalid JSON** |
| Canonical tags | 108/108 pages — all canonical URLs match og:url ✓ |
| og:url | 108/108 pages ✓ |
| og:image | 108/108 pages — **107 have broken HTML** on the tag |
| H1 tags | 108/108 pages have exactly 1 × `<h1>` ✓ |
| Meta descriptions | 108/108 pages ✓ |
| GA4 tracking | 108/108 pages ✓ |
| CSS preload | 108/108 pages ✓ |

**Overall health: 6/10** — Strong fundamentals, but two systemic HTML bugs affect 99% of pages.

---

## Critical Issues

### 1. Broken og:image meta tag — 107 of 108 pages

**Severity:** Critical
**Pages affected:** 107 (all except `city-santa-monica.html`)

Every page has this malformed HTML:

```html
<meta property="og:image" content="https://amyelectric.com/img/hero-electrician.jpg"
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">>
```

**Problems:**
1. The `<meta property="og:image">` tag is **missing its closing `>`** — the tag is never properly closed
2. The `og:image:height` line ends with **double `>>`** — extra stray character
3. Because the first tag isn't closed, `og:image:width` and `og:image:height` may be parsed as attributes of the unclosed og:image tag, not as separate meta tags

**Impact:** Social sharing previews (Facebook, LinkedIn, X/Twitter) may fail to display the OG image, or display it incorrectly. Validators will flag this.

**Fix:** Add closing `>` to the og:image tag and remove the extra `>` from og:image:height:

```html
<meta property="og:image" content="https://amyelectric.com/img/hero-electrician.jpg">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
```

**File:** Affects all 107 pages (every `.html` file except `city-santa-monica.html`).

---

### 2. Invalid JSON-LD — 2 comparison pages

**Severity:** Critical
**Pages affected:**
- `ev-charger-hardwired-vs-plug-in.html`
- `panel-100a-vs-200a.html`

Both pages have a **stray comma** on a line by itself after the `"description"` field, followed by **duplicate `datePublished` and `dateModified` fields**:

```json
"description": "Compare hardwired vs plug-in EV charger installation...",
  ,                              ← STRAY COMMA — breaks JSON parsing
  "datePublished": "2024-01-15",  ← DUPLICATE
  "dateModified": "2026-06-08",   ← DUPLICATE
```

**Impact:** Google Search Console will reject these JSON-LD blocks entirely. The Service schema, FAQPage schema, and BreadcrumbList on these pages are all silently dropped. These two high-value comparison pages get zero rich result eligibility.

**Fix:** Remove the stray comma and duplicate `datePublished`/`dateModified` lines.

---

## High-Severity Issues

### 3. Generic og:image on 60+ pages

**Severity:** High
**Pages affected:** ~60+ pages

Most service pages, emergency pages, city pages, geo pages, and blog posts all use the same generic OG image (`img/hero-electrician.jpg`). Only a handful use page-specific images:
- `ev-charger-installation.html` → `img/ev-charger.jpg`
- `tesla-charger-installation.html` → `img/ev-charger.jpg`
- `commercial-electrical.html` → `img/commercial.jpg`
- `panel-upgrade-signs.html` → `img/panel-upgrade.jpg`
- `gallery.html` → `img/gallery/gallery-panel-siemens-stucco-1200w.webp`
- `privacy-policy.html` → `img/og-home.jpg`

**Impact:** Social shares all look identical. No differentiation in link previews. Wasted opportunity for visual branding per service.

---

### 4. BreadcrumbList issues on emergency & comparison pages

**Severity:** High
**Pages affected:** 7 pages

Emergency pages (`emergency-electrician.html`, `power-outage-repair.html`, `breaker-tripping.html`, `burning-smell-panel.html`, `same-day-electrical-repair.html`) and comparison pages (`ev-charger-hardwired-vs-plug-in.html`, `panel-100a-vs-200a.html`) have only **2-level breadcrumbs** (Home → page) instead of the standard **3-level** (Home → Services → page).

Additionally, the breadcrumb list item **names have concatenated text** with no space:

| Page | Breadcrumb item name |
|---|---|
| `emergency-electrician.html` | `"Emergency Electrician24/7 Service"` |
| `power-outage-repair.html` | `"Power Outage RepairFast Diagnosis & Repair"` |
| `breaker-tripping.html` | `"Breaker Keeps Tripping?We Can Fix It"` |
| `burning-smell-panel.html` | `"Burning Smell fromYour Electrical Panel?"` |
| `same-day-electrical-repair.html` | `"Same-Day ElectricalRepair Service"` |

**Impact:** Breadcrumb rich results may display concatenated nonsense text. Missing middle level means Google can't infer site hierarchy.

---

## Medium-Severity Issues

### 5. Missing BreadcrumbList middle level on emergency pages

**Severity:** Medium
**Pages affected:** 5 emergency pages

All emergency pages jump from "Home" directly to the page name, missing a "Services" or "Emergency" intermediate breadcrumb. Compare to service pages which correctly use Home → Services → [service].

---

### 6. SpeakableSpecification coverage

**Severity:** Medium
**Pages affected:** 90 pages missing it

Only **18 of 108 pages** have `SpeakableSpecification` schema. This helps Google Assistant and voice search identify which sections are best for TTS readout. Currently only some service and emergency pages include it.

**Recommendation:** Add to all pages, targeting the `#quick-answer` or hero section.

---

### 7. No `WebSite` or `SearchAction` schema on homepage

**Severity:** Medium
**Page affected:** `index.html`

The homepage has a comprehensive `Electrician` schema with `OfferCatalog`, `AggregateRating`, and 15+ services, but lacks a `WebSite` schema with `SearchAction`. This enables the Google Sitelinks search box.

**Note:** This only makes sense if the site has a search feature. Since it's a static site with no search, this is informational only.

---

### 8. No `LocalBusiness` type — using `Electrician`

**Severity:** Medium
**Pages affected:** 22 pages

The site uses `@type: "Electrician"` (a subtype of `LocalBusiness`), which is correct per Schema.org. However, `LocalBusiness` is more broadly recognized by Google's rich result systems. The `Electrician` type is valid but less commonly tested by validators.

**Recommendation:** No change needed — `Electrician` is semantically correct and specific.

---

## Low-Severity Issues

### 9. Duplicate FAQ answers across emergency pages

**Severity:** Low
**Pages affected:** 5 emergency pages

Multiple emergency pages have FAQ answers that are copy-pasted identical text across all 3 questions. For example, `burning-smell-panel.html` has the same answer text for "What should I do if I smell burning?", "What causes a burning smell?", and "Is a burning smell a fire risk?" — all return the same evacuation instructions.

Similarly, `same-day-electrical-repair.html` has identical answers for all 3 FAQ questions.

**Impact:** Low — Google may ignore duplicate FAQ content, but it doesn't cause penalties.

---

### 10. No `dateModified` on city pages

**Severity:** Low
**Pages affected:** 16 city pages

City pages have `Electrician` schema but no `dateModified` property. Service pages correctly include `datePublished` and `dateModified`.

---

### 11. Geo pages missing GA4 in `<head>` (minor)

**Severity:** Low
**Pages affected:** 32 geo pages

The 32 geo service pages (`ev-charger-installation-{city}.html`, `panel-upgrade-{city}.html`) include GA4 tracking but via the `gtag()` function without the preceding `window.dataLayer` initialization in a separate script block (it's inline). Not a functional issue but inconsistent with other pages.

---

## Per-Page Schema Summary

| Page type | Schema types | Count |
|---|---|---|
| Homepage | Electrician, OfferCatalog, AggregateRating, FAQPage, BreadcrumbList | 1 |
| Service pages (15) | Service, FAQPage, BreadcrumbList, SpeakableSpecification, HowTo (4 pages) | 15 |
| Emergency pages (5) | FAQPage, BreadcrumbList, SpeakableSpecification | 5 |
| Comparison pages (2) | Service*, FAQPage, BreadcrumbList, SpeakableSpecification | 2 |
| City pages (16) | Electrician, FAQPage, BreadcrumbList | 16 |
| Geo service pages (32) | Electrician, FAQPage, BreadcrumbList | 32 |
| Blog posts (31) | BlogPosting, FAQPage, BreadcrumbList | 31 |
| Blog index | — | 1 |
| Testimonials | Electrician, BreadcrumbList | 1 |
| Gallery | Electrician, BreadcrumbList, ImageGallery, ItemList | 1 |
| Privacy policy | Electrician, BreadcrumbList | 1 |

*Note: Comparison page Service schema is currently broken (invalid JSON).

---

## Canonical & Duplicate Content Analysis

| Check | Result |
|---|---|
| Canonical tags present | 108/108 ✓ |
| og:url matches canonical | 108/108 ✓ |
| Duplicate canonical URLs | 0 ✓ |
| Pages missing og:url | 0 ✓ |

**All canonical URLs are consistent and use extensionless format** (`https://amyelectric.com/panel-upgrade` not `.html`).

---

## Image Alt Text Audit

Only 1 instance of `alt=""` found across 108 pages — in the gallery modal (`gallery.html:543`). This is expected behavior (JavaScript-populated modal image).

All other images have descriptive `alt` text.

---

## HTML Validation Summary

| Issue | Pages | Fix effort |
|---|---|---|
| Missing `>` on og:image meta tag | 107 | 5 min (find & replace) |
| Extra `>>` on og:image:height | 107 | 5 min (find & replace) |
| Invalid JSON-LD (stray comma + duplicate fields) | 2 | 2 min each |
| Concatenated breadcrumb text | 5 | 10 min total |
| 2-level breadcrumbs on emergency/comparison pages | 7 | 15 min total |

---

## Recommended Fix Priority

1. **Fix og:image closing tag** across all 107 pages — systemic find & replace
2. **Fix JSON-LD** on `ev-charger-hardwired-vs-plug-in.html` and `panel-100a-vs-200a.html`
3. **Fix breadcrumb text concatenation** on 5 emergency pages
4. **Add 3-level breadcrumbs** to emergency and comparison pages
5. **Assign page-specific OG images** to high-value service pages
6. **Add SpeakableSpecification** to remaining 90 pages

---

*Audit conducted by automated crawl + manual review of 33 representative pages across all page types.*
