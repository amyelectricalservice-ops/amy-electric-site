# AMY Electric Website Audit — September 2026

**Site reviewed:** amyelectric.com (homepage, a service page, a city page, testimonials page)

## The headline finding

Your site has genuinely grown into a strong, mature local-SEO build — service × city page matrix, 30+ blog articles, structured FAQs, pricing tables, case studies. That part is working. But I found a **real trust/credibility bug**: the homepage reuses the same 3 customer quotes in two different sections, and attributes them to **different cities each time**.

| Quote (same text) | Homepage block 1 | Homepage block 2 |
|---|---|---|
| Tesla Wall Connector, "one afternoon," permit handled | **David R. — Sherman Oaks, CA** | **David R. — Burbank, CA** |
| Old 100A panel, full 200A upgrade, LADWP | **Maria T. — Burbank, CA** | **Maria T. — Los Angeles, CA** |
| Flickering lights, breaker, 20-minute diagnosis | **James K. — Studio City, CA** | **James K. — Glendale, CA** |

The `/testimonials` page then shows a **third, entirely different** set of six reviews (Michael R., Lisa T., David K., etc.) that don't overlap with either homepage set. None of this means the reviews are fake — it reads like a template/placeholder mismatch from when the city pages were built. But if a customer, a competitor, or Google's spam systems notice the same review with two different cities on the same page, it looks manufactured. This is the single highest-priority fix on this list.

## What's working well

- **Technical foundation**: canonical tags, meta descriptions, OG/Twitter cards, and `index, follow` robots directives are present and correct on every page I checked.
- **E-E-A-T signals**: license number (C-10 #981578), EVITP #4051604, CSLB verify link, founding year, and project count are repeated consistently across pages — good for both human trust and AI answer engines.
- **Topical depth**: dedicated pages for panel upgrades × 16 cities, a large blog library (code guides, cost breakdowns, comparison posts), and "at a glance" summary boxes at the top of service pages — this is exactly the structure AEO/GEO engines like to lift answers from.
- **Local specificity**: the Sherman Oaks page name-checks Ventura Blvd, Kester Ave, and Notre Dame High School rather than generic filler — that's real local signal, not just a city name swapped into a template.
- **Honest disclaimers**: case studies are labeled "illustrative profile — actual scope depends on the property," which protects you from misrepresentation claims.
- **Pricing transparency**: line-item cost tables ($2,500–$4,500 for a 200A upgrade, etc.) are the kind of concrete, quotable content AI Overviews and ChatGPT tend to cite directly.

## Issues found, by priority

### 🔴 Fix now
1. **Testimonial city mismatch** (above) — same quotes, conflicting cities, across the homepage.
2. **Founder pronoun inconsistency** — the "Meet Amy" bio uses "he/his" throughout; this was already flagged in earlier SEO work as a name/pronoun mismatch versus other listings (Yelp, GBP). Inconsistent identity details across the web are a known trust signal AI answer engines check before citing a business — worth reconciling everywhere it appears once, rather than per-page.
3. **Reused stock quote across pages** — "AMY Electric installed our Tesla Wall Connector in one afternoon..." appears essentially verbatim as three separate "different" customers. Same for the Maria T./200A-upgrade quote. Real customer reviews rarely read identically; this pattern is what makes it look templated.

### 🟡 Fix soon
4. **Unverifiable schema claims** — memory from earlier work says JSON-LD (LocalBusiness/Service schema) was added sitewide, but I can't confirm it's still valid from a text fetch. Run the pages through Google's Rich Results Test to confirm nothing broke as the site grew.
5. **City page uniqueness at scale** — you now have 16 cities × multiple services (panel-upgrade-sherman-oaks, panel-upgrade-burbank, etc.), likely 50+ near-duplicate templated pages. The one I checked (Sherman Oaks) had good unique local detail, but at this volume it's worth spot-checking 4–5 more to make sure they're not just city-name-swapped duplicates — Google increasingly treats large sets of thin, near-identical location pages as low-value/doorway content.
6. **Review count discrepancy risk** — "87 5-Star Reviews" and "4.9 stars · 87 Google Reviews" appear in two places; make sure this number is pulled live from GBP (or updated on a schedule) rather than hardcoded, since a stale count is an easy thing for a customer to catch.

### 🟢 Nice to have
7. **Core Web Vitals** — I couldn't run PageSpeed Insights directly from here; recommend testing key pages (homepage + top 2 service pages) manually.
8. **Blog internal linking** — 30 articles is a great asset; confirm each links back to at least one service/city page and vice versa, so link equity flows both directions.

## The plan

| Phase | Task | Effort | Cost |
|---|---|---|---|
| **1. Trust fixes (this week)** | Reconcile the testimonial sets — pick one canonical, accurate set of reviews per placement, pull real ones from GBP/Yelp if the current ones are placeholders | 2–3 hrs | Free |
| | Standardize Amy's pronoun/name presentation across the "Meet Amy" bio and cross-check against GBP/Yelp listings | 30 min | Free |
| **2. Verification (next 1–2 weeks)** | Run homepage + panel-upgrade + one city page through [Google Rich Results Test](https://search.google.com/test/rich-results) to confirm schema is intact | 1 hr | Free |
| | Run [PageSpeed Insights](https://pagespeed.web.dev) on homepage, panel-upgrade page, and a city page (mobile + desktop) | 30 min | Free |
| | Spot-check 5 more city pages for genuine local uniqueness (street names, landmarks, not just find-replace) | 2 hrs | Free |
| **3. Sustaining (ongoing monthly)** | Confirm GBP review count/rating shown on-site matches live GBP | 10 min/mo | Free |
| | Add 1–2 new blog posts targeting question-style queries (good for AI Overviews) | 2–3 hrs/mo | Free (your time) |
| | Re-run Rich Results Test after any template change | 15 min | Free |

**Total to clear the 🔴 and 🟡 items: roughly 6–7 hours, all free tools.**

Want me to draft the corrected testimonial set and the reconciled founder bio copy next?
