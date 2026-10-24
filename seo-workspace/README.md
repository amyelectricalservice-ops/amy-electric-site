# AMY Electric SEO Workspace

> **Best action right now:** the site already ranks for reward-heavy demand but wins almost no
> clicks — 21,745 page impressions produced **78 clicks** in the last exported GSC window, with the
> biggest cluster (`whole home rewiring`, 2,727 impressions) sitting at position 41. Fix *authority
> and CTR* on the ~8 URLs that already rank, not content depth.

Last refreshed: 2026-10-24 (full SEO pipeline re-run — context, keywords, clusters, competitors, links; see `reports/content-review-2026-10-24.md`).

## Website

- Primary domain: amyelectric.com
- Target area: Greater Los Angeles — **112 `city-*.html` pages** (16 core + neighbourhoods), plus
  **48 geo service pages** (24 `ev-charger-installation-*` + 24 `panel-upgrade-*`).
  *(Earlier note said "16 city pages, 62+ ZIP codes" — that understated the current inventory.)*
- Hosting: Cloudflare **Workers + Assets** (`run_worker_first: true`), auto-deploy on push to `main`.

## Business facts (do not restate from memory — verify in repo)

- AMY Electric · licensed electrical contractor · **C-10 #981578** · **EVITP #4051604**
- Phone **(818) 302-5614** (`tel:18183025614`) · info@amyelectric.com
- Canonical prices: NEMA **$350–$600**, Tesla **$500–$1,200**, hardwired **$500–$1,200**
- `reviewCount` canonical = **87**, single source `scripts/site_data.py`

## Goals

- Get local leads
- Improve content
- *(Added 2026-10-18)* Convert existing impressions into clicks and calls: the site is
  ranking-but-not-winning, so the metric that matters is **non-brand CTR on positions 8–20**,
  then qualified leads.

## Strategy & Positioning

- Local electrical contractor (C-10 & EVITP licensed)
- Focus on high-value services (EV chargers, panel upgrades, rewiring, emergency)
- **387 gallery photos** (388 rows incl. header in `scripts/photo-manifest.csv`) —
  *(earlier note said "30 real project photos")*
- Phone/Estimate forms available; `/book` online booking (requests confirmed by text)
- Differentiators competitors do **not** have in one place: EVITP certification, a live estimate
  engine, a 387-photo project gallery, and 112 city pages.

## Data sources & their trust level

| Source | Location | Trust | Notes |
| :--- | :--- | :--- | :--- |
| Google Search Console export | `gsc/amyelectric.com-Performance-on-Search-2026-09-05/` | **First-party, real** | Last 3 months ending 2026-09-05. **5+ weeks stale.** |
| OpenSEO MCP (local, `127.0.0.1:4151`) | — | **Reachable but unusable** | Server + project exist; DataForSEO backend returns HTTP 401; GSC/GA4 not connected. See `reports/context-status.md`. |
| DataForSEO MCP | — | **Not callable** | Not exposed to the agent runtime. |
| `websearch` / `webfetch` | — | Directional only | Always labelled `[directional: web]`. |
| Repo (`*.html`, scripts, config) | this worktree | **Verifiable** | Labelled `[repo: <path>]`. |
| Cloudflare MCP | — | Connected | Only MCP server reliably available. |

## Workspace map

```
seo-workspace/
  README.md                       ← this file (context, goals, sources)
  gsc/                            ← real GSC CSVs + intake instructions
  keywords/                       ← opportunities.md, clusters.md, keyword-clusters.md
  competitors/                    ← one study per competitor + README index
  content/                        ← per-cluster content briefs
  outreach/                       ← prospects.md, templates.md, GBP action plan
  reports/                        ← context-status.md, gsc-opportunity-report.md,
                                    improvement-plan-*.md, competitor-landscape.txt,
                                    onpage-seo.txt, technical-seo.txt
```

## Standing constraints

- Never invent metrics; write `unknown` and say why.
- Never unify the 112 city pages' `areaServed` shapes or invent per-city data.
- Never hand-edit built files (`css/style.min.css`, `js/site.min.js`, `js/estimator.min.js`,
  `js/vendor/**`).
- Never run `scripts/sync-faq-schema.py --apply`.
- Only City-of-LA pages may claim LADWP; Alhambra / Bellflower / Carson / Santa Clarita are SCE.

## Sources

- `[repo: AGENTS.md]` — page counts, hosting, canonicals, constraints, pre-push gate
- `[repo: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — impressions/clicks/position
- `[repo: sitemap.xml]` — 306 URLs
- `[repo: scripts/photo-manifest.csv]` — 388 rows
- `[openseo: whoami]`, `[openseo: list_projects]`, `[openseo: get_backlinks_overview]` (HTTP 401),
  `[openseo: get_search_console_performance]` (not configured) — MCP reality check
