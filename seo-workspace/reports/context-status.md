# Context Status — AMY Electric SEO Workspace

**Date:** 2026-10-24 · **Workflow:** 1 (project context / `seo-project-setup`) — refreshed 2026-10-24
**Best action:** nothing to set up — the workspace and the MCP project both exist. The one thing
blocking *live* SEO data is a broken DataForSEO credential in the local OpenSEO server
(`HTTP 401`). Fix that and every keyword/SERP/backlink workflow stops being directional.

---

## Status checklist

| Step | Status | Notes | Next action |
| :--- | :--- | :--- | :--- |
| 1. Working folder | ✅ Done | `seo-workspace/` with `gsc/ keywords/ competitors/ content/ outreach/ reports/` | none |
| 2. Website scope | ✅ Done | amyelectric.com, Greater LA; 315 pages; 307 sitemap URLs; en/Los Angeles (US) market `2840` | none |
| 3. Goals | ✅ Done | Local leads + content improvement; refined to "convert existing impressions to clicks/calls" | none |
| 4. Positioning | ✅ Done | C-10 + EVITP, LA-focused, EV/panel/rewiring/emergency, estimator, 387-photo gallery | none |
| 5. OpenSEO MCP check | ⚠️ **Reachable, not usable** | Server v0.0.12 live at `127.0.0.1:4151`; project `amyelectric.com` (`d6aa8126-ec55-49a7-90cd-fe030ccb6326`) exists; **DataForSEO returns HTTP 401**; GSC + GA4 not connected; project memory empty | Owner: repair DataForSEO credentials in the local OpenSEO self-host config |
| 6. GSC export | ⚠️ Stale | Real export present, window **ends 2026-09-05** (~6 weeks old) | Owner: re-export last 3 months → `gsc/` |
| 7. Asset inventory | ✅ Done | See below | none |
| 8. Next workflow | ✅ Done | Ran workflows 2–5 this session | Re-run 2–4 after fresh GSC + working DataForSEO |

---

## 1. MCP reality check (probed, not assumed)

The `seo-*` skills assume OpenSEO MCP tools. I probed rather than assumed.

**OpenSEO MCP — reachable.** A JSON-RPC `initialize` POST to `http://127.0.0.1:4151/mcp`
returned HTTP 200, `serverInfo: OpenSEO MCP 0.0.12`, and `tools/list` returned **47 tools**
(`research_keywords`, `get_keyword_metrics`, `get_domain_overview`, `get_ranked_keywords`,
`get_backlinks_overview`, `get_serp_results`, `get_local_serp_results`, `get_business_profile`,
`get_search_console_performance`, `get_search_opportunities`, `run_site_audit`, …).

**But every data-backed tool fails.** Verified with two independent calls:

| Probe | Result | Consequence |
| :--- | :--- | :--- |
| `whoami` | ✅ `admin@localhost`, mode `self-hosted`, scopes `none` | server healthy |
| `list_projects` | ✅ 1 project: `amyelectric.com`, market `2840/en` | project mapped |
| `get_project_context` | ✅ returns, but **all sections empty** | no shared memory to reuse |
| `list_saved_keywords` | ✅ "No saved keywords yet" | nothing previously saved |
| `get_keyword_metrics` | ❌ `DataForSEO HTTP 401 on /v3/dataforseo_labs/google/keyword_overview/live` | no volume/KD/CPC |
| `get_backlinks_overview` | ❌ `DataForSEO HTTP 401 on /v3/backlinks/history/live` | no backlink data |
| `get_domain_overview` | ❌ `DataForSEO HTTP 401 on .../domain_rank_overview/live` | no competitor traffic |
| `get_search_console_performance` | ❌ "not configured for Search Console yet" | no fresher GSC |
| `get_search_opportunities` / GA4 tools | ❌ "Google Analytics is not connected" | no GA4 join |

`dataforseo-mcp-server` (the second configured local MCP) is **not exposed to the agent runtime's
tool catalog at all**, so it could not be called even in principle.

**Conclusion — degrade exactly as designed:** GSC CSVs (first-party) → `websearch`/`webfetch`
(`[directional: web]`) → repo facts (`[repo: …]`). Cloudflare MCP is the only fully working MCP
server. **No deliverable in this run contains an invented volume, KD, CPC, traffic or backlink
number.** Where a metric would have come from DataForSEO, it says `unknown`.

---

## 2. Asset inventory (verified this session)

| Asset | Count | Evidence |
| :--- | ---: | :--- |
| Production HTML pages | 315 | `[repo: scripts/audit-site.py]` (2026-10-24) |
| URLs in `sitemap.xml` | 307 | `[repo: sitemap.xml]`, `grep -c '<loc>'` (2026-10-24) |
| `city-*.html` | 112 | `ls city-*.html \| wc -l` |
| Geo EV service pages | 24 | `ls ev-charger-installation-*.html \| wc -l` |
| Geo panel service pages | 24 | `ls panel-upgrade-*.html \| wc -l` |
| Blog posts (`blog/*.html`) | 60 + index | `ls blog/*.html \| wc -l` = 61 |
| Case studies | 4 + index | `[repo: case-studies/]` — `residential-ev-ready-garage`, `service-panel-capacity-plan`, `older-home-safety-correction`, `small-commercial-lighting-refresh` |
| Gallery photos | 387 | `[repo: scripts/photo-manifest.csv]` (388 rows) |
| Reviews canonical | 87 | `[repo: scripts/site_data.py]` |
| Cost / permit guides | present | `electrical-permit-cost-los-angeles.html`, `ladwp-electrical-guide.html` |
| Estimator + booking | present | `js/estimator.js`, `/book` (flatpickr 4.6.13) |

> ⚠️ **Stale documents in this workspace.** `reports/competitor-landscape.txt` is dated
> **2026-06-03** and states AMY has "42 pages / 12 city pages / no case studies / no
> social profiles / blog ~10 posts". Every one of those is now wrong (314 pages, 112 city pages,
> 4 case studies). Treat that file as **competitor intel only**, never as a description of AMY.
> `reports/improvement-plan-2026-10-13.md`'s **P0 emergency consolidation is already shipped**
> (both aliases now `noindex` + canonical + 301 to `/emergency-electrician-los-angeles`, and all
> 112 city pages link an emergency page — the plan said "0 of 112").

---

## 3. Recommendations

1. **Fix the OpenSEO DataForSEO credential** (local self-host) — this single fix unblocks
   keyword volume/KD/CPC, live SERPs, competitor keyword maps and backlink profiles.
2. **Re-export GSC** for the last 3 months; the current window is 6 weeks old and post-dates the
   emergency consolidation, so its effect is invisible in the data we have.
3. **Connect GSC + GA4 to OpenSEO** (needs `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` /
   `BETTER_AUTH_SECRET`, then reconnect from project settings) — unlocks `get_search_opportunities`,
   which joins positions 4–20 with GA4 outcomes and would directly score the near-miss terms.
4. Leave the workspace structure as is — it is already correct; do not rebuild it.

## Sources

- `[openseo: initialize / tools/list / whoami / list_projects / get_project_context / list_saved_keywords]` — reachability and project mapping
- `[openseo: get_keyword_metrics / get_backlinks_overview / get_domain_overview]` — DataForSEO HTTP 401
- `[openseo: get_search_console_performance / get_search_opportunities / get_google_analytics_organic_overview]` — not connected
- `[repo: AGENTS.md]`, `[repo: sitemap.xml]`, `[repo: case-studies/]`, `[repo: scripts/photo-manifest.csv]`
- `[repo: seo-workspace/reports/competitor-landscape.txt]`, `[repo: seo-workspace/reports/improvement-plan-2026-10-13.md]`
- `[repo: _redirects]`, `[repo: emergency-electrician.html]`, `[repo: emergency-electrical.html]` — consolidation verified shipped
