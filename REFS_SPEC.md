# AMY Electric — Reference Specification

## Business Identity
| Field | Value |
|-------|-------|
| Name | AMY Electric |
| License | C-10 #981578 |
| EVITP | #4051604 |
| Phone | (818) 302-5614 |
| Email | info@amyelectric.com |
| Address | 20628 Londelius St, Winnetka, CA 91306 |
| Website | https://amyelectric.com |

## Hosting & Deployment
| Field | Value |
|-------|-------|
| Platform | Cloudflare Workers + Assets |
| Source | GitHub (auto-deploy on push to main) |
| IndexNow Key | 16076f14-4d06-4581-b281-38a7a89804ca |

## Site Metrics
| Metric | Count |
|--------|-------|
| Total HTML files | 315 |
| Root pages | 231 |
| Blog posts | 64 |
| City pages | 112 |
| Geo service pages | 64 |
| Service pages | 17 |
| Comparison pages | 3 |
| Special pages | 6 |
| CSS size | 30KB |
| JS size | 6.4KB |

## Page Types & Schema

### Homepage
- Schema: LocalBusiness, AggregateRating (4.9/5.0, 87 reviews), sameAs
- Nav: Full (Home, Services, EV Chargers, Panel Upgrades, Blog, Reviews, Emergency, Gallery, Service Areas, Call Now)

### Service Pages (17)
- Schema: Service, FAQPage, BreadcrumbList, PriceRange
- Pages: panel-upgrade, ev-charger-installation, electrical-repair, commercial-electrical, lighting-installation, tesla-charger-installation, whole-home-rewiring, surge-protection, emergency-electrician, smoke-co-detector-installation, electrical-safety-inspections, generator-transfer-switch, outlet-switch-installation, ceiling-fan-installation, dedicated-circuits, smart-home-electrical, licensed-electrician-los-angeles

### City Pages (112)
- Schema: Electrician, areaServed (City + DefinedRegion/postalCode), FAQPage, BreadcrumbList
- Coverage: 112 cities across Greater Los Angeles

### Geo Service Pages (64)
- Schema: FAQPage (7 Qs each), BreadcrumbList, Electrician
- Types: panel-upgrade-{city} (16), ev-charger-installation-{city} (16), whole-home-rewiring-{city} (16), + additional geo pages

### Blog Posts (64)
- Schema: BlogPosting, Author (Amy), datePublished, dateModified, FAQPage, BreadcrumbList
- Categories: Cost guides, comparisons, educational, local guides

### Comparison Pages (3)
- Schema: FAQPage, BreadcrumbList
- Pages: ev-charger-vs-panel-upgrade, ev-charger-hardwired-vs-plug-in, panel-100a-vs-200a

### Special Pages (6)
- reviews.html: Customer testimonials, FAQPage
- emergency-electrical.html: Emergency services, FAQPage
- testimonials.html: Additional testimonials
- gallery.html: Project photos (30+ images)
- privacy-policy.html: Privacy policy
- about.html: Company info

## Navigation Structure
```
Home → Services → EV Chargers → Panel Upgrades → Repairs → Service Areas → Blog → Reviews → Emergency → Gallery → Call Now
```

## Robots.txt
- **Allowed**: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, anthropic-ai, Google-Extended, Applebot-Extended, Meta-ExternalAgent, Meta-ExternalFetcher
- **Blocked**: CCBot, Bytespider, cohere-ai

## Scripts
| Script | Purpose |
|--------|---------|
| scripts/add-pages-to-nav.py | Add links to nav across all HTML files |
| scripts/add-footer-links.py | Add footer links across all HTML files |
| scripts/add-blog-to-nav-sitemap.py | Add blog posts to nav and sitemap |
| scripts/indexnow_submit.py | Submit URLs via IndexNow API |
| scripts/process-photos.py | Process and optimize photos |
| scripts/redact-photos.py | Privacy redactions on photos |

## Key Files
| File | Purpose |
|------|---------|
| index.html | Homepage |
| sitemap.xml | XML sitemap (310 URLs) |
| robots.txt | Crawler directives |
| _redirects | Cloudflare URL rewriting |
| css/style.min.css | Production CSS (30KB) |
| js/site.min.js | Production JS (6.4KB) |
| favicon.svg | Site favicon |

## Content Strategy
- **Primary keywords**: EV charger installation Los Angeles, panel upgrade Los Angeles, electrician Los Angeles
- **Geo targeting**: 112 city pages covering Greater Los Angeles
- **Content types**: Service pages, cost guides, comparisons, educational blog posts
- **E-E-A-T signals**: C-10 license, EVITP certification, 15+ years experience, project gallery

## Deployment Checklist
1. Edit HTML files
2. Run nav/sitemap update scripts
3. `git add -A && git commit -m "..."`
4. `git push` (triggers Cloudflare auto-deploy)
5. Run IndexNow submission for new/updated URLs

## Last Updated
September 15, 2026
