# Implementation Roadmap — AMY Electric (from SEO-STRATEGY.md §6)
*Generated 2026-11-07 · Phase 1 shipped 2026-11-04, now Phase 2*

## Phase 2: Expansion (Nov 2026 → Jan 2027) — in progress

| # | Task | Scope | Owner | Status |
|---|------|-------|-------|--------|
| 2.1 | Consolidate 3 duplicate-title pairs | _redirects + canonical to -los-angeles (450 hrefs), breaker already consolidated | agent | ✅ shipped 8f826869 |
| 2.2 | Deepen 6 thin posts (<800 words) to 1,500+ | generator cost, outdoor lighting, dedicated circuit, electrical inspection ×2, smart-home requirements — each + gallery photo proof | agent | TODO |
| 2.3 | Templated internal linking | generate-city-pages.py conditional geo cards + gallery card; avg inbound 1.7 → 3.06 | agent | ✅ shipped 8f826869 |
| 2.4 | Titles/meta + CTR on emergency & rewiring clusters | Rewrite emergency & whole-home-rewiring titles/meta per briefs `seo-workspace/content/emergency-electrician-brief.md` + `whole-home-rewiring-brief.md` | agent | TODO |
| 2.5 | GBP + citations | Claim/optimize GBP (NAP, hours, WhatsApp), Yelp/Apple/Bing, update `sameAs` in schema | owner | BLOCKED — needs Google account |
| 2.6 | Fresh GSC + DataForSEO creds | Re-export GSC 3mo → `seo-workspace/gsc/`, fix OpenSEO 401 | owner | BLOCKED |

## Phase 3: Scale (Jan → Apr 2027)

| # | Task | Gate |
|---|------|------|
| 3.1 | 1 post: recessed lighting cost (47 impr, pos 21.5) | Only if Phase 2 CTR on pos 8–20 moves |
| 3.2 | 1 post: panel-brand hazard (Federal Pacific/Pushmatic) | After 3.1 |
| 3.3 | Local chambers links (Winnetka, Sherman Oaks, Encino) + EVITP directory + gallery asset | — |
| 3.4 | Curated "best of" lists (2–3) | — |
| 3.5 | Perf: critical-CSS split (EV TBT 880ms → <200ms), fix `book` CLS 0.188 | — |

## Phase 4: Authority (Apr → Nov 2027)

- 1–2 thought-leadership/quarter (code changes, electrification, battery storage) — owner-gated
- PR: case studies from gallery + before/after, local media quotes
- Video schema if hero/team video ships
- Monthly audits: `scripts/audit-site.py` + `schema-tool.py validate` + `audit-skills.py` + `audit/lighthouse/REPORT-*.md`

## How we track

- Gate before any push: `schema-tool.py validate → audit-price-drift.py → audit-site.py (348 pages, 0 issues) → audit-skills.py → build-css/js → wrangler --dry-run` per `AGENTS.md`.
- KPI baselines: `SEO-STRATEGY.md §7` — re-measure after fresh GSC.
