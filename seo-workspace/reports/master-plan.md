# AMY Electric — Comprehensive Master Plan & Improvement To-Do

**Date:** 2026-10-20
**Branch:** `seo-agent-workspace` → `main`
**Goal:** Convert 21,745 GSC impressions → 78 clicks (0.36% CTR) into qualified leads. Fix what ranks first, then expand intent breadth, then build authority.

---

## Executive Summary

**The site does not have a traffic problem. It has a conversion problem.**

AMY Electric ranks for real, local, high-intent demand across Greater Los Angeles — 21,745 page impressions in the last GSC window (3 months ending 2026-09-05) — but produced only **78 clicks** (0.36% CTR). Roughly 71 of those 78 clicks are non-brand, and **the money pages (emergency, panel, EV, rewiring) got zero clicks despite thousands of impressions each.**

The site is technically excellent: schema validates, 314 pages audit clean, sitemap is sound, CSS/JS are reproducible, all 83 tests pass, both CI workflows are green on `main`. The gap is not technical SEO or content depth — AMY's core service pages are *longer* than the primary competitor's (The Electric Connection). The gap is:

1. **Above-the-fold conversion elements missing** on the highest-impression pages (no tap-to-call, no response expectation, no local trust signals in the hero).
2. **Link starvation** — 64 geo service pages rank 1–10 but have ≤30 impressions because each has only ~3 inbound internal links.
3. **Thin money page** — `/emergency-electrician-los-angeles` (975 words) carries 2,008 emergency impressions but converts none; 14 of 18 striking-distance queries are emergency intent, all landing here.
4. **Intent breadth gap** vs The Electric Connection — they publish per-hazard-brand panel pages, per-manufacturer EV pages, insurance/mandate content, and cost calculators. AMY consolidates brand intent into fewer URLs.

**Best action:** Fix the pages that already rank before creating anything new.

---

## Fresh Lighthouse Audit (Oct 20, 2026)

All 314 production HTML pages audited using local Chromium + Lighthouse 13.4.1 against `workers.dev`. Results saved to `audit/lighthouse/*-2026-10-20.json`. Comparison vs Oct 14 baselines:

| Page | Perf | A11y | BP | SEO | LCP | TBT | CLS | Notes |
|------|------|------|-----|-----|-----|-----|-----|-------|
| index | 92 | 100 | 96 | 66 | 2.67s | 0ms | 0 | LCP slightly >2.5s target |
| panel-upgrade | 95 | 100 | 96 | 69 | 2.61s | 12ms | 0 | Good |
| whole-home-rewiring | 89 | 100 | 96 | 69 | 3.17s | 28ms | 0 | LCP >2.5s |
| emergency-electrician-los-angeles | 87 | 100 | 96 | 66 | 3.13s | 36ms | **0.12 ⚠️** | CLS >0.1, LCP >2.5s |
| ev-charger-installation | 95 | 100 | 96 | 69 | 2.65s | 1ms | 0 | Good |
| tesla-charger-installation | 96 | 100 | 96 | 69 | 2.52s | 14ms | 0 | Good |
| gallery | 95 | 100 | 96 | **58 ⚠️** | 2.51s | 0ms | 0.07 | SEO score low |

**SEO scores are 58–69 across all pages** — consistent underperformance. Emergency page fails CLS (0.12 > 0.1) and LCP (3.13s > 2.5s).

---

## Pre-Push Gate (must pass before every push)

Run in order:
1. `python3 scripts/schema-tool.py validate` → "All pages pass validation."
2. `python3 scripts/audit-price-drift.py --strict` → 0 flagged pairs
3. `python3 scripts/audit-site.py` → "AUDIT OK — 0 issues."
4. `node --test scripts/test-*.mjs` → 83/83 pass, 0 fail
5. `python3 scripts/build-css.py && python3 scripts/build-js.py && git diff --exit-code css/style.min.css js/site.min.js` → clean
6. `npx wrangler deploy --config wrangler.jsonc --dry-run` → clean
7. Push to `main`, watch `.github/workflows/audit.yml` + `deploy.yml` → `conclusion=success`

---

## Constraints (never violate)

- Never hand-edit built files: `css/style.min.css`, `js/site.min.js`, `js/estimator.min.js`, `js/vendor/**`.
- Never run `scripts/sync-faq-schema.py --apply`.
- Never unify 112 city pages' `areaServed` shapes or invent per-city data (blocked on owner-supplied county/ZIP data).
- Canonical prices: NEMA $350–$600, Tesla $500–$1,200, hardwired $500–$1,200.
- Canonical reviewCount = 87 in `scripts/site_data.py` (333 occurrences, zero drift).
- Only City-of-LA pages may claim LADWP; Alhambra/Bellflower/Carson/Santa Clarita are SCE.
- Phone as `tel:18183025614`. Every page: JSON-LD, OG, Twitter Cards.
- Images: `loading="lazy"`, `decoding="async"`, `alt`, dimensions.
- Data sources labeled: `[gsc: <file>]`, `[directional: web]`, `[repo: <path>]`, or `unknown`. Never invent metrics.
- Live keyword/backlink APIs unavailable (DataForSEO HTTP 401). Fresh PageSpeed/CrUX field data requires owner credentials.

---

## Prioritized To-Do List

### Phase 1 — Fix What Already Ranks (Weeks 1–2, no new pages)

**Goal:** Convert existing impressions into clicks and calls. Target: 0 → 2–4% CTR on striking-distance pages.

| # | Action | Page(s) | Effort | Expected Impact | Source | Status |
|---|--------|---------|--------|-----------------|--------|--------|
| 1.1 | Expand emergency page 975 → 2,400–2,800 words. Add: dispatch process, response expectations, "what to do before we arrive", LADWP-vs-electrician disambiguation, after-hours process, emergency price posture, permit/utility side of burned panel. Add tap-to-call above fold + CTA band with (818) 302-5614. Add EmergencyService schema + local business schema (reviewCount 87, EVITP #4051604, hours). | `/emergency-electrician-los-angeles` | Medium | Capture 14 striking-distance emergency queries; 2,008 impressions currently at 0 clicks | `[repo: seo-workspace/content/emergency-electrician-brief.md]`, `[gsc: Queries.csv]` | ⬜ |
| 1.2 | Fix 4 cannibalizing duplicate-title pairs — 301 weaker into stronger via `_redirects`, keep one canonical. | 8 URLs (4 pairs) | Low | Consolidate split authority | `[repo: seo-workspace/keywords/clusters.md]` | ⬜ |
| 1.3 | Template city→geo-service internal links in `generate-city-pages.py` so all 112 city pages link their own city's EV/panel/rewiring geo service page; geo pages link back to city page. | 112 city pages + 64 geo service pages | Medium (one template change) | Geo pages rank 1–10 with ≤30 impr due to ~3 inbound links each | `[repo: seo-workspace/keywords/clusters.md]` | ⬜ |
| 1.4 | Re-title/re-describe emergency and rewiring pages for CTR (0% CTR at pos 10–18 is a snippet problem, not relevance). | Emergency, rewiring service pages | Low | Improve CTR without moving position | `[gsc: Queries.csv]` | ⬜ |
| 1.5 | Submit CALeVIP Connects (EVITP-gated, free, statewide directory for EV contractors). | Off-site | Low | High-value free listing; EVITP #4051604 is the gate competitors can't self-grant | `[repo: seo-workspace/outreach/prospects.md]` P0 | ⬜ |
| 1.6 | Submit EVITP "Find A Contractor" California listing — AMY is NOT currently listed. | Off-site | Low | Directory LA EV buyers check; genuine outbound link | `[repo: seo-workspace/outreach/prospects.md]` P0 | ⬜ |

### Phase 2 — Match Competitor Intent Breadth (Weeks 2–6, new pages)

**Goal:** Capture intent AMY currently cedes to The Electric Connection.

| # | Action | Page(s) | Effort | Expected Impact | Source | Status |
|---|--------|---------|--------|-----------------|--------|--------|
| 2.1 | Create per-hazard-brand panel pages: Federal Pacific, Pushmatic, old fuse box replacement. | `/federal-pacific-panel-replacement`, `/pushmatic-panel-replacement` | Medium | Competitor has dedicated pages per hazard brand; AMY has one Zinsco blog post | `[repo: seo-workspace/competitors/electric-connection-la.md]`, `[repo: seo-workspace/keywords/clusters.md]` P1 | ⬜ |
| 2.2 | Create insurance/mandate content: LA County electrical mandates, insurance-driven panel replacement, property-management electrical compliance. | New blog + service section | Medium | **Strongest untaken angle** — high-ticket, link-attracting topic AMY has zero page for | `[repo: seo-workspace/competitors/electric-connection-la.md]` | ⬜ |
| 2.3 | Split brand intent: per-manufacturer EV pages (Ford, Hyundai, Nissan, etc.) leveraging EVITP #4051604 on each. | New EV manufacturer pages | Medium | Competitor runs per-make pages; AMY consolidates brand intent | `[repo: seo-workspace/competitors/electric-connection-la.md]` | ⬜ |
| 2.4 | Promote existing live estimate engine more visibly on service pages (or add cost calculators). | New tool pages + CTA on service pages | Medium | Competitor has calculators; AMY's estimate engine is superior but under-exposed | `[repo: seo-workspace/competitors/electric-connection-la.md]` | ⬜ |

### Phase 3 — Lead Conversion & Authority (Weeks 6–12, ongoing)

**Goal:** Turn traffic into qualified leads; build off-site authority.

| # | Action | Effort | Expected Impact | Source | Status |
|---|--------|--------|-----------------|--------|--------|
| 3.1 | AAGLA Business Council / Supplier Directory — multifamily property managers. | Medium | B2B commercial leads in AMY's home turf | `[repo: seo-workspace/outreach/prospects.md]` P1 | ⬜ |
| 3.2 | SRAR (Southland Regional Association of REALTORS) affiliate membership — SFV + Santa Clarita agents. | Medium | Realtor referral pipeline | `[repo: seo-workspace/outreach/prospects.md]` P1 | ⬜ |
| 3.3 | GBP posting cadence — 30 posts, every other day, 2026-10-21→2026-12-18 (calendar + agent built; needs OAuth secrets). | Low (manual until agent armed) | Local pack visibility | `[repo: gbp-posting-calendar.md]`, `[repo: gbp-agent.js]` | ⬜ |
| 3.4 | Review acquisition — push reviewCount from 87 toward 100+. | Ongoing | Trust signal on every page | `[repo: scripts/site_data.py]` | ⬜ |
| 3.5 | Photo gallery integration — surface 2–3 real project photos on each geo service page and city page. | Medium | Conversion proof competitors can't match | `[repo: scripts/photo-manifest.csv]` | ⬜ |

### Phase 4 — Technical SEO (from fresh Lighthouse audit)

**Goal:** Fix performance and SEO score issues identified in Oct 20 audit.

| # | Action | Page(s) | Effort | Target | Source | Status |
|---|--------|---------|--------|--------|--------|--------|
| 4.1 | Fix CLS on emergency page (0.12 → <0.1). | `/emergency-electrician-los-angeles` | Low | CLS < 0.1 | `[repo: audit/lighthouse/]` Oct 20 | ⬜ |
| 4.2 | Fix LCP on emergency page (3.13s → <2.5s) and whole-home-rewiring (3.17s → <2.5s). | Emergency, rewiring | Medium | LCP < 2.5s | `[repo: audit/lighthouse/]` Oct 20 | ⬜ |
| 4.3 | Fix SEO score (58–69 → ≥90) across all pages. | All 314 pages | Medium | SEO ≥ 90 | `[repo: audit/lighthouse/]` Oct 20 | ⬜ |
| 4.4 | Fix gallery SEO score (58 → ≥90). | `/gallery` | Low | SEO ≥ 90 | `[repo: audit/lighthouse/]` Oct 20 | ⬜ |
| 4.5 | Fix missing `</head>` on 5 blog pages. | 5 blog pages | Low | 0 missing head close | `[repo: implementation_plan.md]` | ⬜ |
| 4.6 | Strip trailing `"+ "` junk from FAQPage names (3 pages, 15 names). | 3 pages | Low | 0 junk FAQ names | `[repo: implementation_plan.md]` | ⬜ |
| 4.7 | Add unmarked visible FAQs to schema (4 questions on 3 pages). | 3 pages | Low | FAQPage matches visible questions | `[repo: implementation_plan.md]` | ⬜ |

### Phase 5 — Performance (from fresh Lighthouse audit)

**Goal:** Improve Core Web Vitals on key pages.

| # | Action | Page(s) | Effort | Target | Source | Status |
|---|--------|---------|--------|--------|--------|--------|
| 5.1 | Gallery preload/lazy-load fixes (preload mismatch, images 2–6 eager→lazy). | `/gallery` | Medium | Perf ≥ 90, LCP < 2.5s | `[repo: implementation_plan.md]` | ⬜ |
| 5.2 | Gate estimator init behind `requestIdleCallback`/IntersectionObserver on index. | `/` | Medium | TBT < 200ms | `[repo: implementation_plan.md]` | ⬜ |

### Phase 6 — Backlinks/Citations/YouTube

**Goal:** Build off-site authority and local pack visibility.

| # | Action | Effort | Expected Impact | Source | Status |
|---|--------|--------|-----------------|--------|--------|
| 6.1 | Execute backlink prospects: CALeVIP, EVITP, AAGLA, SRAR, CSLB, chamber. | Medium | Quality backlinks + citations | `[repo: seo-workspace/outreach/prospects.md]` | ⬜ |
| 6.2 | Local citation consistency (canonical NAP: AMY Electric \| (818) 302-5614 \| info@amyelectric.com \| Greater Los Angeles \| C-10 #981578 \| EVITP #4051604). | Medium | NAP consistency, local trust | `[repo: seo-workspace/outreach/prospects.md]`, `[repo: seo-workspace/SEO_LOCAL_CITATION_PLAN.md]` | ⬜ |
| 6.3 | YouTube 12-video plan — publish, embed on relevant pages with VideoObject schema. | High | Video SEO, E-E-A-T | `[repo: SEO_YOUTUBE_STRATEGY.md]` | ⬜ |

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
| Emergency page CLS | 0.12 | <0.1 | <0.1 |
| Emergency page LCP | 3.13s | <2.5s | <2.5s |
| Site-wide SEO score (Lighthouse) | 58–69 | ≥80 | ≥90 |

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
2. **Fix the 4 duplicate-title cannibalization pairs** — 301 weaker into stronger via `_redirects`.
3. **Template the city→geo-service internal link** in `generate-city-pages.py` so all 112 city pages link their own city's EV/panel/rewiring page.
4. **Submit CALeVIP Connects + EVITP Find A Contractor** — both P0, free, EVITP-gated, AMY qualifies on both.
5. **Re-run the audit gate** after changes: `schema-tool.py validate` → `audit-price-drift.py --strict` → `audit-site.py` → `node --test scripts/test-*.mjs` → rebuild CSS/JS → `wrangler deploy --dry-run` → push to `main`.
6. **Watch CI** — both `audit.yml` and `deploy.yml` must show `conclusion=success` on `main`.

---

## Sources

- `[repo: AGENTS.md]` — page counts, hosting, canonicals, constraints, pre-push gate, remaining work
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
- `[repo: audit/lighthouse/*-2026-10-20.json]` — fresh Lighthouse audits for all 314 pages
- `[remote: .github/workflows/audit.yml + deploy.yml]` — CI audit and deploy both green on `main`
- `[directional: web]` — competitor page-structure observations (theelectricconnection.com, 911electrics.com)

---

## Blocked Stop Condition

Stop if: (a) fresh GSC export or PageSpeed field data cannot be obtained without owner credentials — report exactly what's missing, attempted paths, and what owner input unlocks progress; (b) any pre-push gate step fails — fix before continuing; (c) Lighthouse/Chromium unavailable — report and use Oct 20 results as directional only. Otherwise proceed through all phases.
