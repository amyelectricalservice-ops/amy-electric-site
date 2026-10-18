# AMY Electric — Competitor Studies

One file per competitor, written by the `seo` agent (workflow: competitor analysis). Master
landscape and tiering live in [`../reports/competitor-landscape.txt`](../reports/competitor-landscape.txt).

**Last refreshed:** 2026-10-18 · **Session data limitation:** no keyword, SERP, traffic or backlink
data exists for *any* domain in this session — the OpenSEO MCP's DataForSEO backend returns
`HTTP 401` (see `../reports/context-status.md`). Every study therefore relies on **direct page and
sitemap fetches** (labelled `[directional: web]`) plus repo facts. **No study contains an invented
traffic, keyword, difficulty or backlink number; those fields read `unknown`.**

## Files

| Competitor | Domain | File | Status | Pages (verified this session) |
| :--- | :--- | :--- | :--- | :--- |
| **The Electric Connection** (primary) | `theelectricconnection.com` | [`electric-connection-la.md`](electric-connection-la.md) | ✅ studied | 255 URLs |
| 911 Construction & Electric | `911electrics.com` | [`911electrics.com.md`](911electrics.com.md) | ✅ studied | 492 URLs |
| Dynamic Power Group | `dpgcontractors.com` | [`dpgcontractors.com.md`](dpgcontractors.com.md) | ✅ studied | ~80 URLs |
| Branover Contractors | `branovercontractors.com` | [`branovercontractors.com.md`](branovercontractors.com.md) | ⚠️ partial | sitemap not retrievable |
| Bryden Electrical | `brydenelectrical.com` | [`brydenelectrical.com.md`](brydenelectrical.com.md) | ✅ studied | 40 URLs (34 pages + 6 posts) |

## Corrections to this index

- **The primary target's domain is `theelectricconnection.com`, not `electricconnectionla.com`.**
  `electricconnectionla.com` **does not resolve** (HTTP 000). This index previously listed it with a
  *(verify)* flag — now verified and corrected.
- **`readyelectricincusa.com` — homepage returns HTTP 404.** The June 2026 landscape (7-page site,
  "Best Electrician Los Angeles" Yelp award) no longer matches reality. Not studied; treat as
  defunct or relocated until the owner confirms otherwise.
- **`drelectricca.com` — does not resolve** (HTTP 000). Prior landscape already noted it blocks
  automated extraction. Not studied.

## Cross-competitor findings (the three that matter)

1. **AMY's service pages are not too short — they are already longer than the market.** Measured:
   AMY `/whole-home-rewiring` **4,285 words** vs the primary competitor's `/house-rewire/` **3,817**;
   AMY `/panel-upgrade` **5,204** vs their `/panel-upgrades/` **4,100**; AMY `/ev-charger-installation`
   **3,759** vs their EV page **3,747**. **The bottleneck is authority, internal linking and CTR.**
2. **AMY's schema is ahead of all five.** `Electrician` type on 309 pages,
   `OpeningHoursSpecification` on 248, `EducationalOccupationalCredential` on 244, plus `HowTo`,
   `Offer`/`PriceSpecification`, `AggregateRating`, `FAQPage`. None of the five competitor homepages
   carry a ratings block; three carry no local-business type at all.
   ⚠️ The June 2026 landscape's advice to "add Place/Organization/OpeningHours schema" is **stale** —
   it has been done.
3. **Two untaken content angles are shared by the strongest competitors:**
   **insurance-/mandate-driven panel replacement** (`theelectricconnection.com` has two dedicated
   pages on the LA County 82°F cooling mandate and insurance rules; Branover has an insurance panel
   FAQ) and **one page per panel-hazard brand** (Zinsco, Federal Pacific, Pushmatic, fuse boxes).
   AMY covers Zinsco only, in a single blog post.

## Highest-value single action from the competitor set

**AMY Electric is not listed in EVITP's Find A Contractor directory — but 911 Construction &
Electric is** (`evitp.org/california/listing/911-construction-electric-inc`). AMY holds EVITP
certification **#4051604** and is absent from the directory that exists to showcase it. Contact
`info@evitp.org`. See [`911electrics.com.md`](911electrics.com.md) and
[`../outreach/prospects.md`](../outreach/prospects.md).

## Conventions

- Filename = the competitor's domain (or a clear slug where the domain is uncertain).
- Each study: snapshot, biggest lesson, best opportunity to beat them, keyword themes, page/content
  types, backlink notes, head-to-head SERP observations, and priority actions for AMY Electric.
- Separate **evidence** from **inference**; end every study with `## Sources`.
- Never claim a live metric that no tool returned — write `unknown`.
- Clearly flag figures carried over from `competitor-landscape.txt` (dated **2026-06-03**) as
  **dated**, not current.

## Sources

- `[directional: web]` — resolution checks and homepage fetches for all five domains plus `electricconnectionla.com`, `readyelectricincusa.com`, `drelectricca.com`
- `[directional: web]` — sitemap fetches (counts and URL patterns) for all reachable domains
- `[directional: web]` — `evitp.org/california` directory contents
- `[repo: seo-workspace/competitors/*.md]` — the five studies in this folder
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — June 2026 tiering (dated)
- `[openseo: get_domain_overview / get_backlinks_overview / get_ranked_keywords / get_serp_results → DataForSEO HTTP 401]` — no third-party SEO metrics available for any competitor
