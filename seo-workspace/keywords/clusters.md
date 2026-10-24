# Keyword Clusters & Page Mapping — AMY Electric

**Date:** 2026-10-18 · **Workflow:** 3 (`keyword-clustering`) · **Market:** Greater Los Angeles (`2840`/`en`)
**Best action:** the mapping is mostly right — the failure is distribution, not structure. **14 of
the 18 striking-distance queries land on one thin page** (`/emergency-electrician-los-angeles`,
1,482 words) and the **64 geo service pages have ~3 inbound internal links each**. Fix those two
things before any new URL is created.

> This file is the **master mapping**. `keywords/keyword-clusters.md` holds longer historical prose;
> it is superseded for all numbers (it cites 1,011 analysed queries and cluster totals that no
> longer match the export). `keywords/opportunities.md` holds the keyword-level detail.

---

## Mapping summary

- **Clusters:** 11 (9 existing-page clusters, 2 proposed)
- **Pages to create:** 2 (both optional, listed last)
- **Existing pages to update:** 12
- **Cannibalization issues:** 4 (2 severe — exact duplicate titles)
- **Every target below is an existing URL unless marked *proposed*.**

---

## Master cluster → page map

| # | Cluster | Primary keyword | Secondary keywords | Intent | Target page | Priority | GSC impressions | Cannibalization risk |
| :-- | :--- | :--- | :--- | :--- | :--- | :---: | ---: | :--- |
| 1 | **Emergency & same-day** | `emergency electrician los angeles` | `24 hour emergency electrician la`, `same day electrician los angeles`, `emergency fuse box services los angeles ca`, `urgent electrical service in los angeles` | Urgent commercial | `/emergency-electrician-los-angeles` | **P0** | 2,008 | ⚠️ 4 URLs historically held this intent; aliases now canonicalised (see below) |
| 2 | **Whole-home rewiring** | `home rewiring` | `whole home rewiring`, `wiring and rewiring`, `los angeles house rewire`, `kitchen rewiring` | Commercial / research | `/whole-home-rewiring` | **P0** | 3,492 | 🚨 `blog/whole-home-rewiring-guide` (3,444 impr) outranks the service page (40 impr) |
| 3 | **EV charger (generic)** | `ev charger installation los angeles` | `ev charger installation benefits`, `property benefits ev charger`, `level 2 charger installer` | Transactional | `/ev-charger-installation` | **P1** | 1,905 (EV bucket) | ⚠️ vs `/tesla-charger-installation` — OK if brand vs generic stays distinct |
| 4 | **Tesla / branded EV** | `tesla charger installation` | `tesla charger vs others`, `tesla connector alternatives`, `tesla universal wall connector` | Transactional | `/tesla-charger-installation` | **P0** | 338 | ⚠️ `blog/tesla-wall-connector-vs-other-ev-chargers` (589 impr, pos 30.4) outranks it (825 impr, pos 56.9) |
| 5 | **Panel upgrade** | `electrical panel upgrade los angeles` | `electrical panel upgrade near me`, `100 amp vs 200 amp panel`, `zinsco panel replacement` | Transactional | `/panel-upgrade` | **P1** | 590 | ✅ healthy — blog cost post supports the service page |
| 6 | **Geo — city hubs** | `electrician [city]` | `electrician sherman oaks`, `electrician studio city`, `electrician encino`, `electrician van nuys`, `electrician woodland hills`, `electrician burbank` | Local commercial | `/city-*.html` (112 pages) | **P0** | 1,990 | ⚠️ **City pages rank 26–57 for their own city term** — they are being outranked on-query |
| 7 | **Geo — service × city** | `ev charger installation [city]` / `panel upgrade [city]` | `ev charger installation van nuys`, `electrical panel repair glendale`, `electrical panel upgrade woodland hills` | Local transactional | `/ev-charger-installation-*`, `/panel-upgrade-*`, `/whole-home-rewiring-*` (**64 pages**) | **P0** | ~200 | ✅ none — but ~3 inbound links each (link starvation) |
| 8 | **Code & permits** | `california electrical code 2026` | `la electrical code requirements`, `ladwp e-permit`, `electrical permit los angeles` | Informational authority | `/blog/california-electrical-code-changes-2026` | **P1** | 481 | ✅ none — best CTR on the site (1.98%, pos 8.6) |
| 9 | **Commercial / property management** | `commercial electrician los angeles` | `commercial electric installation`, `ev fleet charging`, `multi-family EV charger installation` | B2B commercial | `/commercial-electrical` + `/commercial-ev-charger-installation` | **P2** | 421 | ⚠️ two URLs; keep service vs fleet intent split |
| 10 | **Repairs & safety** | `power outage repair` | `ceiling fan installations`, `surge protection services los angeles`, `gfci`, `smoke detector installation`, `generator installation cost`, `what causes a circuit breaker to trip` | Transactional / specific repair | `/electrical-repair`, `/ceiling-fan-installation`, `/surge-protection`, `/smoke-co-detector-installation`, `/generator-transfer-switch`, `/breaker-tripping` | **P2** | 851 | ✅ distinct URLs exist for each — use them, don't consolidate |
| 11 | **ADU & rental subpanel** | `ADU electrical subpanel requirements LA` | `ADU subpanel cost LA`, `secondary electric meter ADU LADWP` | Commercial / informational | `/adu-electrical` + `/blog/adu-electrical-panel-requirements-la` | **P2** | 0 | ✅ none — **zero captured demand**; needs links, not new content |

### Proposed (only if the above is done and demand still appears)

| # | Cluster | Primary keyword | Rationale | Status |
| :-- | :--- | :--- | :--- | :--- |
| P1 | **Panel-brand hazard pages** | `federal pacific panel replacement los angeles`, `pushmatic panel replacement`, `old fuse box replacement` | The primary competitor runs a dedicated page per hazard brand; AMY has one Zinsco blog post | *proposed* — `federal-pacific-panel-replacement.html` |
| P2 | **EV manufacturer pages** | `ford / hyundai / nissan home charger installation los angeles` | Competitors run per-make pages; AMY's EVITP credential is the differentiator on each | *proposed* — defer until cluster 3/4 positions improve |

---

## Cannibalization register

| Severity | Pages | Evidence | Recommended action |
| :--- | :--- | :--- | :--- |
| 🚨 **Severe** | `/blog/ev-charger-installation-cost-la` and `/blog/ev-charger-installation-cost-los-angeles` | **Identical `<title>`** ("EV Charger Installation Cost Los Angeles [2026]"; the `-la` variant appends "| AMY"), both self-canonical | Consolidate: 301 the weaker into the stronger, keep one canonical |
| 🚨 **Severe** | `/blog/whole-home-rewiring-cost-la` and `/blog/whole-home-rewiring-cost-los-angeles` | Near-identical titles ("Whole Home Rewiring Cost Los Angeles [2026]" / "Whole-Home Rewiring Cost Los Angeles [2026]"), both self-canonical | Consolidate as above |
| ⚠️ Moderate | `/blog/breaker-keeps-tripping-causes` and `/blog/breaker-keeps-tripping-guide` | Near-identical titles ("Why Circuit Breakers Trip: Causes & Fixes" / "Why Your Breaker Keeps Tripping: Causes & Fixes") | Consolidate |
| ⚠️ Moderate | `/whole-home-rewiring` (service) vs `/blog/whole-home-rewiring-guide` (1,547 words, 3,444 impr, pos 37.7) | Blog outranks the transactional page (40 impr) by ~86× on impressions | **Do not merge** — intent differs. Reframe blog as informational with a funnel CTA and internal link to the service page; give the service page the transactional signals it lacks |

**Already resolved (do not re-open):** `/emergency-electrician` and `/emergency-electrical` are
`noindex`, canonical to `/emergency-electrician-los-angeles`, and 301-redirected there; all 112 city
pages link an emergency page. The Oct-13 plan's emergency consolidation is **shipped**
(`[repo: _redirects]`, `[repo: emergency-electrician.html]`).

---

## Per-cluster briefs

Detailed outlines were written for the four clusters where page work has the highest expected
return. Each brief is written to the `seo-content-brief` format (intent, competitor evidence,
gaps, outline, meta, information gain, E-E-A-T, internal links).

| Cluster | Brief | Target page |
| :--- | :--- | :--- |
| 1 — Emergency & same-day | `content/emergency-electrician-brief.md` | `/emergency-electrician-los-angeles` |
| 2 — Whole-home rewiring | `content/whole-home-rewiring-brief.md` | `/whole-home-rewiring` |
| 3/4 — EV & Tesla | `content/ev-charger-installation-brief.md` | `/ev-charger-installation`, `/tesla-charger-installation` |
| 6/7 — Geo pages | `content/geo-service-pages-brief.md` | 112 city + 64 geo service pages |
| 11 — ADU (existing) | `content/adu-electrical-brief.md` | shipped 2026-10-14 |

**Not briefed, deliberately:** panel upgrade (its pages are already 5,204 words with good
positions — the constraint is authority, not content) and code/permit (best-performing cluster on
the site; leave it alone).

### Internal-link opportunity (applies to every cluster)

The single highest-leverage structural change: **112 city pages currently link ~3 times into the 64
geo service pages.** Each city page should link its own city's EV, panel and rewiring service page
where one exists, and the geo service pages should link back to the city page. This is a templated
change to `generate-city-pages.py`, not 112 manual edits.

## New clusters proposed 2026-10-24 (content gaps vs competitors + GSC)

Mapped from `seo-workspace/keywords/opportunities.md` Table C. All target pages are *proposed*
unless they already exist. Briefs live in `seo-workspace/content/`.

| # | Cluster | Primary keyword | Secondary | Intent | Target page | Priority | GSC impressions |
| :-- | :--- | :--- | :--- | :--- | :--- | :---: | ---: |
| 12 | **Panel-brand hazard — Federal Pacific** | `federal pacific panel replacement los angeles` | `fpe stab-lok panel replacement cost` | Commercial / research | *proposed* `blog/federal-pacific-panel-replacement-cost-los-angeles.html` | **P1** | unknown |
| 13 | **Panel-brand hazard — Pushmatic** | `pushmatic panel replacement los angeles` | `bulldog pushmatic panel upgrade cost` | Commercial / research | *proposed* `blog/pushmatic-panel-replacement-cost-los-angeles.html` | **P1** | unknown |
| 14 | **Knob-and-tube cost** | `knob and tube wiring replacement cost los angeles` | `k&t rewiring cost per square foot` | Commercial / research | *proposed* `blog/knob-and-tube-wiring-replacement-cost-los-angeles.html` | **P1** | unknown |
| 15 | **Non-Tesla EV (per-make)** | `non-tesla ev charger installation los angeles` | `level 2 charger installation los angeles`, `rivian home charger installation` | Transactional | `/ev-charger-installation` (enhance) + *proposed* blog | **P2** | unknown |
| 16 | **Recessed lighting cost** | `recessed lighting installation cost los angeles` | `recessed lighting cost per can los angeles` | Commercial / research | `/recessed-lighting-installation` + *proposed* blog | **P0** | 47 (pos 21.5) |
| 17 | **Thin-post deepening** | `electrical inspection cost los angeles`, `outdoor lighting installation cost los angeles`, `adu electrical cost los angeles`, `generator installation cost los angeles` | Mixed | Mixed | existing thin blogs (deepen) | **P2** | 0–low |
| 18 | **Commercial EV charging ROI** | `commercial ev charging installation cost los angeles` | `workplace ev charging cost`, `commercial ev fleet charging roi` | B2B commercial | `/commercial-ev-fleet-charging` (enhance) + *proposed* blog | **P2** | 175 (pos 77.1) |

## Sources

- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — all impression/position figures
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — page-level cluster competition
- `[repo: ls whole-home-rewiring*.html / ev-charger-installation*.html / panel-upgrade*.html]` — 64 geo service pages
- `[repo: blog/*.html <title> and <link rel=canonical>]` — duplicate-title and self-canonical evidence
- `[repo: _redirects]`, `[repo: emergency-electrician.html]` — emergency consolidation shipped
- `[openseo: get_serp_results → DataForSEO HTTP 401]` — SERP-overlap validation unavailable; clusters are mapped on GSC intent + page evidence, not SERP overlap
- `[directional: web]` — competitor page-structure observations
