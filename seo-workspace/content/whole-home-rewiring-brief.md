# Content Brief: whole home rewiring los angeles

**Mode:** improve existing page · **Workflow:** 3 (`keyword-clustering` → `seo-content-brief`)
**Target URL:** `/whole-home-rewiring` (live) — **plus** the blog/page split fix
**Date:** 2026-10-18

---

### Search Intent

**Commercial / research with heavy price intent.** Two searcher types share this query:
(a) an LA homeowner in a 1920–1960 house with two-prong outlets or cloth/knob-and-tube wiring asking
*"do I need this and what will it cost"*, and (b) a seller or agent on a deadline before a sale or
inspection. Google rewards a long-form page with a cost table, a "do you need it" self-assessment and
a permit/process section. Audience: knowledgeable enough to search the term, not enough to know scope.

---

### Competitor Analysis

**⚠️ Method note:** no SERP API available (`get_serp_results` → DataForSEO HTTP 401). These are the
pages that hold this topic, measured live — **not** confirmed ranking positions. Word counts are
extracted; `Score` is my judgement /40.

| # | URL | Key H2 sections | Est. words | Score | Main gap |
| :-- | :--- | :--- | ---: | :---: | :--- |
| — | **AMY `/whole-home-rewiring`** | Does Your Home Need Rewiring in Los Angeles? · Project Photos · How Does the Process Work? · Costs in LA · Also Consider · FAQ | **4,285** | 28/40 | Deep, but 40 impressions at pos 24.6 — no authority pointing at it |
| — | **AMY `/blog/whole-home-rewiring-guide`** | What Is Whole-Home Rewiring? · 6 Signs Your LA Home Needs Rewiring · What to Expect · Costs in LA · Ready to Modernize? · More Resources | **1,547** | 22/40 | **Outranks the service page 86:1 on impressions** (3,444 vs 40) at only pos 37.7 |
| 1 | `theelectricconnection.com/house-rewire/` | Why is a House Rewire Needed? · Do I Need to Rewire my Home? · **How Can I Tell If I Need a House Rewire Without Opening the Walls?** · Customer testimonials · **What Is The Cost for A House Rewire in Los Angeles?** · What Should You Expect During a House Rewire? | **3,817** | 31/40 | Question-shaped H2s mapping to real searches; testimonial block inside the page |
| 2 | `911electrics.com/whole-house-rewiring-cost-los-angeles/` | Signs Your Home May Need Rewiring · What Affects the Cost · The Rewiring Process · Why Use a Licensed Electrician · Talk to a Specialist | *not extractable* (JS-rendered; plain fetch returns 0 words) | — | `[directional: web]` thin templated content behind JS; page is a quote-funnel, not a resource |
| 3 | `brydenelectrical.com/blog/electrical-hazards-in-older-la-homes-…/` | *(post-sitemap blog)* | — | — | `[directional: web]` Bryden only has 6 blog posts total — they compete on service pages, not content volume |

**The decisive measurement:** AMY's service page (4,285 words) is **longer than the best competitor
page** (3,817 words). **Rewiring is not a content-depth problem.** It is an authority + internal-link
problem, and simultaneously a wrong-page-ranks problem.

---

### Content Gaps and Opportunities

**Topic gaps:**
- **"Can you rewire without opening the walls?"** — the #1 competitor answers this in an H2.
  AMY's repo already contains `/blog/rewire-without-opening-walls`; the service page never addresses
  it. GSC shows `can you rewire a house without removing drywall` (3 impr, pos 34.7) plus the
  competitor H2 — real demand AMY is not answering on the money page.
- **Historic-home specificity.** `electrical rewiring for historic santa monica homes` gets 25
  impressions at **position 7.6** — already page one, and the single best-positioned rewiring query.
  Nothing on the service page speaks to historic LA housing stock.
- **Pre-sale / pre-inspection timing.** Seller-deadline rewires are the highest-urgency, highest-price
  jobs and no competitor page addresses the escrow timeline.

**Depth gaps:**
- Partial vs whole-home scope is only handled on a separate blog post
  (`/blog/partial-vs-whole-home-rewire`) — the money page should own the decision.
- Permit path (LADBS vs LADWP vs SCE by city) is not surfaced on the service page. Utility correctness
  matters: only City-of-LA pages may claim LADWP; Alhambra/Bellflower/Carson/Santa Clarita are SCE.

**Quality gaps (the real ones):**
- The **blog post carries 86× the impressions of the service page**, and neither links to the other
  strongly enough to consolidate intent.
- Only 40 impressions reach the 4,285-word page. Effort is being spent on a page Google isn't choosing.

---

### Winning Outline

**H1:** Whole-Home Rewiring in Los Angeles — Cost, Process & Permits
**URL:** `/whole-home-rewiring` (keep)
**Target word count:** ~4,600–5,000 words *(already 4,285; this is targeted addition, not a rewrite —
keep every existing section that is working)*

**Keep / strengthen:**
1. **H2: Does Your Home Need Rewiring in Los Angeles?** — keep. Add the 6-signs checklist inline
   (currently only on the blog). **FS target** for "signs your home needs rewiring".
2. **H2: Whole-Home Rewiring Costs in LA** — keep and strengthen. Verify against the price canonicals;
   keep the "$8,000–$18,000" band already in the title. Add a **2-bedroom vs 3+ bedroom vs partial**
   comparison table (the cluster brief in the older workspace draft claimed $8–12k / $12–20k — **do not
   carry those across without the owner confirming; they are unsupervised numbers**).
3. **H2: How Does the Whole-Home Rewiring Process Work in Los Angeles?** — keep. Add permit path and
   realistic timeline.

**Add new:**
4. **H2: Can You Rewire a Home Without Opening the Walls?** — ~350 words — **FS target**; directly
   answers a competitor H2 and an existing GSC query. Link `/blog/rewire-without-opening-walls`.
5. **H2: Rewiring Historic Los Angeles Homes (Santa Monica, Hollywood, Pasadena)** — ~400 words —
   targets the pos-7.6 historic query. Link `/whole-home-rewiring-santa-monica`,
   `/whole-home-rewiring-hollywood`, `/whole-home-rewiring-pasadena`.
6. **H2: Partial vs Whole-Home Rewire — Which Do You Need?** — ~350 words — owns the decision on the
   money page; link `/blog/partial-vs-whole-home-rewire`.
7. **H2: Rewiring Before a Sale or Inspection** — ~300 words — escrow timeline, what inspectors flag
   (Zinsco/Federal Pacific, ungrounded outlets, cloth wiring), why permits matter at closing.
   **Information gain.**
8. **H2: Permits & Utility Coordination by City** — ~300 words — LADBS / LADWP for City of LA;
   SCE for Alhambra, Bellflower, Carson, Santa Clarita. Keep utility claims city-correct.
9. **H2: Whole-Home Rewiring FAQs** — ~450 words — 8 questions from GSC phrasing.

---

### Recommended Meta Tags

**Title** (58 chars):
`Whole-Home Rewiring Los Angeles | Cost $8K–$18K | AMY Electric`

**Meta Description** (149 chars):
`Whole-home rewiring in Los Angeles: knob-and-tube and cloth wiring replacement, permits handled. See real LA project photos. Call (818) 302-5614.`

*(The current title's `$8,000–$18,000` should be confirmed against the owner's own quote data before
being published in the title — a title price is a promise.)*

---

### Unique Angle and Information Gain

**Owner-published cost and photo evidence.** AMY already has 387 real project photos and a live
estimate engine. No competitor publishes measured actuals. The information gain here is:
(a) real before/after gallery images from actual LA rewires, tagged by neighbourhood and house era,
(b) an escrow/sale timeline nobody else covers, and (c) a city-correct permit and utility matrix.
That is first-hand data, not "more detail".

---

### E-E-A-T Requirements

- C-10 licence number in body text (#981578); EVITP #4051604 where EV readiness is discussed.
- Cite the 2026 California Electrical Code (Title 24 Part 3) for AFCI/GFCI and grounding claims.
- Attribute cost bands to AMY's own completed work — **owner confirmation required before publishing
  ranges**; the price canonicals in `AGENTS.md` are the only pre-approved figures.
- Last-updated date visible on the page.
- Real photography from `img/gallery/` with descriptive alt text and dimensions.

---

### Internal Linking Opportunities

| Anchor text | Target URL | Where |
| :--- | :--- | :--- |
| `whole-home rewiring in Santa Monica` | `/whole-home-rewiring-santa-monica` | §5 historic homes |
| `rewiring in Sherman Oaks` | `/whole-home-rewiring-sherman-oaks` | §5 historic homes |
| `knob-and-tube wiring replacement` | `/blog/knob-and-tube-wiring-replacement-guide` | §4 no-walls section |
| `200A panel upgrade` | `/panel-upgrade` | §6 partial vs whole |
| `whole-home rewiring cost guide` | `/blog/whole-home-rewiring-cost-la` | blog → service page (funnel CTA above the fold) |
| *(inbound)* `whole-home rewiring` | this page | from all 16 `/whole-home-rewiring-*` geo pages, back to the pillar |

**Also required (structural, not content):** the 16 `/whole-home-rewiring-*` geo pages currently have
~3 inbound internal links each. Link them from their matching city pages.

## Sources

- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Queries.csv]` — rewiring bucket 3,492 impr / 0 clicks; `home rewiring` 499 @ 23.2; `electrical rewiring for historic santa monica homes` 25 @ **7.6**; `can you rewire a house without removing drywall` 3 @ 34.7
- `[gsc: seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/Pages.csv]` — `/blog/whole-home-rewiring-guide` 3,444 impr @ 37.7 vs `/whole-home-rewiring` 40 impr @ 24.6
- `[repo: whole-home-rewiring.html]` — 4,285 words, existing H2s
- `[repo: blog/whole-home-rewiring-guide.html]` — 1,547 words
- `[repo: ls whole-home-rewiring*.html]` — 16 geo rewiring pages exist
- `[repo: AGENTS.md]` — price canonicals, SCE city list, reviewCount 87
- `[directional: web]` — theelectricconnection.com/house-rewire/ measured at 3,817 words with the "without opening the walls" H2; 911electrics JS-rendered
- `[openseo: get_serp_results → DataForSEO HTTP 401]` — no confirmed ranking positions
