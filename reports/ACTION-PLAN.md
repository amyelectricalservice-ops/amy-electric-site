# SEO Action Plan — AMY Electric

**Priority Definitions**:
- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

---

## Critical (4 items)

### C1. Fix www.amyelectric.com 522 Error
**Problem**: www subdomain returns Cloudflare 522 (connection timeout). DNS CNAME record `www` → `amyelectric.com` is missing.
**Action**: Log into Cloudflare Dashboard → DNS → Add CNAME record: `www` → `amyelectric.com`, proxied (orange cloud).
**Impact**: Without this, all links pointing to www drop authority, and users may get errors.
**Effort**: 2 minutes (Dashboard). **Blocked on API: read-only token.**

### C2. Fix 3 Blog Posts Missing BlogPosting + BreadcrumbList Schema
**Files**:
- `blog/how-to-choose-electrician-los-angeles.html`
- `blog/signs-you-need-electrical-panel-upgrade.html`
- `blog/smart-home-electrical-upgrades-la.html`
**Action**: These are redirect stubs with `<meta http-equiv="refresh"> + <meta name="robots" content="noindex">`. They currently have only `WebPage` schema. Add `BlogPosting` schema and wrap in appropriate JSON-LD.
**Effort**: 15 minutes.

### C3. Fix Homepage FAQ Typo
**File**: `index.html:517`
**Problem**: Question text: `"Do you offer surge protection for my home?s"` — trailing `?s` instead of `?`
**Action**: Change `home?s` to `home?`
**Effort**: 30 seconds.

### C4. Re-encode Gallery WebP at Quality 80-85
**Problem**: Gallery WebP files are encoded at too-high quality (~95-100), averaging only 1-20% savings over JPEG. Some WebP files are 285 KB (vs 289 KB JPEG — only 1% savings).
**Action**: Run `scripts/process-photos.py` with `--quality 85` flag to re-encode all gallery WebP. Could save 3-4 MB total.
**Effort**: Run script (automated).

---

## High Priority (6 items)

### H1. Expand City Page FAQ from 3→5+ Questions
**Files**: All 16 `city-*.html`
**Action**: Add 2-4 more city-specific FAQ questions (e.g., permitting in that city, local utility requirements, common electrical issues in that area's housing stock).
**Impact**: Deepens FAQPage schema for rich results, improves local relevance.
**Effort**: 2-3 hours (script-assisted).

### H2. Add Facebook, Nextdoor, BBB to sameAs
**Files**: All pages with Electrician schema (105 files)
**Action**: Add `"https://www.facebook.com/...", "https://www.nextdoor.com/...", "https://www.bbb.org/.../amy-electric"` to `sameAs` arrays.
**Pre-req**: Claim/create these profiles first.
**Effort**: 1-2 hours for schema update + profile creation.

### H3. Fix Opening Hours Inconsistency
**Files**: All 16 `city-*.html`
**Action**: Add 24/7 emergency `openingHoursSpecification` (Mon-Sun 00:00-23:59) alongside current Saturday hours to match homepage. This ensures consistency in LocalBusiness schema.
**Effort**: 30 minutes (script-assisted).

### H4. Add FAQPage to testimonials.html
**File**: `testimonials.html`
**Action**: Add FAQPage JSON-LD with 3-4 questions about the review process, how to leave a review, etc.
**Effort**: 15 minutes.

### H5. Fix Duplicate Title: smoke-co-detector
**Files**: `smoke-co-detector-installation.html` and `blog/smoke-co-detector-installation-la.html`
**Action**: Differentiate the service page and blog post titles. Service: "Smoke & CO Detector Installation Los Angeles | AMY Electric". Blog: "Smoke and CO Detector Installation Guide for LA Homes | AMY Electric".
**Effort**: 5 minutes.

### H6. Add Electrician @id to Geo-Page Schemas
**Files**: All 32 geo pages + 5 emergency + privacy-policy.html (38 files)
**Action**: Add `@id` property (e.g., `"@id": "https://amyelectric.com/ev-charger-installation-los-angeles#electrician"`) to Electrician schema for entity linkage. Also add `hasCredential` with C-10 license.
**Effort**: 1 hour (script-assisted).

---

## Medium Priority (5 items)

### M1. Add 1200w/1600w Hero Image Variants
**Files**: Index.html hero `<picture>` + all pages with hero images
**Action**: Add 1200w and 1600w WebP/JPEG sources with corresponding `media` queries for retina displays and large screens.
**Effort**: 2-3 hours (photo processing + HTML updates).

### M2. Expand Geo-Service Page City-Specific Content
**Files**: All 32 `ev-charger-installation-{city}.html` and `panel-upgrade-{city}.html`
**Action**: Add 1-2 unique paragraphs per page about that city's specific electrical landscape (e.g., "In Burbank, many homes from the 1950s still have original 60A panels...").
**Effort**: 4-6 hours (significant content work).

### M3. Add HowTo Schema to Remaining 11 Service Pages
**Files**: 11 service pages without HowTo (ceiling-fan, commercial, dedicated-circuits, electrical-repair, electrical-safety, lighting, outlet-switch, smart-home, smoke-co, surge-protection, tesla-charger)
**Action**: Add HowTo schema with 4-6 steps to each page.
**Effort**: 3-4 hours.

### M4. Add AVIF Sources in Hero `<picture>` Elements
**Files**: All pages with hero images (~56 pages)
**Action**: Add `<source type="image/avif">` before WebP sources for ~30% additional compression savings.
**Effort**: 2 hours (script-assisted).

### M5. Remove datePublished/dateModified from Service Schema
**Files**: 15 root service pages
**Action**: These properties are not valid for `@type: Service`. Remove them from Service JSON-LD blocks. They belong on `WebPage` schema instead.
**Effort**: 30 minutes (script-assisted).

---

## Low Priority (4 items)

### L1. Fix Breadcrumb Text Formatting
**Files**: `blog/ev-charger-installation-cost-la.html`, `blog/panel-upgrade-cost-los-angeles.html`, `blog/emergency-electrician-los-angeles.html`
**Action**: Fix missing spaces in BreadcrumbList `name` fields.
**Effort**: 5 minutes.

### L2. Add WebSite Schema to All City Pages
**Files**: All 16 city pages
**Action**: Mirror the homepage's `WebSite + SearchAction` schema on city pages for site-wide search capability in rich results.
**Effort**: 30 minutes (script-assisted).

### L3. Expand Schema Breadcrumbs on Blog Posts to 3-Level
**Files**: All 33 blog posts
**Action**: Add intermediate "Blog" category in BreadcrumbList (Home > Blog > Post Title) instead of 2-level (Home > Post Title).
**Effort**: 1 hour (script-assisted).

### L4. Convert Gallery to Programmatic srcset
**Files**: `gallery.html`
**Action**: Use `srcset` and `sizes` attributes on gallery images to serve 400w thumbnails on mobile and 1200w on desktop, instead of manual file-per-page selection.
**Effort**: 2 hours.

---

## Implementation Roadmap

### Week 1 (Critical + High Priority)
| Day | Tasks |
|-----|-------|
| Day 1 | [Dashboard] Fix www CNAME record, [Edit] Fix FAQ typo |
| Day 2 | [Script] Fix 3 blog post schema stubs, Fix duplicate title |
| Day 3 | [Script] Add FAQ to testimonials, Fix opening hours |
| Day 4 | [Script] Add @id to 38 geo/emergency schemas |
| Day 5 | [Script] Re-encode gallery WebP at q80 |
| Day 6 | Expand city FAQ from 3→5 Qs (start) |
| Day 7 | Complete city FAQ expansion |

### Week 2 (Medium Priority)
| Day | Tasks |
|-----|-------|
| Day 1-2 | Add 1200w/1600w hero variants |
| Day 3-4 | Add HowTo schema to 11 service pages |
| Day 5 | Add AVIF sources, Remove invalid Schema.org props |
| Day 6-7 | Start geo-service page content expansion |

### Week 3+ (Low Priority + Ongoing)
| Task | Timeline |
|------|----------|
| Fix breadcrumb formatting | Week 3 |
| Add WebSite schema to city pages | Week 3 |
| Expand blog breadcrumbs to 3-level | Week 3 |
| Programmatic srcset for gallery | Week 4 |
| Build citation profiles (Facebook, Nextdoor, BBB) | Week 3-4 |
| 150+ review campaign | Ongoing |

---

## Effort Summary

| Priority | Items | Estimated Total Effort |
|---|---|---|
| Critical | 4 | 20 minutes + 1 script run + Dashboard action |
| High | 6 | 4-6 hours (mostly script-assisted) |
| Medium | 5 | 12-16 hours (significant content work) |
| Low | 4 | 4-5 hours |
| **Total** | **19** | **20-27 hours** |
