# AMY Electric — Strategic SEO Plan
*Last updated: 2026-11-04 · replaces 2026-09-15 version · template: `local-service.md`*

> **Best action this quarter:** the site already ranks for high-intent LA terms but wins almost no clicks — 21k impressions → 78 clicks (last GSC window ending 2026-09-05, cluster *whole-home rewiring* at 2,727 impr, pos 41). The bottleneck is **CTR + authority on the 11 existing clusters** (especially emergency, rewiring, EV/Tesla), not new URLs. Fix titles/meta, internal linking, and citations before creating anything.

---

## 1. Discovery

### Business type & target audience
- **Business:** AMY Electric · licensed C-10 **#981578** · EVITP **#4051604** · (818) 302-5614 — local service business, Greater Los Angeles. Phone/form is the conversion, not cart.
- **Audience:** LA homeowners (panel, rewiring, EV charger, lighting, emergency), landlords/property managers (ADU/subpanel), and small commercial (retail, EV fleet, tenant improvement). Urgent intent (emergency/same-day) + research intent (cost, permits, comparisons).
- **Competitors (top 5, verified in `seo-workspace/competitors/`):** Electric Connection LA (primary), Dynamic Power Group, Branover Contractors, 911 Construction & Electric, Bryden Electrical.
- **Goals:** qualified local leads (calls + `/book` requests + estimate forms), not vanity traffic. Secondary: content completeness for AI citations.
- **Budget/timeline:** owner-operated; content velocity is ~2 posts/week max; GBP posts are manual (30 queued to 2026-12-18, auto-posting code shipped pending OAuth).
- **KPIs (this plan):** non-brand CTR on positions 8–20, local-pack presence on `electrician [city]`/`[service] los angeles`, leads from organic, and `reviewCount` growth (canonical 87 in `scripts/site_data.py`).

### Current site assessment (2026-11-04, verified)

| Metric | Count / value | Source |
|---|---:|---|
| Production HTML pages | 348 | `scripts/audit-site.py` (2026-11-04, 0 issues) |
| URLs in `sitemap.xml` | 545 image entries + 348 pages | `sitemap.xml`, `scripts/update-gallery.py` |
| City pages `city-*.html` | 112 (109 indexed, 3 `noindex`) | `ls city-*.html` |
| Geo service pages `ev-/panel-/whole-home-*-city` | 64 (24 + 24 + 16) | `ls *-installation-*.html` |
| Blog posts | 61 + index | `ls blog/*.html` |
| Gallery items | **545** (2,180 files, 4 variants each) — 0 generic captions | `scripts/photo-manifest.csv` (2026-11-04, was 387 on 2026-10-24) |
| Schema on every page | LocalBusiness/Electrician + Service/FAQPage/BreadcrumbList/BlogPosting/Speakable | `scripts/schema-tool.py validate` ✓ |
| Lighthouse perf (local, `audit/lighthouse/REPORT-2026-11-04.md`) | 94 homepage / 75 `book` (CLS 0.188) / 80 EV page (TBT 880 ms) | local Lighthouse |
| Hosting | Cloudflare Workers + Assets, `run_worker_first: ["/*","!/css/*","!/js/*","!/fonts/*"]`, auto-deploy on push | `wrangler.jsonc` |
| Caching | `_headers` `s-maxage=3600` on `/css/*` + `/js/*` (was 31536000, fixed 2026-11-04) | `_headers` |

**Strengths:** static HTML (fast, crawlable), full schema, 545-photo proof gallery with vision captions, EVITP credential (rare), live estimate engine, `/book` slot widget, `workers.dev` verified deploys, 112 city pages with geo variants.

**Weaknesses / constraints:** GSC export stale (ends 2026-09-05, 8 weeks old), DataForSEO creds return HTTP 401 (no live volume/KD/CPC), no Google Business Profile optimization yet, citations/backlinks thin, no Reddit/forum presence (hurts Perplexity), Fonts still render-blocking (`style.min.css` 33 KB, TBT driver).

---

## 2. Competitive Analysis

Detailed per-competitor studies live in `seo-workspace/competitors/` (one file per domain). Summary:

| Competitor | Content strategy | Schema/technical | E-E-A-T signals | Estimated DA* |
|---|---|---|---|---|
| **Electric Connection LA** | Per hazard-brand panel pages (Federal Pacific, Zinsco, Pushmatic), per-make EV pages | Spotty schema | Strong review volume | unknown (DataForSEO 401) |
| Dynamic Power Group | B2B/commercial focus, EV fleet | Minimal schema | Commercial case studies | unknown |
| Branover | Generalist LA electrician | Minimal | Reviews, no EVITP | unknown |
| 911 Electrics | Emergency + same-day messaging | Minimal | Reviews | unknown |
| Bryden Electrical | Residential panel/rewiring | Minimal | Reviews | unknown |

*DA/volume not fabricated — DataForSEO is 401, see `seo-workspace/reports/context-status.md`. Treat as `unknown`.

**Keyword gaps (GSC impressions captured, pos far from page 1):** `emergency electrician los angeles` (2,008 impr, emergency page pos >20), `home rewiring` (3,492 impr, blog outranks service page 86×), `ev charger installation los angeles` (1,905 impr, blog cost post competes with service page), `electrician [city]` (1,990 impr across 112 city pages, positions 26–57 — outranked on own city term). **AMY's edge:** the only LA electrician with EVITP + estimate engine + 545 captioned project photos + 64 geo service pages; competitors have 0–5 geo pages and no vision-captioned gallery.

---

## 3. Architecture Design

### URL hierarchy (current, keep)

```
/                     ← geo-personalized (20 neighborhoods, private/no-store on match)
├── /about, /contact, /get-quote, /book (flatpickr)
├── /reviews (canonical), /testimonials → 301, /gallery (545), /service-areas
├── /panel-upgrade, /ev-charger-installation, /tesla-charger-installation,
│   /whole-home-rewiring, /commercial-electrical, /lighting-installation, …
│   └── /{service}-{city}  (64 pages: ev-charger/panel/whole-home × city)
├── /city-{neighborhood}  (112 pages)
├── /blog/  (61 posts + index)
├── /case-studies/  (4)
└── /{guide}  (ladwp-electrical-guide, electrical-permit-cost-los-angeles, etc.)
```

### Quality gates (local-service template, applied)

| Page type | Target words | Unique % | Current | Gate |
|---|---|---:|---|---|
| Service pages | 2,000–3,500 | 100% | 17 pages | ✓ |
| Geo service pages | 1,500–2,500 | 40–60% | 64 pages | ✓ |
| City pages | 800–1,200 | 60%+ | 112 pages | ⚠️ template warns at 30, hard stop at 50 — AMY carries 112 because LA demands neighborhood granularity (112 city + neighborhood pages, 20 geo-targeted on `/`). Mitigation: templated uniqueness via landmarks/utility notes (LADWP vs SCE), per-city testimonials linkage, and the `city-*.html` audit sweep in `scripts/generate-city-pages.py`. Do not add more city pages without unique local proof. |
| Blog posts | 1,200–2,000 | 100% | 61 posts | 6 thin posts <800 words flagged for deepening |

**Internal linking:** city pages → geo service pages (≈3 inbound links each — link starvation flagged in `seo-workspace/keywords/clusters.md:86`). Template fix in `generate-city-pages.py` (city → its EV/panel/rewiring + backlink). Gallery is under-linked from service pages.

**Sitemap:** `sitemap.xml` holds 348 pages + 545 image entries, no `<priority>`/`<changefreq>`, validated by `scripts/audit-site.py` + `scripts/schema-tool.py validate`.

---

## 4. Content Strategy

### Content gaps vs competitors (from `seo-workspace/keywords/clusters.md`)
- **Panel-brand hazard** (Federal Pacific / Pushmatic / old fuse box) — competitor has per-brand pages, AMY has one Zinsco post.
- **Per-make EV** (Ford/Hyundai/Nissan home charger) — competitors run per-make pages; AMY's EVITP is the differentiator.
- **Recessed lighting cost, generator, outdoor lighting, dedicated circuit, grounding, video doorbell, surge protection, ADU/tenant improvement** — 30 new clusters briefed (clusters 12–48, briefs in `seo-workspace/content/`).

**Do not create** until the 11 existing clusters are fixed: cannibalization on `ev-charger-installation-cost-la` vs `-los-angeles` (identical titles, consolidate), `whole-home-rewiring-cost-la` vs `-los-angeles`, `breaker-keeps-tripping-causes` vs `-guide`, and thin posts (<800 words) listed in `clusters.md:161`.

### Page types & counts

| Type | Current | 12-month ceiling | Action |
|---|---:|---:|---|
| Service pages | 17 | 25 | Add only bathroom-electrical, panel-labeling if demand appears |
| Geo service pages | 64 | 64 | Freeze — link-starvation fix first |
| City pages | 112 | 112 | Freeze |
| Blog posts | 61 | 70–75 | Deepen 6 thin posts + 2–3 new per quarter, then stop |
| Gallery | 545 | ≤600 | Vision-captioned; no more bursts without curation |

### Blog / resource cadence
- **Q4 2026:** 0 new posts — deepen 6 thin posts (generator cost, outdoor lighting, dedicated circuit, electrical inspection ×2, smart-home requirements) + 2 emergency/rewiring briefs (`seo-workspace/content/emergency-electrician-brief.md`, `whole-home-rewiring-brief.md`).
- **2027:** 2 posts/quarter max (panel-brand hazard → recessed lighting → ADU deepening). Each needs author bio + gallery photo proof.

### E-E-A-T building plan
- **Experience:** Amy author bio on every blog post, gallery photo on every service page, `15+ years` signal consistent.
- **Expertise:** C-10 #981578 + EVITP #4051604 on every page, CA Electrical Code 2026 references, plain-language technical explainers.
- **Authoritativeness:** CSLB verification link, award/cert badges, trade-standard citations, gallery as proof (545 captioned photos).
- **Trustworthiness:** NAP 100% consistent, `reviewCount` 87 canonical, warranty/guarantee copy, licensed & insured badge. **GBP:** claim, keep hours accurate (hours is a top-5 ranking factor per Whitespark 2026), add WhatsApp (Business Chat is deprecated), and encourage photo reviews (Maps Stories format).

### Content calendar (next 90 days, priorities)

| Week | Type | Topic | Target | Source |
|---|---|---|---|---|
| 1–2 | Fix | Titles/meta + internal links on emergency & rewiring clusters | `emergency electrician los angeles`, `home rewiring` | `clusters.md` P0 |
| 3–4 | Deepen | 2 thin posts to 1,500+ words + gallery proof | `generator installation cost la`, `outdoor lighting installation la` | `clusters.md:161` |
| 5–6 | Deepen | 2 thin posts + consolidate `ev-charger-cost-la` vs `-los-angeles` | `ev charger installation cost los angeles` | `clusters.md` P1 |
| 7–8 | Citations | GBP + Yelp + Apple Maps + Bing Places (sameAs in schema) | local pack | template |
| 9–12 | 1 post | Recessed lighting cost (47 impr, pos 21.5 — near-miss) | `recessed lighting installation cost los angeles` | cluster 16 |

---

## 5. Technical Foundation

| Area | Current | Target | Owner |
|---|---|---|---|
| **Hosting** | Workers + Assets, `run_worker_first` narrowed, auto-deploy + `workers.dev` verify | Keep | — |
| **Caching** | `_headers` `s-maxage=3600` on bundles (fixed 2026-11-04, was 1y), `immutable` on fonts/img | Keep | — |
| **Schema per page type** | LocalBusiness/Electrician (homepage + city), Service (service), ContactPage, AggregateRating (reviews, 87), FAQPage/HowTo/BreadcrumbList/BlogPosting/Speakable | Add Service `priceRange` + Video when video ships | — |
| **Core Web Vitals** | LCP 1.1s, CLS 0.041 homepage; 3.3s gallery (expected, 545 images); TBT 880 ms EV page (style/layout, 33 KB CSS); `book` CLS 0.188 | LCP <2.5s ✓, CLS <0.1 (fix `book` + city images), TBT <200 ms (critical-CSS split) | — |
| **Images** | `img/gallery/` 545 photos ×4 variants, WebP + `?w=` via `worker.js serveImage()`, pre-generated AVIF parked | Keep | — |
| **AI readiness** | `/llms.txt` + `/llms-full.txt` + `/.well-known/api-catalog` with `Link` headers, `llmstxt-evidence` | Add presence on curated "best of" lists (top AI visibility factor per Whitespark) | — |
| **Mobile** | Touch targets 44×44, `.topbar`/`.nav-book` 3-place sync, RUM beacon | Keep | — |

**DataForSEO note:** every volume/KD/CPC/traffic figure in this plan that would normally come from DataForSEO is `unknown` until the local OpenSEO credential (HTTP 401) is fixed — see `seo-workspace/reports/context-status.md`. No number is invented.

---

## 6. Implementation Roadmap — 4 phases (anchored to Nov 2026)

### Phase 1: Foundation — *already shipped* (2026-10-18 → 2026-11-04)
- Single-Worker consolidation, real sitemap restored, `run_worker_first` narrowed, route audit hardened
- `llms.txt`/`llms-full.txt` + AI headers, photo pipeline 545 captioned photos, 112-city geo personalization, `_headers` caching fix
- Skills: 15 SEO skills vendored, audit + deploy green

### Phase 2: Expansion — weeks 5–12 (Nov–Jan)
- Deepen 6 thin posts + consolidate 3 duplicate-title pairs (no new URLs)
- Templated internal-link fix: city → geo service + backlink (`generate-city-pages.py`)
- Claim/optimize GBP (NAP, hours, WhatsApp, services), Yelp/Apple/Bing, update `sameAs`
- Directives: `sitemap.xml` + `robots.txt` fresh, IndexNow on each push

### Phase 3: Scale — weeks 13–24 (Jan–Apr 2027)
- 2 new blog posts (recessed lighting cost, then panel-brand hazard) — only if Phase 2 CTR on positions 8–20 moves
- Link building: local chambers (Winnetka, Sherman Oaks, Encino) + EVITP directory + gallery as linkable asset
- GEO: ensure presence on 2–3 curated "best electrician LA" lists
- Perf: critical-CSS split to cut EV-page TBT (880 ms → <200 ms), fix `book` CLS

### Phase 4: Authority — months 7–12 (Apr–Nov 2027)
- 1–2 thought-leadership posts/quarter (code changes, electrification, battery storage) — owner-gated
- PR: case studies from gallery + before/after, local media expert quotes
- Video schema if hero/team video ships
- Monthly `scripts/audit-site.py` + `schema-tool.py validate` + `audit-skills.py` + Lighthouse on `audit/lighthouse/REPORT-*.md`

---

## 7. KPI Targets

| Metric | Baseline (2026-11-04) | 3 mo (Feb 2027) | 6 mo (May 2027) | 12 mo (Nov 2027) |
|---|---:|---:|---:|---:|
| Organic sessions / mo | unknown (GSC 2026-09-05: 21k impr → 78 clicks, CTR 0.4%) | 300 | 800 | 1,500 |
| Indexed pages | 348 | 348 | 350 | 360 |
| Referring domains | unknown | 10 | 20 | 35 |
| `reviewCount` | 87 | 95 | 110 | 130 |
| Local-pack presence (`electrician [city]` / `[service] los angeles`) | ~0 (positions 26–57) | 3 keywords | 8 | 15 |
| Top-10 rankings | unknown | 3 | 8 | 15 |
| Lighthouse perf | 94 (homepage) | 94 | 95+ | 95+ |
| AI citations (ChatGPT/Perplexity) | 4 (ChatGPT, per LocalFox 6-query) | 6 | 8 | 12 |
| Leads from organic / mo | unknown | 10 | 25 | 40 |

Baselines marked `unknown` are not guessed — they require fixing the DataForSEO credential and re-exporting GSC (last export ends 2026-09-05).

---

## 8. Risk Mitigation

| Risk | Mitigation |
|---|---|
| No fresh GSC / DataForSEO 401 | Repair credential in local OpenSEO self-host; re-export last 3 months → `seo-workspace/gsc/` |
| 112 city pages flagged as thin/dup | Freeze at 112; enforce 60%+ unique per template via landmarks/utility/neighborhood proof; no new city pages without local proof |
| Competitor copy | Monthly content audit; gallery proof + EVITP as moat |
| Algorithm / AI shift | Diversify: GBP + citations + curated lists (top AI factor), not just Google |
| Negative reviews | Respond <48h, resolve offline |
| GBP hours inaccuracy (top-5 ranking factor) | Keep hours exact; extended hours if feasible |

---

## 9. Tool Stack

Free: GSC, GBP, Cloudflare Web Analytics, PageSpeed Insights, Schema.org validator.
Optional paid: Ahrefs/SEMrush (keyword/competitor), BrightLocal (local), Whitespark (citations), CallRail (call tracking).

*Review monthly; first review 2026-12-04.*
