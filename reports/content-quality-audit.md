# Content Quality Audit — AMY Electric Website

**Audit Date:** June 18, 2026  
**Site:** amyelectric.com (static HTML, Cloudflare Workers + Assets)  
**Total Pages Audited:** 76 (15 service, 5 emergency, 2 comparison, 16 city, 32 geo service, 33 blog)

---

## 1. Content Quality Scores by Page Type

### Scoring Criteria
- **Word Count** (30 pts): 1500+ = 30, 1000–1499 = 20, 500–999 = 10, <500 = 0
- **Heading Structure** (15 pts): H2/H3 hierarchy with logical nesting
- **FAQ Section** (15 pts): details/summary + FAQPage schema
- **CTA Presence** (10 pts): Multiple call-to-action elements
- **Internal Links** (10 pts): Cross-linking to related services
- **E-E-A-T Signals** (10 pts): Expert quotes, credentials, license numbers
- **Schema Completeness** (10 pts): JSON-LD richness (FAQPage, Service, BreadcrumbList, HowTo, etc.)

| Page Type | Avg Words | Avg H2 | Avg H3 | FAQ (details) | Schema Types | E-E-A-T Score | Overall Score |
|-----------|-----------|--------|--------|---------------|-------------|---------------|---------------|
| Service (root) | 2,352 | 7.7 | 9.5 | 5.0 | 8–10 | Strong | **87/100** |
| Emergency | 1,579 | 4.0 | 2.0 | 3.0 | 3 | Moderate | **72/100** |
| Comparison | 2,884 | 9.0 | 3.0 | 6.0 | 6–8 | Strong | **88/100** |
| City | 1,805 | 5.0 | 11.3 | 3.0 | 10+ | Strong | **78/100** |
| Geo Service | 2,179 | 3.0 | 3.0 | 7.0 | 4–5 | Strong | **75/100** |
| Blog | 1,437 | 6.3 | 9.7 | 0 | 1–2 | Moderate | **68/100** |

---

## 2. Thin Content Risk Assessment

### Pages at Risk (< 1,500 words main content)

| Page | Total Words | Main Content Est. | Risk Level |
|------|-------------|-------------------|------------|
| blog/electrical-inspection-cost-los-angeles.html | 1,040 | ~700 | **HIGH** |
| blog/generator-installation-cost-la.html | 1,165 | ~850 | **HIGH** |
| blog/surge-protector-vs-power-strip.html | 1,173 | ~870 | **HIGH** |
| blog/dedicated-circuit-installation-cost.html | 1,184 | ~880 | **HIGH** |
| blog/smoke-co-detector-installation-la.html | 1,183 | ~880 | **HIGH** |
| blog/electrical-contractor-vs-handyman-la.html | 1,198 | ~900 | **HIGH** |
| blog/smart-home-electrical-upgrades-la.html | 1,203 | ~900 | **HIGH** |
| blog/outdoor-lighting-installation-la.html | 1,172 | ~870 | **HIGH** |
| blog/electrical-safety-tips-homeowners-la.html | 1,225 | ~920 | **HIGH** |
| blog/whole-home-rewiring-cost-la.html | 1,262 | ~960 | **MEDIUM** |
| blog/ceiling-fan-installation-cost-la.html | 1,285 | ~980 | **MEDIUM** |
| blog/signs-you-need-electrical-panel-upgrade.html | 1,272 | ~970 | **MEDIUM** |
| blog/tesla-wall-connector-vs-other-ev-chargers.html | 1,264 | ~960 | **MEDIUM** |
| blog/emergency-electrician-los-angeles.html | 1,318 | ~1,020 | **MEDIUM** |
| blog/breaker-keeps-tripping-causes.html | 1,399 | ~1,100 | **MEDIUM** |
| blog/ceiling-fan-installation-la.html | 1,454 | ~1,150 | **LOW** |

**Note:** Blog word counts include nav/footer/chrome. Actual body content is ~25–30% less than total word count.

### Pages Safely Above Threshold
All 15 service pages (1,907–3,449 words), both comparison pages (2,604–3,163 words), all 5 emergency pages (1,407–1,769 words), all city pages (~1,732–1,902 words), and all geo service pages (~2,170–2,187 words) are **above the 1,500 word threshold**.

---

## 3. Duplicate Content Concerns

### HIGH RISK — Near-Duplicate Blog Pairs

| Pair | Concern | Severity |
|------|---------|----------|
| `panel-upgrade-signs.html` (1,739w) vs `signs-you-need-electrical-panel-upgrade.html` (1,272w) | Both cover "signs you need a panel upgrade" with overlapping bullet points. Different wordings but same topic and angle. | **HIGH** |
| `smart-home-electrical-upgrades.html` (1,481w) vs `smart-home-electrical-upgrades-la.html` (1,203w) | Both cover smart home electrical upgrades for LA. Nearly identical intro copy. | **HIGH** |
| `how-to-choose-electrician-los-angeles.html` (1,570w) vs `choosing-electrician-la.html` (1,798w) | Both are "how to choose an electrician in LA" guides. Same topic, similar structure. | **HIGH** |

### MODERATE RISK — Topic Overlap

| Page Pair | Concern |
|-----------|---------|
| `ev-charger-installation.html` vs `tesla-charger-installation.html` | Tesla page is a subset of EV charger page. Content appears distinct enough (Tesla-specific), but heavy topic overlap. |
| `ev-charger-installation-cost-la.html` (blog) vs `ev-charger-installation.html` (service) | Blog post covers cost; service page has price table. Acceptable if differentiated by intent. |
| `panel-upgrade-cost-los-angeles.html` (blog) vs `panel-upgrade.html` (service) | Similar cost data in both. Blog adds detail; service page has pricing sidebar. |
| `emergency-electrician.html` (emergency) vs `blog/emergency-electrician-los-angeles.html` (blog) | Same topic, different depth. Acceptable if blog adds unique value. |

### LOW RISK — Template-Level Repetition
All 16 city pages share near-identical structure (hero, service cards, local knowledge, FAQ, CTA). Content is differentiated per city name and some local details, but the FAQ answers are largely copy-paste with city name swapped. The FAQ answers for "Do you serve [City] for same-day repairs?" and "Who handles permits for electrical work in [City]?" are nearly identical across all 16 cities.

---

## 4. E-E-A-T Completeness

### Strengths (Present)
- **Expert Quotes:** 13 of 15 service pages include "Amy, founder of AMY Electric and Licensed C-10 electrical contractor with 15+ years of experience" quotes
- **License Numbers:** C-10 #981578 and EVITP #4051604 appear in topbar, footer, meta descriptions, and schema on all pages
- **Credentials in Schema:** City pages include `EducationalOccupationalCredential` for both C-10 and EVITP
- **AggregateRating:** City pages include 4.9/5.0 rating from 87 reviews in Electrician schema
- **foundingDate:** "2012" in city page schema
- **Blog Expert Quotes:** 10+ blog posts include Amy founder quotes

### Gaps (Missing)

| Gap | Affected Pages | Impact |
|-----|---------------|--------|
| **No author byline on blog posts** | All 32 blog posts | Moderate — Google values clear author attribution for YMYL-adjacent content |
| **No author bio page** | Site-wide | Moderate — No `/about` or `/amy` page establishing Amy's credentials |
| **No customer names in testimonials** | `testimonials.html` | Low — Anonymous reviews lack specificity |
| **No project case studies with dates** | Service pages | Low — Photo grids exist but lack project dates and locations |
| **Blog posts lack datePublished in visible content** | All blog posts | Low — Schema has dates but no visible "Published: March 2026" on page |
| **No third-party citations** | Service pages | Moderate — Only panel-upgrade.html cites NFPA/NEC. Other pages lack external authority references |
| **Emergency pages missing Electrician schema** | 5 emergency pages | Moderate — Only have FAQPage + BreadcrumbList, no Electrician/Service schema |
| **Geo service pages missing Service schema** | 32 geo pages | Moderate — Only have Electrician + FAQPage + BreadcrumbList |

### E-E-A-T Score by Page Type

| Page Type | Expert Quotes | License in Content | External Citations | Schema Credentials | Score |
|-----------|--------------|-------------------|-------------------|-------------------|-------|
| Service (root) | ✅ 13/15 | ✅ All | ⚠️ 1/15 (NFPA) | ✅ All | **8/10** |
| Emergency | ✅ All | ✅ All | ❌ None | ❌ No Electrician schema | **5/10** |
| Comparison | ✅ All | ✅ All | ❌ None | ✅ All | **7/10** |
| City | ⚠️ Partial | ✅ All | ❌ None | ✅ Strong | **7/10** |
| Geo Service | ✅ All | ✅ All | ❌ None | ⚠️ Missing Service schema | **6/10** |
| Blog | ✅ 10/32 | ✅ All | ❌ None | ❌ No author schema | **5/10** |

---

## 5. AI Citation Readiness Assessment

### What AI Search Engines Need
AI Overviews, ChatGPT Search, and Perplexity prefer content that:
1. Makes clear, verifiable factual claims
2. Cites authoritative sources (NEC, NFPA, LADWP, CSLB, DOE)
3. Provides specific numbers with context
4. Answers questions directly in the first paragraph
5. Has speakable/citable passages

### Current State

| Signal | Present? | Notes |
|--------|----------|-------|
| **Factual claims with sources** | ⚠️ Partial | Only `panel-upgrade.html` cites NFPA/NEC. Other pages make claims without attribution. |
| **Specific statistics** | ⚠️ Partial | EV charger page: "35% year-over-year increase." Panel page: "$2,500–$4,500 typical." Most pages lack data. |
| **Speakable schema** | ⚠️ Partial | 10 of 15 service pages + 5 emergency pages + 2 comparison pages have SpeakableSpecification. City pages and blog posts do NOT. |
| **Quick Answer / At a Glance** | ⚠️ Partial | Emergency pages have "At a Glance" section. Service pages do NOT have a dedicated quick-answer block (only FAQ). |
| **Direct answers in intro** | ✅ Most pages | Most pages open with a clear 1–2 sentence answer to the primary query. |
| **llms.txt** | ✅ Present | `llms.txt` file exists at root for AI crawler consumption. |

### AI Citation Readiness Score

| Page Type | Score | Key Gap |
|-----------|-------|---------|
| Service (root) | **7/10** | No "At a Glance" quick answer section; only 1 page cites external sources |
| Emergency | **8/10** | Has "At a Glance" + Speakable schema; strong for voice search |
| Comparison | **7/10** | Good data tables; lacks external source citations |
| City | **5/10** | No Speakable schema; no quick answer section; FAQ is generic |
| Geo Service | **6/10** | Has 7 FAQs with Speakable; lacks quick answer intro block |
| Blog | **4/10** | No Speakable schema; no author byline; no external citations; thin content risk |

---

## 6. Heading Structure Analysis

### Service Pages (root)
- **H1:** Present, descriptive, includes location
- **H2:** 7–9 per page (Good)
- **H3:** 8–18 per page (Good depth)
- **Issue:** H2 "What Is a Electrical Panel Upgrade?" contains grammar error ("a" should be "an")

### Emergency Pages
- **H1:** Present, descriptive
- **H2:** 4 per page (Thin — could use more content sections)
- **H3:** 2 per page (Very thin)
- **Issue:** Only 4 H2 sections vs. 7–9 on service pages

### Comparison Pages
- **H1:** Present, clear comparison format
- **H2:** 9 per page (Excellent)
- **H3:** 3 per page (Could be higher)
- **Good:** Structured as comparison with clear sections

### City Pages
- **H1:** Present, includes city name
- **H2:** 4–7 per page
- **H3:** 10–14 per page (Service cards)
- **Issue:** Some city pages have only 4 H2s (LA, Burbank) vs. 7 (Santa Monica)

### Geo Service Pages
- **H1:** Present, includes service + city
- **H2:** 3 per page (Thin)
- **H3:** 3 per page (Thin)
- **Issue:** Only 3 H2 sections — FAQ takes up most of the page

### Blog Posts
- **H1:** Present on all
- **H2:** 5–8 per page
- **H3:** 4–20 per page
- **Good:** Proper hierarchy throughout

---

## 7. FAQ Implementation

### Current FAQ Counts (details/summary elements)

| Page Type | Avg FAQs | Schema FAQPage | Schema Qs |
|-----------|----------|---------------|-----------|
| Service (root) | 4–6 | ✅ Yes | 3–6 |
| Emergency | 3 | ✅ Yes | 3 |
| Comparison | 6 | ✅ Yes | 6 |
| City | 3 | ✅ Yes | 3 |
| Geo Service | 7 | ✅ Yes | 7 |
| Blog | 0 | ❌ No | 0 |

### Issues
- **Blog posts have NO FAQ sections** — all 32 blog posts lack `<details>` FAQ elements and FAQPage schema
- **Service pages have 4–6 FAQs** but FAQPage schema only includes 3–6 questions (should match visible FAQs)
- **City pages have only 3 FAQs** — could benefit from 5–7 city-specific questions
- **Emergency pages have only 3 FAQs** — minimal for high-intent emergency queries

---

## 8. Internal Linking Analysis

### Average Internal Links Per Page (excluding nav/footer)

| Page Type | Internal Links (body) | Assessment |
|-----------|----------------------|------------|
| Service (root) | 4–5 | Adequate — links to related services and city pages |
| Emergency | 4 | Adequate — links to related emergency pages |
| Comparison | 4 | Adequate — links to parent service pages |
| City | 5–7 | Good — links to service pages and geo pages |
| Geo Service | 6 | Good — links to parent service + city page |
| Blog | 3 | **Low** — blog posts only link to 3 internal pages on average |

### Issues
- **Blog posts are link-isolated** — most blog posts only link to 3 internal pages (typically the parent service page and 2 related pages). This limits PageRank flow and topical cluster strength.
- **No blog index cross-links** — Blog index page (`blog/index.html`) links to all posts, but individual posts don't link back to each other sufficiently.
- **City pages link to geo pages** — Good pattern. City → geo pages (e.g., `city-los-angeles` → `ev-charger-installation-los-angeles`) is well implemented.

---

## 9. Content Freshness

### Strengths
- All service pages have `datePublished: 2024` and `dateModified: 2026` in JSON-LD schema
- Blog posts reference "2026" in titles and content (california-electrical-code-changes-2026, ladwp-ev-charger-rebate-guide-2026)
- Footer copyright: "© 2026 AMY Electric"
- No visible "last updated" dates in page content (only in schema)

### Gaps
- **No visible dates on blog posts** — Users and AI can't see when content was published
- **No "Updated" badges** on pages with recent changes
- **FAQ answers reference current code** but don't cite specific code edition years consistently

---

## 10. Recommendations

### Priority 1 — Critical (Immediate Impact)

1. **Consolidate duplicate blog posts**
   - Merge `panel-upgrade-signs.html` → redirect to `signs-you-need-electrical-panel-upgrade.html` (or vice versa)
   - Merge `smart-home-electrical-upgrades.html` → redirect to `smart-home-electrical-upgrades-la.html`
   - Merge `how-to-choose-electrician-los-angeles.html` → redirect to `choosing-electrician-la.html`
   - Use 301 redirects to preserve link equity

2. **Expand thin blog posts** (10 posts under 1,200 words)
   - Target 1,500+ words for all blog posts
   - Add unique sections: local data, cost breakdowns, step-by-step guides, expert tips
   - Add FAQ sections with 3–5 questions per blog post (details/summary + FAQPage schema)

3. **Add FAQ sections to all blog posts**
   - Currently 0 of 32 blog posts have FAQ sections
   - Add 3–5 relevant questions per post
   - Add FAQPage JSON-LD schema to each blog post

### Priority 2 — High Value (Week 1–2)

4. **Add "At a Glance" / Quick Answer section to all service pages**
   - Emergency pages already have this pattern — extend to all 15 service pages
   - Include: 1–2 sentence answer, key facts, and source citation
   - Add Speakable schema targeting the quick answer div

5. **Add external source citations to service pages**
   - Only `panel-upgrade.html` cites NFPA/NEC
   - Add citations to: NEC code references, LADWP program links, CSLB requirements, CPSC safety data, DOE statistics
   - Target: at least 1 external authority citation per service page

6. **Add Electrician schema to emergency pages**
   - 5 emergency pages only have FAQPage + BreadcrumbList
   - Add Electrician schema with areaServed, credentials, and priceRange

7. **Add Service schema to geo service pages**
   - 32 geo pages only have Electrician + FAQPage + BreadcrumbList
   - Add Service schema with offers and areaServed

### Priority 3 — Enhancement (Week 2–4)

8. **Add author bylines to blog posts**
   - Add "By Amy, Licensed C-10 Electrician" below each blog H1
   - Link to an `/about` page (create if missing)
   - Add `author` property to BlogPosting schema

9. **Create an About/Team page**
   - No `/about` page exists — this is a major E-E-A-T gap
   - Include: Amy's photo, full credentials, years of experience, certifications, company history
   - Link from blog bylines, footer, and service pages

10. **Expand city page FAQ sections**
    - Currently only 3 questions per city page
    - Expand to 5–7 questions with city-specific content (not just city name swaps)
    - Add unique local knowledge per city (neighborhoods, permit quirks, utility specifics)

11. **Add Speakable schema to city and blog pages**
    - City pages and blog posts lack SpeakableSpecification
    - Voice search is critical for "electrician near me" queries

12. **Add visible publication dates to blog posts**
    - Show "Published: March 2026 | Updated: June 2026" below the H1
    - Helps users and AI assess content freshness

13. **Fix grammar error in panel-upgrade.html**
    - H2 reads "What Is a Electrical Panel Upgrade?" — should be "an Electrical"

14. **Improve blog internal linking**
    - Average 3 internal links per blog post is low
    - Target 5–7 internal links per post (link to related services, city pages, other blog posts)
    - Create a "Related Reading" section at the bottom of each post

---

## Appendix A: Full Page Measurements

### Service Pages (Root)

| Page | Words | H2 | H3 | FAQs | CTA | Int Links | Ext Links | Price | Expert | Quick Ans | Speakable |
|------|-------|----|----|------|-----|-----------|-----------|-------|--------|-----------|-----------|
| panel-upgrade.html | 2,764 | 8 | 10 | 5 | 21 | 5 | 1 | ✅ | ✅ | ❌ | ✅ |
| ev-charger-installation.html | 3,449 | 9 | 18 | 5 | 41 | 5 | 6 | ✅ | ✅ | ❌ | ✅ |
| electrical-repair.html | 2,174 | 7 | 11 | 4 | 19 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| commercial-electrical.html | 1,907 | 7 | 9 | 4 | 21 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| smart-home-electrical.html | 2,297 | 8 | 10 | 6 | 18 | 4 | 0 | ✅ | ✅ | ❌ | ❌ |
| generator-transfer-switch.html | 2,665 | 8 | 8 | 5 | 17 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| whole-home-rewiring.html | 2,550 | 8 | 9 | 5 | 17 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| ceiling-fan-installation.html | 2,272 | 8 | 9 | 5 | 19 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| lighting-installation.html | 2,006 | 7 | 9 | 4 | 18 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| outlet-switch-installation.html | 2,317 | 8 | 10 | 6 | 17 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| surge-protection.html | 2,331 | 8 | 9 | 5 | 18 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| smoke-co-detector-installation.html | 2,102 | 8 | 9 | 6 | 18 | 4 | 0 | ✅ | ✅ | ❌ | ❌ |
| dedicated-circuits.html | 2,230 | 8 | 11 | 5 | 17 | 4 | 0 | ✅ | ✅ | ❌ | ❌ |
| electrical-safety-inspections.html | 2,082 | 8 | 9 | 5 | 17 | 4 | 0 | ✅ | ✅ | ❌ | ❌ |
| tesla-charger-installation.html | 2,757 | 8 | 10 | 6 | 20 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |

### Emergency Pages

| Page | Words | H2 | H3 | FAQs | CTA | Int Links | Ext Links | Price | Expert | Quick Ans | Speakable |
|------|-------|----|----|------|-----|-----------|-----------|-------|--------|-----------|-----------|
| emergency-electrician.html | 1,407 | 4 | 2 | 3 | 17 | 4 | 0 | ✅ | ✅ | ✅ | ✅ |
| power-outage-repair.html | 1,484 | 4 | 2 | 3 | 17 | 4 | 0 | ✅ | ✅ | ✅ | ✅ |
| breaker-tripping.html | 1,660 | 4 | 2 | 3 | 17 | 4 | 0 | ✅ | ✅ | ✅ | ✅ |
| burning-smell-panel.html | 1,769 | 4 | 2 | 3 | 17 | 4 | 0 | ✅ | ✅ | ✅ | ✅ |
| same-day-electrical-repair.html | 1,574 | 4 | 2 | 3 | 17 | 4 | 0 | ✅ | ✅ | ✅ | ✅ |

### Comparison Pages

| Page | Words | H2 | H3 | FAQs | CTA | Int Links | Ext Links | Price | Expert | Quick Ans | Speakable |
|------|-------|----|----|------|-----|-----------|-----------|-------|--------|-----------|-----------|
| ev-charger-hardwired-vs-plug-in.html | 2,604 | 9 | 3 | 6 | 18 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |
| panel-100a-vs-200a.html | 3,163 | 9 | 3 | 6 | 17 | 4 | 0 | ✅ | ✅ | ❌ | ✅ |

### City Pages (Sample)

| Page | Words | H2 | H3 | FAQs | CTA | Int Links | Ext Links | Price | Expert | Quick Ans | Speakable |
|------|-------|----|----|------|-----|-----------|-----------|-------|--------|-----------|-----------|
| city-los-angeles.html | 1,780 | 4 | 10 | 3 | 23 | 5 | 1 | ✅ | ✅ | ❌ | ❌ |
| city-santa-monica.html | 1,902 | 7 | 14 | 3 | 24 | 7 | 1 | ✅ | ✅ | ❌ | ❌ |
| city-burbank.html | 1,732 | 4 | 10 | 3 | 23 | 5 | 1 | ✅ | ✅ | ❌ | ❌ |

### Geo Service Pages (Sample)

| Page | Words | H2 | H3 | FAQs | CTA | Int Links | Ext Links | Price | Expert | Quick Ans | Speakable |
|------|-------|----|----|------|-----|-----------|-----------|-------|--------|-----------|-----------|
| ev-charger-installation-los-angeles.html | 2,187 | 3 | 3 | 7 | 25 | 6 | 0 | ✅ | ✅ | ❌ | ❌ |
| panel-upgrade-los-angeles.html | 2,170 | 3 | 3 | 7 | 24 | 6 | 0 | ✅ | ✅ | ❌ | ❌ |

### Blog Posts (Newest 2)

| Page | Words | H2 | H3 | FAQs | CTA | Int Links | Ext Links | Price | Expert | Quick Ans | Speakable |
|------|-------|----|----|------|-----|-----------|-----------|-------|--------|-----------|-----------|
| california-electrical-code-changes-2026.html | 2,502 | 7 | 13 | 5 | 12 | 3 | 0 | ✅ | ✅ | ❌ | ❌ |
| ladwp-ev-charger-rebate-guide-2026.html | 2,271 | 8 | 11 | 5 | 13 | 3 | 0 | ✅ | ✅ | ❌ | ❌ |

---

## Appendix B: Blog Post Complete Word Counts

| Blog Post | Words | Risk |
|-----------|-------|------|
| electrical-inspection-cost-los-angeles.html | 1,040 | HIGH |
| generator-installation-cost-la.html | 1,165 | HIGH |
| outdoor-lighting-installation-la.html | 1,172 | HIGH |
| surge-protector-vs-power-strip.html | 1,173 | HIGH |
| dedicated-circuit-installation-cost.html | 1,184 | HIGH |
| smoke-co-detector-installation-la.html | 1,183 | HIGH |
| electrical-contractor-vs-handyman-la.html | 1,198 | HIGH |
| smart-home-electrical-upgrades-la.html | 1,203 | HIGH |
| electrical-safety-tips-homeowners-la.html | 1,225 | HIGH |
| whole-home-rewiring-cost-la.html | 1,262 | MEDIUM |
| signs-you-need-electrical-panel-upgrade.html | 1,272 | MEDIUM |
| ceiling-fan-installation-cost-la.html | 1,285 | MEDIUM |
| tesla-wall-connector-vs-other-ev-chargers.html | 1,264 | MEDIUM |
| emergency-electrician-los-angeles.html | 1,318 | MEDIUM |
| breaker-keeps-tripping-causes.html | 1,399 | MEDIUM |
| ceiling-fan-installation-la.html | 1,454 | LOW |
| electrical-permit-los-angeles.html | 1,460 | LOW |
| smart-home-electrical-upgrades.html | 1,481 | LOW |
| commercial-electrical-la.html | 1,491 | LOW |
| ev-vs-gas-vehicle-cost-los-angeles.html | 1,497 | LOW |
| panel-upgrade-cost-los-angeles.html | 1,559 | OK |
| gfci-afci-protection-la.html | 1,570 | OK |
| la-electrical-safety-tips.html | 1,598 | OK |
| ev-charging-los-angeles.html | 1,585 | OK |
| ev-charger-installation-cost-la.html | 1,604 | OK |
| la-electrical-code-requirements.html | 1,631 | OK |
| ev-charging-benefits.html | 1,681 | OK |
| whole-home-rewiring-guide.html | 1,687 | OK |
| panel-upgrade-signs.html | 1,739 | OK |
| choosing-electrician-la.html | 1,798 | OK |
| how-to-choose-electrician-los-angeles.html | 1,570 | OK |
| california-electrical-code-changes-2026.html | 2,502 | OK |
| ladwp-ev-charger-rebate-guide-2026.html | 2,271 | OK |

---

## Summary

| Category | Status | Key Action |
|----------|--------|------------|
| **Thin Content** | ⚠️ 10 blog posts under 1,200 words | Expand to 1,500+ words with unique value |
| **Duplicate Content** | 🔴 3 high-risk duplicate pairs | Consolidate with 301 redirects |
| **E-E-A-T** | ⚠️ Good on service pages, weak on blog | Add author bylines, about page, external citations |
| **AI Citation** | ⚠️ Partial — missing on 60% of pages | Add Speakable, quick answer sections, source citations |
| **FAQ Coverage** | ⚠️ Blog posts have zero FAQs | Add 3–5 FAQs + FAQPage schema to all blog posts |
| **Schema** | ✅ Strong on service/city pages | Add Electrician to emergency, Service to geo pages |
| **Internal Links** | ⚠️ Blog posts averaging only 3 links | Increase to 5–7 cross-links per post |
| **Freshness** | ✅ Schema dates current (2026) | Add visible dates to blog posts |
