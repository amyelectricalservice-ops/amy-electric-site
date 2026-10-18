# Competitor Study — 911 Construction & Electric

**Domain:** `911electrics.com` · **Date:** 2026-10-18 · **Workflow:** 4 (`competitor-analysis`)
**Tier (from `reports/competitor-landscape.txt`):** Tier 1

> **Best action:** they are the **most programmatic competitor** — **492 URLs** (the prior landscape
> said ~73, so they have grown ~7×). Their advantage is footprint breadth, not content quality:
> their pages are JS-rendered templates whose H2s repeat "Get Your Free Quote" twice. The one thing
> AMY must copy is their **EVITP directory listing** — they are in, AMY is not.

---

## Snapshot

| Attribute | Value | Evidence |
| :--- | :--- | :--- |
| Title (services) | `Electrician in Los Angeles, CA \| 911 Electric` | fetch |
| Phone / email | `747-255-8595` · `info@911electrics.com` | fetch |
| Pages | **492 URLs** in `sitemap.xml` | sitemap fetch |
| Service-area claim | "Licensed electrician serving **43+ communities** across Los Angeles County — Pasadena, Glendale, Burbank, the San Fernando Valley and beyond. **24/7 emergency service**" | `/service-areas/` |
| URL patterns | `/<service>-los-angeles/`, `electrician-<city>-ca/`, `/services/<city>-ca/` | sitemap |
| Schema | **`Electrician`** + `GeoCoordinates` + `OpeningHoursSpecification` + `PostalAddress` + `EducationalOccupationalCredential` + `FAQPage` + `City` | JSON-LD `@type` extraction |
| Rendering | **JS-rendered** — plain fetch returns **0 extractable words** on service pages | measured |
| Platform | WordPress + Elementor + Yoast (prior landscape) | — |
| Traffic / keywords / backlinks | **unknown** — `get_domain_overview`/`get_backlinks_overview` → DataForSEO HTTP 401 | — |

## Biggest lesson

**Programmatic scale + a specific schema type.** They pair a very large templated URL set with the
**`Electrician` schema type** (more specific than `LocalBusiness`) plus `GeoCoordinates` and
`EducationalOccupationalCredential` — the same trio AMY uses. Their `/service-areas/` hub explicitly
claims 43+ communities and 24/7, which is a clean, crawlable local relevance signal.

## Best opportunity to beat them

1. **Verify whether their scale is real or thin.** Plain fetches of three service pages
   (`/ev-charger-installation-los-angeles-ca/`, `/emergency-electrician-los-angeles-ca/`,
   `/whole-house-rewiring-cost-los-angeles/`) returned **zero extractable body text** and repeated
   boilerplate H2s ("Get Your Free Quote" … "Get Your Free Quote Today"). If their content is
   genuinely client-side-only and template-repeated, thick unique content can beat it — but
   **this needs a rendered-crawl check to confirm**, which no available tool can do this session.
2. **Content depth AMY already has.** AMY's city and service pages are static HTML with thousands of
   words of unique text; theirs is a template shell per URL.
3. **Their EVITP advantage is a listing, not a product.** See below — it is closable in an afternoon.

## ⭐ The EVITP directory gap (verified)

| Check | Result |
| :--- | :--- |
| Is 911 Construction & Electric in EVITP's Find A Contractor directory? | **YES** — `evitp.org/california/listing/911-construction-electric-inc` (listing id 2206) |
| Is AMY Electric in it? | **NO** — no match for "AMY", "Winnetka" or "91306" on `evitp.org/california` |
| What AMY holds | EVITP certification **#4051604** |

They also publish EVITP explainer content (`/what-is-evitp-certification-los-angeles/`,
`/why-evitp-certification-matters-for-ev-charger-incentives-los-angeles/`,
`/why-hiring-an-evitp-certified-installer-matters-in-los-angeles/`) — competing on AMY's own
credential while holding the trade-directory link AMY lacks. Fixing this is the highest
effort-to-reward item in the workspace (see `outreach/prospects.md`).

## Area | Their pattern | Evidence | AMY opportunity

| Area | Their pattern | Evidence | AMY opportunity |
| :--- | :--- | :--- | :--- |
| URL scale | 492 URLs incl. `/<service>-los-angeles/` long-tail set | sitemap | Do not chase scale; match intent instead |
| Long-tail service pages | Dedicated pages for `zinsco-panel-replacement`, `two-prong-to-three-prong-outlet`, `whole-house-surge-protector-installation`, `warehouse-lighting-installation`, `video-doorbell-installation`, `under-cabinet-lighting-installation` | sitemap | AMY has `/surge-protection`, `/outlet-switch-installation`, `/lighting-installation` — cover the same intents without new sprawl |
| EVITP authority | Directory listing + 3 explainer pages | `evitp.org/california` | **P0** — get AMY listed |
| Emergency | 24/7 + `emergency-electrician-los-angeles-ca/` page | sitemap + copy | AMY is in the striking distance for 14 emergency queries — win them |
| FAQ coverage | `FAQPage` schema on service pages | extracted | AMY does this too (24 Q/Answer pairs on the homepage) |
| Content depth | Thin/JS-rendered, repeated H2s | measured 0 words | AMY's static, long-form pages are the structural advantage |

## Top keyword themes (inventory-derived, not rank data)

`electrician Los Angeles CA` · `emergency electrician` (24/7) · `electrical panel upgrades` ·
`EV charger installation` · `whole-house rewiring cost` · `Zinsco / Federal Pacific panel replacement` ·
`surge protection` · `whole-house generator` · `warehouse / commercial lighting` ·
`EVITP certification` · 40+ community-specific `electrician-<city>-ca` pages

## Backlink / authority notes

**`unknown`** — `get_backlinks_overview` → HTTP 401. Prior landscape (June 2026) noted a "geo
sitemap" and GA4 (`gtag`) active; the live 492-URL sitemap confirms the programmatic strategy is
ongoing.

## Head-to-head SERP observations

⚠️ No SERP data (`get_serp_results` → HTTP 401). Structural overlap is direct and heavy: they hold
city pages for Encino, Sherman Oaks, Studio City, West Los Angeles, North Hollywood, Glendale,
Burbank, Culver City, Santa Monica, Pasadena, Calabasas, Woodland Hills, Van Nuys — i.e. the exact
cities where AMY gets its city-page impressions (`electrician sherman oaks` 296 impr @ 37.0,
`electrician encino` 181 @ 55.2, `electrician van nuys` 170 @ 56.0).

## Priority actions for AMY Electric

1. **P0 — Get listed in EVITP's Find A Contractor directory** (`info@evitp.org`). Verified gap, trade
   authority link, and it is the credential AMY already paid for.
2. **P1 — Win the emergency cluster.** 14 of AMY's 18 striking-distance queries are emergency intent
   and they sit against a page (1,482 words) much thinner than AMY's other money pages.
3. **P1 — Publish EVITP explainer content** (the "why it matters for rebates" angle) so AMY owns the
   credential narrative rather than ceding it.
4. **P2 — Commission a rendered crawl** to confirm whether their 492 pages carry unique content; that
   determines whether AMY can beat them on depth or must outrank them on links.

## Sources

- `[directional: web]` — `https://911electrics.com/sitemap.xml` → 492 `<loc>` URLs (patterns reviewed in full)
- `[directional: web]` — fetches of `/services/los-angeles-ca/`, `/service-areas/`, `/ev-charger-installation-los-angeles-ca/`, `/emergency-electrician-los-angeles-ca/`, `/whole-house-rewiring-cost-los-angeles/`: titles, descriptions, schema `@type` list, phone, email; **0 extractable body words** on service pages
- `[directional: web]` — `evitp.org/california`: 911 Construction & Electric listed (`/california/listing/911-construction-electric-inc`, id 2206); **no AMY/Winnetka/91306 match**
- `[directional: web]` — `evitp.org/frequently-asked-questions` (Approved contractor vs Certified electrician distinction), `calevip.org/find-ev-charging-providers`
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — Tier 1, ~73 pages, EVITP mention, geo sitemap attribution (dated 2026-06-03 — page count now stale)
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — AMY's city-term positions
- `[openseo: get_domain_overview / get_backlinks_overview / get_serp_results → DataForSEO HTTP 401]` — no traffic, keyword, backlink or SERP data
