# AMY Electric — Content Quality & Image Audit
**Date:** July 23, 2026
**Scope:** 108 HTML pages (homepage, 15 service pages, 16 city pages, 32 geo pages, 33 blog posts, 12 special/info pages)

---

## CONTENT SCORE: 86/100

### Title Tags
- **Total pages:** 108 — all have `<title>` tags (0 missing)
- **Length range:** 41–71 chars
- **Ideal range (50–60 chars):** 100 pages (93%) — excellent coverage
- **Over 60 chars (2):**
  - `blog/california-electrical-code-changes-2026.html` — 71 chars
  - `blog/smoke-co-detector-installation-la.html` — 62 chars
- **Under 50 chars (1):**
  - `privacy-policy.html` — 41 chars (acceptable for utility page)
- **Duplicates:** 0 — every title is unique
- **Pattern consistency:** City pages use "Electrician in {City}, CA | Panel Upgrades | AMY Electric" (51–60 chars). Service pages use "{Service} Los Angeles | AMY Electric" (50–56 chars). Blog posts use descriptive titles with "AMY Electric" suffix.

### Meta Descriptions
- **Total pages:** 108 — all have meta descriptions (0 missing)
- **Length range:** 118–166 chars
- **Ideal range (120–160 chars):** 97 pages (90%)
- **Over 160 chars (2):**
  - `blog/smoke-co-detector-installation-la.html` — 166 chars (truncated in SERPs)
  - `panel-upgrade-burbank.html` — 160 chars (borderline)
- **Under 120 chars (3):**
  - `blog/signs-you-need-electrical-panel-upgrade.html` — 118 chars
  - `blog/how-to-choose-electrician-los-angeles.html` — 126 chars
  - `blog/smart-home-electrical-upgrades-la.html` — 132 chars
- **Duplicates:** 0 — all unique
- **Pattern:** All descriptions end with "Call (818) 302-5614." (good CTA). City page descriptions follow template with city name swapped. Geo pages include "Licensed C-10 #981578" (E-E-A-T signal).

### H1 Tags
- **Total pages:** 108 — all have exactly 1 H1 (0 missing, 0 multiple)
- **Length range:** 18–63 chars
- **Duplicates by pattern (acceptable for geo pages):**
  - "Panel Upgrade in {City}" — 16 instances (geo pages)
  - "EV Charger Installation in {City}" — 16 instances (geo pages)
  - "Electrician in {City}" — 15 instances (city pages)
- **All unique H1 content:** Yes — each H1 contains the specific city name
- **Quality:** H1s are descriptive, keyword-rich, and match search intent. Service page H1s clearly state the service and location.

### E-E-A-T Assessment
| Signal | Status | Details |
|--------|--------|---------|
| License number (C-10 #981578) | **Present** | Homepage topbar, meta descriptions, JSON-LD `hasCredential`, city page descriptions |
| EVITP cert (#4051604) | **Present** | Homepage topbar, OG description, JSON-LD, EV charger pages |
| Years of experience | **Present** | Schema `foundingDate: "2012"`, founder description "15+ years of experience" |
| Founder/author name | **Present** | Schema `founder.name: "Amy"`, blog bylines "By Amy, Licensed C-10 Electrician" |
| Blog author attribution | **29/33 posts** | 3 posts missing `author-bio`/`byline` + 3 posts missing `author-amy` images |
| Testimonials page | **Present** | `testimonials.html` with AggregateRating schema (4.9 stars, 87 reviews) |
| Before/after gallery | **Present** | `gallery.html` — 309 real project photos (103 MB total) |
| About page | **MISSING** | No `about.html` exists. No link to about/our-story anywhere |
| Google Business Profile | **Linked** | Schema `sameAs` includes Yelp, Google Maps, Facebook |
| Address verified | **Present** | 20628 Londelius St, Winnetka, CA 91306 (schema + topbar) |
| Schema coverage | **Strong** | Electrician (74), FAQPage (102/108), BreadcrumbList (108/108), BlogPosting (33), Service (on service pages) |

**E-E-A-T Gaps:**
1. **No about page** — critical for YMYL trust. Google's Quality Raters look for this.
2. **3 blog posts missing author attribution** — `how-to-choose-electrician-los-angeles.html`, `signs-you-need-electrical-panel-upgrade.html`, `smart-home-electrical-upgrades-la.html`
3. **3 blog posts missing author images** — same 3 posts above (stubs/redirects with no author-amy images)
4. **No team photos or credentials page** — would strengthen expertise signals

### Thin Content
- **Service pages:** All 15 service pages >1,000 words. Minimum: `same-day-electrical-repair.html` (1,020 words). Excellent.
- **City pages:** All 16 city pages >1,900 words. Minimum: `city-hollywood.html` (1,919 words). Excellent.
- **Geo pages:** All 32 geo pages >1,900 words. Minimum: `panel-upgrade-hollywood.html` (1,921 words). Excellent.
- **Blog posts under 300 words (3 — all redirect stubs):**
  - `blog/smart-home-electrical-upgrades-la.html` — 96 words ("This article has moved. Click here.")
  - `blog/how-to-choose-electrician-los-angeles.html` — 103 words (redirect stub)
  - `blog/signs-you-need-electrical-panel-upgrade.html` — 110 words (redirect stub)
- **Blog posts 300–500 words:** 0
- **All other blog posts:** >700 words. Longest: `blog/california-electrical-code-changes-2026.html` (1,981 words)

**Assessment:** The 3 redirect stubs are the only thin content. These should be either proper 301 redirects or contain actual content. They currently have minimal content + a "moved" message, which may confuse crawlers.

### Readability
**Analyzed:** `panel-upgrade.html`, `ev-charger-installation.html`, `whole-home-rewiring.html`

| Metric | Finding |
|--------|---------|
| Font | Source Serif 4, 17px, line-height 1.65 (excellent for readability) |
| Sentence length | Mostly 10–20 words. Some longer sentences in technical explanations (25–30 words) |
| Paragraph length | 1–3 sentences per paragraph. Good use of `<details>` for FAQ sections |
| Jargon usage | Technical terms like "NEMA 14-50", "200A", "knob-and-tube", "EVITP" appear. Most are explained in context or via FAQ |
| Flesch-Kincaid estimate | Grade 8–9 (appropriate for homeowner audience) |
| Technical terms explained | "Level 2 charging" explained, "panel amperage" contextualized, "EVITP" defined on EV pages |

**Readability strengths:**
- Short paragraphs, scannable headings
- FAQ sections answer common questions
- Phone number in every section CTA
- Badge indicators (Licensed C-10, EVITP, 15+ years)

**Readability gaps:**
- Some technical jargon in service descriptions could use inline definitions
- `whole-home-rewiring.html` mentions "aluminum wiring remediation" without plain-English explanation

### Internal Linking
| Page category | Avg internal links | Min links |
|---------------|-------------------|-----------|
| Geo service pages (32) | 6 | 6 |
| City pages (16) | 5 | 5 |
| Root service pages (15) | 4 | 4 |
| Blog posts (33) | 3 | 0 |
| Special pages (12) | 4 | 1 |

**Pages with fewest links (orphan risk):**
- `index.html` — 1 internal link (acceptable: homepage has nav + footer)
- `blog/how-to-choose-electrician-los-angeles.html` — 0 links (redirect stub)
- `blog/signs-you-need-electrical-panel-upgrade.html` — 0 links (redirect stub)
- `blog/smart-home-electrical-upgrades-la.html` — 0 links (redirect stub)

**Assessment:** Internal linking is solid. Geo pages link to parent service + city + other geo pages. Blog posts link to related services. The 3 redirect stubs have 0 internal links (they're essentially dead ends).

### Open Graph & Twitter Cards
| Coverage | Pages |
|----------|-------|
| OG:title | 108/108 (100%) |
| OG:description | 108/108 (100%) |
| OG:image | 108/108 (100%) |
| twitter:card | 108/108 (100%) |
| twitter:title | 108/108 (100%) |
| twitter:description | 108/108 (100%) |
| twitter:image | 105/108 (97%) |

**Issues found:**
- **3 blog posts missing `twitter:image`:** `how-to-choose-electrician-los-angeles.html`, `signs-you-need-electrical-panel-upgrade.html`, `smart-home-electrical-upgrades-la.html` (same redirect stubs)
- **3 blog posts using `property="twitter:*"` instead of `name="twitter:*"`:** Same 3 redirect stubs — Twitter tag attribute should be `name`, not `property`
- **Duplicate `og:image` count=3 on 105 pages:** These pages have OG:image repeated 3 times (OG + Twitter + duplicate). Not harmful but unnecessary.
- **3 blog posts with `OG:image=1` only:** Missing Twitter image tag entirely

---

## IMAGE SCORE: 78/100

### Image Inventory
| Category | Count | Notes |
|----------|-------|-------|
| Main images (`img/`) | 37 files | JPG + WebP + PNG |
| Gallery images (`img/gallery/`) | 1,236 files | 309 JPEG + 927 WebP + some 400w variants |
| **Total image files** | **1,273** | |

**Format distribution:**
- WebP: 927 gallery + ~15 main = ~942 files
- JPEG: 309 gallery + ~20 main = ~329 files
- PNG: ~2 files (minimal)

**Size analysis:**
| Image type | Avg JPEG | Avg WebP | Savings |
|------------|----------|----------|---------|
| Gallery (1200w) | 168 KB | 55 KB | 67% |
| Main service images | 85–134 KB | 77–109 KB | ~15–30% |
| Hero image | 95 KB (JPEG) | 80 KB (WebP) | 16% |

**Largest images:**
- `img/commercial-800w.jpg` — 134 KB
- `img/commercial.jpg` — 122 KB
- `img/lighting-800w.jpg` — 112 KB

**Gallery stats:**
- Total size: 103 MB
- Largest JPEG: 366 KB (`photo-20230215-03-1200w.jpg`)
- Largest WebP: 328 KB (same photo, WebP variant)

### Alt Text Coverage
- **Total `<img>` tags across site:** 93
- **Images with non-empty alt text:** 93/93 (100%)
- **Images with `alt=""` (empty):** 0
- **Assessment:** Perfect alt text coverage. All images have descriptive alt attributes.

### Lazy Loading
- **Images with `loading="lazy"`:** 70/93 (75%)
- **Images with `loading="eager"`:** 0/93 (0%)
- **Images with no loading attribute:** 23/93 (25%)

**Breakdown:**
- Blog author images (1 per post): 22 of 29 posts have `loading="lazy"` on author image. 7 posts have no loading attribute.
- 3 redirect stubs have 1 image each with no loading attribute.
- Hero images on service pages correctly have no `loading="lazy"` (above the fold).

**Assessment:** Lazy loading is well-implemented on main content images. The 23 images missing the attribute are author thumbnails and redirect stub images — low-impact but should be fixed for completeness.

### Image Dimensions
- **Images with `width=` attribute:** 200 instances across all pages (includes CSS pseudo-dimensions)
- **Images with `height=` attribute:** 92 instances
- **Assessment:** Width and height are specified on most `<img>` tags. This helps prevent CLS (Cumulative Layout Shift). The hero image on `index.html` uses `aspect-ratio: 4/3` in CSS as a CLS prevention measure.

### Hero Image Analysis
| Property | Value |
|----------|-------|
| File | `img/hero-electrician-*.webp` / `img/hero-electrician.jpg` |
| Format | WebP (primary) + JPEG fallback |
| Sizes | 400w (80 KB WebP), 800w (80 KB WebP), 1200w (95 KB JPEG) |
| Preloaded | **Yes** — `<link rel="preload" as="image">` with media queries for responsive variants |
| fetchpriority | **high** — correct for LCP element |
| Lazy loaded | **No** — correct (above the fold) |
| srcset | **Yes** — responsive variants via `<link rel="preload">` with `imagesrcset` |
| Sizes | **Yes** — responsive sizing via `imagesizes` |

**Assessment:** Hero image is perfectly optimized for LCP. Preloaded with responsive variants, correct fetch priority, no lazy loading. This is textbook implementation.

### Blog Author Images
- **Author images exist:** `img/author-amy-200w.jpg` (7.7 KB), `img/author-amy-200w.webp` (5.6 KB), `img/author-amy-400w.jpg` (28 KB), `img/author-amy-400w.webp` (21 KB)
- **Blog posts with author images:** 29/33 (88%)
- **Blog posts missing author images (4):**
  - `blog/how-to-choose-electrician-los-angeles.html` — redirect stub, no author section
  - `blog/index.html` — blog index, no author section
  - `blog/signs-you-need-electrical-panel-upgrade.html` — redirect stub
  - `blog/smart-home-electrical-upgrades-la.html` — redirect stub

**Assessment:** Author images are present on all substantive blog posts. The 4 missing are redirect stubs/blog index. Dimensions are specified (200w and 400w variants in both JPEG and WebP). Good practice.

### Responsive Images (srcset)
- **Pages with `srcset`:** 57/108 (53%)
- **Pages with `sizes`:** 54/108 (50%)
- **Gallery:** Uses `srcset` with 400w + 1200w variants per photo
- **Main service images:** Use `srcset` with 400w + 800w + 1200w variants
- **City pages:** Use `srcset` on the main image (1 per page)
- **Blog posts:** 23 posts have `srcset`, rest don't (blog images are author thumbnails only)

**Assessment:** Responsive image implementation is solid for the main content images. Gallery has proper srcset with 2 variants. Blog posts don't need srcset as they primarily have author thumbnails.

### Pages with No Images (52 pages)
- All 16 geo service pages: 0 images (content-only, template-driven)
- All 16 city pages: 0 images (same reason)
- 12 blog posts: 0 images (text-only posts)
- 8 special pages: 0 images (`breaker-tripping`, `burning-smell-panel`, `emergency-electrician`, `ev-charger-hardwired-vs-plug-in`, `power-outage-repair`, `same-day-electrical-repair`, `privacy-policy`, `testimonials`)

**Assessment:** Many pages rely on CSS styling rather than images. City/geo pages could benefit from at least 1 relevant image. Text-heavy service pages like `emergency-electrician.html` and `breaker-tripping.html` would benefit from illustrative images.

---

## PRIORITY ACTIONS

### Critical
1. **Create an About page** (`about.html`) — Missing entirely. YMYL trust signal. Should include founder story, credentials, license verification links, team photos, and company history. Link from nav and footer on all pages.

### High
2. **Fix 3 redirect blog stubs** — `blog/how-to-choose-electrician-los-angeles.html`, `blog/signs-you-need-electrical-panel-upgrade.html`, `blog/smart-home-electrical-upgrades-la.html` are thin (96–110 words), have 0 internal links, missing author images, missing twitter:image, and use wrong Twitter tag attributes. Either implement proper 301 redirects to the target pages or restore full content.
3. **Add `loading="lazy"` to 23 images** missing the attribute (mostly blog author thumbnails). Quick fix for completeness and CLS prevention.
4. **Fix Twitter tag attributes** on 3 blog posts — change `property="twitter:*"` to `name="twitter:*"`. Twitter cards may not render correctly with `property`.

### Medium
5. **Trim 2 meta descriptions over 160 chars** — `blog/smoke-co-detector-installation-la.html` (166 chars) and `panel-upgrade-burbank.html` (160 chars). They'll be truncated in SERPs.
6. **Add images to 52 text-only pages** — Especially high-value service pages (`emergency-electrician.html`, `breaker-tripping.html`, `burning-smell-panel.html`) and all 16 city pages. Even 1 relevant image improves engagement and image search visibility.
7. **Differentiate city page meta descriptions** — All 16 city page descriptions follow the same template with only the city name changed. Consider adding city-specific details (e.g., local landmarks, permits, LADWP zone) for differentiation.
8. **Add `blog/index.html` author attribution** — Blog index page should have author/byline for consistency.

### Low
9. **Trim 1 title tag over 70 chars** — `blog/california-electrical-code-changes-2026.html` (71 chars). Google may truncate it.
10. **Normalize OG:image count** — 105 pages have `og:image` repeated 3 times (OG + Twitter + duplicate). Not harmful but unnecessary code bloat.
11. **Consider adding `hreflang` tags** — Not required for a local business, but if expanding to bilingual content (Spanish), plan for it.
12. **Gallery image compression** — Largest JPEGs are 340–366 KB. Running through additional compression could save ~20% without quality loss.

---

## SUMMARY

| Category | Score | Key Finding |
|----------|-------|-------------|
| Title Tags | 95/100 | All present, 93% in ideal range, 0 duplicates |
| Meta Descriptions | 90/100 | All present, 90% in ideal range, 0 duplicates |
| H1 Tags | 95/100 | All present, 1 per page, unique content |
| E-E-A-T | 82/100 | Strong signals (license, certs, schema, reviews) but missing About page |
| Thin Content | 92/100 | Only 3 redirect stubs are thin. All substantive pages >700 words |
| Readability | 88/100 | Grade 8–9, good paragraph structure, some jargon undefined |
| Internal Linking | 85/100 | Solid structure. 3 dead-end redirect stubs |
| OG/Twitter | 90/100 | 100% OG coverage. 3 posts missing twitter:image + wrong attribute |
| Image Formats | 92/100 | WebP + JPEG dual format. Gallery 67% smaller in WebP |
| Alt Text | 100/100 | 93/93 images have descriptive alt text |
| Lazy Loading | 80/100 | 75% coverage. 23 images (author thumbs) missing attribute |
| Image Dimensions | 85/100 | Width/height on most images. Hero uses aspect-ratio CSS |
| Hero Image | 98/100 | Textbook LCP optimization: preload + fetchpriority + responsive |
| Blog Author Images | 88/100 | 29/33 posts have author images. 4 missing (stubs/index) |
| Responsive Images | 82/100 | srcset on 53% of pages (all main content images) |

**Overall Content Score: 86/100**
**Overall Image Score: 78/100**
