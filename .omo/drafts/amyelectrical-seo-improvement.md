# Draft: amyelectrical-seo-improvement

> Durable planning record for the ulw-plan workflow. This file is a draft; the plan artifact
> itself lives at `.omo/plans/amyelectrical-seo-improvement.md` and is created only after the
> approval gate.

## Request state

- **Request**: "audit website and make a plan to improve" (amyelectric.com, AMY Electric LA electrical contractor site).
- **Intent**: CLEAR (outcome = one decision-complete executable improvement plan).
- **Review required**: `false` (no accuracy modifier requested; CLEAR path → dual review optional, user chooses at delivery).
- **Classification**: Architecture — 6 independent modules, site-wide impact (up to 114 real pages).
- **Slug**: `amyelectrical-seo-improvement`
- **Plan path**: `.omo/plans/amyelectrical-seo-improvement.md`
- **Pending action policy**: `review_required=false` -> "write .omo/plans/<slug>.md" after approval.

## Environment constraint (tool deviation)

- `scaffold-plan.mjs` requires `node` on a shell; the Exec/bash tool is **not available** in this
  environment (toolset dropped mid-session). The scaffold step is therefore performed by hand,
  reproducing the script's emitted template headers verbatim at generation time.
- Background subagents were repeatedly killed by the runtime (11 launches, all confirmed dead via
  `session_info`; no transcript output). All exploration in this audit was executed inline by the
  planner (read/grep/glob/websearch/webfetch). Review subagents (Metis/Momus/Oracle) may fail
  identically; if approval requires the dual review and both reviewer lanes die, record `INCONCLUSIVE`
  per the lifecycle contract instead of fabricating receipts.

## Audit findings (evidence)

### Verified healthy (baseline, post-fix)
- 622 JSON-LD blocks parse with 0 errors (after 2 repairs: `licensed-electrician-los-angeles.html`
  unbalanced braces; `tesla-charger-installation.html` raw HTML in FAQ Answer text).
- 0 broken internal HTML links (6,825 checked; the 3 "missing" blog files are intentional noindex stubs).
- Every real page: title (50-60 chars; only `blog/ladwp-e-permit-guide.html` = 68), meta description,
  canonical, og:title/og:image, exactly one H1, alt text present.
- 0 duplicate titles/descriptions across real pages.
- Fonts all exist (after fixing 404.html refs -> BarlowCondensed-700.woff2, SourceSerif4-400.woff2).
- robots.txt now disallows /api/, /reports/, /amyelectric-site/, /partials/, /~ and explicitly allows
  8 AI crawlers; blocks 3 training crawlers.
- _headers (CSP, HSTS, frame-deny, nosniff, Referrer-Policy, Permissions-Policy; immutable 1yr assets),
  _redirects (/*.html 301 to clean), wrangler.jsonc (assets ".", auto-trailing-slash, 404-page) healthy.
- llms.txt (3.8 KB) present & correct.

### Open/fugging items (candidates for plan todos)
1. **`amyelectric-site/` stale snapshot** — 19 tracked files duplicated from the live tree; now
   robots-blocked. Destructive (git rm) -> owner decision; default = quarantine and block (tracked,
   noindex, robots-disallowed), deletion optional.
2. **Title length outlier** — blog/ladpwp-e-permit-guide.html title 68 chars (>65 target).
3. **Third-party NAP/citation drift** — home-security.com lists AMY as a *security systems* company
   with 0 reviews (industry + review-count mismatch); Yelp address typo "Londeline" vs "Londelin St";
   findglocal/celende listings unknown. Fix is owner action on directory platforms; plan will
   document the directory corrections as owner-actions, not site edits.
4. **gallery.html weight** — 273 KB, 309 photos, inline critical CSS; candidate for LCP savings on
   desktop/mobile.
5. **Measurement gap** — GA4/event tags absent (Cloudflare Analytics only) per AGENTS.md; no
   site-side phone_click/cta_click/form_submit events despite the GA4 checklist in AGENTS.md.
6. **SEO-STRATEGY.md (July 28 2026)** — strategy umbrella already exists; plan must complement, not
   overwrite.
7. **Blog depth** — 37 posts exist; content E-E-A-T depth on core money pages and blog index could

## Topology (locked set)

| # | Component | Outcome | Status | Evidence |
|---|-----------|---------|--------|----------|
| T1 | Technical SEO hygiene (title outlier, edge canonical cases, stale-snapshot policy, link/schema regression checks) | verified clean | not started | audit above |
| T2 | Content & E-E-A-T depth (core service pages, blog index, city pages) | depth | not started | SEO-STRATEGY weaknesses |
| T3 | Local SEO / NAP & citations (report wrong-listing corrections) | drift closed (owner-side) | owner action only | findglocal/Yelp findings |
| T4 | AI/GEO visibility (llms.txt upkeep, schema enrichment, AI-citation readiness) | GEO-ready | not started | GEO baseline in strategy |
| T5 | Performance & CWV (defer gallery JS, LCP on homepage, mobile 90+) | >90 mobile PSU | not started | LH 85/100 perf baseline |
| T6 | Measurement & events (site-side phone/cta/form events + GA4/GSC owner tasks) | measurable | not started | AGENTS.md audit checklist |

## Approval gate (decision pending)

status: `awaiting-approval` — brief presented once; any next reply that accepts the approach =
approval to WRITE PLAN ONLY. Never implementation.

pending-action [after approval]: write and fill `.omo/plans/amyelectrical-seo-improvement.md`,
run mandatory Metis gap analysis, fill TL;DR last, then deliver with the
start-or-high-accuracy-review question.

## Review / session receipts

- review_required: false -> no pre-scheduled review. If user requests at delivery, initialize a
  review round with momus + independent oracle against the COMPLETE plan file, both must approve
  before summary; record receipts here (plan_path, plan_sha256, review_round_id, lane results).

## Environment caveat (recorded)

- No shell -> scaffold replaced by editorial template emission, validated at HR6/HR7 generation step.
- Sub-agents variably dead; each review lane must show a session/process receipt before claiming
  success. Absent receipt -> INCONCLUSIVE per contract.