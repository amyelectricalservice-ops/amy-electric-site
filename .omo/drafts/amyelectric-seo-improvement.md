# Draft: amyelectrical-seo-improvement

> Durable planning record for the ulw-plan workflow. This file is a draft — the plan artifact itself lives at `.omo/plans/amyelectrical-seo-improvement.md` and is created only after the approval gate.

## Request state

- **Request**: "audit website and make a plan to improve" (a.myelectric.com, AMY Electric LA electrical contractor site).
- **Intent**: CLEAR (outcome = one decision-complete executable improvement plan).
- **Review required**: `false` (no accuracy modifier requested; CLEAR path so dual review is optional).
- **Classification**: Architecture — 6 independent modules, site-wide impact (up to 114 real pages).
- **Slug**: `amyelectrical-seo-improvement`
- **Plan path**: `.omo/plans/amyelectrical-seo-improvement.md`
- **Pending action policy**: `review_required=false` → "write .omo/plans/<slug>.md" after approval.

## Environment constraint (tool deviation)

- `scaffold-plan.mjs` requires `node` on a shell; the Exec/bash tool is **not available** in this
  environment (toolset dropped mid-session). The scaffold step is therefore performed by hand below,
  reproducing the script's emitted template headers verbatim at generation time.
- Background subagents were repeatedly killed by the runtime (11 launches, all confirmed dead via
  `session_info`). All exploration in this audit was executed inline by the planner (read/grep/glob/
  websearch/webfetch). Review subagents (Metis/Momus/Oracle) may fail identically; if approval
  requires the dual review and both reviewer lanes die, record `INCONCLUSIVE` per the lifecycle
  contract instead of fabricating receipts.

## Audit findings (evidence)

### Verified healthy (baseline, post-fix)
- 622 JSON-LD blocks parse with 0 errors (after 2 repairs: licensed-electrician-los-angeles.html
  unbalanced braces; tesla-charger-installation.html raw HTML in FAQ Answer).
- 0 broken internal HTML links (6,825 checked; 3 'missing' blog files are intentional noindex stubs).
- Every real page: title (50-60 chars; only blog/ladwp-e-permit-guide.html = 68), meta description,
  canonical, og:title/og:image, exactly 1 H1, alt text present.
- 0 duplicate titles/descriptions across real pages.
- Fonts all exist (after fixing 404.html refs → BarlowCondensed-700.woff2, SourceSerif4-400.woff2).
- robots.txt now disallows /api/, /reports/, /amyelectric-site/, /partials/, /~ and explicitly allows
  8 AI crawlers; blocks 3 training crawlers.
- _headers (CSP, HSTS, frame-deny, nosniff, Referrer-Policy, Permissions-Policy; immutable 1yr assets),
  _redirects (/*.html :splat 301), wrangler.jsonc (assets ".", auto-trailing-slash, 404-page) healthy.
- llms.txt (3.8 KB) present & correct.

### Open/flagiation items (candidates for plan todos)
1. **amyelectrac-site/ stale snapshot** — 19 tracked files duplicated from live tree; now robots-blocked.
   Destructive (git rm) → owner decision; default recommended = inline quarantine, leave tracked, block.
2. **Title length outlier** — `blog/ladwp-e-permit-guide.html` title 68 chars (>65 target).
3. **Third-party NAP/citation drift** — home-security.com lists AMY as security-systems co with 0
   reviews (industry + review-count mismatch); Yelp displays address typo "Londelres" vs "Londelius St";
   findglocal/celende listings unknown accuracy. Site-side fix not possible — owner action on
   directories; plan will document the outstanding directory corrections as owner tasks.
4. **Gallery.html weight** — 273 KB / 309 photos; inline critical CSS; candidates for LCP savings.
5. **Old.GA removal confirmed** — GA4/event code absent (Cloudflare Analytics only) per AGENTS.md;
   llms no analytic measurement for phone_click/cta_click/form_submit. Plan to add site-side events.
6. **SEO-STRATEGY.md (July 28)** — strategy umbrella exists; plan must complement, not overwrite.
7. **Blog index/ratio** — 37 posts; thin for some docs; content E-E-A-T expansion on core money pages.

## Topology (locked set, confirm in approval brief)

| # | Component | Outcome | Status | Evidence |
|---|-----------|---------|--------|----------|
| T1 | Technical SEO hygiene (fix remaining title, canonical edge cases, stale snapshot policy) | healthy baseline maintained | not started | audit above |
| T2 | Content & E-E-A-T depth (money pages + blog index + service grid) | depth | not started | SEO-STRATEGY weaknesses |
| T3 | Local SEO / NAP & citations | drift closed + GAL optimized overseas | owner action only | find call listings |
| T4 | AI/GEO visibility (llms.txt, schema enrichment, chatgpt/llm citations) | AAA neat | not started | GEO baseline |
| T5 | Performance & CWV (gallery/clicks downloaded, LCP on homepage) | >90 mobile | not started | LH 85/100 perf baseline |
| T6 | Measurement & events (phone_click, cta_click, form_submit + GA4/GSC dashboard owner tasks) | measurable | not started | GA4 checklist in AGENTS.md |

## Approval gate (decision is pending)

status: `awaiting-approval-board` — present once; any next reply that accepts the approach = approval
to WRITE PLAN ONLY. Never implementation.

pending-action [after approval]: write and fill `.omo/plans/amyelectrical-seo-improvement.md`,
run mandatory Metis gap analysis, fill TL;DR last, then deliver.

## Review / session receipts

- review_required: false → no pre-scheduled review. If the user requests it at delivery, initialize
  review round with THIS failed: momus + independent oracle against the COMPLETE plan file, and
  require both to approve before summary.
- (filled at plan time: plan_path, plan_sha256, review_round_id, lane receipts)

## ⚠️ Environment caveat recorded
- No shell → scaffold run is skipped; template headers produced by editorial (verbatim), validated
  at HR6/HR7 in generation step.
- Sub-agents (Morn-note) variably dead; any reviewer lane must show a client bridge receipt before
  claiming success. Absent receipt → INCONCLUSIVE (contract lane).