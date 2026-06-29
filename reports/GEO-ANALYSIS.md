# GEO Analysis: amyelectric.com

**Date**: 2026-06-29
**URL**: https://amyelectric.com
**Business**: AMY Electric — Licensed C-10 electrical contractor, Los Angeles

---

## GEO Readiness Score: 76/100

| Category | Score | Weight |
|----------|-------|--------|
| Technical Accessibility | 18/20 | 20% |
| Citability | 16/25 | 25% |
| Structural Readability | 18/20 | 20% |
| Authority & Brand Signals | 14/20 | 20% |
| Multi-Modal Content | 10/15 | 15% |

---

## 1. AI Crawler Access Status: 18/20

**Excellent** — explicitly allows 8 AI crawlers, blocks 3 training crawlers.

| Crawler | Status | Purpose |
|---------|--------|---------|
| GPTBot | ✅ Allowed | ChatGPT web search |
| OAI-SearchBot | ✅ Allowed | OpenAI search features |
| ChatGPT-User | ✅ Allowed | ChatGPT browsing |
| ClaudeBot | ✅ Allowed | Claude web features |
| PerplexityBot | ✅ Allowed | Perplexity AI search |
| anthropic-ai | ✅ Allowed | Claude training |
| Google-Extended | ✅ Allowed | Gemini AI training |
| Applebot-Extended | ✅ Allowed | Apple Intelligence |
| CCBot | ❌ Blocked | Common Crawl training |
| Bytespider | ❌ Blocked | ByteDance training |
| cohere-ai | ❌ Blocked | Cohere training |

**Gap**: Missing `Meta-ExternalAgent` and `Meta-ExternalFetcher` (Meta AI crawlers added March 2026). Add:
```
User-agent: Meta-ExternalAgent
Allow: /

User-agent: Meta-ExternalFetcher
Allow: /
```

---

## 2. llms.txt Status: ✅ Present (Excellent)

**File**: `/llms.txt` — HTTP 200, well-structured, comprehensive.

**Coverage**:
- ✅ Title + description
- ✅ Key facts (license #s, phone, email, address, years in business, rating)
- ✅ All services listed with descriptions, price ranges, and internal links
- ✅ All 16 service areas listed
- ✅ About section (testimonials, gallery, blog links)
- ✅ Suggestions section (8 common questions)
- ✅ Privacy policy link
- ✅ RSL 1.0 license link

**Also**: Page includes `<link rel="alternate" type="text/markdown" href="/llms.txt">` in `<head>` — strong signal.

**RSL 1.0**: ✅ Present at `/rsl.json` — `search-and-summarize` permission, attribution required. One of few sites with full implementation.

---

## 3. Brand Mention Analysis: 14/20

| Platform | Presence | Impact |
|----------|----------|--------|
| **Wikipedia** | ❌ No page | Not expected for local contractor |
| **Reddit** | ❌ No mentions | High-impact gap (47% of ChatGPT citations, 67% of Perplexity citations come from Reddit) |
| **YouTube** | ❌ No channel | High-impact gap (correlates 0.737 with AI citations — strongest signal) |
| **LinkedIn** | ❌ No business page | Moderate-impact gap |
| **Facebook** | ✅ Active page (85 likes) | Weak signal |
| **Yelp** | ✅ Active listing | Weak signal for AI |
| **CALeVIP** | ✅ Listed as EV installer | Strong niche signal |
| **BuildZoom** | ✅ Score 99 (top 15%) | Moderate signal |
| **LocalFox AI Tracker** | ✅ ChatGPT cites AMY Electric 4x (#5 in LA) | Strong signal |

**Critical insight**: YouTube mentions have the **strongest correlation** with AI citations (0.737). Reddit is the #1 citation source for Perplexity (46.7%) and #2 for ChatGPT (11.3%). Both are absent.

### Real AI Visibility (LocalFox, June 2026)

| AI Platform | AMY Electric Rank |
|-------------|-------------------|
| **ChatGPT** | #5 (cited 4x across 6 queries) |
| **Perplexity** | Not cited |

---

## 4. Passage-Level Citability: 16/25

### Homepage

| Section | Words | Citability | Notes |
|---------|-------|-----------|-------|
| Hero description | 134 | ⭐⭐⭐ | Within optimal range (134-167). Contains: license #, founding year, service area list, services summary. Good quotable intro. |
| FAQ Q4 (EV cost) | 39 | ⭐⭐⭐⭐ | "Most Level 2 EV charger installations run $350–$900" — self-contained, specific data point |
| FAQ Q5 (service area) | 37 | ⭐⭐⭐ | Clear enumeration of 16 cities |
| FAQ Q6 (panel upgrade cost) | 37 | ⭐⭐⭐⭐ | "$2,500–$4,500" with specific factors |
| FAQ Q8 (charger sizing) | 49 | ⭐⭐⭐⭐ | "40A charger delivers about 30 miles of range per hour" — specific technical data |
| FAQ Q10 (hardwired vs plug-in) | 44 | ⭐⭐⭐⭐ | Clear comparison, technical specs |
| Why Choose Us points | 30-40 each | ⭐⭐⭐ | Good but no specific data points |
| Testimonials | 20-30 each | ⭐⭐⭐ | Real customer quotes with city attribution |

### Service Pages (e.g., EV Charger Installation)

| Section | Words | Citability | Notes |
|---------|-------|-----------|-------|
| HowTo steps | 40-60 each | ⭐⭐⭐⭐ | Step-by-step with specific details |
| FAQ answers | 30-50 each | ⭐⭐⭐⭐ | Price ranges, technical specs, permit details |
| Pricing section | varies | ⭐⭐⭐⭐⭐ | Specific dollar amounts |

### Blog Posts

| Citability Issue | Severity |
|------------------|----------|
| First passage contains nav/site chrome text (not clean content) | Medium |
| No "What is..." definition in first 40-60 words | Medium |
| Blog posts have author byline + date + FAQ sections | Good |

**Gaps**:
- Optimal 134-167 word self-contained answer blocks are rare (hero description is the only one)
- Blog posts start with nav chrome text before reaching content
- No "X is..." or "X refers to..." structured definitions
- No unique data points that aren't available on competitors' sites (pricing, timeframes)

---

## 5. Structural Readability: 18/20

| Criteria | Status |
|----------|--------|
| Semantic heading hierarchy (H1→H2→H3) | ✅ Excellent |
| Question-based H2 headings | ✅ "What Electrical Services Do We Offer?", "Why Do LA Homeowners Choose AMY Electric?" |
| Short paragraphs (2-4 sentences) | ✅ |
| Tables for comparative data | 🔶 Present on comparison pages only |
| Ordered/unordered lists | ✅ Service grid, Why Choose list, FAQ details |
| FAQ sections with clear Q&A | ✅ 15 Q&As on homepage, 7 on each service/city page |
| Breadcrumb navigation | ✅ On every page |
| Price ranges in headings | ✅ |

---

## 6. Multi-Modal Content: 10/15

| Asset | Status |
|-------|--------|
| Hero image (homepage) | ✅ WebP + JPG, lazy/eager loading |
| Service images | ✅ Limited (hero images per page) |
| Gallery (30+ project photos) | ✅ 309 photos with captions |
| Video content | ❌ None |
| Infographics/charts | ❌ None |
| Interactive calculators | ❌ None |
| Before/after comparisons | ❌ None published (79 identified in raw photos) |

---

## 7. Technical Accessibility: 20/20

| Criteria | Status |
|----------|--------|
| Server-side rendering | ✅ All content HTML-rendered (static site) |
| JavaScript dependency for content | ❌ Not required — analytics only |
| robots.txt | ✅ Properly configured |
| Canonical URLs | ✅ On every page |
| Sitemap | ✅ 105 URLs, 309 images |
| Preload hints | ✅ Fonts, hero image |
| OG/Twitter cards | ✅ On every page |

---

## 8. Schema for AI Discoverability: ⭐⭐⭐⭐⭐

Excellent schema coverage across the site:

| Schema Type | Pages | AI Citation Value |
|-------------|-------|-------------------|
| **Electrician** (LocalBusiness) | Homepage + 16 city pages | High — directly tells AI: business type, location, services, hours, payment, reviews |
| **OfferCatalog** (14 services) | Homepage | High — itemizes every service |
| **FAQPage** | All pages (15 on homepage, 7 on each service/city) | High — natural answer format |
| **HowTo** | 4 service pages | High — step-by-step processes |
| **BlogPosting** | 31 blog posts | High — article understanding |
| **BreadcrumbList** | All pages | Medium — context |
| **SpeakableSpecification** | Homepage | High — tells AI which content to read aloud/cite |
| **AggregateRating** (4.9/87) | Homepage | High — social proof |
| **hasCredential** (C-10 + EVITP) | Homepage | High — authority signal |
| **WebSite + SearchAction** | Homepage | Medium |
| **Person** (founder) | Homepage | Medium — author authority |
| **Organization** | Homepage | Medium |

---

## 9. Platform-Specific AI Visibility

### Google AI Overviews
- **Likely visibility**: Moderate. Strong technical SEO, schema, and FAQ content. 92% of citations come from top-10 pages — but the site's domain lacks backlink authority.
- **Risk factor**: Backlink profile and domain authority are weak (buildzoom score is only third-party signal).

### ChatGPT Web Search
- **Reported visibility**: Cited 4x across 6 queries (#5 in LA) per LocalFox (June 2026). Stronger than Perplexity.
- **Likely feed**: Wikipedia (47.9%), Reddit (11.3%) — neither mentions AMY Electric.

### Perplexity
- **Reported visibility**: Not cited per LocalFox. 46.7% of Perplexity citations come from Reddit — zero Reddit presence explains this gap.

---

## 10. Top 5 Highest-Impact Changes

### 🔴 HIGH PRIORITY

**1. Create a YouTube channel with 5-10 project videos**
- YouTube mentions correlate **0.737** with AI citations (strongest signal by 3x)
- Film: EV charger install timelapse, panel upgrade walkthrough, before/after rewiring
- Cost: $0 equipment (phone camera) + 2-3 hours filming
- Impact: Directly feeds ChatGPT, Google AIO, and Perplexity citations

**2. Get listed on Reddit (r/LosAngeles, r/AskLosAngeles)**
- Reddit is #1 Perplexity citation source (46.7%) and #2 for ChatGPT (11.3%)
- Tactics:
  - Monitor r/LosAngeles for "electrician recommendation" threads
  - Ask satisfied customers to mention "AMY Electric" in relevant threads
  - Do NOT self-promote — Reddit bans it. Focus on getting organic mentions.
- Impact: Fill the single biggest AI citation gap

**3. Create Wikipedia-style entity page (or Wikidata entry)**
- Wikipedia is cited by ChatGPT in 47.9% of responses
- AMY Electric is unlikely to get a Wikipedia article (not enough third-party coverage), but a **Wikidata entry** is achievable
- Add founder "Amram Edry" to Wikidata with C-10 license credential
- Impact: Feeds the Wikipedia citation slot for ChatGPT

### 🟡 MEDIUM PRIORITY

**4. Add original data points and statistics to service pages**
- Create unique content AI can cite: "We've installed 200+ EV chargers in LA — average install time is 3.2 hours"
- Survey customer data for original statistics
- Publish as blog posts with author attribution
- Impact: Differentiates from competitors' content, gives AI something unique to cite

### 🟢 LOW PRIORITY

**5. Add infographics and before/after image sets**
- Multi-modal content sees 156% higher AI selection rates
- 79 before/after photos already identified in raw photo cache — publish them
- Create simple infographics (panel upgrade comparison, cost breakdown chart)
- Impact: Increases selection rate when AI surfaces content

---

## Quick Wins (This Week)

1. ✅ **Already done**: AI crawlers allowed, llms.txt present, RSL 1.0, SpeakableSpecification, rich schema
2. 🟡 Add `Meta-ExternalAgent` and `Meta-ExternalFetcher` to robots.txt
3. 🟡 Create a YouTube channel and upload 1 video (EV charger install timelapse)
4. 🟡 Add founder "Amram Edry" to Wikidata
5. 🟡 Add "What is [topic]?" definition paragraph to top of each service page (first 40-60 words)
6. 🟡 Publish 3 before/after photo sets from `_candidates/before-after/`

---

## Schema Recommendations

| Schema | Pages | Priority | Why |
|--------|-------|----------|-----|
| ✅ Electrician (with credentials) | Homepage, city pages | Done | Tells AI: licensed, insured, certified |
| ✅ FAQPage | All pages | Done | Natural citation format |
| ✅ HowTo | Service pages | Done | Step-by-step extractable |
| ✅ BlogPosting | Blog | Done | Article understanding |
| ✅ SpeakableSpecification | Homepage | Done | AI voice/citation hints |
| 🔶 VideoObject | New YouTube content | Medium | Ties video to pages |
| 🔶 Product (for EV chargers) | Service page | Low | Not a product business |

---

## Content Reformatting Suggestions

### Homepage Hero Paragraph
**Current** (134 words — good length, but dense):
```
AMY Electric is a trusted Los Angeles electrical contractor built on safety,
code-compliance, and craftsmanship. Since 2012, we have been serving...
```

**Suggestion**: Restructure into a "Who, How, Why" format for easier AI extraction:
```
What is AMY Electric? AMY Electric is a Los Angeles electrical contractor
specializing in EV charger installation, panel upgrades, and commercial
electrical work. Founded in 2012, we hold a California C-10 license
(#981578) and EVITP certification (#4051604).

We serve homeowners, property managers, and businesses across 16 cities
in Greater Los Angeles. Every project is permitted, inspected, and backed
by full liability insurance. Our electricians are direct-dispatch — you
talk to the person doing the work.
```

### Blog Posts
**Issue**: First 60 words contain nav chrome text before content.

**Fix**: Add a one-sentence "What is this article about?" introductory paragraph in the `<main>` content area, before any navigation:

```html
<p class="article-intro">This guide explains [topic] for Los Angeles homeowners,
covering costs, permitting, timelines, and what to expect from a professional
installation.</p>
```

---

## Summary

| Metric | Score |
|--------|-------|
| **GEO Readiness** | **76/100** |
| AI Crawlers Allowed | 8 of 10 major |
| llms.txt | ✅ Complete |
| RSL 1.0 | ✅ Present |
| Schema Coverage | Excellent (8+ types) |
| SSG (static) | ✅ All content JS-free |
| Brand: YouTube | ❌ Missing |
| Brand: Reddit | ❌ Missing |
| Brand: Wikipedia/Wikidata | ❌ Missing |
| ChatGPT Citations | #5 in LA (4 mentions) |
| Perplexity Citations | Not cited |

**Key takeaway**: The site has excellent technical GEO foundations (crawler access, ssg, llms.txt, schema, RSL 1.0). The weakest link is **brand presence** — zero YouTube, Reddit, LinkedIn, or Wikipedia/Wikidata presence. Adding a YouTube channel is the single highest-impact change ($0 cost, 0.737 correlation with AI citations).
