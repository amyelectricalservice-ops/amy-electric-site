# Competitor Study — The Electric Connection (Electric Connection LA)

**Domain:** `theelectricconnection.com` ⚠️ *not* `electricconnectionla.com`
**Date:** 2026-10-18 · **Workflow:** 4 (`competitor-analysis`) · **Primary named target**

> **Best action:** they beat AMY on **breadth of intent coverage** (panel-brand hazard pages,
> per-manufacturer EV pages, insurance/mandate content, themed review pages) — not on depth.
> AMY's core service pages are already **longer** than theirs (rewiring 4,285 vs 3,817 words;
> panel 5,204 vs 4,100). Copy their *coverage*, not their *length*, and beat them on local
> photography and a real estimator.

---

## Domain correction (evidence)

`competitors/README.md` listed `electricconnectionla.com *(verify)*`. Verified this session:
- `electricconnectionla.com` → **does not resolve** (`curl` exit, HTTP `000`)
- Their live site is **`https://www.theelectricconnection.com/`** (HTTP 200)
- Google-affiliated profiles use "The Electric Connection" — Facebook
  `@electricconnectionlosangeles`, LinkedIn owner **Kim Hopkins**, Yelp "THE ELECTRIC CONNECTION",
  2706 S Robertson Blvd, Los Angeles, CA 90034

Every study of "Electric Connection LA" must use `theelectricconnection.com`.

---

## Snapshot

| Attribute | Value | Evidence |
| :--- | :--- | :--- |
| Domain | `theelectricconnection.com` | fetch |
| Positioning | "Los Angeles Electrician \| Licensed Insured Local Electrician" | title tag |
| Years / trust claims | "since 1979", "40+ years", **"Lifetime Guarantee"**, "Over 100+ Customer Reviews" | page copy + meta descriptions |
| Phones | `(800) 990-9490` (main), `(818) 446-0888`, `(213) 401-2334` | page copy / Yelp |
| Email | `service@electricconnection.com` | their site |
| Address | 2706 S Robertson Blvd, Los Angeles, CA 90034 | Yelp |
| Platform | WordPress (Yoast-style sitemap index) | `/sitemap_index.xml`, `/page-sitemap.xml` |
| Pages | **255 URLs** in `page-sitemap.xml` | sitemap fetch |
| City pages | **~150** `/electrician-<city>-ca/` | sitemap |
| Schema | LocalBusiness + City + State + Service + OfferCatalog + AggregateRating + BreadcrumbList + PostalAddress + OpeningHours traits | homepage JSON-LD `@type` extraction |
| Calculators | `/house-rewire-cost-calculator/`, `/ev-charger-installation-cost-calculator/` | sitemap |
| Organic traffic / keywords / backlinks | **unknown** | `[openseo: get_domain_overview → DataForSEO HTTP 401]`; `get_backlinks_overview` likewise 401 |

---

## Biggest lesson

**They monetise intent breadth with narrow, single-purpose pages.** Where AMY writes one long page,
they write a page per hazard brand (`zinsco-panel-upgrade-replace`, `federal-pacific-panel-upgrade-or-replace`,
`pushmatic-electrical-panel`, `old-fuse-boxes`), a page per EV manufacturer (Tesla, Ford, Nissan,
Porsche, Hyundai, Mitsubishi), and a page per offer (`free-ev-panel-upgrade-quote`,
`free-house-rewire-quote`, `free-ev-charger-estimate`). Each page is a separate entry point for a
separate query, and each is fed by a strong internal link graph.

## Best opportunity to beat them

Three concrete openings, all verified:

1. **Their geo pages are templated and thin-titled.** `/electrician-sherman-oaks-ca/` has
   `<title>Sherman Oaks Electrician</title>` — no service, no brand, no differentiator; the
   description is a copy-paste of the same "since 1979. 100+ customer reviews & lifetime guarantee"
   string used for Encino. AMY's `Sherman Oaks Electrician | Panel Upgrades | AMY Electric` is
   strictly better. **Do not copy their template.**
2. **They have no real project photography at scale.** `/recent-job-photos/` is one page. AMY has
   **387 real project photos**. Per-city and per-service photographic proof is an unfalsifiable
   advantage they cannot cheaply match.
3. **They reach into markets AMY doesn't need.** Roughly a third of their city pages are Orange
   County / Santa Clarita / Ventura (Costa Mesa, Brea, Yorba Linda, Newport Beach, Fillmore,
   Simi Valley, Moorpark). Their footprint is spread; AMY's 176 geo URLs can be *deeper* in the SFV
   and central LA where AMY actually works.

---

## Area | Their pattern | Evidence | AMY opportunity

| Area | Their pattern | Evidence | AMY opportunity |
| :--- | :--- | :--- | :--- |
| **Hazard-brand panel pages** | One page per panel brand/era: Zinsco, Federal Pacific, Pushmatic, old fuse boxes | sitemap URLs `[directional: web]` | AMY has only one Zinsco blog post. Propose `/federal-pacific-panel-replacement` + `/pushmatic-panel-replacement` (see `keywords/clusters.md` proposed cluster P1) |
| **Per-manufacturer EV pages** | Tesla, Ford, Nissan, Porsche, Hyundai, Mitsubishi + `/tesla-charging/`, `/tesla-universal-wall-connector/`, `/commissioning-steps-for-tesla-wall-connector/` | sitemap | AMY holds EVITP #4051604 and consolidates. Split brand intent out of `/tesla-charger-installation` (338 impr, pos 67.8) |
| **Insurance / mandate content** | `/la-county-82f-cooling-mandate/`, `/meeting-the-new-82-mandate-new-insurance-rules-…/`, `/electrical-panel-replacements-for-property-management-companies/` | sitemap | **Strongest untaken angle.** Insurance-driven panel replacement is a high-ticket, link-attracting topic AMY has zero page for |
| **Offer landing pages** | `/free-panel-upgrade-quote/`, `/free-house-rewire-quote/`, `/free-ev-charger-estimate/` | sitemap | AMY has a live estimator + `/book` — arguably better, but it isn't expressed as service-specific entry pages |
| **Themed review pages** | ~20 `/all-reviews/<theme>/` + `/recent-reviews/`, `/yelp-reviews/`, `/property-management-reviews/` | sitemap | AMY canonicalises to `/reviews` with 87 reviews; themed review pages are a low-cost content type AMY could adopt |
| **Calculators** | Rewire + EV charger cost calculators | sitemap | AMY already has a stronger engine (`05-estimate-data.js`); the gap is *promotion and indexing*, not capability |
| **Property management vertical** | Dedicated PM pages, PM reviews, multi-unit site-visit form, PM info video | sitemap | Maps to AMY's `/commercial-electrical`, `/commercial-ev-charger-installation` — matches the AAGLA/SRAR outreach in `outreach/prospects.md` |
| **Service page depth** | house-rewire 3,817 words; panel-upgrades 4,100; EV 3,747 | measured live fetch | **AMY is already deeper** (4,285 / 5,204 / 3,759). Depth is not the battleground |
| **Schema** | LocalBusiness + City + State + Service + OfferCatalog + AggregateRating | extracted | AMY is **ahead** — Electrician type on 309 pages, OpeningHoursSpecification on 248, EducationalOccupationalCredential on 244 |
| **Geo titles** | Templated, no service/brand qualifier | fetched titles | AMY's are better — keep |

---

## Top keyword themes (attributed to observed page types, not to keyword-rank data)

⚠️ **No keyword or traffic data exists for this domain** — `get_domain_overview` and
`get_ranked_keywords` both fail with `DataForSEO HTTP 401`. The themes below are inferred from their
*page inventory*, which is legitimate evidence, and are labelled as inventory-derived.

- **Panel & hazard** — Zinsco, Federal Pacific, Pushmatic, fuse boxes, 200A service, insurance-required replacement
- **Whole-house rewiring** — house rewire, cloth-insulated wiring, aluminium wiring replacement, ungrounded wiring, voltage drop
- **EV / Tesla** — EV charger installation, Tesla Home Charger, Tesla Universal Wall Connector, per-make pages
- **Emergency / service calls** — service calls, electrical troubleshooting
- **Property management** — PM panel replacements, multi-unit site visits
- **Geo** — ~150 `electrician-<city>-ca` pages across LA County, SFV, Orange County, Ventura
- **Lighting** — lighting installation, recessed, track, pendant, landscape lighting

## Content / page types working for them

Single-intent service pages · brand-hazard pages · per-manufacturer EV pages · cost calculators ·
free-quote offer pages · themed review pages · city pages · topical "tips/" mini-pages
(`/tips/circuit-breaker-troubleshooting/`, `/tips/smoke-detectors/`, …18 of them) ·
video testimonial pages · property-management vertical pages.

## Backlink / authority notes

**`unknown`.** `get_backlinks_overview` for their domain returned `DataForSEO HTTP 401`, so no total
backlinks, referring domains, authority score or anchor distribution could be obtained. Any authority
claim would be fabrication. Inference only: their 40+ year history, Yelp presence (145 photos listed
on the Yelp profile) and "lifetime guarantee" messaging suggest established local citations, but this
is **unverified**.

## Head-to-head SERP observations

⚠️ **No SERP data.** `get_serp_results` fails (HTTP 401), so no confirmed ranking comparison exists
for any query. What can be said from evidence:

- Both sites target the same clusters: emergency, panel upgrade, whole-home rewiring, EV/Tesla,
  and the same SFV/Central-LA cities (their list includes Sherman Oaks, Encino, Woodland Hills,
  Van Nuys, Burbank, Glendale, Santa Monica, Culver City, Calabasas — an almost exact overlap with
  AMY's 112 city pages).
- AMY's `/whole-home-rewiring` receives 40 impressions at pos 24.6; `/blog/whole-home-rewiring-guide`
  gets 3,444 at pos 37.7. Their equivalent is a single purpose-built 3,817-word page. AMY's
  impressions are reaching a blog post, theirs reach a converter.
- **Direct conflict:** if their `/electrician-sherman-oaks-ca/` and AMY's `/city-sherman-oaks`
  compete for `electrician sherman oaks` (296 impressions, AMY at **pos 37.0**), AMY is losing that
  query despite having the better title.

## Priority actions for AMY Electric

1. **P0 — Build the hazard-brand panel pages** they have and AMY doesn't (Federal Pacific, Pushmatic,
   old fuse boxes). AMY already ranks for Zinsco intent via one blog post.
2. **P0 — Own the insurance/mandate angle.** They have two dedicated pages on the LA County 82°F
   cooling mandate + insurance panel rules. AMY has none. High-ticket, link-worthy, and squarely
   within AMY's licence.
3. **P1 — Split brand intent** out of `/tesla-charger-installation` so one page isn't fighting for
   `tesla charger installation` (pos 67.8) and `tesla charger vs others` (pos 17.3) at once.
4. **P1 — Deploy the 387 photos by city and service.** This is the one place AMY can win outright.
5. **P2 — Adopt the cheapest page types they have:** themed review pages and service-specific quote
   pages, both of which AMY can generate from existing assets.
6. **Do not** copy: templated city titles, the duplicated phone numbers across the site, or a
   `wp-sitemap`-style URL sprawl.

---

## Evidence vs inference

**Evidence (measured this session):** domain resolution; title/description strings; JSON-LD `@type`
inventory; sitemap URL counts and patterns; measured word counts of three service pages
(3,817 / 4,100 / 3,747); phones, email, address; Yelp/LinkedIn/Facebook profile existence.

**Inference (labelled):** which clusters they "win"; that their content is thin behind JS on
some pages; that their authority is high. Their traffic, keyword count, backlinks, and any specific
ranking position are **unknown** — no tool returned them.

## Sources

- `[directional: web]` — `https://www.theelectricconnection.com/` fetch (title, description, JSON-LD `@type` list)
- `[directional: web]` — `https://www.theelectricconnection.com/page-sitemap.xml` → 255 `<loc>` URLs (full list reviewed)
- `[directional: web]` — measured word counts: `/house-rewire/` 3,817 · `/panel-upgrades/` 4,100 · `/electric-vehicle-ev-charger-installation/` 3,747
- `[directional: web]` — fetched titles for `/electrician-sherman-oaks-ca/`, `/electrician-encino-ca/`
- `[directional: web]` — websearch results: Yelp profile (2706 S Robertson Blvd), LinkedIn (Kim Hopkins, Owner), Facebook `@electricconnectionlosangeles`
- `[directional: web]` — `electricconnectionla.com` does not resolve (HTTP 000)
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — prior tiering (dated 2026-06-03; page counts and AMY description within it are stale)
- `[openseo: get_domain_overview / get_backlinks_overview / get_ranked_keywords / get_serp_results → DataForSEO HTTP 401]` — traffic, keyword, backlink and SERP data unavailable
- `[repo: index.html / ev-charger-installation.html]` — AMY schema `@type` inventory for the comparison; `[repo: grep -l]` counts (Electrician 309, OpeningHoursSpecification 248, EducationalOccupationalCredential 244)
