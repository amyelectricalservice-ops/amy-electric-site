# Competitor Study — Branover Contractors Inc

**Domain:** `branovercontractors.com` (canonical host `www.branovercontractors.com`)
**Date:** 2026-10-18 · **Workflow:** 4 (`competitor-analysis`) · **Tier:** Tier 1

> **Best action:** they are the **content-volume benchmark** in this market (170 blog posts and 25+
> city pages per the June 2026 landscape) and they run a **fully populated local schema graph**
> (`Place` + `PostalAddress` + `Person` + `Article`, Rank Math-generated). Their weakness is time:
> "since 1985 / family owned" is the whole pitch, with no visible specialisation. AMY should not
> attempt to match 170 posts — it should out-specialise them on EV (EVITP), where they show no
> credential claim we could find.

---

## Snapshot

| Attribute | Value | Evidence |
| :--- | :--- | :--- |
| Title | `Los Angeles Electrician - Licensed Local Electrical Contractor in LA` | fetch |
| Description | "Los Angeles electrician servicing Los Angeles **since 1985**. Licensed. Family owned & operated. Free Estimates. Call us today @ **323-467-6661**." | fetch |
| Phones / email | `(323) 467-6040`, `(323) 467-6661` · `info@branovercontractors.com` | fetch |
| Platform | WordPress + Astra + Rank Math (prior landscape) | — |
| Schema | **`Place` + `PostalAddress` + `Organization` + `Person` + `Article` + `WebPage` + `WebSite` + `ImageObject` + `SearchAction`** | JSON-LD `@type` extraction |
| Sitemap | `robots.txt` → `Sitemap: https://www.branovercontractors.com/sitemap_index.xml` — **index and sub-sitemaps returned 0 `<loc>` entries in this session** | robots + sitemap fetches |
| Pages | ~255 (85 pages + 170 posts) — **June 2026 figure, not re-verified this session** | prior landscape |
| Location pages | 25+ (`encino-electrician`, `sherman-oaks-electrician`, `beverly-hills-electrician`, …) — June 2026 | prior landscape |
| Licence | C10 484143; since 1985 | prior landscape |
| Traffic / keywords / backlinks | **unknown** — `get_domain_overview`/`get_backlinks_overview` → DataForSEO HTTP 401 | — |

⚠️ **Data limitation:** their sitemap could not be retrieved this session (the index URL from
`robots.txt` returned no `<loc>` entries). Their page counts and location-page list are therefore
carried from the **June 2026 landscape file** and must be treated as dated, not current.

## Biggest lesson

**Rank Math's complete local graph, on every page.** Their schema includes `Place` with a full
address, `Organization` with `sameAs` and email, `Person` for authorship, and `Article`/`WebPage`
alongside. That is a machine-readable entity declaration — the strongest in this competitor set.
*(AMY is still ahead overall: `Electrician` type on 309 pages, `OpeningHoursSpecification` on 248,
`EducationalOccupationalCredential` on 244, plus `HowTo` and `Offer`/`PriceSpecification` — which
they do not appear to run.)*

## Best opportunity to beat them

1. **Specialisation vs generalism.** Their positioning is "licensed, family owned, since 1985".
   AMY's is C-10 **plus EVITP #4051604** — a specialised credential for the highest-growth service
   line (EV charging). Branover shows no EVITP claim in the sources reviewed.
2. **Do not fight on blog volume.** 170 posts vs AMY's 60. Matching that is not a good use of effort;
   AMY's wins come from 176 geo URLs and specialised service pages.
3. **Their case studies are worth copying as a *format*.** Prior landscape records "10+ detailed
   project entries". AMY already has 4 (`case-studies/`) — a low-cost expansion path with the 387
   photos behind it.

## Area | Their pattern | Evidence | AMY opportunity

| Area | Their pattern | Evidence | AMY opportunity |
| :--- | :--- | :--- | :--- |
| Schema | Full Rank Math local graph incl. `Place`, `Person`, `Article`, `sameAs` | extracted | AMY ahead on service-specific types; consider adding `sameAs` social profiles if the owner supplies them |
| Blog | ~170 posts (June 2026) | prior landscape | Don't match volume; target the 60 AMY has at the right page type |
| Location pages | 25+ `<city>-electrician` URLs | prior landscape | AMY has 112 city + 64 geo service pages |
| Case studies | 10+ project entries | prior landscape | **P2 to expand** — AMY has 4; photos already exist |
| Insurance panel FAQ | Insurance-specific panel replacement FAQ | prior landscape | Same untaken angle as `theelectricconnection.com` — insurance-driven panel replacement |
| Years in business | "since 1985" as primary trust signal | fetched description | AMY counter-positions on certification, not longevity |
| Multi-county reach | LA + SFV + Orange + Ventura (prior landscape) | prior landscape | AMY should stay denser in the SFV/central LA |

## Top keyword themes (from prior landscape + page inventory; not rank data)

`Los Angeles electrician` · `electric panel upgrade` · `EV charger installation` ·
`electrical code compliance` · `property management electrical` ·
`Zinsco/Federal Pacific panel replacement` · `surge protection` · `<city>-electrician` × 25+

## Backlink / authority notes

**`unknown`** — `get_backlinks_overview` → HTTP 401. Prior landscape attributes their visibility to
site size (255 pages) and blog volume (170 posts), which is a plausible but **unverified** inference.

## Head-to-head SERP observations

⚠️ No SERP data (`get_serp_results` → HTTP 401). Their `sherman-oaks-electrician` and
`beverly-hills-electrician` URLs overlap AMY's `/city-sherman-oaks` and `/city-beverly-hills`.
Note AMY's `/city-beverly-hills` already earns 343 impressions at pos 48.6 — the two are fighting
for the same terms with no way to confirm positions this session.

## Priority actions for AMY Electric

1. **P1** — Counter-position on EVITP specialisation wherever Branover's "since 1985" genericism
   appears in the SERP for AMY's priority EV terms.
2. **P2** — Expand `case-studies/` from 4 toward 8–10 entries, reusing gallery photos per
   service×city; this matches their strongest content format at almost no cost.
3. **P2** — Publish the insurance-driven panel replacement content that both Branover and
   `theelectricconnection.com` already cover and AMY does not.
4. **P3** — Add `sameAs` social profiles to schema **only if the owner supplies real profiles**
   (do not invent them).

## Sources

- `[directional: web]` — `https://www.branovercontractors.com/` fetch: title, description, phone numbers, email, JSON-LD `@type` list
- `[directional: web]` — `branovercontractors.com/robots.txt` (points to `www.branovercontractors.com/sitemap_index.xml`); sitemap and sub-sitemaps returned **0 `<loc>` entries** this session
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — ~255 pages, 170 posts, 25+ location pages, C10 484143, since 1985, 10+ case studies, insurance panel FAQ, Rank Math with `Place`/`Organization`/`Article` (**dated 2026-06-03 — page counts not re-verified**)
- `[repo: index.html]`, `[repo: grep -l]` — AMY schema inventory (Electrician 309 / OpeningHours 248 / Credential 244)
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — `/city-beverly-hills` 343 impressions @ 48.6
- `[openseo: get_domain_overview / get_backlinks_overview / get_serp_results → DataForSEO HTTP 401]` — no traffic, keyword, backlink or SERP data
