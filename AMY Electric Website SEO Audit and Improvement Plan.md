# AMY Electric: Website SEO Audit and Improvement Plan

- [ ] Oct 22, 2026 · @Amy

## Executive summary

amyelectric.com has strong topical depth and local relevance, but out-of-date facts, contradictory claims and a very large set of templated city pages are holding back trust and search performance. Overall: needs work, with good bones.

Biggest strength: dedicated pages for every service, long FAQs, cost tables, permit and utility detail, and credentials (C-10 #981578, EVITP #4051604) placed in titles and on every page.

**Top 3 priorities**

1. Correct outdated and conflicting facts: the federal 30C credit expired June 30, 2026, the LADWP rebate is now larger than the site says, and prices, timelines, project counts and experience years disagree between pages.
2. Fix trust signals: two different testimonial sets with the same names in different cities, an unverifiable review count, and insurance wording that should be checked against the public contractor license record.
3. Consolidate duplicate URLs and audit the roughly 110 templated city pages before they dilute the whole site.

| Area | Rating | Why |
| --- | --- | --- |
| Content depth | Strong | Service, FAQ, cost and permit content on every core page |
| Factual accuracy | Needs work | Expired federal credit, outdated rebate, conflicting prices and counts |
| Trust signals | Needs work | Conflicting testimonials, review math, insurance wording |
| On-page basics | Good | Unique titles and descriptions, canonicals, OG tags; some titles over 60 characters |
| Site structure | Needs work | Duplicate URLs, inconsistent internal links, a template bug |
| Local and off-site | Needs work | Yelp address typo and mismatched listing text |
| Technical (speed, schema, sitemap) | Not measured | No tool connected; checks listed in the plan |

Scope: I read the homepage, EV charger page, panel upgrade page, reviews page, service-areas page, one city page and one blog post, plus public listings. Rankings, volumes, backlinks and speed were not measured.

## Findings

The site's biggest risks are factual, not structural: the same claim appears with different numbers on different pages. Search engines and AI answer engines both penalize that.

### Trust and accuracy

| # | Issue | Where | Severity | Fix |
| --- | --- | --- | --- | --- |
| 1 | Federal 30C charger credit shown as current and "through 2032"; it ended June 30, 2026 | EV charger page, EV cost blog, Tesla page | Critical | Remove or replace with a one-line "ended" note |
| 2 | LADWP rebate appears as $200 (Tesla page), $500 (homepage, EV page, blog), $1,000–$1,500 (blog intro) and $1,000 (Winnetka page) | Five pages | Critical | Use one current figure with a link to LADWP |
| 3 | Three different testimonial sets (homepage, /reviews, /testimonials); Maria T. is in Burbank on one and Glendale on another, James K. in Studio City and Pasadena | Homepage, /reviews, /testimonials | Critical | One verified set tied to real Google or Yelp reviews |
| 4 | Pages claim workers' comp and a team of electricians; a public license-record mirror lists workers' comp as exempt (no employees) | Site-wide | Critical (verify) | Check cslb.ca.gov and make the wording match |
| 5 | Founder is "Amy ... her" on the About page and "Amram ... he" on service and blog pages | About, EV page, blog bylines | High | One public name and pronoun everywhere: use Amram and "he" (the About page says Amy and "her") |
| 6 | Experience: "15+ years" and "14+ years" on the same About page; license issued 2013 | About, homepage, blog | High | State founding year (2012) and let readers compute it |
| 7 | Project counts: "2,000+ projects" (homepage), "over 200 completed projects" (blog byline), "200+ EV chargers" and "thousands" (About) | Four pages | High | One defensible number per claim |
| 8 | "87 verified 5-star reviews" next to a 4.9 rating; "87" and "87+" used interchangeably | Homepage, /reviews, About | High | Match the live Google count and rating exactly |
| 9 | Pricing and timing conflict: EV install low end $350 vs $500; 2–4 hours vs 1–2 days vs 3–5 hours; permit $150–$400 vs $75–$200; Zinsco/FPE $2,000–$3,600 vs $2,800–$4,800 | EV, Tesla, panel pages, blog | High | One pricing source of truth |
| 10 | "Tesla-Certified Installers" and a 4-year warranty claimed without support; Wall Connector speed 44 vs 35+ miles per hour | Tesla page | Medium | Remove or substantiate |
| 11 | "24/7" and "same-day" claims vs listed Mon–Fri 7 AM–5 PM hours | City pages, homepage, Yelp | Medium | Align claim and hours |
| 12 | All four case studies are illustrative, not real jobs (labeled honestly) | /case-studies | Medium | Replace with real projects and photos over time |

### On-page

| Page | Issue | Severity | Fix |
| --- | --- | --- | --- |
| Homepage, EV page, EV cost blog | Title tags run about 62–64 characters with credential numbers that truncate in results | Medium | Keep titles to 60 characters; move license numbers to descriptions |
| Several pages | og:title differs from the title tag | Medium | Align them |
| Beverly Hills city page | Heavily templated; two FAQ answers repeat the same permit point | High | Add real local detail and projects |
| Winnetka city page | Best local page: about 650–700 words, a dated February 2026 project, LADWP detail. Still about 65–75% template | Medium | Use as the model for the top city pages |
| Tesla page | "At a Glance" says $350–$1,200 while the headline range is $500–$1,200 | Medium | Reconcile |
| Meta descriptions | Specific, with prices and phone; homepage sits near the length limit | Low | Trim a few words |
| Images | Descriptive alt text on images checked | Pass | Keep |

### Site structure

| Issue | Detail | Severity | Fix |
| --- | --- | --- | --- |
| Home URL | Internal links point to /index while the canonical is / | High | Link to / and redirect /index |
| Reviews URL | Navigation points to /reviews on some pages and /testimonials on others | High | One URL, 301 the other |
| Emergency URL | Three variants: /emergency-electrician-los-angeles, /emergency-electrical, /emergency-electrician | High | One URL, 301 the rest |
| Blog duplicates | EV cost and whole-home rewiring cost each exist at two slugs (-la and -los-angeles); /panel-upgrade-signs is listed twice as "7 Signs" and "8 Signs"; /choosing-electrician-la and /smart-home-electrical-upgrades are also listed twice | High | Merge, redirect, keep the stronger version |
| Blog index | Header says 33 articles; the list shows 62 entries (61 unique URLs) with no dates | Medium | Fix the count; show publish and update dates |
| Topic overlap | Five or more posts each on panel signs, rewiring and smart-home topics | Medium | Merge into pillar pages |
| Location pages | About 110 city pages plus about 24 EV and 24 panel city variants | High | Keep and deepen the top 15–20; merge or noindex the rest |
| /service-areas | Heading reads "All %d Service Areas"; text says "Winnetka plus 16 cities" above a list of 100+ | High | Fix the template bug and the wording |

### Technical

| Check | Status | Details |
| --- | --- | --- |
| HTTPS | Pass | Every page loaded over https |
| Mobile viewport | Pass | Meta tag present on pages checked |
| Canonicals and robots meta | Pass | Self-canonical, index and follow; /index link conflict noted above |
| Open Graph and Twitter tags | Pass | Present with images |
| robots.txt and sitemap.xml | Unverified | Could not be fetched with the tools available |
| Structured data | Unverified | Not visible in the fetched output; test with Google's Rich Results Test |
| Broken links | Unverified | Not crawled |
| Page speed and Core Web Vitals | Not measured | Run PageSpeed Insights |

### Off-site listings

| Listing | Issue | Fix |
| --- | --- | --- |
| Yelp | Street spelled "Londeliues" (site and license record say Londelius); specialties text has typos and omits EV and panel work; hours 7–5 | Correct address and rewrite the description |
| CALeVIP | Service area "Anywhere in California" and a generic description | Narrow to Los Angeles and add EV detail |
| License record | Public record shows the license expiring March 31, 2027 | Calendar a renewal reminder now |
| Google Business Profile | Not checked | Confirm name, address, phone, hours and review count match the site |

## Keyword opportunities

The fastest wins are rebate, credential and near-home neighborhood terms, where the site already has pages and competitors show little depth. Difficulty and opportunity are my judgment; search volume and current rankings were not measured, so pull rankings from Search Console.

| Keyword | Difficulty | Opportunity | Intent | Recommended content |
| --- | --- | --- | --- | --- |
| LADWP EV charger rebate 2026 | Easy | High | Informational / commercial | Rewrite the rebate guide with current amounts |
| EVITP certified electrician Los Angeles | Easy | High | Commercial | Promote the existing EVITP post to a landing page |
| Tesla Wall Connector installation Los Angeles | Moderate | High | Transactional | Strengthen the existing Tesla page |
| EV charger installation Sherman Oaks, Studio City, Encino | Moderate | High | Transactional | Deepen the existing city pages |
| Electrician Winnetka, West Hills, Northridge | Easy | High | Transactional | Home-base neighborhood pages |
| EV charger installation cost Los Angeles | Moderate to hard | High | Commercial | Merge the two duplicate cost posts |
| EV charger for condo or apartment (AB 2565) | Easy | Medium | Informational | Tenant and HOA guide |
| NEMA 14-50 outlet installation Los Angeles | Easy | Medium | Transactional | Standalone page |
| Do I need a panel upgrade for an EV charger | Moderate | Medium | Informational | Add FAQ markup to the comparison page |
| 200 amp panel upgrade cost Los Angeles | Hard | Medium | Commercial | Update with one consistent price range |
| Federal Pacific or Zinsco panel replacement Los Angeles | Easy to moderate | Medium | Transactional | Safety-led landing page |
| LADBS electrical permit for EV charger | Easy | Medium | Informational | Consolidate the existing permit posts |
| Whole-home rewiring cost Los Angeles | Moderate | Medium | Commercial | Merge the duplicate rewiring posts |
| Commercial or multi-unit EV charging Los Angeles | Moderate | Medium | Commercial | B2B page with real project proof |
| Emergency electrician Los Angeles | Hard | Low to medium | Transactional | Align the 24/7 claim with real hours first |

## Content gaps and competitors

The blog already has 61 unique posts, so the gaps are in proof, consolidation and a few missing topics rather than volume.

| Gap | Why it matters | Format | Priority | Effort |
| --- | --- | --- | --- | --- |
| Real project pages with photos and permit details | All four case studies are illustrative; real proof lifts trust and conversions | Case studies | High | Multi-day, ongoing |
| One consolidated EV cost post | Two near-identical posts compete with each other | Merge and 301 | High | Half day |
| LADWP rebate guide refresh | Current guide carries wrong amounts and a federal credit that ended | Rewrite | High | Quick win (1–2 hours) |
| EVITP landing page | An EVITP post exists but is buried; credential searchers need a landing page | Promote post to page | Medium | Half day |
| Condo and renter EV charging (AB 2565) | No post on the topic in the 62-entry list | Guide | Medium | Half day |
| Load management and power sharing | Answers the "do I need a panel upgrade" objection | Blog | Low | Quick win |
| Commercial and multi-unit EV charging | Only a general commercial post; no dedicated page with real work shown | Landing page | Medium | Half day plus real project |

### Competitor comparison

This comparison is directional, from public pages and listings only. Backlinks, speed and rankings were not measured.

| Dimension | AMY Electric | [Trout Electric](https://www.troutelectricusa.com/cities-we-serve/southern-california/los-angeles/los-angeles-ev-charger-installation/) | [Ready Electric](https://www.mannpublications.com/mannreport/2026/06/13/ready-electric-expands-24-7-licensed-electrician-services-across-los-angeles/) | [911 Construction & Electric](https://calevip.org/evsp/911-construction-electric-inc) |
| --- | --- | --- | --- | --- |
| EV-specific LA page | Yes: costs, process, rebates, FAQs | Dedicated LA home EV charger page with free estimates | EV listed among general services | CALeVIP profile mentions Level 2 and 3 installs |
| Local targeting | 16 featured cities plus about 100 more pages | LA city page | Names neighborhoods such as Highland Park, Eagle Rock and Silver Lake | Greater LA |
| Credentials shown | C-10 and EVITP in titles | Not seen | Licensed, insured, bonded | C-10, General B, EVITP |
| Off-site presence | Yelp and CALeVIP need cleanup | Not checked | June 2026 press release | CALeVIP profile, founded 2017 |

AMY has more visible content depth than the competitor pages I saw. The closest credential rival is 911 Construction & Electric, which also lists EVITP.

## Improvement plan

Three phases, about 10 hours this week, 15–20 hours over the next month, and an ongoing quarter of content work. Each phase fixes trust first, then structure, then growth. All tools listed are free.

### Phase 1: This week (about 8–10 hours)

| # | Task | Time | Impact | Tool |
| --- | --- | --- | --- | --- |
| 1 | Correct the 30C credit and LADWP rebate everywhere (search the site folder for "30C", "2032", "$500", "ChargeUp") | 2 hours | High | Editor search; the fix sheet already covers the pages I read |
| 2 | Write one facts sheet (prices, install times, permit fees, years, project counts, hours), then update every page to match | 2–3 hours | High | Spreadsheet or text file |
| 3 | Use Amram and "he" everywhere; update About, byline and quotes | 30 min | Medium | Editor |
| 4 | Replace the three testimonial sets with one set copied from real, consenting Google or Yelp reviews | 1–2 hours | High | Google Business Profile export |
| 5 | Check workers' comp status at the contractor license board and fix the insurance wording | 30 min | High | cslb.ca.gov |
| 6 | Fix the "%d" bug; link to / instead of /index; one Reviews URL; one emergency URL; add 301 redirects | 1–2 hours | High | \_redirects (Netlify) or vercel.json (Vercel) |
| 7 | Fix the Yelp address spelling and description; narrow the CALeVIP service area | 30 min | Medium | Yelp and CALeVIP dashboards |
| 8 | Set a calendar reminder for the March 31, 2027 license renewal | 5 min | Medium | Calendar |

### Phase 2: Weeks 2–4 (about 15–20 hours)

| # | Task | Time | Impact | Tool |
| --- | --- | --- | --- | --- |
| 1 | Merge duplicate blog posts (EV cost, rewiring cost, panel signs, smart home, choosing an electrician) and redirect; fix the "33 articles" count; show dates | 4 hours | High | Editor, redirects file |
| 2 | Trim titles to 60 characters; align og:title with each title tag | 1.5 hours | Medium | Editor |
| 3 | Rewrite the LADWP rebate guide with current amounts and a link to LADWP | 1.5 hours | High | Editor |
| 4 | Verify the site in Search Console, submit the sitemap, review the Pages report; run PageSpeed Insights on three pages and Google's Rich Results Test; crawl the site | 2–3 hours | High | Google Search Console, PageSpeed Insights, Rich Results Test, Screaming Frog (free to 500 URLs) |
| 5 | Decide which city pages to keep, merge or noindex, using Search Console impressions | 3 hours | High | Search Console |
| 6 | Confirm the Google Business Profile matches the site (name, address, phone, hours, review count) | 30 min | Medium | Google Business Profile |
| 7 | Add real photos and details to the first two case studies | 2–3 hours | High | Phone photos from recent jobs |

### Phase 3: This quarter (November to January)

| # | Task | Time | Impact | Tool |
| --- | --- | --- | --- | --- |
| 1 | Deepen the top 15–20 city pages using the Winnetka page as the model: a real project, the permit office, local specifics | About 1 hour each | High | Editor, job photos |
| 2 | Publish the EVITP landing page, condo and renter guide, and commercial EV page | 6–8 hours | Medium | Editor |
| 3 | Turn all four case studies into real projects | Ongoing | High | Job photos |
| 4 | Ask every finished customer for a Google review using your review link | 15 min a week | High | Google review link |
| 5 | Re-audit in January with real ranking and traffic data; set targets | 3 hours | Medium | Search Console, Bing Webmaster Tools |

Track three numbers monthly: Search Console clicks on EV and panel terms, calls and form submissions, and Google review count.

## What was not measured

No SEO tool was connected, so these items need your own free checks before the January re-audit.

| Not measured | Free way to measure |
| --- | --- |
| Rankings and search volume | Google Search Console performance report |
| Page speed and Core Web Vitals | PageSpeed Insights |
| Structured data (schema) | Google Rich Results Test |
| robots.txt and sitemap.xml | Open both in a browser; check Search Console sitemaps |
| Broken links and redirects | Screaming Frog free crawl |
| Backlinks | Bing Webmaster Tools and Search Console links report |
| Google Business Profile details and live review count | Google Business Profile dashboard |

## Sources

Site pages were opened in full on October 22, 2026. External facts below come from search-result excerpts, not full page reads, so confirm amounts before publishing.

**Site pages reviewed**

- [Homepage](https://amyelectric.com/index), [EV charger installation](https://amyelectric.com/ev-charger-installation), [Panel upgrade](https://amyelectric.com/panel-upgrade), [Tesla charger installation](https://amyelectric.com/tesla-charger-installation)
- [Reviews](https://amyelectric.com/reviews), [Testimonials](https://amyelectric.com/testimonials), [About](https://amyelectric.com/about), [Case studies](https://amyelectric.com/case-studies/), [Service areas](https://amyelectric.com/service-areas)
- [Beverly Hills page](https://amyelectric.com/city-beverly-hills), [Winnetka page](https://amyelectric.com/city-winnetka), [EV cost blog post](https://amyelectric.com/blog/ev-charger-installation-cost-la), [Blog index](https://amyelectric.com/blog/)

**External facts**

- Federal 30C credit ended June 30, 2026: [Federal EV Charger Tax Credit Ended June 30, 2026](https://eviqo.io/blogs/news/federal-ev-charger-tax-credit-2026-how-to-claim-30-back-section-30c)
- LADWP residential charger rebate ($1,000 plus $500 for Lifeline or EZ-SAVE): [LADWP electric vehicle programs](https://acquia.ladwp.com/residential-services/programs-and-rebates-residential/electric-vehicles)
- $250 dedicated EV meter rebate: [LADWP rebate overview](https://solaroptimum.com/ladwp-ev-charger-rebate/)
- License record mirror (workers' comp exempt, expires March 31, 2027): [License record for #981578](https://www.prelien.co/contractor/a-m-y-electric-981578)
- Yelp listing: [AMY Electric on Yelp](https://yelp.com/biz/amy-electric-los-angeles)
- CALeVIP listing: [AMY Electric on CALeVIP](https://calevip.org/evsp/amy-electric)
- Competitors: [Trout Electric](https://www.troutelectricusa.com/cities-we-serve/southern-california/los-angeles/los-angeles-ev-charger-installation/), [Ready Electric](https://www.mannpublications.com/mannreport/2026/06/13/ready-electric-expands-24-7-licensed-electrician-services-across-los-angeles/), [911 Construction & Electric](https://calevip.org/evsp/911-construction-electric-inc)
