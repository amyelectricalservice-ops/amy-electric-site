# Competitor Study — Dynamic Power Group

**Domain:** `dpgcontractors.com` · **Date:** 2026-10-18 · **Workflow:** 4 (`competitor-analysis`)
**Tier (from `reports/competitor-landscape.txt`):** Tier 1

> **Best action:** their homepage is an **8,335-word** conversion machine and their only schema is
> `Organization` + `FAQPage` — no `LocalBusiness`/`Electrician` type, no `AggregateRating`. AMY is
> ahead on schema and on service-page depth. The lesson to take is their **homepage as a service hub**,
> not their technical setup.

---

## Snapshot

| Attribute | Value | Evidence |
| :--- | :--- | :--- |
| Title | `Los Angeles Electricians \| Free Estimates \| Dynamic Power Group` | fetch |
| Description | "Licensed & insured LA electricians **since 2016**. Panel upgrades, EV charger installation, rewiring & emergency electrical repairs. Free estimates…" | fetch |
| Phone / email | `(323) 977-6577` · `info@dpgcontractors.com` | fetch |
| Platform | WordPress + Elementor + Yoast (per prior landscape) | sitemap structure |
| Pages | **80 URLs** in `sitemap.xml` = 62 pages + 22 posts (approx; index lists post/page/category sitemaps) | sitemap fetch |
| Service pages | `/commercial-electrical-services-in-los-angeles/`, `/residential-electrical-services/`, `/emergency-electrical-service/`, `/electrical-troubleshooting-services/`, `/electrical-installation-service/`, `/services/` | sitemap |
| Homepage length | **8,335 words** (measured) | fetch + strip |
| Schema | `Organization`, `WebPage`, `WebSite`, `FAQPage` (Question/Answer), `BreadcrumbList`, `ImageObject` — **no `LocalBusiness`, no `AggregateRating`** | JSON-LD `@type` extraction |
| Job/recruiting pages | 8+ application/job pages in `page-sitemap.xml` | sitemap |
| Traffic / keywords / backlinks | **unknown** — `get_domain_overview`/`get_backlinks_overview` → DataForSEO HTTP 401 | — |

## Biggest lesson

**The homepage is doing the work of ten landing pages.** 8,335 words covering services, a 3-step
booking flow, latest projects, testimonials and conversion blocks — plus `FAQPage` schema so the
answers are eligible for rich results. They have no strong local schema, yet the page is an
everything-hub for `Los Angeles electrician` intent.

## Best opportunity to beat them

1. **Schema gap.** Their homepage has no `LocalBusiness`/`Electrician` type and no `AggregateRating`.
   AMY runs `Electrician` on 309 pages, `OpeningHoursSpecification` on 248, and 87 aggregate-rating
   reviews. AMY should lean into rich-result eligibility (reviews, hours) they cannot match.
2. **Thin service coverage.** 62 pages total vs AMY's 314 — they cover ~5 core services with no
   geo × service matrix and no blog depth (22 posts vs AMY's 60).
3. **"Since 2016" vs AMY's credentialed specificity.** DPG claims 7,000+ customers (per prior
   landscape); AMY's differentiator is verifiable certification (C-10 #981578, EVITP #4051604),
   which is stronger for EV work than a customer count.

## Area | Their pattern | Evidence | AMY opportunity

| Area | Their pattern | Evidence | AMY opportunity |
| :--- | :--- | :--- | :--- |
| Homepage | 8,335-word service hub with FAQ schema | measured | AMY's homepage is 563 GSC impressions @ pos 12.3 / 25 clicks — it *converts* best already. Consider a services-hub expansion, not a rewrite |
| Service coverage | ~5 core services, no geo×service matrix | sitemap | AMY's 64 geo service pages are unmatched here |
| Blog | 22 posts, cost/emergency-led ("emergency electrical service costs in LA", "understanding upgrade electrical panel cost") | `post-sitemap.xml` | AMY's 60 posts already exceed this; the gap is page-type targeting, not count |
| Schema | Organization + FAQPage only | extracted | AMY ahead: Electrician type, OpeningHours, EducationalOccupationalCredential, HowTo, Offer/PriceSpecification |
| Reviews | "7000+ happy customers" claim; 5-year limited labour warranty (prior landscape) | prior landscape | AMY's canonical 87 reviews + licence numbers are more verifiable |
| Recruiting pages | 8+ job/application pages indexed | sitemap | Not an SEO priority for AMY |

## Top keyword themes (inventory-derived, not rank data)

`electrical contractor Los Angeles` · `commercial electrical services Los Angeles` ·
`residential electrical services` · `emergency electrical service` · `electrical troubleshooting` ·
`electrical installation` · `panel upgrade cost` · `EV charger installation` · `EV charging` ·
`lighting installation` · `wiring` · `surge protection`

## Backlink / authority notes

**`unknown`** — `get_backlinks_overview` returned `DataForSEO HTTP 401`. The prior landscape claims
"7000+ happy customers", "5-year limited labor warranty", "same-day service" and dual licensing
(CA #1076003); those are **their marketing claims as recorded in June 2026**, not verified metrics.

## Head-to-head SERP observations

⚠️ No SERP data (`get_serp_results` → HTTP 401). Their emergency and panel-cost blog posts target
the same buying-intent queries AMY gets impressions for (`emergency electrical service` 123 impr @
pos 38.7; `electrical panel upgrade los angeles` 136 @ 62.9) — but no positional comparison is
verifiable.

## Priority actions for AMY Electric

1. **P1** — Push review + hours rich results harder: AMY's `AggregateRating` (87 reviews) and
   `OpeningHoursSpecification` (248 pages) are a visible advantage over DPG's schema.
2. **P2** — Consider expanding the homepage into a fuller service hub only if the emergency and
   rewiring page work lands first; homepage already performs best on the site (pos 12.3).
3. **P3** — Do not chase their job-posting pages.

## Sources

- `[directional: web]` — `https://dpgcontractors.com/` fetch: title, description, JSON-LD `@type` list, phone, email, measured homepage length 8,335 words
- `[directional: web]` — `https://dpgcontractors.com/sitemap.xml` → 80 `<loc>`; `post-sitemap.xml` → 22; `page-sitemap.xml` → 62
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — Tier 1, CA #1076003, 7,000+ customers, 5-year warranty, Yoast schema (dated 2026-06-03)
- `[repo: index.html]` — AMY schema inventory; `[repo: grep -l]` — Electrician 309 / OpeningHours 248 / Credential 244
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — AMY's positions on overlapping terms
- `[openseo: get_domain_overview / get_backlinks_overview / get_serp_results → DataForSEO HTTP 401]` — no traffic, keyword, backlink or SERP data
