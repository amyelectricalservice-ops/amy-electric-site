# Content Brief: Geo Pages — 112 city pages + 64 service×city pages

**Mode:** improve existing pages (structural, not per-page rewrite)
**Target URLs:** `/city-*.html` (112) and `/ev-charger-installation-*`, `/panel-upgrade-*`,
`/whole-home-rewiring-*` (64)
**Date:** 2026-10-18

---

### Search Intent

**Local commercial / local transactional.** Every query in this cluster carries a place name, which
means Google is choosing between (a) a map pack, and (b) a page on a site that demonstrably serves that
place. The searcher wants "an electrician who will actually come to *my* city", not a national page
with a city name inserted.

**The single most important fact in this brief:** AMY's city pages rank **positions 26–57 for their own
city terms**, while its service×city pages rank **positions 1–18 on tiny volume**. Both halves of the
geo footprint are under-performing for opposite reasons — authority on one side, link starvation on the
other.

---

### Competitor Analysis

**⚠️ Method note:** no SERP API available (`get_serp_results` → DataForSEO HTTP 401). These are
sitemap-verified URL patterns, not confirmed rankings.

| # | Competitor | Geo URL pattern | Geo page count | Notes |
| :-- | :--- | :--- | ---: | :--- |
| 1 | **theelectricconnection.com** (primary) | `/electrician-<city>-ca/` | **~150** in a 255-URL page-sitemap | Covers neighbourhoods AMY has (Arleta, Boyle Heights, Koreatown, Silver Lake, Valley Village, Toluca Lake, Universal City, North Hills, Pacoima, Sun Valley, Tarzana, Winnetka) **plus** markets AMY does not serve (Orange County, Santa Clarita, Castaic, Fillmore, Simi Valley) |
| 2 | **911electrics.com** | `/<service>-los-angeles/` and `/electrician-<city>-ca/` | **492 URLs total** | Massive programmatic footprint; plus a `/service-areas/` hub |
| 3 | **brydenelectrical.com** | `/service-areas/<city>/` | ~5 | Small — competes on service pages instead |
| 4 | **branovercontractors.com** | `<city>-electrician` | 25+ (per `competitor-landscape.txt`, June 2026) | ⚠️ sitemap not retrievable this session (robots.txt points to `www.branovercontractors.com/sitemap_index.xml`, which returned empty) |
| — | **AMY Electric** | `/city-<slug>` + `/<service>-<city>` | **112 + 64 = 176** | Largest geo footprint of the set, but city pages lose their own terms and geo service pages are orphaned |

**AMY's structural advantage is real and measurable:** 176 geo URLs beats every competitor on count.
The primary competitor's geo titles are thin templated patterns (`<title>Sherman Oaks Electrician</title>`,
`<title>Encino Electrician</title>`) — **no service qualifier, no brand, no differentiator.** AMY's are
already better: `Sherman Oaks Electrician | Panel Upgrades | AMY Electric`. *Do not trade that away to
copy them.*

---

### Content Gaps and Opportunities

**Topic gaps (per-city, not per-template):**
- City pages do not connect the city to the **services that city actually buys**. A Santa Monica page
  should lead with historic-home rewiring (AMY already ranks **#7.6** for
  `electrical rewiring for historic santa monica homes`); a Sherman Oaks page should lead with panel +
  EV.
- City pages do not link their own city's EV / panel / rewiring service page. **This is the gap.**

**Depth gaps:**
- No per-city project evidence. AMY has 387 real photos; city pages don't show work *in that city*.
  This is the most available and least-used differentiator in the whole workspace.

**Quality gaps (measured):**
- `electrician sherman oaks`: 296 impressions, **position 37.0**, 0 clicks — while `/city-sherman-oaks`
  has 348 impressions at 35.6.
- `electrician studio city` 192 impr @ 25.9; `electrician encino` 181 @ 55.2;
  `electrician woodland hills` 176 @ 54.1; `electrician van nuys` 170 @ 56.0;
  `electrician burbank` 152 @ 55.8.
- Geo **service** pages: `/whole-home-rewiring-santa-monica` pos **1.0** on 2 impressions;
  `/panel-upgrade-culver-city` pos **8.0** on 4; `/ev-charger-installation-encino` pos **6.4** on 7;
  `/panel-upgrade-pasadena` pos 10.5 on 8; `/panel-upgrade-burbank` pos 10.5 on 23;
  `/ev-charger-installation-van-nuys` pos 17.6 on 30.
- **Each geo service page is linked from only 3 HTML files site-wide** (`[repo: grep -rl]`).

---

### Winning Outline

This cluster is fixed by **two structural changes plus a light per-page pass** — not by rewriting 176
pages.

#### Change 1 — Wire the geo graph (highest leverage, lowest risk)

In `generate-city-pages.py` (the template — do not hand-edit 112 files):

1. On every `/city-<slug>` page, add a "Services in <City>" block linking, where they exist:
   - `/ev-charger-installation-<slug>`
   - `/panel-upgrade-<slug>`
   - `/whole-home-rewiring-<slug>`
2. On every service×city page, add a link back to `/city-<slug>` and to the matching root service page
   (`/ev-charger-installation`, `/panel-upgrade`, `/whole-home-rewiring`).
3. Keep the existing emergency link (all 112 city pages already link one).

**Expected effect:** the 64 geo service pages currently sit at positions 1–18 on ≤30 impressions.
Internal links are the one input they are missing. This is the cheapest position gain available on the
site.

#### Change 2 — Lead each city page with that city's highest-demand service

Do not rewrite all 112. Prioritise the 12 cities with measured demand, and reorder the existing
sections so the highest-demand service is first:

| City page | GSC city-query signal | Lead section should be |
| :--- | :--- | :--- |
| `/city-sherman-oaks` | `electrician sherman oaks` 296 impr @ 37.0 | Panel + EV |
| `/city-studio-city` | `electrician studio city` 192 @ 25.9 | Panel + rewiring (older stock) |
| `/city-encino` | `electrician encino` 181 @ 55.2 | Panel + EV |
| `/city-woodland-hills` | `electrician woodland hills` 176 @ 54.1 | Panel + EV |
| `/city-van-nuys` | `electrician van nuys` 170 @ 56.0; `ev charger installation van nuys` 36 @ 16.2 | EV charger (strongest local EV signal) |
| `/city-burbank` | `electrician burbank` 152 @ 55.8; `burbank house rewire` 3 @ 11.0 | Rewiring + panel |
| `/city-santa-monica` | `electrician santa monica` 50 @ 36.2; historic rewiring 25 @ **7.6** | **Historic-home rewiring** |
| `/city-north-hollywood` | `electrician north hollywood` 53 @ 59.7 | Panel + EV |
| `/city-glendale` | `ev charger installation glendale` 18 @ 51.0; `electrical panel upgrade glendale` 14 @ 77.9 | Panel + EV |
| `/city-culver-city` | `/city-culver-city` 164 impr @ 37.9; `commercial electrician culver city` 21 @ 23.1 | Commercial + panel |
| `/city-pasadena` | `/city-pasadena` 80 impr @ 57.3 | Rewiring (older stock) |
| `/city-calabasas` | `/city-calabasas` 253 impr @ 35.9 | Panel + EV |

#### Per-page template (apply to the 12 above)

1. **H1:** `<City> Electrician — Panel Upgrades, EV Chargers & Rewiring` (keep the city + service
   pattern; it already beats the primary competitor's bare city title).
2. **H2: Electrical Services in <City>** — the new "Services in <City>" link block (Change 1).
3. **H2: Recent Projects in <City>** — 2–3 gallery photos, alt text naming the city and work type.
   **Information gain — only AMY can do this.**
4. **H2: Local Electrical Considerations in <City>** — house-era and utility facts **only where the
   owner has supplied them**. ⚠️ Hard constraint: **do not invent counties, ZIPs, landmarks or
   `areaServed` data.** The 112 pages currently use 3 valid `areaServed` shapes — leave them.
5. **H2: Permit & Utility Notes** — City of LA → LADBS/LADWP; **Alhambra, Bellflower, Carson, Santa
   Clarita → SCE** (`SCE_CITIES` in `generate-city-pages.py`). Keep city-correct.
6. **H2: <City> Electrical FAQs** — 4–6 questions.
7. **H2: Services in <City> — Call (818) 302-5614** — CTA.

⚠️ **Do not** attempt `areaServed` unification as part of this work. It remains blocked on
owner-supplied per-city county/ZIP data.

---

### Recommended Meta Tags

**Current pattern is good — keep it.** Example (`/city-sherman-oaks`):
`Sherman Oaks Electrician | Panel Upgrades | AMY Electric` (58 chars)

**Recommended refinement for the 12 priority cities** — add the strongest local service and a trust
marker, keep ≤60 chars:
- Sherman Oaks: `Sherman Oaks Electrician | Panel & EV Charger | C-10`
- Santa Monica: `Santa Monica Electrician | Home Rewiring | C-10 #981578`

**Meta description pattern** (keep the existing shape, 130–150 chars):
`<City> electrician serving the San Fernando Valley. Panel upgrades, EV charger installation and whole-home rewiring. Licensed C-10 #981578. Call (818) 302-5614.` — swap the geographic qualifier to match the actual city; **do not claim service areas the owner has not confirmed.**

---

### Unique Angle and Information Gain

**Per-city photographic proof.** 387 real project photos exist and city pages show none of them
by location. A Sherman Oaks page with three actual Sherman Oaks jobs is unfalsifiable evidence that the
primary competitor — with ~150 templated city pages and no local photography — cannot match. Pair it
with city-correct permit/utility notes (LADBS+LADWP vs SCE), which templated competitor pages
routinely get wrong.

---

### E-E-A-T Requirements

- C-10 licence #981578 on every city page (already present in most).
- City-correct utility claims — LADWP only for City of LA; SCE for Alhambra, Bellflower, Carson,
  Santa Clarita. `grep -rl 'coordinate with SCE' city-*.html` must return only those four.
- Real local photography with city-named alt text.
- `areaServed` shapes stay as-is until the owner supplies verified data.
- Canonical `reviewCount` 87 from `scripts/site_data.py` — never hand-edit.

---

### Internal Linking Opportunities

| Anchor text | Target URL | Where |
| :--- | :--- | :--- |
| `EV charger installation in Van Nuys` | `/ev-charger-installation-van-nuys` | `/city-van-nuys` §2 |
| `panel upgrade in Burbank` | `/panel-upgrade-burbank` | `/city-burbank` §2 |
| `whole-home rewiring in Santa Monica` | `/whole-home-rewiring-santa-monica` | `/city-santa-monica` §2 |
| `electrician in Sherman Oaks` | `/city-sherman-oaks` | every `/ev-charger-installation-*`, `/panel-upgrade-*`, `/whole-home-rewiring-*` matching slug |
| `24/7 emergency electrician` | `/emergency-electrician-los-angeles` | already on all 112 city pages — keep |

## Sources

- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — city terms: sherman oaks 296 @ 37.0; studio city 192 @ 25.9; encino 181 @ 55.2; woodland hills 176 @ 54.1; van nuys 170 @ 56.0; burbank 152 @ 55.8; santa monica 50 @ 36.2; historic santa monica rewiring 25 @ **7.6**; glendale EV 18 @ 51.0; culver city commercial 21 @ 23.1
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — `/city-sherman-oaks` 348 impr @ 35.6; `/city-van-nuys` 344 @ 40.0; `/city-beverly-hills` 343 @ 48.6; `/city-calabasas` 253 @ 35.9; geo service pages 1–30 impr at pos 1.0–17.6
- `[repo: grep -rl 'ev-charger-installation-van-nuys' --include='*.html' .]` — 3 files per geo service page
- `[repo: ls city-*.html]` 112 · `[repo: ls ev-charger-installation*.html]` 25 (24 geo + root) · `[repo: ls panel-upgrade*.html]` 25 · `[repo: ls whole-home-rewiring*.html]` 17 (16 geo + root) → **64 geo service pages total** (repo docs say 48)
- `[repo: city-sherman-oaks.html]` — existing title pattern · `[repo: generate-city-pages.py]` — `SCE_CITIES`, template
- `[repo: AGENTS.md]` — `areaServed` unification blocked, price canonicals, utility correctness rule
- `[directional: web]` — sitemaps of theelectricconnection.com (255 URLs, ~150 `/electrician-<city>-ca/`), 911electrics.com (492 URLs), brydenelectrical.com (`/service-areas/<city>/`)
- `[repo: seo-workspace/reports/competitor-landscape.txt]` — Branover "25+ location pages" (June 2026; sitemap not retrievable this session)
- `[openseo: get_serp_results → DataForSEO HTTP 401]` — no confirmed ranking positions
