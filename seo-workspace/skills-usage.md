# Skill usage — AMY Electric site

Every skill vendored in `.agents/skills/` (hash-pinned in `skills-lock.json`),
mirrored into `.claude/skills/` as symlinks. Validate with:

```bash
python3 scripts/audit-skills.py
```

## Skills list

| Skill | Type | Used by |
|---|---|---|
| `seo-project-setup` | SEO | `seo` agent, workflow 1 |
| `keyword-research` | SEO | `seo` agent, workflow 2 |
| `keyword-clustering` | SEO | `seo` agent, workflow 3 |
| `competitor-analysis` | SEO | `seo` agent, workflow 4 |
| `link-prospecting` | SEO | `seo` agent, workflow 5 |
| `seo-content-brief` | SEO | `seo` agent (new pages) |
| `seo-page` | SEO | `seo` agent (single URL) |
| `seo-technical` | SEO | `seo` agent (tech/crawl) |
| `seo-sitemap` | SEO | `seo` agent, `geo-linking` |
| `seo-images` | SEO | `seo` agent (images/gallery) |
| `seo-audit` | SEO | `seo` agent (full-site audit) |
| `seo-local` | SEO | `seo` agent (local/GBP; distinct from `gbp`) |
| `seo-geo` | SEO | `seo` agent (AI visibility) |
| `seo-schema` | SEO | `seo` agent (JSON-LD) |
| `seo-content` | SEO | `seo` agent (E-E-A-T) |
| `seo-programmatic` | SEO | `seo` + `geo-linking` (template safeguards) |
| `seo-hreflang` | SEO | `seo` agent |
| `seo-drift` | SEO | `seo` agent |
| `seo-competitor-pages` | SEO | `seo` agent (vs/alternatives) |
| `seo-cluster` | SEO | `seo` agent (topic architecture) |
| `seo-coach` | SEO | `seo` agent (guidance mode) |
| `competitive-landscape` | SEO | `seo` agent (market view) |
| `web-perf` | Perf | `web-perf` agent |
| `workers-best-practices` | Cloudflare | `gbp` agent (Worker code) |
| `workers-profiling` | Cloudflare | on demand |
| `wrangler` | Cloudflare | `gbp`, `geo-linking`, `web-perf`, `seo` |
| `cf-cli` | Cloudflare | `gbp` (Cloudflare CLI) |
| `cloudflare` | Cloudflare | on demand (product selection) |
| `turnstile-spin` | Cloudflare | on demand (bot verification) |

## Degradation

Only the `cloudflare` MCP server is connected. OpenSEO/DataForSEO are usually
unavailable. When a skill assumes those tools, degrade in this order:

1. GSC CSVs in `seo-workspace/gsc/` — tag `[gsc: <file>]`.
2. `websearch`/`webfetch` — tag `[directional: web]`.
3. Repo facts — tag `[repo: <path>]`.

Never report a number from a tool you did not call. Write `unknown` if unsourced.

## History

- 2026-11-03: Vendored 15 additional SEO skills from the global pool
  (`seo-content-brief`, `seo-page`, `seo-technical`, `seo-sitemap`,
  `seo-images`, `seo-audit`, `seo-local`, `seo-geo`, `seo-schema`,
  `seo-content`, `seo-programmatic`, `seo-hreflang`, `seo-drift`,
  `seo-competitor-pages`, `seo-cluster`); pruned 12 irrelevant Cloudflare
  skills (`agents-sdk`, `basin`, `k2`, `nextjs-on-cloudflare`, `sandbox-*`,
  `cloudflare-one*`, `cloudflare-email-service`, `durable-objects`); added
  `.claude/skills/` symlink mirror, `scripts/audit-skills.py`, and a
  `web-perf` agent.
