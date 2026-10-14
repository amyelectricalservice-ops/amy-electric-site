# SEO Improvement Plan — data-driven (GSC 2026-09-05 + live audit 2026-10-13)

## Headline finding: impressions without clicks = fragmentation, not demand

| Cluster | Impressions | Clicks | Problem |
|---|---|---|---|
| Emergency | 2,170 | 0 | 4 URLs split the cluster; best ranker is a blog post (pos 12.6) |
| Rewiring | 3,791 | 0 | Blog guide (3,444 imps, pos 37.7) buries service page (40 imps) |
| Tesla | 1,414 | 1 | Only converting query on site; blog (pos 30) beats service page (pos 57) |
| Panel | ~1,100 | 5 | Healthiest cluster; blog cost post (pos 21) supports service page |

Pattern: **informational blog pages outrank transactional service pages**, and
internal link equity points at URLs Google doesn't prefer (`emergency-electrical`
has 252 inbound links but ~0 impressions).

## P0 — Emergency consolidation (dev; biggest ROI on site)

Three near-duplicate service pages (~40KB each) + one ranking blog post:

- `emergency-electrical` (nav-linked, 252 inbound, ~0 impressions)
- `emergency-electrician` (1,291 imps, pos 45)
- `emergency-electrician-los-angeles` (35 imps, pos 18.3; exact-match slug)
- `blog/emergency-electrician-los-angeles` (841 imps, pos 12.6 — closest to page 1)

Actions:
1. Primary = `emergency-electrician-los-angeles` (exact-match slug for the
   404-impression money query; workspace target agrees).
2. Canonicalize `emergency-electrician` + `emergency-electrical` → primary;
   keep both in `sitemap.xml` — CI (`audit.yml` sitemap-integrity gate) requires
   every indexable page listed, so delisting is not an option without a CI
   change. Canonical consolidation works with listed URLs.
3. Keep the ranking blog post but reframe as informational: move service CTA +
   tap-to-call above the fold, canonical stays self, links to primary.
4. Add emergency links to city pages (currently 0 of 112 link any emergency
   page) — highest-impression cluster has the weakest local support.

## P1 — Service-page transactional upgrades (dev)

For `whole-home-rewiring`, `tesla-charger-installation`, `panel-upgrade`:
distinct transactional intent vs ranking blog posts (price tables, permit
timelines, tap-to-call above fold, availability signals). Blogs keep
informational intent + funnel CTAs to service pages. Do not merge — intent
differs; win both slots.

## P2 — Off-site (owner; nothing here needs a developer)

- Prospect list (`outreach/prospects.md`): PlugShare, LA Chamber, realtor/HOA
  guest posts, AAGLA — status all still pending.
- GBP playbook exists (`outreach/local-seo-gbp-action-plan.md`): hours accuracy
  (top-5 local factor), weekly posts, keyword-rich review push.
- Fresh GSC export: current data is 5+ weeks old; re-run this report after it.

## P3 — Content (next briefs after ADU, which shipped)

Per `keywords/opportunities.md` P0s: Tesla Wall Connector installer angle,
`200 amp panel upgrade cost LA` price-table section, LADWP rebate checklist —
all map to existing pages, no new URLs needed.

## Verification after each change

`schema-tool.py validate` → `audit-site.py` (313 pages, 0 issues) →
price-drift → estimator tests → confirm live on apex (never workers.dev for
behavioral checks). Re-pull GSC in 3–4 weeks and re-run cluster table above.
