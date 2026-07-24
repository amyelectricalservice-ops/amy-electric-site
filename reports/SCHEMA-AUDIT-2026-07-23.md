# AMY Electric — Schema & Structured Data Audit
**Date:** July 23, 2026

## Coverage Summary

| Schema Type | Pages With | Pages Without | Coverage |
|-------------|-----------|---------------|----------|
| Electrician/LocalBusiness | 108 | 0 | 100% |
| FAQPage | 102 | 6 | 94% |
| BreadcrumbList | 108 | 0 | 100% |
| Service | 50 | 58 | 46% |
| BlogPosting | 33 | 1 | 97% (blog posts only) |
| WebSite | 17 | 91 | 16% (homepage + city pages) |
| Organization | 32 | 76 | 30% (homepage + blog posts) |
| HowTo | 15 | 93 | 14% |
| Person | 35 | 73 | 32% |
| SpeakableSpecification | 87 | 21 | 81% |

**Total HTML files:** 108
**Pages with JSON-LD:** 108 (100%)
**JSON-LD parse errors:** 0

---

## Page Category Breakdown

| Category | Count | Example Files |
|----------|-------|---------------|
| Homepage | 1 | `index.html` |
| Service | 22 | `panel-upgrade.html`, `ev-charger-installation.html` |
| City | 16 | `city-burbank.html`, `city-los-angeles.html` |
| Geo-service | 32 | `ev-charger-installation-burbank.html`, `panel-upgrade-encino.html` |
| Blog | 34 | `blog/breaker-keeps-tripping-causes.html`, `blog/index.html` |
| Special | 3 | `gallery.html`, `testimonials.html`, `privacy-policy.html` |

---

## Detailed Findings by Schema Type

### Electrician / LocalBusiness (108 pages)

**Coverage:** 108/108 — every page has an Electrician schema block.

**Structure per page type:**
- **Homepage:** Single canonical Electrician with `@id: "https://amyelectric.com"`, full address, geo coordinates, openingHoursSpecification, aggregateRating, hasOfferCatalog, hasCredential, areaServed, sameAs
- **Service pages (22):** Electrician with `@id` per page URL, address, geo, credentials, aggregateRating, priceRange — but **all 22 missing areaServed**
- **City pages (16):** Same structure as service pages — **all 16 missing areaServed**
- **Geo-service pages (32):** Same structure — **all 32 missing areaServed**
- **Blog pages (34):** 31 have Electrician (not all), 3 have it within BlogPosting publisher
- **Special pages (3):** All 3 have Electrician

**Required fields check (all 108 pages):**

| Field | Present | Missing |
|-------|---------|---------|
| name | 108 | 0 |
| telephone | 108 | 0 |
| address | 108 | 0 |
| priceRange | 108 | 0 |
| url | 108 | 0 |
| geo | 108 | 0 |
| openingHoursSpecification | 108 | 0 |
| aggregateRating | 108 | 0 |
| hasCredential | 108 | 0 |
| **areaServed** | **35** | **73** |

**areaServed gap:** Only the homepage (1), some blog pages (~31), and 3 special pages include `areaServed`. All 22 service pages, 16 city pages, and 32 geo-service pages are missing it.

**@id strategy:** Each page uses a unique `@id` matching its canonical URL (e.g., `https://amyelectric.com/panel-upgrade`). This is correct — allows Google to merge entity data across pages.

**Address consistency:** All Electrician schemas use the same business address:
- 20628 Londelius St, Winnetka, CA 91306
- Matches visible footer address on all pages ✓

---

### Service Schema (50 pages)

**Pages with Service schema:**
- 32 geo-service pages (ev-charger-installation-{city}, panel-upgrade-{city}) — 100%
- 17 root service pages (panel-upgrade, ev-charger-installation, ceiling-fan-installation, etc.) — 77%
- 1 comparison page (panel-100a-vs-200a)

**5 service pages WITHOUT Service schema:**
1. `breaker-tripping.html`
2. `burning-smell-panel.html`
3. `emergency-electrician.html`
4. `power-outage-repair.html`
5. `same-day-electrical-repair.html`

**Geo-service Service schema structure (32 pages):**
```json
{
  "@type": "Service",
  "serviceType": "EV Charger Installation",
  "provider": {"@type": "Electrician", "name": "AMY Electric", "url": "https://amyelectric.com"},
  "areaServed": {"@type": "City", "name": "Burbank"},
  "offers": {"@type": "Offer", "priceCurrency": "USD", "priceRange": "$800-$2500"}
}
```
**Issues:** All 32 geo-service Service schemas missing `name` and `description` fields.

**Root service pages Service schema (17 pages):**
- 15 have priceRange in offers ✓
- 2 comparison pages (ev-charger-hardwired-vs-plug-in, panel-100a-vs-200a) have Service with offers but no price/priceRange

---

### FAQPage Schema (102 pages)

**Pages WITH FAQPage:** 102/108

**6 pages WITHOUT FAQPage:**
1. `blog/gfci-afci-protection-la.html`
2. `blog/how-to-choose-electrician-los-angeles.html`
3. `blog/index.html`
4. `blog/signs-you-need-electrical-panel-upgrade.html`
5. `blog/smart-home-electrical-upgrades-la.html`
6. `privacy-policy.html` (no visible FAQs on page, so N/A)

**FAQ structure:** Well-formed `mainEntity` array with Question → acceptedAnswer nesting. All validated ✓.

**Content-schema mismatches found:**

| Page | Issue |
|------|-------|
| `index.html` | 16 HTML `<summary>` elements but only 15 schema questions (form toggle counted) |
| `city-santa-monica.html` | 7 HTML summaries but only 5 schema questions (2 duplicate HTML FAQs not in schema) |
| `ev-charger-installation.html` | 5 HTML summaries but only 4 schema questions |
| `panel-upgrade.html` | 5 HTML summaries but only 3 schema questions |
| `gallery.html` | 3 schema questions but 0 visible FAQ sections |
| `testimonials.html` | 3 schema questions but 0 visible FAQ sections |
| `blog/california-electrical-code-changes-2026.html` | 5 HTML summaries but only 4 schema questions |
| `blog/generator-installation-cost-la.html` | 3 schema questions but 0 visible FAQ sections |
| `blog/ladwp-ev-charger-rebate-guide-2026.html` | 5 HTML summaries but only 4 schema questions |

**FAQ text mismatches (schema ≠ HTML):**
- `burning-smell-panel.html`: "from" vs "in" wording differences
- `ev-charger-hardwired-vs-plug-in.html`: 3 questions differ (schema has different phrasing)
- `ev-charger-installation.html`: questions are shifted — schema Q3 = HTML Q4, etc.
- `panel-100a-vs-200a.html`: 5 questions completely mismatched between schema and HTML
- `panel-upgrade.html`: 2 questions mismatched
- `blog/california-electrical-code-changes-2026.html`: 3 questions mismatched
- `blog/ladwp-ev-charger-rebate-guide-2026.html`: 3 questions mismatched
- All 16 city pages: HTML has trailing `▾` characters in summary text but schema strips them (minor)

---

### Duplicate FAQs in HTML (16 city pages)

All 16 city pages have **2 duplicate `<details>` elements** in the HTML:

| Duplicate Question | Appears In |
|--------------------|-----------|
| "Are you licensed and insured to work in {city}?" | All 16 city pages |
| "Do you offer free estimates for electrical work in {city}?" | All 16 city pages |

The JSON-LD FAQPage schema correctly includes each question only once (7 questions), but the HTML renders 7 `<details>` elements with 2 duplicates. This means the visible page shows duplicate FAQ sections.

---

### BreadcrumbList Schema (108 pages)

**Coverage:** 108/108 ✓

**Structure:** All pages have correct sequential position numbering (1, 2, 3). No position gaps or duplicates found.

**Position 2 link patterns:**

| Pattern | Pages | URL |
|---------|-------|-----|
| Services → Homepage | 7 | `https://amyelectric.com/` |
| Services → Homepage#services | 47 | `https://amyelectric.com/#services` |
| Service Areas → city-los-angeles | 16 | `https://amyelectric.com/city-los-angeles` |
| Blog → /blog | 30 | `https://amyelectric.com/blog` |
| Blog → /blog/ | 1 | `https://amyelectric.com/blog/` |
| Blog → /blog/index | 3 | `https://amyelectric.com/blog/index` |
| Gallery → (empty) | 1 | `""` |
| Privacy Policy → (empty) | 1 | `""` |
| Testimonials → /testimonials | 1 | `https://amyelectric.com/testimonials` |

**Issues found:**

| Issue | Pages Affected |
|-------|---------------|
| Empty URL in BreadcrumbList position 2 | `gallery.html`, `privacy-policy.html` |
| `item: null` in BreadcrumbList position 3 | `city-los-angeles.html` |
| Blog URL inconsistency (`/blog` vs `/blog/` vs `/blog/index`) | 3 blog pages use `/blog/index`, 1 uses `/blog/`, 30 use `/blog` |
| "Service Areas" links to `city-los-angeles.html` (not a proper index page) | All 16 city pages |
| "Services" links to homepage anchor (not a services index page) | 54 service/geo pages |

---

### BlogPosting Schema (33 pages)

**Coverage:** 33/34 blog posts (blog/index.html uses `Blog` type instead, which is correct)

**3 blog posts with severely incomplete BlogPosting:**

| Page | Missing Fields |
|------|---------------|
| `blog/how-to-choose-electrician-los-angeles.html` | author, publisher, datePublished, image, description, url |
| `blog/signs-you-need-electrical-panel-upgrade.html` | author, publisher, datePublished, image, description, url |
| `blog/smart-home-electrical-upgrades-la.html` | author, publisher, datePublished, image, description, url |

These 3 pages only have `headline` and `mainEntityOfPage` in their BlogPosting — Google may ignore the rich result entirely.

**30 working BlogPosting pages have:**
- headline ✓
- author (Person with name, image, description, url) ✓
- publisher (Organization with name and logo) ✓
- datePublished ✓
- dateModified ✓
- image ✓
- description ✓
- mainEntityOfPage ✓

---

### HowTo Schema (15 pages)

**Coverage:** 15/108 (14%)

**Pages with HowTo:**
- `panel-upgrade.html` (5 steps)
- `ev-charger-installation.html`
- `generator-transfer-switch.html`
- `whole-home-rewiring.html`
- 11 other service pages

**All validated:** name, step array with HowToStep type and text ✓

**Service pages WITHOUT HowTo (7 pages):**
- `breaker-tripping.html`
- `burning-smell-panel.html`
- `emergency-electrician.html`
- `panel-100a-vs-200a.html` (comparison page, N/A)
- `power-outage-repair.html`
- `same-day-electrical-repair.html`
- `ev-charger-hardwired-vs-plug-in.html` (comparison page, N/A)

---

### WebSite Schema (17 pages)

**Coverage:** 17/108 (16%) — homepage + 16 city pages

**Structure:** All include `name`, `url`, and `potentialAction` → `SearchAction` → `EntryPoint` with `urlTemplate`

**All validated:** ✓

**Note:** Only present on homepage and city pages. Not on service or blog pages (acceptable — WebSite schema is typically homepage-only).

---

### Organization Schema (32 pages)

**Coverage:** 32/108 (30%) — homepage + 31 blog posts

**Structure:** All include `name`, `url`, `logo`, `contactPoint` (telephone, contactType, availableLanguage), `sameAs`

**Homepage Organization sameAs links:**
- Yelp: `https://www.yelp.com/biz/amy-electric-los-angeles`
- Google Business: `https://g.page/r/CVdK9ZAvNBrZEAI/review`
- Google Maps: `https://maps.app.goo.gl/WTNSkHRUgULPBHpc9`
- Facebook: `https://www.facebook.com/people/Amy-Electric/100063766463600/`

**All validated:** ✓

---

### Person Schema (35 pages)

**Coverage:** 35/108 (32%) — homepage + 31 blog posts + 3 special pages

**Structure:** `name`, `description`, `image`, `url`, `knowsAbout`

**All validated:** ✓

---

### SpeakableSpecification (87 pages)

**Coverage:** 87/108 (81%)

**Structure:**
```json
{
  "@type": "SpeakableSpecification",
  "cssSelector": [".page-hero h1", ".page-hero p"]
}
```

**15 service pages WITHOUT SpeakableSpecification:**
- `breaker-tripping.html`
- `burning-smell-panel.html`
- `ceiling-fan-installation.html`
- `commercial-electrical.html`
- `electrical-repair.html`
- `emergency-electrician.html`
- `generator-transfer-switch.html`
- `lighting-installation.html`
- `outlet-switch-installation.html`
- `panel-100a-vs-200a.html`
- `power-outage-repair.html`
- `same-day-electrical-repair.html`
- `surge-protection.html`
- `tesla-charger-installation.html`
- `whole-home-rewiring.html`

---

## JSON-LD Syntax Errors

**None found.** All 108 pages parse successfully. No trailing commas, no invalid quoting, no missing `@context`.

---

## Content-Schema Mismatches

### Critical Mismatches

1. **`ev-charger-installation.html` FAQ shift:** Schema has "How much does EV charger installation cost in Los Angeles?" as Q3, but HTML has "Are there rebates for EV charger installation in LA?" at that position. The schema and HTML FAQ order don't match.

2. **`panel-100a-vs-200a.html` FAQ complete mismatch:** Schema has 5 questions that don't match any of the 5 HTML questions. Schema Qs: "How much does a 100A vs 200A panel upgrade cost in Los Angeles?", "Is 200A required for an EV charger?", etc. HTML Qs: "Does Los Angeles building code require 200A panels?", "Is 200A worth the extra cost?", etc.

3. **`blog/california-electrical-code-changes-2026.html` FAQ mismatch:** 3 of 4 schema questions don't match HTML. Schema has "Do I need AFCI breakers in my Los Angeles home?" but HTML has "Do I need to upgrade my existing home to meet 2026 code?"

4. **`blog/ladwp-ev-charger-rebate-guide-2026.html` FAQ mismatch:** 3 of 4 schema questions don't match HTML.

### Minor Mismatches

5. **HTML trailing `▾` in FAQ summaries:** All city and geo-service pages have `▾` character in `<summary>` text that's stripped in schema. Not a real issue (visual-only).

6. **`index.html` form toggle counted as FAQ:** The "📋 Detailed Estimate Form (4 additional fields)" `<summary>` is counted as the first HTML summary, making the count 16 vs 15 schema questions. The schema correctly excludes it.

7. **`gallery.html` and `testimonials.html`:** Have 3 FAQ questions in schema but 0 visible `<details>/<summary>` elements in HTML. The FAQ content may be rendered via JavaScript or simply not visible.

---

## Recommendations

### Priority 1 — High Impact (Fix Immediately)

1. **Fix 3 incomplete BlogPosting schemas** — `blog/how-to-choose-electrician-los-angeles.html`, `blog/signs-you-need-electrical-panel-upgrade.html`, `blog/smart-home-electrical-upgrades-la.html` are missing author, publisher, datePublished, image, and description. Without these, Google won't show rich results for these posts.

2. **Add Service schema to 5 missing service pages** — `breaker-tripping.html`, `burning-smell-panel.html`, `emergency-electrician.html`, `power-outage-repair.html`, `same-day-electrical-repair.html`. These are high-intent service pages that would benefit from rich results.

3. **Fix FAQ content mismatches on 4 pages** — `ev-charger-installation.html`, `panel-100a-vs-200a.html`, `blog/california-electrical-code-changes-2026.html`, `blog/ladwp-ev-charger-rebate-guide-2026.html` have schema FAQ text that doesn't match visible HTML. Google may ignore or penalize mismatched FAQ schema.

4. **Remove duplicate `<details>` elements from 16 city pages** — Each city page renders 2 FAQ questions twice in HTML. Remove the duplicate `<details>` blocks. The schema already correctly has 7 unique questions.

### Priority 2 — Medium Impact

5. **Add `name` and `description` to 32 geo-service Service schemas** — Currently only have `serviceType`, `provider`, `areaServed`, and `offers`. Adding `name` (e.g., "EV Charger Installation in Burbank") and `description` would improve rich result eligibility.

6. **Add `areaServed` to 73 Electrician schemas** — All service, city, and geo-service pages are missing `areaServed` in the Electrician block. This is valuable local SEO signal data.

7. **Add FAQPage schema to 4 blog posts missing it** — `blog/gfci-afci-protection-la.html`, `blog/how-to-choose-electrician-los-angeles.html`, `blog/signs-you-need-electrical-panel-upgrade.html`, `blog/smart-home-electrical-upgrades-la.html`.

8. **Add SpeakableSpecification to 15 service pages** — Missing from: breaker-tripping, burning-smell-panel, ceiling-fan-installation, commercial-electrical, electrical-repair, emergency-electrician, generator-transfer-switch, lighting-installation, outlet-switch-installation, panel-100a-vs-200a, power-outage-repair, same-day-electrical-repair, surge-protection, tesla-charger-installation, whole-home-rewiring.

### Priority 3 — Low Impact (Polish)

9. **Fix empty BreadcrumbList URLs** — `gallery.html` and `privacy-policy.html` have empty `item` in position 2. Add proper URLs.

10. **Fix `city-los-angeles.html` BreadcrumbList position 3** — `item` is `null`. Should be `https://amyelectric.com/city-los-angeles`.

11. **Standardize Blog BreadcrumbList position 2 URL** — 3 pages use `/blog/index`, 1 uses `/blog/`, 30 use `/blog`. Pick one canonical format.

12. **Consider adding FAQPage to `privacy-policy.html`** — Has 3 FAQ questions in schema but no visible FAQ section. Either remove the schema or add visible FAQ content.

13. **Add FAQPage to `blog/generator-installation-cost-la.html`** — Has 3 schema questions but no visible FAQ section.
