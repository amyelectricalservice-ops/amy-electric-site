# Competitor Study — Bryden Electrical

**Domain:** `brydenelectrical.com` · **Date:** 2026-10-18 · **Workflow:** 4 (`competitor-analysis`)
**Tier (from `reports/competitor-landscape.txt`):** Tier 1

> **Best action:** Bryden is the closest **positioning** competitor (EV/electrification + panel
> upgrades, since 1984) but the **weakest content competitor** — only **6 blog posts** and **34
> pages**. Its real asset is a manufacturer partnership (Qmerit, per the June landscape) and a
> FranklinWH battery offer. AMY should take the **per-make EV structure** and the battery/electrification
> topic, and beat them comfortably on content.

---

## Snapshot

| Attribute | Value | Evidence |
| :--- | :--- | :--- |
| Title | `Electrical Contracting in Los Angeles, CA \| Bryden` | fetch |
| Description | "Residential and commercial electrical services, EV charging installations, & more. Get to know our electrical contracting company before scheduling service." | fetch |
| Phone | `(310) 470-2900` | fetch |
| Platform | WordPress + Total theme / WPBakery + Gravity Forms (prior landscape) | — |
| Pages | **sitemap index = 6 sub-sitemaps**: `post` (6), `page` (34), `testimonials`, `category`, `testimonials_category`, `author` | sitemap fetch |
| Service structure | `/residential-electrical-services/` with children (`indoor-lighting`, `electrical-switches-outlets`, `smoke-detectors`), `/commercial-electrical-services/`, `/ev-chargers/ev-charger-installation-quote/`, `/service-areas/beverly-hills/` | `page-sitemap.xml` |
| Blog posts | **6** — incl. "How to set up a home charger for your first electric vehicle", "EV tax credits for California homeowners — the real 2026 breakdown", "Battery storage isn't just for solar homes", "Electrical hazards in older LA homes", "The importance of regular electrical maintenance for businesses", "Understanding the electrical load of modern homes" | `post-sitemap.xml` |
| Schema | `Organization` + `WebPage` + `WebSite` + `BreadcrumbList` + `ImageObject` — **no `LocalBusiness`/`Electrician`, no `AggregateRating`** | JSON-LD `@type` extraction |
| Defect observed | A placeholder phone **`(999) 999-9999`** appears in the homepage HTML alongside the real number | fetch |
| Traffic / keywords / backlinks | **unknown** — `get_domain_overview`/`get_backlinks_overview` → DataForSEO HTTP 401 | — |

## Biggest lesson

**A tiny, well-targeted blog beats a large one.** Six posts, each aimed at a distinct high-intent
topic: first-EV home charging, **2026 California EV tax credits**, battery storage economics, and
older-LA-home electrical hazards. That is a curated set of commercially-adjacent questions, not
volume — and it maps directly onto clusters where AMY already has impressions.

## Best opportunity to beat them

1. **Content volume is trivially beatable** — 6 posts vs AMY's 60, and 34 pages vs 314.
2. **Schema gap.** No `LocalBusiness`/`Electrician` type, no `AggregateRating`. AMY runs
   `Electrician` on 309 pages with 87 aggregate-rated reviews — a rich-result advantage today.
3. **Their content is time-sensitive and will decay.** "EV tax credits for California homeowners —
   the real 2026 breakdown" is a 2026-dated piece. AMY's `ladwp-ev-charger-rebate-guide-2026` can
   win that query by being kept current — but **only with verified rebate figures** (no invented
   amounts).
4. **Qmerit is their differentiator, EVITP is AMY's.** They hold a manufacturer/installer
   partnership; AMY holds EVITP #4051604 **and** is missing from the EVITP directory — fixing that
   closes this specific gap (see `911electrics.com.md`).

## Area | Their pattern | Evidence | AMY opportunity

| Area | Their pattern | Evidence | AMY opportunity |
| :--- | :--- | :--- | :--- |
| Blog strategy | 6 curated, high-intent posts (EV tax credits, first-EV charging, battery storage, older-home hazards) | `post-sitemap.xml` | **Adopt the topic list** — AMY has `/blog/ladwp-ev-charger-rebate-guide-2026` and older-home content; make sure the 2026 tax-credit angle is covered and dated |
| Service structure | Nested `/residential-electrical-services/<subservice>/` | `page-sitemap.xml` | AMY's flat structure is fine; no change needed |
| Service areas | `/service-areas/<city>/` — only a handful | `page-sitemap.xml` | AMY's 176 geo URLs dominate |
| Battery storage | FranklinWH battery installation (prior landscape) | prior landscape | **Untaken topic** for AMY — but the owner must confirm the service exists before any page is written |
| Electrification hub | A dedicated "Electrification" top-bar page (prior landscape) | prior landscape | A `/electrification` hub could tie EV + panel + battery together — *proposed, owner decision* |
| Schema | Organization only, no local type, no ratings | extracted | AMY ahead |
| Defect | Placeholder `(999) 999-9999` phone in HTML | fetch | Sanity-check AMY's own contact markup for the same class of bug |

## Top keyword themes (inventory-derived, not rank data)

`electrical contracting Los Angeles` · `residential electrical services` · `commercial electrical services` ·
`EV charging installation` · `EV tax credits California` · `home charger first EV` ·
`battery storage` · `electrical load modern homes` · `electrical hazards older LA homes` ·
`indoor lighting`, `switches & outlets`, `smoke detectors`, `EV charger installation quote`

## Backlink / authority notes

**`unknown`** — `get_backlinks_overview` → HTTP 401. Prior landscape notes Qmerit certification and
Gravity Forms quoting; Qmerit partnership pages are a plausible citation source but that is
**inference, not evidence**.

## Head-to-head SERP observations

⚠️ No SERP data (`get_serp_results` → HTTP 401). Topic overlap is real where it matters: both target
EV charger installation, panel upgrades, and older-LA-home rewiring/safety. Their
`electric-hazards-in-older-la-homes` post overlaps AMY's
`/blog/electrical-safety-checklist-older-los-angeles-homes` and `/whole-home-rewiring` — a cluster
where AMY holds 3,492 impressions.

## Priority actions for AMY Electric

1. **P1** — Keep `ladwp-ev-charger-rebate-guide-2026` current and add the **2026 EV tax credit**
   angle they cover (needs a verified, cited source — no invented figures).
2. **P2** — Decide with the owner whether battery storage / electrification is a real service line;
   if yes it is a genuine gap, if no it is out of scope.
3. **P2** — Audit AMY's own phone/contact markup for stale or placeholder values (their `999-9999`
   bug is a reminder; AMY's canonical number is `(818) 302-5614`, `tel:18183025614`).
4. **P3** — No other action: AMY already out-scales them on every content dimension.

## Sources

- `[directional: web]` — `https://brydenelectrical.com/` and `/residential-electrical-services/` fetches: title, description, phone, JSON-LD `@type` list, placeholder phone `(999) 999-9999`
- `[directional: web]` — `brydenelectrical.com/sitemap.xml` (6 sub-sitemaps); `post-sitemap.xml` → 6 URLs; `page-sitemap.xml` → 34 URLs
- `[directional: web]` — `brydenelectrical.com/ev-chargers/ev-charger-installation-quote/` measured at **1,832 words** (H2s not extractable)
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — since 1984, Qmerit partner, FranklinWH battery, "Electrification" page, Gravity Forms, phone (310) 470-2900 (**dated 2026-06-03**)
- `[repo: index.html]`, `[repo: grep -l]` — AMY schema inventory; `[repo: AGENTS.md]` — canonical phone and price canonicals
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — rewiring cluster 3,492 impressions
- `[openseo: get_domain_overview / get_backlinks_overview / get_serp_results → DataForSEO HTTP 401]` — no traffic, keyword, backlink or SERP data
