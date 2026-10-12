# MAPS-ANALYSIS-amyelectric.com.md

Maps platform presence audit for **AMY Electric** (amyelectric.com).
Generated 2026-10-12. Method: Tier 0 (free) — no DataForSEO, no Google Maps Platform key.

## 1. Maps Health Score: 67/100

| Dimension | Score | Basis |
|---|---|---|
| Street address published + in schema | 15/15 | 20628 Londelius St, Winnetka, CA 91306, in footer + `PostalAddress` on all pages |
| Phone consistency (site-internal) | 10/10 | +1-818-302-5614 in schema, (818) 302-5614 in copy, 11x homepage |
| Hours schema-vs-visible agreement | 5/10 | Schema says MF closes 17:00 / Sat 14:00; visible copy says 6 PM / 4 PM |
| Schema completeness (maps-relevant) | 10/15 | `geo`, `address`, `areaServed` present; `hasMap` missing everywhere; no Maps embed |
| OpenStreetMap business presence | 0/10 | Nominatim name search for "AMY Electric, Winnetka, CA" returns zero results |
| Review signals usable by Google | 4/10 | 4.9★/87 claimed on-site and in `aggregateRating` on 304 pages — Google ignores self-published LocalBusiness review markup |
| Profile-URL consistency | 8/10 | Yelp `amy-electric-los-angeles` on 245 pages, but `amy-electric-winnetka` on 1 page |
| Cross-platform verifiability | 5/10 | Google/Bing/Apple listings could not be confirmed at Tier 0 (see §7) |
| Service-area coverage in schema | 10/10 | `areaServed` on 305 pages; 16 city pages + service-areas hub |

## 2. Capability tier: Tier 0 (Free)

No DataForSEO MCP tools and no Google Maps Platform key are available in this
environment, so this is a **Tier 0** analysis. Available: Nominatim geocoding,
Overpass (attempted — see §6), website-signal extraction, static GBP checklist,
schema review. **Not available**: geo-grid rank tracking + SoLV, live GBP
profile audit, review velocity/sentiment, GBP post/Q&A data, Tripadvisor/
Trustpilot pulls. The skill's `references/` files are absent from the installed
skill (only `SKILL.md` + `LICENSE.txt` ship), so free-API query templates were
reconstructed from the Overpass/Nominatim public APIs directly.

## 3. Geo-grid rank tracking: not run (Tier 1+)

Requires DataForSEO Maps SERP per-coordinate calls. A 7x7 grid (49 points) was
not executed — no credits available and none consumed (**cost report: $0**).
Recommend re-running with `/seo maps grid "electrician" "Winnetka, CA"` once
Tier 1 exists; center on the rooftop coordinate below, not the schema one.

## 4. GBP profile audit (Tier 0 manual)

25-field checklist reduced to what is website-detectable:

| # | Field | Status | Evidence |
|---|---|---|---|
| 1 | Business name | Present | `name: AMY Electric` in schema, all pages |
| 2 | Address | Present | Footer + schema, all pages |
| 3 | Phone | Present | tel:+1-818-302-5614 |
| 4 | Website | Present | Self-evident |
| 5 | Primary category signal | Present | `@type: Electrician` |
| 6 | Hours | **Mismatch** | Schema MF 07:00–17:00 / Sat 08:00–14:00 vs visible Mon–Fri 7–6 / Sat 8–4 |
| 7 | Service area | Present | 16 city pages, `areaServed`, ZIP list |
| 8 | Geo coordinates | Present, verify | Schema 34.22281, -118.58241 vs Nominatim rooftop 34.22903, -118.58282 (~700 m apart) |
| 9–25 | Photos, posts, Q&A, attributes, booking link, services list, reviews, responses, etc. | **Unknown — requires Tier 1** | Not detectable from the website |

## 5. Review intelligence: not available live (Tier 1+)

What is known is all self-published: 4.9 stars / 87 reviews claimed in copy
and stamped into `aggregateRating` on 304 of ~312 production pages. Two
cautions: (a) Google explicitly ignores review markup a LocalBusiness places
about itself, so this markup buys no rich-result eligibility; (b) the count
is static text — if the real Google/Yelp counts have moved on, site and
profiles disagree, which erodes trust. Verify the live counts and either sync
the number or drop the markup. No velocity, distribution, response-rate, or
fake-review analysis is possible without review-API access.

## 6. Competitor landscape (Tier 0, degraded)

Overpass was attempted three ways (main instance GET+POST, two mirrors).
`overpass-api.de` returns `406 Not Acceptable` on this network path;
`overpass.kumi.systems` and `overpass.private.coffee` answered one trivial
probe but timed out (empty body) on every real query. **No OSM competitor
enumeration was obtained** — treat density as unknown rather than zero.

Qualitative landscape from web search (Winnetka / Canoga Park / SFV 91306):

| Competitor | Signal |
|---|---|
| The Electric Connection (theelectricconnection.com) | Dedicated Winnetka page, "100+ reviews" messaging |
| Robinson's Electric | Experience.com top-rated Winnetka listing |
| U.S. Electric Force | BuildZoom top-15% CA contractor, 5/5 Yelp SFV |
| Alpha One Electric / EC Electric | 5/5 Yelp SFV |
| LED Guys, Kennedy Electric | Canoga Park same-day positioning |

Takeaway: the immediate radius is contested by review-heavy incumbents and
lead-gen platforms (Yelp, HomeAdvisor, BuildZoom, Angi). AMY's differentiators
on maps would be EV-charger specialization (EVITP) + the 16-city content
footprint, but neither is visible without a claimed, categorized GBP.

## 7. Cross-platform presence

| Platform | Status |
|---|---|
| Google (GBP / Maps) | **Unconfirmed.** Cannot verify existence, claim state, or categories at Tier 0. Highest-value unknown in this report. |
| Bing Places | **Unconfirmed.** bing.com/maps is JS-gated; fetch returns a shell. Manual check required. |
| Apple Maps / Business Connect | **Unconfirmed.** No public API; check businessconnect.apple.com. |
| OpenStreetMap | **Absent as a business.** Address resolves (house 20628 Londelius St, 34.22903, -118.58282) but no `craft=electrician` node/way carries the AMY Electric name. Adding one is free and feeds every OSM consumer. |
| Yelp | Present — but split: `amy-electric-los-angeles` (245 pages) vs `amy-electric-winnetka` (`blog/is-your-home-ev-ready-los-angeles.html` only). |

## 8. Schema recommendation

Do not add more `aggregateRating` (already everywhere, and self-serving).
Concrete JSON-LD fixes, homepage first:

1. **Add `hasMap`** pointing at the Google Maps listing URL once claimed
   (e.g. `"hasMap": "https://www.google.com/maps/search/?api=1&query=AMY+Electric+Winnetka+CA"` as a placeholder is *not* recommended — add only the real listing URL).
2. **Fix hours mismatch**: schema MF `17:00` vs visible `6 PM`; Sat `14:00` vs visible `4 PM`. Pick the true hours, change both together. (The 00:00–23:59 emergency entry is fine.)
3. **Fix the one divergent Yelp URL** in `blog/is-your-home-ev-ready-los-angeles.html` → `amy-electric-winnetka` should be `amy-electric-los-angeles` (or vice versa — but pick one).
4. **Verify the map pin**: schema `34.22281, -118.58241` sits ~700 m from the Nominatim rooftop `34.22903, -118.58282`. Confirm which is the shop door and use it everywhere.

## 9. Top 10 prioritized actions

1. **[Critical] Confirm/claim the Google Business Profile** (category: Electrician; add EV-charging + panel-upgrade services). Everything else is commentary until this exists.
2. **[Critical] Reconcile schema hours with visible hours** (MF 5 PM vs 6 PM, Sat 2 PM vs 4 PM) — a direct trust/ranking signal.
3. **[High] Add the business to OpenStreetMap** (`craft=electrician` + name/phone/website/hours) — free, permanent, feeds Apple and dozens of downstream maps.
4. **[High] Audit the live Google review count/rating vs the site's static "4.9★ 87"**; sync or drop the self-published `aggregateRating`.
5. **[High] Claim Bing Places + Apple Business Connect** with identical NAP.
6. **[Medium] Fix the single divergent Yelp URL** (`is-your-home-ev-ready-los-angeles.html`).
7. **[Medium] Add `hasMap`** once the GBP URL is known.
8. **[Medium] Verify the geo pin** (700 m schema-vs-rooftop gap) and unify.
9. **[Low] Add a Maps embed or "get directions" link** on contact/service-area pages — a Tier-0-detectable GBP signal currently absent (0 embeds).
10. **[Low] Re-run this analysis at Tier 1**: geo-grid for "electrician" + "ev charger installation" over the SFV, live GBP audit, review velocity vs the 18-day-gap rule.

## 10. Cost report

**$0.00 / 0 DataForSEO credits.** Nominatim (2 calls) and Overpass probes are free APIs; web search is unmetered here.

## 11. Limitations

- No live Google/Bing/Apple data: listing existence, rank, reviews, photos, posts, Q&A all unverified.
- No competitor enumeration (Overpass unusable on this network path) — §6 is qualitative.
- Review health (velocity, distribution, response rate, 18-day-gap check) not assessed.
- `sameAs` completeness beyond Yelp/Facebook not audited (only spot-checked).
- On-page local signals (content, internal linking, city-page quality) are seo-local territory — recommend `/seo local https://amyelectric.com` as the companion pass.
