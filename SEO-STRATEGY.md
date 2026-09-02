# AMY Electric — Strategic SEO Plan
*Last Updated: July 28, 2026*

## Executive Summary

AMY Electric is a licensed C-10 electrical contractor serving Greater Los Angeles. The website (amyelectric.com) is a static HTML marketing site on Cloudflare Workers + Assets with 111+ live pages, including service pages, geo-specific landing pages, city pages, and 34 blog posts. ChatGPT already cites AMY Electric #5 in Los Angeles (4x across 6 queries per LocalFox). The strategic goal is to expand organic rankings, dominate local search for high-intent keywords, and build authority through content and E-E-A-T signals.

---

## 1. Current State Assessment

### Site Metrics (July 28, 2026)
| Metric | Baseline | Current |
|--------|----------|---------|
| Lighthouse Performance | 72/100 | 85/100 |
| Lighthouse Accessibility | 96/100 | 100/100 |
| Lighthouse SEO | 100/100 | 100/100 |
| Total HTML Pages | 0 | 111+ |
| Blog Posts | 0 | 34 |
| Service Pages | 0 | 17 (15 + 2 new) |
| City Pages | 0 | 16 |
| Geo Service Pages | 0 | 32 |
| FAQ Entries | 0 | 224+ |
| Schema Types | 0 | LocalBusiness, Service, FAQPage, HowTo, BreadcrumbList, BlogPosting |
| Network Weight | 295KB | 173KB (-41%) |

### Strengths
- Static HTML → excellent crawlability, no JS dependency
- Full schema coverage (LocalBusiness, FAQPage, BreadcrumbList, HowTo)
- 10 AI crawlers explicitly allowed in robots.txt
- 100/100 accessibility and SEO scores
- NAP consistency 100% (111/111 pages)
- ChatGPT citation confirmed (#5 in LA)

### Weaknesses
- No Google Search Console / Analytics credentials (Amy to provide)
- No Google Business Profile optimization
- Limited backlink profile
- No Reddit/forum presence (affects Perplexity)
- Some orphaned pages (smoke-co-detector, about) — partially resolved
- No reviews strategy or testimonial schema

---

## 2. Competitive Landscape (LA Electrical Contractors)

### Top 5 Competitors
| Competitor | Strengths | Weaknesses |
|------------|-----------|------------|
| **Riverside Electrical** | Strong Google reviews, established | Generic content, limited city pages |
| **Hiller Electric** | Established brand, good GBP | Old website, poor schema |
| **LA Electric** | Exact match domain | Thin content, poor UX |
| **Bright Electric** | Good reviews, professional site | Limited content depth |
| **Pacific Electrical** | Large service area | No geo-specific pages |

### Keyword Gaps
AMY Electric is NOT ranking for:
- "electrician los angeles" (volume: 5,400/mo)
- "ev charger installation los angeles" (volume: 2,900/mo)
- "panel upgrade los angeles" (volume: 2,400/mo)
- "emergency electrician los angeles" (volume: 1,600/mo)
- "electrical contractor los angeles" (volume: 1,300/mo)

### AMY's Advantages
1. **Static HTML** — faster, more reliable than competitors' CMS sites
2. **Schema-rich** — most competitors lack structured data
3. **Geo-specific pages** — 32 competitor pages vs competitors' 0-5
4. **AI citations** — ChatGPT already references AMY
5. **E-E-A-T** — C-10 license, EVITP certification, author profiles

---

## Month 6 authority execution docs

- [YouTube video SEO strategy](SEO_YOUTUBE_STRATEGY.md)
- [Backlink outreach plan](SEO_BACKLINK_OUTREACH_PLAN.md)
- [Local citation plan](SEO_LOCAL_CITATION_PLAN.md)
- [Manual AI visibility baseline](SEO_AI_VISIBILITY_BASELINE.md)

## 3. Architecture & URL Structure

### Current URL Hierarchy
```
/
├── index.html (Homepage)
├── /about.html
├── /testimonials.html
├── /gallery.html
├── /privacy-policy.html
├── /404.html (NEW)
├── /smoke-co-detector-installation.html
├── /panel-upgrade.html
├── /ev-charger-installation.html
├── /electrical-repair.html
├── /commercial-electrical.html
├── /lighting-installation.html
├── /tesla-charger-installation.html
├── /whole-home-rewiring.html
├── /surge-protection.html
├── /emergency-electrician.html
├── /licensed-electrician-los-angeles.html
├── /{city-name}.html (16 cities)
├── /panel-upgrade-{city}.html (16 geo)
├── /ev-charger-installation-{city}.html (16 geo)
└── /blog/
    ├── index.html
    └── /{blog-slug}.html (34 posts)
```

### Quality Gates
| Page Type | Target Words | Unique % | Max Pages |
|-----------|-------------|----------|-----------|
| Service Pages | 2,000-3,500 | 100% | 25 |
| Geo Service Pages | 1,500-2,500 | 40-60% | 50 |
| City Pages | 800-1,200 | 60%+ | 20 |
| Blog Posts | 1,200-2,000 | 100% | 60 |

**Current: 111 pages → Target 6-month: 135 pages → Target 12-month: 155 pages**

---

## 4. Content Strategy

### Content Pillars

#### Pillar 1: EV Charging (Primary)
- **Core Page**: ev-charger-installation.html
- **Supporting**: tesla-charger-installation.html
- **Geo**: 16 ev-charger-installation-{city} pages
- **Blog**: 8+ posts (cost, benefits, comparison, rebates, etc.)
- **Target Keywords**: "ev charger installation los angeles", "home ev charger cost la", "tesla wall connector installation"

#### Pillar 2: Panel Upgrades (High Intent)
- **Core Page**: panel-upgrade.html
- **Supporting**: panel-100a-vs-200a.html
- **Geo**: 16 panel-upgrade-{city} pages
- **Blog**: 5+ posts (signs, costs, 100a vs 200a, etc.)
- **Target Keywords**: "200a panel upgrade los angeles", "electrical panel upgrade cost la"

#### Pillar 3: Electrical Safety (Trust Building)
- **Core Pages**: smoke-co-detector-installation.html, electrical-safety-inspections.html
- **Blog**: 6+ posts (safety tips, code changes, inspections)
- **Target Keywords**: "smoke detector installation los angeles", "electrical safety inspection la"

#### Pillar 4: Emergency Services (High Conversion)
- **Core Page**: emergency-electrician.html
- **Supporting**: power-outage-repair.html, breaker-tripping.html, burning-smell-panel.html, same-day-electrical-repair.html
- **Blog**: 3+ posts (when to call, triage, etc.)
- **Target Keywords**: "emergency electrician los angeles", "24 hour electrician la"

#### Pillar 5: Smart Home & Emerging
- **Core Page**: smart-home-electrical.html
- **Blog**: 4+ posts (smart switches, EV fleet, home automation)
- **Target Keywords**: "smart home electrician los angeles"

### Content Calendar (Next 90 Days)

#### August 2026 (Weeks 1-4)
| Week | Content Type | Topic | Target Keyword |
|------|-------------|-------|----------------|
| 1 | Blog Post | "Electrical Panel Labeling: Why It Matters" | panel labeling los angeles |
| 1 | Blog Post | "Signs Your Home Needs Rewiring" | rewiring signs los angeles |
| 2 | Blog Post | "EV Charger Installation Timeline" | ev charger installation time |
| 2 | Blog Post | "Aluminum Wiring: LA Home Guide" | aluminum wiring los angeles |
| 3 | Blog Post | "Kitchen Electrical Upgrade Checklist" | kitchen electrical upgrade la |
| 3 | Blog Post | "GFCI vs AFCI Protection Guide" | gfci afci electrical code |
| 4 | Service Page | "Electrical Panel Labeling" (NEW) | panel labeling service la |
| 4 | Blog Post | "Smart Home Wiring Basics" | smart home wiring los angeles |

#### September 2026 (Weeks 5-8)
| Week | Content Type | Topic | Target Keyword |
|------|-------------|-------|----------------|
| 5 | Blog Post | "Generator Transfer Switch Guide" | generator switch los angeles |
| 5 | Blog Post | "Outdoor Lighting Safety Code" | outdoor lighting code la |
| 6 | Blog Post | "Ceiling Fan Cost Guide" | ceiling fan installation cost |
| 6 | Blog Post | "Dedicated Circuit: When You Need One" | dedicated circuit installation |
| 7 | Blog Post | "Electrical Inspection Checklist" | electrical inspection checklist |
| 7 | Blog Post | "Home EV Ready: What to Know" | ev ready home los angeles |
| 8 | Service Page | "Bathroom Electrical Safety" (NEW) | bathroom electrical la |
| 8 | Blog Post | "Holiday Lighting Safety" | holiday lighting electrical |

#### October 2026 (Weeks 9-12)
| Week | Content Type | Topic | Target Keyword |
|------|-------------|-------|----------------|
| 9 | Blog Post | "Power Outage Prep Guide" | power outage preparation la |
| 9 | Blog Post | "Bathroom GFCI Requirements" | bathroom gfci code los angeles |
| 10 | Blog Post | "Emergency Lighting for Businesses" | emergency lighting commercial |
| 10 | Blog Post | "Whole-Home Generator Guide" | whole home generator los angeles |
| 11 | Blog Post | "EV Charger Comparison 2026" | ev charger comparison guide |
| 11 | Blog Post | "Knob and Tube Wiring Replacement" | knob and tube wiring la |
| 12 | Blog Post | "Electrical Permit Process Guide" | electrical permit process la |
| 12 | Geo Pages | Add 4 new geo pages | {service}-{city} combinations |

### E-E-A-T Building Plan

#### Experience
- Add "Amy" author bio to all blog posts
- Include specific project examples (with permission)
- Link to gallery photos with descriptions
- Add "15+ years experience" signal consistently

#### Expertise
- C-10 #981578 mentioned on every page
- EVITP #4051604 on EV-related content
- Reference California Electrical Code sections
- Explain technical concepts in plain language

#### Authoritativeness
- Link to CSLB license verification
- Add awards/certifications badges
- Include industry association memberships
- Reference trade publications and standards

#### Trustworthiness
- Display NAP consistently (already 100%)
- Add Google Reviews widget (once Google Place ID provided)
- Include warranty/guarantee information
- Add "Licensed & Insured" badge to header

---

## 5. Technical SEO Roadmap

### Priority 1: Fix Existing Issues (August 1-8)
- [x] Fix sticky bar #estimate anchor (DONE)
- [x] Add 404.html (DONE)
- [x] Link orphaned pages (DONE)
- [ ] Submit sitemap to Google Search Console
- [ ] Request re-indexing of updated pages

### Priority 2: Local SEO Setup (August 8-15)
- [ ] Claim/optimize Google Business Profile
- [ ] Add Google Place ID for Reviews widget
- [ ] Create Apple Maps listing
- [ ] Create Bing Places listing
- [ ] Update sameAs schema with new profiles

### Priority 3: Schema Enhancement (August 15-31)
- [ ] Add AggregateRating schema to testimonials page
- [ ] Add Reviews schema with Google Place ID
- [ ] Add Service schema with priceRange to service pages
- [ ] Add Video schema for future video content
- [ ] Add Event schema for workshops/classes

### Priority 4: Performance (September 2026)
- [ ] Lazy load images in gallery
- [ ] Optimize LCP to <2.0s
- [ ] Reduce CSS to <20KB
- [ ] Reduce JS to <2KB

### Priority 5: Content Expansion (October 2026)
- [ ] Create new service pages (bathroom electrical, panel labeling)
- [ ] Create 4 new geo pages
- [ ] Publish 12 new blog posts
- [ ] Update sitemap with new pages

---

## 6. Link Building Strategy

### Tier 1: Citations (Weeks 1-4)
- [ ] Google Business Profile
- [ ] Yelp business page
- [ ] Apple Maps listing
- [ ] Bing Places listing
- [ ] BBB profile (if applicable)
- [ ] Angi (formerly Angie's List)
- [ ] HomeAdvisor
- [ ] Thumbtack
- [ ] Porch
- [ ] BuildZoom

### Tier 2: Local Directories (Weeks 5-8)
- [ ] Los Angeles Chamber of Commerce
- [ ] LA Business Directory
- [ ] Winnetka Chamber of Commerce
- [ ] Sherman Oaks Chamber
- [ ] Encino Chamber
- [ ] Burbank Chamber
- [ ] Glendale Chamber

### Tier 3: Industry/Content Links (Weeks 9-12)
- [ ] Guest posts on home improvement blogs
- [ ] Q&A on Reddit (r/LosAngeles, r/homeimprovement)
- [ ] Quora answers about electrical topics
- [ ] HARO (Help A Reporter Out) responses
- [ ] Local news/TV station expert quotes

### Tier 4: Digital PR (Months 4-6)
- [ ] Press releases for new services
- [ ] Case studies with before/after photos
- [ ] Industry publication features
- [ ] Local media expert quotes

---

## 7. KPI Targets & Success Metrics

### 3-Month Targets (August-October 2026)
| Metric | Baseline | Target |
|--------|----------|--------|
| Organic Traffic (monthly) | Unknown | 500+ sessions |
| Indexed Pages | 111 | 125+ |
| Backlinks | Unknown | 15+ referring domains |
| Google Reviews | Unknown | 5+ new reviews |
| Lighthouse Performance | 85 | 88+ |
| Schema Coverage | 95% | 98%+ |

### 6-Month Targets (January 2027)
| Metric | Baseline | Target |
|--------|----------|--------|
| Organic Traffic (monthly) | Unknown | 1,500+ sessions |
| Top 10 Rankings | 0 | 5+ keywords |
| Top 20 Rankings | 0 | 15+ keywords |
| Google Reviews | Unknown | 15+ total |
| Local Pack Presence | Unknown | 3+ keywords |
| Perplexity Citations | 0 | 3+ mentions |

### 12-Month Targets (July 2027)
| Metric | Baseline | Target |
|--------|----------|--------|
| Organic Traffic (monthly) | Unknown | 3,000+ sessions |
| Top 10 Rankings | 0 | 15+ keywords |
| Domain Authority | Unknown | 20+ |
| Google Reviews | Unknown | 30+ total |
| AI Citations | 4 (ChatGPT) | 10+ across platforms |
| Monthly Leads from Organic | Unknown | 50+ form submissions |

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| No Google Search Console access | Request from Amy ASAP; priority blocker |
| No Google Analytics | Enable Cloudflare Web Analytics (free, no code) |
| Competitor content copying | Regular content audits; emphasize unique local expertise |
| Google algorithm updates | Diversify traffic sources; build email list |
| Negative reviews | Respond within 48 hours; resolve offline |
| AI citation decline | Build Reddit/forum presence; improve E-E-A-T |
| Slow content production | Batch content creation; use templates |

---

## 9. Immediate Action Items (Next 2 Weeks)

### Week 1 (Jul 28-Aug 3)
1. **Amy**: Request Google Search Console access
2. **Amy**: Claim/optimize Google Business Profile
3. **Amy**: Add Google Place ID to site
4. **Amy**: Create Yelp business page
5. **Amy**: Create Apple Maps listing

### Week 2 (Aug 4-10)
1. **Amy**: Submit sitemap to Google Search Console
2. **Amy**: Request re-indexing of 10 priority pages
3. **Site**: Enable Cloudflare Web Analytics
4. **Site**: Add Google Reviews widget (once Place ID provided)
5. **Site**: Publish 2 new blog posts (panel labeling, rewiring signs)

---

## 10. Appendix: Recommended Tool Stack

### Free Tools
- **Google Search Console**: Indexing, performance tracking
- **Google Business Profile**: Local visibility
- **Cloudflare Web Analytics**: Privacy-first traffic data
- **PageSpeed Insights**: Core Web Vitals monitoring
- **Schema.org Validator**: Structured data validation

### Paid Tools (Optional)
- **Ahrefs/SEMrush**: Keyword tracking, competitor analysis
- **BrightLocal**: Local SEO management
- **Whitespark**: Citation building and tracking
- **CallRail**: Phone call tracking

---

*This plan should be reviewed monthly and updated based on actual performance data. First review: September 1, 2026.*
