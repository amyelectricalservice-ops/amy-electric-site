# Content Plan — Next (AMY Electric)

**Best action:** ship the two **consolidation + deepen** projects first (`home rewiring` 499 impressions at pos 23.2 and `EV charger installation cost` 30–94 impressions at pos 22–63 are both split across near-duplicate blog URLs that cannibalise each other), then add the two missing **service pages** competitors already own (`/generator-installation`, `/electrical-troubleshooting`). Do not create another net-new URL until the duplicate-title pairs in `keywords/clusters.md` are 301-merged.

**Date:** 2026-10-27 · **Sources:** GSC export 2026-09-05 (5+ weeks stale), repo page inventory, competitor studies. **No invented volumes** — every impression/position figure is `[gsc: Queries.csv]` or `[gsc: Pages.csv]`; web-derived observations are tagged `[directional: web]`.

---

## 1. High-impression, zero-click queries (position < 40)

From `Queries.csv` (1,000 queries). Filter: `Position < 40`, `Clicks = 0`, `Impressions ≥ 30`. 35 queries qualify; the 20 highest shown. All currently produce **0 clicks**.

| # | Query | Impr | Pos | Best existing target | Gap / action |
| :-- | :--- | ---: | ---: | :--- | :--- |
| 1 | `home rewiring` | 499 | 23.24 | `/whole-home-rewiring` (service, 40 impr) vs `/blog/whole-home-rewiring-guide` (3,444 impr, pos 37.7) | Blog outranks service page 86×; consolidate cost dupes + deepen |
| 2 | `emergency electrician los angeles` | 404 | 17.07 | `/emergency-electrician-los-angeles` | Title/CTR rewrite + deepen (1,482 → 2,500+ words) |
| 3 | `electrician sherman oaks` | 296 | 37.04 | `/city-sherman-oaks` | City page ranks for its own term at 37 — link + content fix, not new page |
| 4 | `electrician studio city` | 192 | 25.91 | `/city-studio-city` | Same as above |
| 5 | `electrical emergency service` | 123 | 38.74 | `/emergency-electrician-los-angeles` | Title rewrite (emergency intent) |
| 6 | `same day electrician los angeles` | 90 | 17.94 | `/emergency-electrician-los-angeles` | Title/CTR rewrite |
| 7 | `los angeles electrical safety` | 86 | 26.53 | `/electrical-safety-inspections` + 3 scattered blogs | **No hub page** → new guide (see §5 item 6) |
| 8 | `electrical safety inspection cost` | 70 | 25.80 | `/blog/electrical-safety-inspection-cost-los-angeles` (shipped) | Deepen + title rewrite |
| 9 | `same day electrical repair los angeles` | 69 | 13.68 | `/same-day-electrical-repair` | Striking distance — title/meta rewrite first |
| 10 | `tesla connector alternatives` | 68 | 31.69 | `/blog/tesla-wall-connector-vs-other-ev-chargers` | Refresh comparison content |
| 11 | `tesla charger vs others` | 61 | 17.31 | same as above | Striking distance |
| 12 | `ceiling fan installation los angeles` | 60 | 39.35 | `/ceiling-fan-installation` | Deepen service page (shipped cost blog exists) |
| 13 | `commercial electric installation` | 57 | 32.81 | `/commercial-electrical` | B2B page deepen + links |
| 14 | `updating electrical wiring` | 57 | 35.28 | `/whole-home-rewiring` | Funnel into rewiring page |
| 15 | `electrical wiring upgrade` | 56 | 32.71 | `/whole-home-rewiring` | Same |
| 16 | `24 hour emergency electrician la` | 55 | 15.65 | `/emergency-electrician-los-angeles` | Striking distance |
| 17 | `recessed lighting installation los angeles` | 47 | 21.47 | `/recessed-lighting-installation` (873 words) | **Deepen service page** (shipped cost blog exists) |
| 18 | `ev charger installation van nuys` | 36 | 16.17 | `/ev-charger-installation-van-nuys` | Striking distance; link-starved geo page |
| 19 | `ev charger installation cost los angeles` | 30 | 22.40 | two duplicate cost blogs | Consolidate + deepen |
| 20 | `electrical services calabasas` | 30 | 31.87 | `/city-calabasas` | City page link fix |

**Source:** `[gsc: Queries.csv]`. No search-volume/KD/CPC data available (OpenSEO MCP DataForSEO backend returns HTTP 401 — see `reports/context-status.md`).

---

## 2. Pages with high impressions but poor CTR (title/description rewrite candidates)

Pages with `Impressions ≥ 200` and `CTR < 1%` (or 0 clicks) from `Pages.csv`. These are snippet problems, not relevance problems — Google already shows them.

| Page | Impr | Clicks | CTR | Pos | Rewrite priority |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `/blog/whole-home-rewiring-guide` | 3,444 | 0 | 0% | 37.66 | **P0** — outranks the service page; retitle to transactional-ish question H2s |
| `/emergency-electrician` (redirect source, noindex) | 1,291 | 0 | 0% | 44.96 | Leave noindex; ensure 301 to `/emergency-electrician-los-angeles` holds |
| `/blog/la-electrical-code-requirements` | 944 | 3 | 0.32% | 32.53 | **P1** — code cluster's second-best page; rewrite meta |
| `/tesla-charger-installation` | 825 | 0 | 0% | 56.92 | **P1** — 338-impr query `tesla charger installation` sits at pos 67.8 |
| `/blog/ev-charger-installation-cost-la` | 517 | 1 | 0.19% | 87.86 | Consolidate into the `-los-angeles` variant |
| `/panel-upgrade` | 472 | 2 | 0.42% | 49.38 | **P1** — `electrical panel upgrade los angeles` 136 impr pos 62.9 |
| `/blog/panel-upgrade-cost-los-angeles` | 428 | 2 | 0.47% | 21.10 | **P0** — striking distance; rewrite title/meta |
| `/blog/ev-charging-benefits` | 362 | 0 | 0% | 73.42 | Low priority (pos 73) |
| `/same-day-electrical-repair` | 360 | 0 | 0% | 37.15 | **P1** — rewrite meta; missing `datePublished` (E-E-A-T gap) |
| `/city-sherman-oaks` | 348 | 0 | 0% | 35.64 | City page link/content fix |
| `/city-van-nuys` | 344 | 0 | 0% | 40.05 | Same |
| `/city-beverly-hills` | 343 | 0 | 0% | 48.59 | Same |
| `/city-burbank` | 336 | 0 | 0% | 50.68 | Same |
| `/commercial-electrical` | 330 | 0 | 0% | 71.75 | B2B deepen + links |
| `/city-woodland-hills` | 279 | 1 | 0.36% | 51.70 | City page fix |
| `/ev-charger-installation` | 279 | 0 | 0% | 53.72 | **P1** — generic EV transactional page |
| `/city-studio-city` | 265 | 0 | 0% | 25.65 | **P0** — striking distance (pos 25.7) |
| `/city-santa-monica` | 255 | 0 | 0% | 27.82 | **P1** |
| `/lighting-installation` | 254 | 0 | 0% | 37.13 | **P1** |
| `/blog/panel-upgrade-vs-rewiring` | 215 | 0 | 0% | 30.74 | Refresh + internal link to service page |
| `/blog/ladwp-ev-charger-rebate-guide-2026` | 212 | 0 | 0% | 11.97 | **P0** — striking distance; rewrite title/meta |
| `/blog/gfci-afci-protection-la` | 311 | 2 | 0.64% | 18.19 | **P0** — striking distance |

**Source:** `[gsc: Pages.csv]`.

---

## 3. Content gaps vs competitors

Verified against the five competitor studies in `seo-workspace/competitors/` (direct fetches, `[directional: web]`) and the primary target `theelectricconnection.com` (fetched 2026-10-27):

1. **Generator installation as a service** — competitor lists "Generator Installation" as a top-level service; AMY only has `/generator-transfer-switch` and `/portable-vs-standby-generator`. No service page. GSC: `generator installation cost` 133 impr pos 82.32, `standby generator installation cost` 59 impr pos 74.9.
2. **Service calls & troubleshooting** — competitor has a dedicated `/electrical-troubleshooting/` page; AMY has only blogs (`electrical-troubleshooting-diagnostics-cost-los-angeles`, `breaker-keeps-tripping-*`). GSC: `electrical emergency service` 123 impr pos 38.74.
3. **Insurance- / mandate-driven panel replacement** — competitor runs two dedicated pages on the LA County 82°F cooling mandate and insurance-required panel upgrades; AMY has none (only `/panel-upgrade`). High commercial intent, zero direct GSC query but maps to `electrical panel upgrade los angeles` 136 impr.
4. **Zinsco panel replacement cost** — competitor has a dedicated Zinsco page; AMY has only the hazards blog (`sylvania-zinsco-panel-hazards-replacement`, 1,130 words) with no cost-focused post. (FPE and Pushmatic cost posts already shipped.)
5. **Per-make EV chargers beyond Tesla** — competitor runs per-manufacturer pages (Ford, Nissan, Porsche, Hyundai, Mitsubishi); AMY has Tesla only. A non-Tesla hub blog shipped; per-make split deferred until demand appears (clusters.md P2).
6. **Los Angeles home electrical safety hub** — AMY has scattered safety content but no single hub capturing `los angeles electrical safety` (86 impr pos 26.53).
7. **Commercial EV charging ROI / cost** — AMY has service pages but no cost/ROI blog; competitor leans on property-management angle. GSC: `commercial electrician los angeles` 175 impr pos 77.11.

---

## 4. Cannibalization risks to clear before adding pages

| Risk | Pages | Evidence | Action before new content |
| :--- | :--- | :--- | :--- |
| 🚨 Severe | `/blog/ev-charger-installation-cost-la` ↔ `/blog/ev-charger-installation-cost-los-angeles` | Identical `<title>` | 301 weaker → stronger; keep one canonical |
| 🚨 Severe | `/blog/whole-home-rewiring-cost-la` ↔ `/blog/whole-home-rewiring-cost-los-angeles` | Near-identical titles | 301 weaker → stronger |
| ⚠️ Moderate | `/blog/breaker-keeps-tripping-causes` ↔ `/blog/breaker-keeps-tripping-guide` | Near-identical titles | 301 weaker → stronger |
| ⚠️ Moderate | `/whole-home-rewiring` (service, 40 impr) vs `/blog/whole-home-rewiring-guide` (3,444 impr, pos 37.7) | Blog outranks transactional page 86× | Do **not** merge — reframe blog as informational with funnel CTA + internal link to service page |
| ⚠️ Moderate | `/tesla-charger-installation` (825 impr, pos 56.9) vs `/blog/tesla-wall-connector-vs-other-ev-chargers` (589 impr, pos 30.4) | Blog outranks service page | Keep brand-vs-generic split; cross-link both directions |
| ⚠️ Low | New `/generator-installation` vs `/generator-transfer-switch` | Different intent (full install vs transfer switch) | Cross-link; no merge |
| ⚠️ Low | New safety hub vs `/electrical-safety-inspections` | Hub (informational) vs service (transactional) | Keep distinct; hub links to service page |

**Source:** `[repo: *.html <title> and <link rel=canonical>]`, `[gsc: Pages.csv]`, `[repo: keywords/clusters.md]`.

---

## 5. Recommended new pages / content additions (10)

Priority order. Word-count targets follow repo floors: blog posts ≥ 1,500 words, service pages ≥ 1,200 words (`[repo: content-review-2026-10-24.md]`).

| # | Type | Target query (GSC) | Suggested title | Suggested URL slug | Why it captures traffic | Word target | Cannibalization risk |
| :-- | :--- | :--- | :--- | :--- | :--- | ---: | :--- |
| 1 | **Consolidate + deepen** (existing) | `home rewiring` — 499 impr, pos 23.24 | Home Rewiring Cost in Los Angeles [2026]: Do You Need a Full Rewire? | Merge `/blog/whole-home-rewiring-cost-la` → `/blog/whole-home-rewiring-cost-los-angeles` (canonical), then deepen | Highest single local-impression term with 0 clicks; currently split across two near-duplicate URLs that split authority | 2,000+ | 🚨 Must 301-merge the `-la` variant first |
| 2 | **Consolidate + deepen** (existing) | `ev charger installation cost los angeles` — 30 impr, pos 22.40 (plus 94 impr at pos 63.04 for `ev charger installation los angeles`) | EV Charger Installation Cost in Los Angeles [2026]: Level 2, Permits & Rebates | Merge `/blog/ev-charger-installation-cost-la` → `/blog/ev-charger-installation-cost-los-angeles` (canonical), then deepen | Duplicate-title pair splits the only EV cost demand; add ChargeUp LA $1,500 rebate, panel-capacity, permit content | 2,000+ | 🚨 Must 301-merge the `-la` variant first |
| 3 | **New service page** | `electrical emergency service` — 123 impr, pos 38.74; `generator installation cost` 133 impr pos 82.32 | Generator Installation Los Angeles \| Standby & Portable Backup Power | `/generator-installation` | Competitor lists "Generator Installation" as a top-level service; AMY has no service page (only transfer-switch + portable-vs-standby posts). Brief exists: `content/generator-installation-los-angeles-brief.md` | 1,500+ | Low — distinct from `/generator-transfer-switch` |
| 4 | **New service page** | `electrical emergency service` — 123 impr, pos 38.74 | Electrical Troubleshooting & Diagnostics Los Angeles \| Same-Day Service Calls | `/electrical-troubleshooting` | Competitor has dedicated `/electrical-troubleshooting/`; AMY has only blogs. Maps to urgent-intent cluster (14 of 18 striking-distance terms are emergency). Brief exists: `content/electrical-troubleshooting-diagnostics-los-angeles-brief.md` | 1,500+ | Low — distinct from `/electrical-repair` |
| 5 | **New blog post** | `electrical panel upgrade los angeles` — 136 impr, pos 62.94 (insurance/mandate long-tail) | Does Homeowners Insurance Require a Panel Upgrade in Los Angeles? (LA County 82°F Rule Explained) | `/blog/panel-upgrade-insurance-requirements-los-angeles` | Competitor owns two dedicated pages on the LA County cooling mandate + insurance-required upgrades; AMY has none. High commercial intent, differentiator (C-10 + EVITP). **No brief yet — create one.** | 1,500+ | Low — informational vs `/panel-upgrade` transactional |
| 6 | **New blog hub** | `los angeles electrical safety` — 86 impr, pos 26.53 | Los Angeles Home Electrical Safety Guide: Inspections, Panels, Fire Prevention | `/blog/los-angeles-home-electrical-safety-guide` | No single page captures this query; AMY has 4 scattered safety posts. Hub consolidates authority and links to `/electrical-safety-inspections`. **No brief yet — create one.** | 1,500+ | Low — hub vs `/electrical-safety-inspections` service |
| 7 | **New blog post** | Panel bucket — 590 impr (Zinsco/FPE hazards) | Zinsco Panel Replacement Cost in Los Angeles [2026]: Hazards, Insurance & Replacement | `/blog/zinsco-panel-replacement-cost-los-angeles` | Competitor has dedicated Zinsco page; AMY only has the hazards blog (1,130 words, no cost focus). FPE + Pushmatic cost posts already shipped — Zinsco is the gap. **No brief yet — create one.** | 1,500+ | Low — cross-link with `/blog/sylvania-zinsco-panel-hazards-replacement` |
| 8 | **New blog post** | `commercial electrician los angeles` — 175 impr, pos 77.11; `commercial electric installation` 57 impr pos 32.81 | Commercial EV Charging Cost & ROI in Los Angeles [2026]: Workplace, Fleet & Multi-Family | `/blog/commercial-ev-charging-cost-roi-los-angeles` | AMY has service pages but no cost/ROI content; competitor leans on property-management angle. Brief exists: `content/commercial-ev-charging-roi-cost-los-angeles-brief.md` (not shipped) | 1,800+ | Low — B2B ROI vs `/commercial-ev-fleet-charging` service |
| 9 | **Deepen existing service page** | `recessed lighting installation los angeles` — 47 impr, pos 21.47 | (keep title; expand body) | `/recessed-lighting-installation` (873 → 1,500+ words) | Striking distance (pos 21.5) with a thin page just above the 800-word floor; cost blog already shipped. Competitor lists recessed lighting as a named service. | 1,500+ | None — same URL |
| 10 | **Deepen existing** (service + blog) | Code/permit bucket — 481 impr, 1 click (best CTR on site) | (keep titles; expand) | `/electrical-permit-cost-los-angeles` + `/blog/electrical-permit-los-angeles` | Only cluster with a real click; deepen permit-fee tables and LADBS steps. Brief exists: `content/electrical-permit-cost-los-angeles-deepening-brief.md` | 1,500+ each | None — same URLs |

**Source:** `[gsc: Queries.csv]`, `[gsc: Pages.csv]`, `[repo: content-review-2026-10-24.md]`, `[repo: keywords/clusters.md]`, `[directional: web]` (competitor service lists).

---

## 6. Items deliberately NOT recommended

- **New content for `whole home rewiring`** (2,727 impr, pos 41.23) — mostly national/unqualified traffic (Brooklyn neighbourhoods, other CA markets, PA ZIPs). AMY cannot serve it. `[gsc: Queries.csv]` non-local table.
- **`ev charger installation renovation cost`** (162 impr, pos 222.05) — spam-adjacent SERP; not actionable.
- **Per-make EV pages** (Ford, Nissan, etc.) — deferred until the generic EV cluster (pos 53–68) improves; single hub post shipped first.
- **Battery storage / electrification hub** — 0 captured GSC demand; owner decision pending (P3).
- **City-page net-new URLs** — 112 city pages already exist; the problem is ranking (pos 26–57) and link starvation, not coverage. Fix via `generate-city-pages.py` template links + title rewrites.
- **More panel-upgrade depth** — `/panel-upgrade` is already 5,204 words with healthy positions; constraint is authority/links, not content.

---

## 7. Measurement / success criteria

- Re-pull GSC after the next export (current export is 5+ weeks stale, ending 2026-09-05). Track non-brand CTR on the 8 URLs in §2 and positions on the 20 queries in §1.
- Target: move at least 3 of the §1 queries from pos 11–25 into the top 10 within one GSC window; raise CTR on `/blog/panel-upgrade-cost-los-angeles` (pos 21.1, 0.47% CTR) and `/blog/ladwp-ev-charger-rebate-guide-2026` (pos 12.0, 0% CTR) above 2%.
- Do not judge success on `whole home rewiring` impressions (national dilution).

---

## Sources

- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — all impression/position/click figures in §1, §5.
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — all page-level impression/CTR/position figures in §2.
- `[repo: seo-workspace/keywords/clusters.md]` — cluster mapping, cannibalization register, brief inventory.
- `[repo: seo-workspace/keywords/opportunities.md]` — Table A/B/C opportunity tables.
- `[repo: seo-workspace/reports/content-review-2026-10-24.md]` — word-count floors, E-E-A-T gaps, auditor baselines.
- `[repo: seo-workspace/competitors/README.md]` and `[repo: seo-workspace/competitors/*.md]` — competitor service lists and content gaps.
- `[repo: seo-workspace/reports/gsc-opportunity-report.md]` — earlier striking-distance analysis.
- `[directional: web]` — `theelectricconnection.com` homepage service list (fetched 2026-10-27): Generator Installation, Service Calls & Troubleshooting, Property Management, Lighting Projects, recessed/landscape lighting.
- `[openseo: get_serp_results → DataForSEO HTTP 401]` — no SERP/keyword-volume/backlink data available; all competitor observations are direct fetches, not confirmed rankings.