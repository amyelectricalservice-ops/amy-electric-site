# GEO & AI Readiness Analysis — amyelectric.com

**Date**: 2026-06-10
**URL**: https://amyelectric.com/
**Overall GEO Readiness Score**: **92/100**

---

## 1. AI Crawler Access Status — ✅ PASS (Critical)

| Crawler | Status | Details |
|---------|--------|---------|
| **GPTBot** (OpenAI) | ✅ Allowed | `User-agent: GPTBot` → `Allow: /` |
| **OAI-SearchBot** (OpenAI) | ✅ Allowed | `User-agent: OAI-SearchBot` → `Allow: /` |
| **ChatGPT-User** (OpenAI) | ✅ Allowed | `User-agent: ChatGPT-User` → `Allow: /` |
| **ClaudeBot** (Anthropic) | ✅ Allowed | `User-agent: ClaudeBot` → `Allow: /` |
| **PerplexityBot** (Perplexity) | ✅ Allowed | `User-agent: PerplexityBot` → `Allow: /` |
| **anthropic-ai** (Anthropic training) | ✅ Allowed | `User-agent: anthropic-ai` → `Allow: /` |
| **Google-Extended** (Google AI) | ✅ Allowed | `User-agent: Google-Extended` → `Allow: /` |
| **Applebot-Extended** (Apple AI) | ✅ Allowed | `User-agent: Applebot-Extended` → `Allow: /` |
| **CCBot** (Common Crawl training) | 🚫 Blocked | `Disallow: /` |
| **Bytespider** (ByteDance training) | 🚫 Blocked | `Disallow: /` |
| **cohere-ai** (Cohere training) | 🚫 Blocked | `Disallow: /` |

**Severity**: ✅ None — All 8 AI search crawlers are explicitly allowed. Training crawlers are appropriately blocked. RSL reference and sitemap link are present.

---

## 2. llms.txt — ✅ PASS (Important)

**URL**: https://amyelectric.com/llms.txt
**Status**: ✅ Exists and properly formatted

| Criteria | Result |
|----------|--------|
| H1 title | ✅ `# AMY Electric — Los Angeles Licensed Electrician` |
| Description blockquote | ✅ `> AMY Electric is a licensed C-10 electrical contractor (#981578)...` |
| Key Facts section | ✅ License #, EVITP #, years in business, reviews, address, phone, email, hours |
| Services section | ✅ 10 service links with descriptions and price ranges (`$350–$900`, `$2,500–$4,500`) |
| Service Areas section | ✅ All 16 cities listed |
| Suggestions (People Also Ask) | ✅ 8 question-based suggestions |
| Privacy policy link | ✅ Present |
| RSL link | ✅ Present |
| Contact info | ✅ Phone, email, address, hours all present |

**Recommendation**: Consider adding last-modified date metadata at the top of the file.

---

## 3. llms-full.txt — ⚠️ WARNING (Optional)

**URL**: https://amyelectric.com/llms-full.txt
**Status**: ❌ 404 — Does not exist

**Severity**: Low. llms.txt is present and thorough. This is an optional supplementary file for sites with very deep content. Not a priority.

---

## 4. RSL (Robots Search License) — ✅ PASS (Important)

**URL**: https://amyelectric.com/rsl.json
**Status**: ✅ Exists and valid JSON

| Field | Value |
|-------|-------|
| `@context` | `https://rsl.xyz/context` |
| `@type` | `RobotsSearchLicense` |
| `license` | `https://rsl.xyz/licenses/1.0/` |
| `crawler` | `*` (all) |
| `permission` | `search-and-summarize` |
| `attribution` | `true` |
| `modified` | `2026-06-08` |

**Severity**: ✅ None — Fully compliant with RSL 1.0 standard. Allows search-and-summarize with attribution.

---

## 5. Passage-Level Citability — ✅ GOOD (Important)

### Homepage

| Criteria | Result | Details |
|----------|--------|---------|
| Question-based H2 headings | ✅ | "What Electrical Services Do We Offer in Los Angeles?", "Why Do Los Angeles Homeowners Choose AMY Electric?", "What Electrical Guides Should LA Homeowners Read?" |
| Definition block (134-167 words ideal) | ⚠️ | Hero description is ~80 words — slightly below optimal range for AI citation extraction |
| Bullet-pointed facts/stats | ✅ | Trust bar (6 items), badges (3 items), service grid, why-choose-us numbered list |
| FAQ section | ✅ | 5 Q&A pairs using `<details>` + FAQPage schema |

### EV Charger Installation Page

| Criteria | Result | Details |
|----------|--------|---------|
| Question-based H2 | ✅ | "What Is Level 2 EV Charger Installation?", "How Does the EV Charger Installation Process Work?", "What Rebates and Incentives Are Available for EV Charger Installation in LA?" |
| Definition block | ✅ | ~150 words — within optimal 134-167 word range for AI citation |
| Process list | ✅ | Numbered 4-step process with clear sub-headings |
| Pricing table | ✅ | Structured price table ($350-$550, $450-$750, $500-$900, +$2,500-$4,500) |
| FAQ | ✅ | 5 Q&A pairs |

### Panel Upgrade Page

| Criteria | Result | Details |
|----------|--------|---------|
| Question-based H2 | ✅ | "What Is a Electrical Panel Upgrade?", "What Are the Signs You Need a Panel Upgrade?", "How Does the Panel Upgrade Process Work in LA?" |
| Definition block | ✅ | ~120 words — good, could expand slightly toward 134-167 |
| Symptom checklist | ✅ | 7-item bulleted list of panel failure signs |
| Process | ✅ | Numbered 5-step process |
| Pricing table | ✅ | $2,500-$4,500 range with breakdown |

**Recommendations**:
- Expand the homepage hero description by 40-60 words to hit the 134-167 optimal citation range
- Add a short definition paragraph under "Why Do Los Angeles Homeowners Choose AMY Electric?" for AI to cite
- Add "What Is..." definition blocks to the remaining service pages that don't have one (repairs, commercial, lighting)

---

## 6. Open Graph / Twitter Cards — ✅ PASS (Important)

| Tag | Value | Status |
|-----|-------|--------|
| `og:title` | "Electrician Los Angeles \| Panel Upgrades, EV Chargers & Repairs \| AMY Electric" | ✅ |
| `og:description` | "Licensed LA electricians. Panel upgrades, EV chargers, repairs. C-10 #981578 · EVITP #4051604." | ✅ |
| `og:url` | `https://amyelectric.com/` | ✅ |
| `og:type` | `website` | ✅ |
| `og:image` | `https://amyelectric.com/img/og-home.jpg` | ✅ |
| `og:site_name` | `AMY Electric` | ✅ |
| `twitter:card` | `summary_large_image` | ✅ |
| `twitter:title` | "Electrician Los Angeles \| Panel Upgrades, EV Chargers & Repairs \| AMY Electric" | ✅ |
| `twitter:description` | "Licensed LA electricians. Panel upgrades, EV chargers, repairs. C-10 #981578 · EVITP #4051604." | ✅ |
| `twitter:image` | `https://amyelectric.com/img/og-home.jpg` | ✅ |

**Severity**: ✅ None — All OG and Twitter Card tags are present and correctly configured.

---

## 7. Brand Mentions — ✅ STRONG (Moderate)

"AMY Electric" appears consistently:

| Location | Mentions |
|----------|----------|
| Page title | `Licensed Electrician in Los Angeles, CA | AMY Electric` |
| Logo | "AMY Electric" in header + footer |
| Hero H1 | "AMY Electric is a trusted Los Angeles electrical contractor..." |
| Trust bar | Implicit (brand-adjacent) |
| Why Choose Us | "Why Do Los Angeles Homeowners Choose AMY Electric?" |
| Testimonials | "AMY Electric installed our Tesla Wall Connector..." |
| Footer | "AMY Electric" + address + license |
| OG title | "Electrician Los Angeles | ... | AMY Electric" |
| Schema `@id` | `https://amyelectric.com` |
| URL structure | `amyelectric.com` domain |

**Severity**: ✅ None — Strong, consistent brand presence across all channels. Brand name appears in title, headings, body text, schema, and social cards.

---

## 8. Schema Markup — ✅ EXCELLENT (Important)

Schemas detected on homepage:

| Schema Type | Status | Details |
|-------------|--------|---------|
| **Electrician** (LocalBusiness) | ✅ | Full markup: name, address, geo, phone, hours, rating (4.9/87), 14 services, 17 areaServed cities, 2 credentials, 3 reviews, sameAs |
| **Organization** | ✅ | name, url, logo, contactPoint, sameAs |
| **Person** (founder) | ✅ | name, description, image, knowsAbout (4 topics) |
| **WebSite** | ✅ | url, searchAction |
| **FAQPage** | ✅ | 4 question/answer pairs |
| **BreadcrumbList** | ✅ | Home position |

Schemas detected across other pages:
- **FAQPage**: On 14+ service pages
- **BreadcrumbList**: On all service/city pages
- **Service** (subtypes): EVChargerInstallation, ElectricalPanelUpgrade on geo- targeted pages
- **BlogPosting**: On 31 blog pages (confirmed via grep)

**Severity**: ✅ None — Rich, comprehensive schema coverage with proper `@id` references, sameAs, and credential identifiers.

---

## 9. GEO Readiness Summary

### Score Breakdown

| Factor | Weight | Score | Notes |
|--------|--------|-------|-------|
| AI Crawler Access | 15% | 15/15 | All 8 AI crawlers allowed, training crawlers blocked |
| llms.txt + RSL | 15% | 15/15 | Both present, well-formed, RSL 1.0 compliant |
| Passage-Level Citability | 25% | 21/25 | Good definition blocks and Q&A H2s; hero block slightly short |
| Open Graph / Social | 10% | 10/10 | All required OG and Twitter tags present |
| Brand Consistency | 10% | 10/10 | Strong brand presence everywhere |
| Schema Markup | 15% | 15/15 | Comprehensive structure data coverage |
| Technical Accessibility | 10% | 6/10 | No llms-full.txt; no publication dates visible on homepage content |

**Total**: 92/100 — Excellent GEO readiness

### Top 5 Highest-Impact Improvements

1. **Expand homepage hero description** to 134-167 words for optimal AI citation length
2. **Add publication/updated dates** to content sections (blog posts and service pages)
3. **Add "What Is..." definition blocks** to the remaining service pages (repairs, commercial, lighting) that currently lack them
4. **Add sameAs links to Person schema** (LinkedIn, Wikipedia if applicable) to strengthen authority signals
5. **Create llms-full.txt** with full page content for comprehensive AI crawler access (optional, low priority)

### Quick Wins

- Add `<meta name="dateModified" content="2026-06-10">` to service pages
- Add a brief "What Is Commercial Electrical Work?" section to the commercial page
- Add LinkedIn URL to Person schema for founder authority signal
- Add publication date to blog posts in both visible content and BlogPosting schema
