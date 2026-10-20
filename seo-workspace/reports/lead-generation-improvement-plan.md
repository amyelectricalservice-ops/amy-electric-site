# AMY Electric — Lead Generation Audit & Improvement Plan

**Date:** 2026-10-20
**Source of truth:** `[repo: AGENTS.md]`, `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/]`, `[repo: seo-workspace/keywords/opportunities.md]`, `[repo: seo-workspace/keywords/clusters.md]`, `[repo: seo-workspace/competitors/]`, `[repo: seo-workspace/content/]`, `[repo: seo-workspace/outreach/prospects.md]`

---

## Executive Summary

**The site does not have a traffic problem. It has a conversion problem.**

AMY Electric ranks for real, local, high-intent demand across Greater Los Angeles — 21,745 page impressions in the last GSC window — but produced only **78 clicks** (0.36% CTR). Roughly 71 of those 78 clicks are non-brand, and **the money pages (emergency, panel, EV, rewiring) got zero clicks despite thousands of impressions each.**

The site is technically excellent: schema validates, 314 pages audit clean, sitemap is sound, CSS/JS are reproducible, all 83 tests pass. The gap is not technical SEO or content depth — AMY's core service pages are *longer* than the primary competitor's. The gap is:

1. **Above-the-fold conversion elements missing** on the highest-impression pages (no tap-to-call, no response expectation, no local trust signals in the hero).
2. **Link starvation** — 64 geo service pages rank 1–10 but have ≤30 impressions because each has only ~3 inbound internal links.
3. **Thin money page** — `/emergency-electrician-los-angeles` (975 words) carries 2,008 emergency impressions but converts none; the 14 striking-distance emergency queries all land here.
4. **Intent breadth gap** vs The Electric Connection — they publish per-hazard-brand panel pages, per-manufacturer EV pages, insurance/mandate content, and cost calculators. AMY consolidates brand intent into fewer URLs.

**Best action:** Fix the pages that already rank before creating anything new. The 18 striking-distance queries (positions 8–20) are one small push from page one, and 14 of them are emergency intent — the highest-value service AMY offers.

---

## Audit Findings

### A. Technical SEO — PASS (no action needed)

| Check | Result | Source |
|-------|--------|--------|
| Schema validation | All 314 pages pass | `[repo: scripts/schema-tool.py validate]` |
| Site audit | 0 issues across 314 pages | `[repo: scripts/audit-site.py]` |
| Price drift | 0 flagged pairs, 0 glued prices | `[repo: scripts/audit-price-drift.py]` |
| Tests | 83/83 pass, 25 suites | `[repo: node --test scripts/test-*.mjs]` |
| Wrangler dry-run | Clean, all bindings recognized | `[repo: npx wrangler deploy --dry-run]` |
| Sitemap | 306 URLs, all self-canonical | `[repo: sitemap.xml]` |
| CI audit workflow | Green on `main` | `[remote: .github/workflows/audit.yml + deploy.yml]` |

### B. Search Performance — CRITICAL GAP

**Site-wide (last GSC window, 3 months ending 2026-09-05):**

| Metric | Value | Assessment |
|--------|-------|------------|
| Page impressions | 21,745 | Real demand exists |
| Clicks | 78 | 0.36% CTR — effectively unmonetised |
| Non-brand clicks | ~71 of 78 | Brand is ~9% of clicks |
| Mobile avg position | 26.6 | Emergency searchers are on mobile |
| Desktop avg position | 43.3 | |

**Page-level (top impression URLs):**

| URL | Impressions | Clicks | CTR | Position | Assessment |
|-----|-------------|--------|-----|----------|------------|
| `/` (homepage) | 563 | 25 | 4.44% | 12.3 | Only page with meaningful CTR |
| `/blog/california-electrical-code-changes-2026` | 1,113 | 22 | 1.98% | 8.57 | Best-performing informational page |
| `/panel-upgrade` | 472 | 2 | 0.42% | 49.38 | Buried |
| `/emergency-electrician-los-angeles` | ~1,291 (old alias) + service page | 0 | 0% | ~18-45 | **Zero clicks on emergency demand** |
| `/whole-home-rewiring-guide` (blog) | 3,444 | 0 | 0% | 37.66 | Outranks service page 86× on impressions |
| `/tesla-charger-installation` | 825 | 0 | 0% | 56.92 | Buried despite EVITP credential |
| `/ev-charger-installation` | 279 | 0 | 0% | 53.72 | Buried |

**Striking distance (positions 8–20, ≥20 impressions, non-brand): 18 terms, 0 clicks.** 14 are emergency intent, all pointing at one thin page.

### C. Content / Landing Page — CRITICAL GAP

**Emergency page is 975 words** vs panel (2,990) and rewiring (2,483). It carries 2,008 emergency impressions with 0 clicks.

**Geo service pages rank at/near position 1 but get single-digit impressions** — e.g., `/whole-home-rewiring-santa-monica` at position 1.0 with 2 impressions, `/panel-upgrade-culver-city` at position 8.0 with 4 impressions. Each has only ~3 inbound internal links site-wide. **This is link starvation, not a content problem.**

**Cannibalization (4 pairs):**
- `/blog/ev-charger-installation-cost-la` vs `/blog/ev-charger-installation-cost-los-angeles` — identical titles
- `/blog/whole-home-rewiring-cost-la` vs `/blog/whole-home-rewiring-cost-los-angeles` — near-identical titles
- `/blog/breaker-keeps-tripping-causes` vs `/blog/breaker-keeps-tripping-guide` — near-identical titles
- `/whole-home-rewiring` (service) vs `/blog/whole-home-rewiring-guide` — blog outranks service page 86× on impressions

### D. Competitive Landscape — INTENT BREADTH GAP

**Primary competitor: The Electric Connection (`theelectricconnection.com`)**

| Feature | Electric Connection | AMY Electric | AMY Advantage |
|---------|-------------------|--------------|---------------|
| Core service page length | 3,800–4,100 words | 4,285–5,204 words | AMY deeper on core pages |
| Per-hazard-brand panel pages | Yes (Zinsco, Federal Pacific, Pushmatic, fuse boxes) | One Zinsco blog post only | **Competitor leads** |
| Per-manufacturer EV pages | Tesla, Ford, Nissan, Porsche, Hyundai, Mitsubishi | Consolidated into fewer URLs | **Competitor leads** |
| Insurance/mandate content | Yes (LA County mandates, insurance rules) | Zero pages | **Competitor leads** |
| Cost calculators | House rewire, EV charger install | Live estimate engine (superior) | AMY superior |
| Real project photography | Thin (one page) | **387 photos** | **AMY major advantage** |
| EVITP certification | Unknown | **#4051604** | **AMY unique** |
| City page titles | Thin ("Sherman Oaks Electrician") | Service + brand + differentiator | AMY better |
| City page count | ~150 (spread thin, incl. OC/Ventura) | 112 (focused on LA/SFV) | AMY more focused |

**AMY's unfalsifiable advantages competitors cannot cheaply match:** EVITP #4051604, live estimate engine, 387-photo project gallery, 112 focused city pages.

---

## Improvement Plan — Three Phases

### Phase 1: Fix What Already Ranks (Weeks 1–2, no new pages)

**Goal:** Convert existing impressions into clicks and calls. Target: 0 → 2–4% CTR on striking-distance pages.

| # | Action | Page(s) | Effort | Expected Impact | Source |
|---|--------|---------|--------|-----------------|--------|
| 1.1 | Expand emergency page 975 → 2,400–2,800 words. Add: dispatch process, response expectations, "what to do before we arrive", LADWP-vs-electrician disambiguation, after-hours process, emergency price posture, permit/utility side of burned panel. | `/emergency-electrician-los-angeles` | Medium | Capture 14 striking-distance emergency queries; 2,008 impressions currently at 0 clicks | `[repo: seo-workspace/content/emergency-electrician-brief.md]` |
| 1.2 | Add tap-to-call phone badge above the fold on emergency page + CTA-band with "(818) 302-5614". | `/emergency-electrician-los-angeles` | Low | Mobile emergency searchers convert on phone, not forms | `[gsc: Devices.csv]` mobile pos 26.6 |
| 1.3 | Add `EmergencyService` schema + local business schema with reviewCount 87, EVITP credential, hours. | `/emergency-electrician-los-angeles` | Low | Rich result eligibility, trust signals | `[repo: scripts/site_data.py]` |
| 1.4 | Fix 4 duplicate-title cannibalization pairs — 301 weaker into stronger, keep one canonical. | 8 URLs (4 pairs) | Low | Consolidate split authority | `[repo: seo-workspace/keywords/clusters.md]` |
| 1.5 | Add internal links from 112 city pages → each city's own EV/panel/rewiring geo service page; link back from geo page to city page. Templated via `generate-city-pages.py` — not 112 manual edits. | 112 city pages + 64 geo service pages | Medium (one template change) | Geo pages currently rank 1–10 with ≤30 impr due to ~3 inbound links each | `[repo: seo-workspace/keywords/clusters.md]` |
| 1.6 | Re-title/re-describe emergency and rewiring pages for CTR (0% CTR at pos 10–18 is a snippet problem, not relevance). | Emergency, rewiring service pages | Low | Improve CTR without moving position | `[gsc: Queries.csv]` |

### Phase 2: Match Competitor Intent Breadth (Weeks 2–6, new pages)

**Goal:** Capture intent AMY currently cedes to The Electric Connection.

| # | Action | Page(s) | Effort | Expected Impact | Source |
|---|--------|---------|--------|-----------------|--------|
| 2.1 | Create per-hazard-brand panel pages: Federal Pacific, Pushmatic, old fuse box replacement. | `/federal-pacific-panel-replacement`, `/pushmatic-panel-replacement` | Medium | Competitor has dedicated pages per hazard brand; AMY has one Zinsco blog post | `[repo: seo-workspace/competitors/electric-connection-la.md]`, `[repo: seo-workspace/keywords/clusters.md]` proposed P1 |
| 2.2 | Create insurance/mandate content: LA County electrical mandates, insurance-driven panel replacement, property-management electrical compliance. | New blog + service section | Medium | **Strongest untaken angle** — high-ticket, link-attracting topic AMY has zero page for | `[repo: seo-workspace/competitors/electric-connection-la.md]` |
| 2.3 | Split brand intent: per-manufacturer EV pages (Ford, Hyundai, Nissan, etc.) leveraging EVITP #4051604 on each. | New EV manufacturer pages | Medium | Competitor runs per-make pages; AMY consolidates brand intent | `[repo: seo-workspace/competitors/electric-connection-la.md]` |
| 2.4 | Add cost calculators (rewire cost, EV charger install cost) — or promote the existing live estimate engine more visibly on service pages. | New tool pages + CTA on service pages | Medium | Competitor has calculators; AMY's estimate engine is superior but under-exposed | `[repo: seo-workspace/competitors/electric-connection-la.md]` |

### Phase 3: Lead Conversion & Authority (Weeks 6–12, ongoing)

**Goal:** Turn traffic into qualified leads; build off-site authority.

| # | Action | Effort | Expected Impact | Source |
|---|--------|--------|-----------------|--------|
| 3.1 | Submit AMY to CALeVIP Connects (EVITP-gated, free, statewide directory for EV contractors). | Low | High-value free listing; EVITP #4051604 is the gate competitors can't self-grant | `[repo: seo-workspace/outreach/prospects.md]` P0 |
| 3.2 | Submit AMY to EVITP "Find A Contractor" California listing — AMY is NOT currently listed. | Low | Directory LA EV buyers check; genuine outbound link | `[repo: seo-workspace/outreach/prospects.md]` P0 |
| 3.3 | AAGLA Business Council / Supplier Directory — multifamily property managers (panel upgrades, EV-ready garages, subpanels). | Medium | B2B commercial leads in AMY's home turf | `[repo: seo-workspace/outreach/prospects.md]` P1 |
| 3.4 | SRAR (Southland Regional Association of REALTORS) affiliate membership — SFV + Santa Clarita agents hitting panel/rewiring at escrow. | Medium | Realtor referral pipeline | `[repo: seo-workspace/outreach/prospects.md]` P1 |
| 3.5 | GBP posting cadence — 30 posts, every other day, 2026-10-21→2026-12-18 (calendar + agent already built; needs OAuth secrets). | Low (manual until agent armed) | Local pack visibility | `[repo: gbp-posting-calendar.md]`, `[repo: gbp-agent.js]` |
| 3.6 | Review acquisition — push reviewCount from 87 toward 100+. More reviews = better CTR + local pack. | Ongoing | Trust signal on every page | `[repo: scripts/site_data.py]` |
| 3.7 | Photo gallery integration — surface 2–3 real project photos on each geo service page and city page. AMY's 387 photos are an unfalsifiable advantage. | Medium | Conversion proof competitors can't match | `[repo: scripts/photo-manifest.csv]` |

---

## Success Metrics (30/60/90 days)

| Metric | Baseline | 30-day target | 90-day target |
|--------|----------|---------------|---------------|
| Non-brand clicks (GSC) | ~71/window | 100–120 | 150–200 |
| Emergency page clicks | 0 | 5–10 | 15–25 |
| Striking-distance CTR (pos 8–20) | 0% | 2–4% | 5–8% |
| Geo service page impressions (64 pages) | ~200 total | 400–600 | 800–1,200 |
| reviewCount | 87 | 90–95 | 100+ |
| Qualified leads (form + phone) | unknown | +25% | +50% |

> `[repo: AGENTS.md]` notes `reviewCount` canonical = 87 in `scripts/site_data.py` (333 occurrences, zero drift). Any bump must be made in one place.

---

## What NOT to Do (explicitly de-prioritised)

| Item | Reason |
|------|--------|
| New content for `whole home rewiring` (national term) | 2,727 impressions are mostly non-local (Brooklyn, PA, other CA markets). AMY cannot serve them. `[gsc: Queries.csv]` |
| New content for `ev charger installation renovation cost` | Position 222 — spam-adjacent SERP. `[gsc: Queries.csv]` |
| Copying competitor's thin city-page template | AMY's city titles (service + brand + differentiator) are strictly better. `[repo: seo-workspace/competitors/electric-connection-la.md]` |
| Unifying the 112 city pages' `areaServed` shapes | Blocked on owner-supplied per-city county/ZIP data; inventing data violates constraints. `[repo: AGENTS.md]` |
| Running `scripts/sync-faq-schema.py --apply` | Rewrites answers; verified harmful 2026-10-12. `[repo: AGENTS.md]` |

---

## Immediate Next Steps (this week)

1. **Expand `/emergency-electrician-los-angeles`** using the existing brief at `seo-workspace/content/emergency-electrician-brief.md` (target 2,400–2,800 words, tap-to-call above fold, EmergencyService schema).
2. **Fix the 4 duplicate-title cannibalization pairs** — 301 weaker into stronger.
3. **Template the city→geo-service internal link** in `generate-city-pages.py` so all 112 city pages link their own city's EV/panel/rewiring page.
4. **Submit CALeVIP Connects + EVITP Find A Contractor** — both P0, free, EVITP-gated, AMY qualifies on both.
5. **Re-run the audit gate** after changes: `schema-tool.py validate` → `audit-price-drift.py --strict` → `audit-site.py` → `node --test scripts/test-*.mjs` → rebuild CSS/JS → `wrangler deploy --dry-run` → push to `main`.

---

## Sources

- `[repo: AGENTS.md]` — page counts, hosting, canonicals, constraints, pre-push gate
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — 1,000 queries, impressions/clicks/CTR/position
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — 142 pages, 21,745 impressions, 78 clicks
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Devices.csv]` — mobile 26.6 vs desktop 43.3 avg position
- `[repo: seo-workspace/keywords/opportunities.md]` — keyword opportunity table, striking-distance register
- `[repo: seo-workspace/keywords/clusters.md]` — cluster→page map, cannibalization register, internal-link opportunity
- `[repo: seo-workspace/content/emergency-electrician-brief.md]` — emergency page winning outline
- `[repo: seo-workspace/competitors/electric-connection-la.md]` — competitor intent breadth analysis
- `[repo: seo-workspace/outreach/prospects.md]` — link prospect directory (CALeVIP, EVITP, AAGLA, SRAR, CSLB, chamber)
- `[repo: scripts/site_data.py]` — canonical reviewCount 87, business data, single source of truth
- `[repo: sitemap.xml]` — 306 URLs
- `[repo: scripts/photo-manifest.csv]` — 388 rows (387 photos)
- `[remote: .github/workflows/audit.yml + deploy.yml]` — CI audit and deploy both green on `main` at `2104264c`
- `[directional: web]` — competitor page-structure observations (theelectricconnection.com, 911electrics.com)