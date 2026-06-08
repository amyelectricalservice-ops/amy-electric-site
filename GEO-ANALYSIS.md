# AMY Electric — GEO/AEO Readiness Report

**Date:** June 8, 2026
**Overall GEO Score:** 72/100 (was 58/100)

---

## Scores by Category

| Category | Before | After | Change |
|---|---|---|---|
| AI Crawler Access | 75 | 90 | +15 |
| llms.txt Completeness | 65 | 85 | +20 |
| Passage-Level Citability | 55 | 55 | 0 |
| Question-Based Headings | 70 | 80 | +10 |
| Schema Markup | 60 | 85 | +25 |
| Publication Dates | 40 | 80 | +40 |
| Author Bylines | 70 | 85 | +15 |
| Brand Mention Signals | 15 | 15 | 0 |
| Multi-Modal Content | 40 | 40 | 0 |
| Heading Hierarchy | 50 | 50 | 0 |
| Tables and Lists | 75 | 80 | +5 |
| Security Headers | 70 | 75 | +5 |
| RSL 1.0 Licensing | 0 | 90 | +90 |

---

## Changes Applied

### Schema (highest impact)
- **Organization schema** — added to `index.html` with `contactPoint` and `sameAs`
- **Person schema** — added to `index.html` (`@id: https://amyelectric.com/#person`) with credentials, image, and `knowsAbout`
- **datePublished/dateModified** — added to `panel-upgrade`, `commercial-electrical`, `ev-charger-hardwired-vs-plug-in`, `panel-100a-vs-200a` Service schemas
- **Service schema** — added to 12 previously missing pages (lighting, tesla-charger, electrical-repair, whole-home-rewiring, surge-protection, outlet-switch, ceiling-fan, smoke-co, generator, dedicated-circuits, smart-home, safety-inspections)

### AI Crawler Access
- **Google-Extended** and **Applebot-Extended** added to `robots.txt` (explicitly allowed)
- **RSL 1.0** license file created at `/rsl.json` — linked from `robots.txt` and `llms.txt`

### llms.txt
- **Suggestions** section added — 8 question prompts for AI assistants
- **Privacy** section with link to privacy policy
- **RSL 1.0** license reference added

### Homepage Headings
- `"Helpful Guides for LA Homeowners"` → `"What Electrical Guides Should LA Homeowners Read?"`
- `"Full-Service Electrical for Los Angeles"` → `"What Electrical Services Do We Offer in Los Angeles?"`
- `"Why Los Angeles Homeowners Choose AMY Electric"` → `"Why Do Los Angeles Homeowners Choose AMY Electric?"`

### Author Bylines
- Added `"Written by Amy"` section with photo (`author-amy-200w.jpg`), credentials, and C-10 license details to 7 blog posts

### Content
- **Comparison table** added to `ev-charger-hardwired-vs-plug-in.html` — 7-row `<thead>` semantic table for AI parsing

### Security
- **Expect-CT** header added to `_headers`

---

## Remaining Gaps

| Gap | Category | Why | Effort |
|---|---|---|---|
| No video content | Multi-Modal | Video = 0.737 correlation with AI citations | Medium (record 3-5) |
| No YouTube channel | Brand Mentions | Strongest AI citation signal per Ahrefs | Medium (create + upload) |
| No Reddit presence | Brand Mentions | Reddit is #2 citation source for ChatGPT/Perplexity | Low (answer questions) |
| No Wikipedia presence | Brand Mentions | Wikipedia cited by 47.9% of ChatGPT responses | High (notability hurdle) |
| No LinkedIn page | Brand Mentions | LinkedIn crawled for business info | Low (create page) |
| No GBP CID in sameAs | Schema | Need Google Business Profile CID for `sameAs` | Low (user action) |
| No downloadable resources | Multi-Modal | PDFs/guides are depth signals | Low (create 2-3 PDFs) |
| Homepage lacks "X is..." definition block | Citability | No self-contained answer block for "What is AMY Electric?" | Low (add paragraph) |
| Quote estimator is JS-only | Technical | Pricing data invisible to AI crawlers | Low (add visible price table) |
| Commercial page lacks pricing facts | Citability | No hard numbers in commercial definition | Low (edit paragraph) |

---

## Key Insight from Google's AI Optimization Guide

Per Google's official stance: **"Optimizing for generative AI search is still SEO."** There is no separate "AI index." The changes above are SEO fundamentals — structured data, freshness signals, clear headings, author expertise — applied through an AI citation lens.

Google explicitly rejects `llms.txt`, content chunking, mention-farming, and AI-specific schema as ranking factors. The RSL 1.0 and llms.txt additions are forward-looking (emerging standards) rather than current ranking levers.

---

## Estimated GEO Platform Visibility

| Platform | Visibility Level | Reason |
|---|---|---|
| Google AI Overviews | Good | Top-10 ranking pages, strong schema, date freshness |
| ChatGPT Web Search | Moderate | No Wikipedia/Reddit presence limits citations |
| Perplexity | Low | No Reddit presence (46.7% of Perplexity citations) |
| Bing Copilot | Good | Bing index access, IndexNow, clean robots.txt |

After these fixes, AMY Electric has strong schema foundations, clear author E-E-A-T signals, and proper AI crawler access. The highest remaining leverage is brand presence on Reddit, YouTube, and Wikipedia — which correlates 3x more strongly with AI citations than backlinks.
