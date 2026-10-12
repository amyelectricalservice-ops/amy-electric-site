# LOCAL-SEO-ANALYSIS-amyelectric.com.md

On-page local SEO audit for **AMY Electric** (amyelectric.com). Generated
2026-10-12. Companion to `MAPS-ANALYSIS-amyelectric.com.md`, which covers the
maps platforms; this file covers website-level signals only. No DataForSEO —
citation checks are manual, pack position and backlinks unassessed.

## 1. Local SEO Score: 59/100

| Dimension (weight) | Score | Basis |
|---|---|---|
| GBP signals (25%) | 12/25 | Correct `Electrician` subtype, visible hours; zero GBP integration — no Maps embed, place ID, review widget, or post/photo signals on any page |
| Reviews & reputation (20%) | 11/20 | 4.9★/87 claimed + `aggregateRating` on 304 pages; no recency markers, no response data, multi-platform presence unverifiable at this tier |
| Local on-page SEO (20%) | 16/20 | City+service title/H1, NAP in footer, dedicated service pages, 112 city pages with Local Knowledge + ZIPs, hub-and-spoke via service-areas (109 links), `tel:` + forms |
| NAP consistency & citations (15%) | 9/15 | Name/address/phone consistent except schema-vs-visible hours and one divergent Yelp URL; Yelp + Facebook in `sameAs`; no BBB/chamber/directory signals detected |
| Local schema markup (10%) | 8/10 | Correct `Electrician` subtype site-wide, `geo` 5-decimal, hours, phone, `priceRange`, `image`; hours mismatch costs the rest |
| Local link & authority (10%) | 3/10 | No chamber, BBB, press, "best of", or community signals detectable in page HTML |

## 2. Business type: Hybrid

Physical street address in footer + `PostalAddress` schema (brick-and-mortar
signals) combined with "serving Greater Los Angeles" language, 16 city pages,
62+ ZIP codes, and `areaServed` (SAB signals). Full NAP + map checks apply;
no SAB exemptions taken.

## 3. Industry vertical: Home Services

Signals: service-area pages, emergency service section, "free estimates",
C-10 license + EVITP certification, same-day response. Industry checks applied:
areaServed + Service coverage present; license/credential markup present
(`hasCredential` with CSLB verification URL). No review-gating language found
in quote-form copy (relevant: gating = Google fake-engagement violation +
FTC $53,088/violation).

## 4. GBP optimization checklist (website-detectable signals)

| Signal | Status |
|---|---|
| Primary category alignment (`Electrician`) | Present, correct |
| Maps embed / place ID / review widget | **Missing, all 312 pages** |
| Business hours visible on page | Present (but disagrees with schema — see §6) |
| Service-area content | Strong (16 city pages, service-areas hub) |
| Posts / photos / Q&A / booking-link signals | Not detectable (requires Tier 1) |
| GBP link-URL strategy | N/A at this tier |

Per Sterling Sky, do not point the GBP website link at the strongest organic
page if that page already ranks — use the homepage or a location hub.

## 5. Review health snapshot

- Claimed: 4.9 stars, 87 reviews (copy + `aggregateRating`, 304 pages).
- Magic threshold (10+ reviews): cleared on paper.
- 4.5★ bar (31% of consumers filter below): cleared on paper.
- Velocity / 18-day-gap rule: **unassessable** — no dates on site, no API.
- Owner responses: **unassessable** from the website.
- Risk: static "87" drifts from live counts over time; Google ignores the
  self-published markup itself, so its only function is on-site persuasion —
  which backfires the moment it disagrees with the profiles.

## 6. NAP consistency audit

| Source | Name | Address | Phone | Hours |
|---|---|---|---|---|
| Visible HTML (footer) | AMY Electric | 20628 Londelius St, Winnetka, CA 91306 | (818) 302-5614 | Mon–Fri 7–6, Sat 8–4 |
| JSON-LD schema | AMY Electric | identical | +1-818-302-5614 | **MF 07:00–17:00, Sat 08:00–14:00** |
| GBP | — | — | — | unknown (Tier 1) |

Two discrepancies, both already filed in the maps report: the hours mismatch
and `blog/is-your-home-ev-ready-los-angeles.html` pointing at Yelp
`amy-electric-winnetka` while 245 pages use `amy-electric-los-angeles`.

## 7. Citation presence check (manual, Tier 1 directories)

- Yelp: referenced (`sameAs`, 245+1 pages). Live listing status unverified.
- Facebook: referenced (`sameAs`, Amy-Electric page ID present).
- BBB / Angi / Thumbtack / HomeAdvisor / BuildZoom / Chamber: **no references
  detected** in page HTML. Whether listings exist is unknown; no links point
  to them either way.
- Data aggregators (Data Axle, Foursquare, Neustar): status unknown.
- Apple Business Connect / Bing Places: claiming recommended (ChatGPT sources
  Bing index; Apple usage doubled to 27% — BrightLocal 2026).

## 8. Local schema status

Present and valid on all pages (`schema-tool.py validate` clean). Subtype
`Electrician` is correct for the vertical. `geo` meets 5-decimal precision.
`priceRange: "$$"` follows convention. Single location + service areas, so no
`branchOf` needed. Ready-to-apply fixes:

1. Align `openingHoursSpecification` closes with visible copy (17:00→18:00
   MF if 6 PM is true; 14:00→16:00 Sat if 4 PM is true) — homepage first,
   then the shared block across all pages.
2. Add `hasMap` with the real GBP URL once claimed.
3. Leave `aggregateRating` as-is only if the numbers are synced with live
   profiles; otherwise drop it (it earns no rich results and stale numbers
   erode trust).

## 9. Location page quality (112 `city-*.html`)

Structure per page: `Electrician` JSON-LD with `areaServed` (City +
DefinedRegion/postalCode), Local Knowledge section, FAQ, BreadcrumbList.
Three are deliberately `noindex` (non-serviceable names). Swap-test result
2026-10-12 (5 sampled pages, city names + ZIPs masked, chrome stripped):
two templates exist. The **rich template** (~13–14k chars visible body;
e.g. studio-city, simi-valley — unique "Neighborhoods, Permitting &
Electrical Architecture" sections) passes comfortably. The **thin template**
(~6.2–6.5k chars; sampled montecito-heights / fox-hills / pacoima are
78–88% identical after masking — same H2 skeleton, same two opening
paragraphs word-for-word) **fails**: swapping the city name leaves nothing
else to change. By body length, **67 of 112 pages use the thin template**
and 45 the rich one. Localization priority: give thin pages one truly local
section each (housing stock + panel vintages + permit quirks + 2–3
hyperlocal landmarks), starting with the highest-traffic ones per GSC.

## 10. Top 10 prioritized actions

1. [Critical] Reconcile schema hours with visible hours (same fix as maps §9.2 — one edit, two reports).
2. [Critical] Sync or drop the static "4.9★ 87 reviews" claim + markup.
3. [High] Add a Google Maps embed (lazy-loaded) or directions link to service-area/contact pages — currently zero embeds in 312 pages.
4. [High] Run the 5-page swap test on city pages; localize failures.
5. [High] Claim Bing Places + Apple Business Connect with identical NAP (AI-assistant visibility: ChatGPT sources Bing/Yelp, not GBP).
6. [Medium] Fix the one divergent Yelp URL.
7. [Medium] Add `hasMap` once GBP is claimed.
8. [Medium] Pursue 1–2 local authority links (chamber, BBB, neighborhood press) — the authority dimension scores 3/10 and "best of" lists are the #1 AI-visibility citation factor.
9. [Low] Submit to the three data aggregators for downstream citation distribution.
10. [Low] Run `/seo geo` for the AI-visibility pass (68% of local searches show AI Overviews; mobile AI packs show 1–2 businesses).

## 11. Limitations

Could not assess: live local-pack position, review velocity/responses, GBP
Insights, backlink profile/Domain Authority, competitor on-page comparison,
citation completeness beyond manual `sameAs` inspection. Tools that fill the
gaps: DataForSEO (`google_local_pack_serp`, `business_listings`), Ahrefs/Moz
(backlinks), GBP Insights (impressions/actions). Observation outside this
skill's scope, flagged for the site owner: `licensed-electrician-los-angeles.html`
quotes "EV charger installation at $800 to $2,500" and "panel upgrades at
$1,800 to $4,000" in visible copy — worth a look in the next
`audit-price-drift` sweep, since neither matches current canonicals.
