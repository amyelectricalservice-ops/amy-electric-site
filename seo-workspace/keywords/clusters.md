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

---

## New clusters proposed 2026-10-24 (deep scan) — briefs in `seo-workspace/content/`

All target pages are *proposed* unless they already exist. Brief filename in the last column.

| # | Cluster | Primary keyword | Secondary | Intent | Target page | Priority | GSC impressions | Brief |
| :-- | :--- | :--- | :--- | :--- | :--- | :---: | ---: | :--- |
| 19 | **Smart home electrical** | `smart home electrical cost los angeles` | smart panel, dedicated circuits, surge | Commercial / research | *proposed* blog + deepen `/smart-home-electrical` | **P0** | 25 (pos 16.0) | `smart-home-electrical-cost-los-angeles-brief.md` |
| 20 | **Electrical safety inspection** | `electrical safety inspection cost los angeles` | home electrical inspection cost, ladbs | Informational / authority | *proposed* blog + deepen `/electrical-safety-inspections` | **P1** | 70 (pos 25.8) | `electrical-safety-inspection-cost-los-angeles-brief.md` |
| 21 | **Generator installation** | `generator installation los angeles` | standby generator installation cost | Commercial / research | *proposed* blog + new `/generator-installation` | **P1** | 133 (pos 82.3) | `generator-installation-los-angeles-brief.md` |
| 22 | **Outdoor / landscape lighting** | `outdoor landscape lighting installation cost los angeles` | landscape lighting installation cost | Commercial / research | *proposed* blog + deepen `/lighting-installation-los-angeles` | **P2** | 0 captured | `outdoor-landscape-lighting-installation-los-angeles-brief.md` |
| 23 | **Dedicated circuit cost** | `dedicated circuit installation cost los angeles` | cost to install a dedicated circuit | Commercial / research | *proposed* blog + deepen `/dedicated-circuits` | **P1** | 27 (pos 25.8) | `dedicated-circuit-installation-cost-los-angeles-brief.md` |
| 24 | **Cloth-insulated wiring** | `cloth insulated wiring replacement los angeles` | cloth wiring hazards | Commercial / research | *proposed* blog | **P2** | 0 captured | `cloth-wiring-replacement-los-angeles-brief.md` |
| 25 | **Grounding / ungrounded** | `grounding ungrounded wiring upgrade los angeles` | two-prong to three-prong outlet | Commercial / research | *proposed* blog | **P2** | 0 captured | `grounding-ungrounded-wiring-upgrade-los-angeles-brief.md` |
| 26 | **Residential remodel electrical** | `residential remodel renovation electrical los angeles` | electrician for remodel | B2B / commercial | *proposed* blog + new service page | **P2** | 5–27 | `residential-remodel-renovation-electrical-los-angeles-brief.md` |
| 27 | **GFCI outlet installation** | `gfci outlet installation los angeles` | gfci outlet cost | Commercial / research | *proposed* blog + deepen `/outlet-switch-installation` | **P1** | 55 (aggregate) | `gfci-outlet-installation-los-angeles-brief.md` |
| 28 | **Electrical troubleshooting** | `electrical troubleshooting diagnostics los angeles` | electrical diagnostic cost | Urgent / commercial | *proposed* blog + new `/electrical-troubleshooting` | **P1** | 123 (pos 38.7) | `electrical-troubleshooting-diagnostics-los-angeles-brief.md` |
| 29 | **Two-prong to three-prong** | `two-prong to three-prong outlet upgrade los angeles` | ungrounded outlet upgrade | Commercial / research | *proposed* blog | **P2** | 0 captured | `two-prong-to-three-prong-outlet-upgrade-los-angeles-brief.md` |
| 30 | **Video doorbell** | `video doorbell installation los angeles` | ring doorbell installation cost | Transactional | *proposed* blog | **P2** | 0 captured | `video-doorbell-installation-los-angeles-brief.md` |
| 31 | **Warehouse / commercial lighting** | `warehouse commercial lighting installation los angeles` | commercial led retrofit cost | B2B commercial | *proposed* blog + enhance `/commercial-electrical` | **P2** | 175 (pos 77.1) | `warehouse-commercial-lighting-installation-los-angeles-brief.md` |
| 32 | **Battery storage / electrification** | `home battery storage electrification los angeles` | home battery backup cost | Commercial / research | *proposed* (owner decision) | **P3** | 0 captured | `battery-storage-electrification-hub-los-angeles-brief.md` |
| 33 | **Home automation electrical** | `home automation electrical los angeles` | home automation wiring cost | Commercial / research | deepen `/home-automation-electrical` | **P2** | 0 captured | `home-automation-electrical-deepening-los-angeles-brief.md` |
| 34 | **Tenant improvement electrical** | `tenant improvement electrical los angeles` | ti electrical cost | B2B commercial | deepen `/tenant-improvement-electrical` | **P2** | 0 captured | `tenant-improvement-electrical-deepening-los-angeles-brief.md` |
| 35 | **Ceiling fan cost** | `ceiling fan installation cost los angeles` | ceiling fan install cost | Commercial / research | *proposed* blog + deepen `/ceiling-fan-installation` | **P1** | 60 (pos 39.4) | `ceiling-fan-installation-cost-los-angeles-brief.md` |
| 36 | **Whole-home surge protection** | `whole-home surge protection cost los angeles` | surge protector installation cost | Commercial / research | *proposed* blog + deepen `/surge-protection` | **P1** | 29 (pos 22.3) | `surge-protection-installation-cost-los-angeles-brief.md` |
| 37 | **Under-cabinet lighting** | `under-cabinet lighting installation cost los angeles` | under cabinet led lighting cost | Commercial / research | *proposed* blog | **P2** | 0 captured | `under-cabinet-lighting-installation-los-angeles-brief.md` |
| 38 | **Commercial code compliance** | `commercial electrical code compliance los angeles` | code compliance inspection cost | B2B commercial | *proposed* blog + enhance `/commercial-electrical` | **P2** | 15 (pos 39.5) | `electrical-code-compliance-los-angeles-brief.md` |
| 39 | **Electrical permit cost (deepen)** | `electrical permit cost los angeles` | ladbs permit fees | Informational / authority | deepen `/electrical-permit-cost-los-angeles` | **P1** | 481 bucket | `electrical-permit-cost-los-angeles-deepening-brief.md` |
| 40 | **ADU electrical (deepen)** | `adu electrical requirements los angeles` | adu subpanel cost | Commercial / research | deepen `/adu-electrical` + blog | **P2** | 0 captured | `adu-electrical-deepening-los-angeles-brief.md` |
| 41 | **Smoke/CO detector cost** | `smoke co detector installation cost los angeles` | hardwired smoke detector cost | Commercial / research | *proposed* blog + deepen `/smoke-co-detector-installation` | **P2** | 0 captured | `smoke-co-detector-installation-cost-los-angeles-brief.md` |
| 42 | **Panel upgrade (insurance/mandate)** | `panel upgrade cost los angeles` | la county cooling mandate | Commercial / research | *proposed* blog + enhance `/panel-upgrade` | **P1** | 136 (pos 62.9) | `panel-upgrade-cost-los-angeles-deepening-brief.md` |
| 43 | **Whole-home rewiring cost** | `whole home rewiring cost los angeles` | how to tell if need rewire | Commercial / research | *proposed* blog + enhance `/whole-home-rewiring` | **P1** | 499 (pos 23.2) | `whole-home-rewiring-cost-los-angeles-deepening-brief.md` |
| 44 | **Aluminum wiring (enhance)** | `aluminum wiring repair cost los angeles` | repair vs replace | Commercial / research | enhance shipped post | **P2** | 0 captured | `aluminum-wiring-repair-cost-los-angeles-deepening-brief.md` |
| 45 | **Fuse box (enhance)** | `fuse box replacement cost los angeles` | fuse box vs breaker panel | Commercial / research | enhance shipped post | **P2** | 0 captured | `fuse-box-replacement-cost-los-angeles-deepening-brief.md` |
| 46 | **EV charger cost (consolidate)** | `ev charger installation cost los angeles` | ladwp chargeup rebate | Commercial / research | consolidate `-la`/`-los-angeles` + deepen | **P1** | 30 (pos 22.4) | `ev-charger-installation-cost-los-angeles-deepening-brief.md` |
| 47 | **Electrical repair cost** | `electrical repair cost los angeles` | dead outlet cost | Urgent / commercial | *proposed* blog + deepen `/electrical-repair` | **P1** | 123 (pos 38.7) | `electrical-repair-cost-los-angeles-deepening-brief.md` |
| 48 | **Knob-and-tube (enhance)** | `knob and tube wiring replacement cost los angeles` | knob and tube removal cost | Commercial / research | enhance shipped post | **P2** | 0 captured | `knob-and-tube-wiring-replacement-cost-los-angeles-deepening-brief.md` |

### Cannibalization / consolidation reminders

- `/blog/ev-charger-installation-cost-la` and `/blog/ev-charger-installation-cost-los-angeles` — identical titles; consolidate (301 weaker → stronger).
- `/blog/whole-home-rewiring-cost-la` and `/blog/whole-home-rewiring-cost-los-angeles` — near-identical titles; consolidate.
- `/blog/breaker-keeps-tripping-causes` and `/blog/breaker-keeps-tripping-guide` — near-identical titles; consolidate.
- `/blog/adu-electrical-panel-requirements-la` (465 words) and `/adu-electrical` (988 words) — merge or deepen both.
- `/blog/generator-installation-cost-la` (628 words), `/blog/outdoor-lighting-installation-la` (794 words), `/blog/dedicated-circuit-installation-cost.html` (770 words), `/blog/electrical-inspection-cost-los-angeles` (724 words), `/blog/electrical-inspection-what-to-expect` (595 words), `/blog/smart-home-electrical-requirements` (628 words) — all below the 1,500-word blog floor; deepen or merge.

### Sources

- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — all impression/position figures
- `[repo: *.html word counts]` — thin page inventory
- `[directional: web]` — theelectricconnection.com, 911electrics.com, dpgcontractors.com, brydenelectrical.com service lists
- `[repo: scripts/site_data.py]` — reviewCount 87
