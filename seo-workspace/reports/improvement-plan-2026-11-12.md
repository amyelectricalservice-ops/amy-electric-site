# AMY Electric — Improvement Plan (post-audit)

**Date:** 2026-11-12 · **Scope:** `/home/amram/WEBSITE` (342 production pages, 317 sitemap URLs) + live `workers.dev`
**Baseline:** all gates green — `audit-site` 342/0, `schema-tool` pass, `price-drift --strict` 0, `node --test` 84/84, `lint.sh` OK, CSS/JS rebuild clean, `wrangler dry-run` ok, live 200s + correct cache headers. Lighthouse mobile 100/100/100/100 on all 8 sampled pages after the perf pass. Playwright: 0 console/page errors, 0 failed requests, 0 broken images, 0 duplicate IDs, 0 horizontal overflow at 390px across 18 pages.

## 1. What shipped (PR #42 + #43, merged to main, deployed)

**SEO / geo (Phase 1–2):** wired 6 city hubs both ways (Sherman Oaks, Studio City, Encino, Van Nuys, Woodland Hills, Burbank) — city page gains the missing rewiring card, service page links back to hub + overview. Split same-day vs emergency canonical intent (both self-canonical, cross-linked). Wired lighting hubs → recessed spoke. Tesla brand-vs-generic funnel split. Tightened homepage meta to 138 chars. Quarantined dead `functions/`.

**Perf/a11y (Lighthouse + Playwright):**
- 0/315 pages overflow horizontally at 390px (was 12). Fixed inline `.two-col` grid (2 pages), 92 price-table scroll wrappers, 4 trust-bar/photo splices, 2 `minmax(320px)` containers, 4 hand-rolled footers.
- 68 pages moved off synchronous stylesheet → async preload + inline critical CSS. Render-blocking gone; blog TBT 190→0 ms, FID 180→20 ms.
- Repaired malformed `<picture>` markup on 4 service hubs (stray `<source>`, missing opening tags, duplicated unreachable sources).
- `sizes` attribute on 32 photo-grid pictures corrected to the precise `calc(...)` form so mobile picks 400w instead of 800w.
- `scripts/lint.sh` added (ruff + py_compile with SyntaxWarning-as-error + node --check), wired into pre-push gate. All 75 ruff findings cleared; main's `apply-photo-captions.py` (5 E701/E702) cleaned during merge.

**Tooling:** `city-winnetka` Electrician JSON-LD canonicalized (unblocked the deploy).

## 2. Remaining findings (prioritized)

### P0 — owner-gated, highest ROI (code side shipped)

1. **GBP posts, every other day** — `gbp-posting-calendar.md`, 30 posts, 2026-10-21→2026-12-18, copy-paste from `gbp-posts-document.txt`. ~5 min each. No agent needed. (Highest ROI per AGENTS.md.)
2. **GBP auto-posting agent** — code shipped (`gbp-agent.js` + daily 16:00 UTC cron). Pending: 5 `wrangler secret put` (Google Cloud OAuth + location ID), dry-run, go live.
3. **Fresh GSC export** — current export ends 2026-09-05 (~9 weeks stale). 21,745 impressions → 78 clicks, every non-brand term at 0% CTR. Connect GSC+GA4 to OpenSEO; repair DataForSEO 401. All non-GSC numbers are `unknown`/directional until this lands.
4. **Hero photo** — replace "LA CITY ELECTRIC" shirt with a real AMY tech shot; agent swaps via photo pipeline when supplied.
5. **PageSpeed field check** — run pagespeed.web.dev on homepage, compare CrUX LCP/INP/CLS to targets (<2.5s / <200ms / <0.1 / 90+ mobile).

### P1 — code-side, medium effort, measurable wins

6. **Image delivery (Lighthouse `image-delivery-insight`, 82–179 KiB on home/panel/gallery).** Two distinct causes:
   - **Compression:** `hero-electrician-400.webp` (30 KB) and the 800w gallery variants (40–84 KB at 800×600) are heavier than needed. Re-encode with cwebp `-q 70` (currently ~q85) via `process-photos.py` / `optimize-images.py`. Estimated 20–30% reduction, ~15–40 KB per page.
   - **Variant granularity:** gallery pipeline emits 400/800/1200 only. At 2× DPR on a 550px card, 800w is the smallest that doesn't upscale; a 600w variant would save ~30 KB per image at 2×. Add a 600w step to `process-photos.py` (and `update-gallery.py`'s srcset) — touches 366 photos × 2 formats. Defer until (a) is done and measured.
   - Note: the `sizes` attribute is now correct (precise `calc(...)` form); the remaining "wasted bytes" is largely a DPR artifact, not a bug.

7. **`/book` page (Lighthouse `unminified-*`, `unused-javascript`, `legacy-javascript`).** 27 KiB unused JS + 28 KiB legacy polyfills from flatpickr 4.6.13 (pinned, vendored, must not hand-edit). Options:
   - (a) Upgrade to flatpickr 4.6.13 → a newer 4.x that ships a smaller core (policy pins 4.6.13; would need owner sign-off).
   - (b) Lazy-load flatpickr only when the date input is focused (currently loaded on page load). Saves ~30 KiB on first paint. Medium effort, good win.
   - (c) Minify `js/book.js` (2 KiB) and generate `flatpickr-dark-4.6.13.min.css` via a build script (reproducible, not hand-edited). Marginal (~3 KiB) but clears the audit.

8. **`unused-css-rules` (18–25 KiB, 69% of 31 KB stylesheet, on every page).** Single cached file (max-age 3600), so the per-page waste is theoretical. Real fix is per-template CSS splitting (base+header+footer shared; page-specific sections loaded on demand). High effort, moderate payoff (~5 KiB br per page). Defer unless CrUX shows TTFB issues.

9. **TBT on heavy pages (home 280 ms, panel 210 ms, same 360 ms, tesla 390 ms).** No long tasks >50 ms captured by the Long Tasks API on real hardware — these are 4×-CPU-throttle artifacts. Not actionable; the underlying `site.min.js` is 19 KB and executes in 16–23 ms. Monitor via CrUX INP instead.

10. **Consolidate the 3-place inline CSS rule.** `.topbar`, `.nav-book`, and the touch-targets block live in `css/src/`, `style.min.css`, and an inline `/*...*/` marker in 161–305 HTML files plus `generate-city-pages.py`. Every CSS change requires 4 edits. Add a build step (`scripts/sync-inline-critical-css.py`) that regenerates the inline block from `css/src/` so the marker stays the single source. Medium effort, prevents future drift.

11. **Structural validator in `audit-site.py`.** The trust-bar/photo splice went undetected because no audit checked `<picture>`/`</picture>` balance or `<section>` nesting inside `.trust-bar-inner`. Add a `html.parser`-based check (0 issues target) so this class of bug fails CI. Small effort, high value.

12. **Archive one-off `fix-*.py` scripts.** ~10 historical one-shot scripts (fix-schema-faq-dedup, fix-seo-issues, fix-picture-v2, etc.) are still in `scripts/` and run by `lint.sh`/`compileall`. Move to `scripts/archive/` (excluded from lint). Reduces noise; no behavior change.

### P2 — owner-side, moves positions 20→10 (no code)

13. **`areaServed` unification** — blocked on owner-supplied per-city county/ZIP/Wikipedia data (112 pages in 3 valid shapes). Do not invent.
14. **Authority building** — CALeVIP Connects (EVITP #4051604 gated, free) + EVITP directory, AAGLA, SRAR, LA chambers; realtor/property-manager editorial with gallery assets. No backlink data available — do not invent numbers.
15. **Review count hygiene** — bump `BUSINESS["aggregateRating"]["reviewCount"]` (87) in `scripts/site_data.py` as Google reviews grow; 336 occurrences, validator fails on drift.
16. **Human EV prose/grid price sweeps** — `audit-price-drift.py` is non-blocking by design; blind spots: CSS-grid comparison tables, prose pricing a charger without naming one, ranges near no service phrase.
17. **Brand mentions** — YouTube/Reddit/Wikipedia presence; real-world effort, not code.

### P3 — defer / hold

18. **ADU / commercial / panel-brand / EV-make pages** — no captured demand yet (GSC data stale). Re-evaluate after Phase 0 data refresh.
19. **`/book` nav placement** — visual call held (nav-menu + sticky-bar "Book" placement). Owner decision.
20. **AVIF variants** — measured and parked (needs subscription or pre-generated variants).
21. **`areaServed` unification** — blocked (see 13).

## 3. Suggested execution order

| Week | Focus | Owner | Agent |
|---|---|---|---|
| 1 | Phase 0 data refresh (GSC, DataForSEO, rebase) | owner | — |
| 1 | P1.1 hero compression + cwebp re-encode | agent | small PR |
| 1 | P1.11 structural validator in audit-site.py | agent | small PR |
| 2 | P1.7 (b) lazy-load flatpickr on /book | agent | medium PR |
| 2 | P1.10 inline-CSS sync build step | agent | medium PR |
| 2 | P1.12 archive one-off scripts | agent | small PR |
| 3+ | P1.6 600w gallery variant (pipeline) | agent | large PR, measure first |
| 3+ | P2 authority (CALeVIP, chambers, realtors) | owner | — |
| ongoing | GBP posts every other day | owner | 5 min each |

## 4. What NOT to touch (per AGENTS.md + this audit)

- HTML cache `max-age=300, s-maxage=60, SWR=600` — do not "fix" back to `must-revalidate`.
- RUM beacon `send.to /cdn-cgi/rum` — 404 from curl/workers.dev is by design.
- Geo personalization `private, no-store` on `/`.
- Rocket Loader OFF.
- Vendored flatpickr 4.6.13 (never hand-edit).
- `sync-faq-schema.py --apply` (rewrites answers).
- `reviewCount` without a human review.
- `areaServed` shapes without owner data.
- Zone routes (single-Worker invariant; `audit-cloudflare-routes.py` guards it).

## 5. Verification commands (run before any push)

```bash
python3 scripts/schema-tool.py validate
python3 scripts/audit-price-drift.py --strict
python3 scripts/audit-site.py
node --test scripts/test-*.mjs
bash scripts/lint.sh
python3 scripts/build-css.py && python3 scripts/build-js.py && git diff --exit-code -- css/style.min.css js/site.min.js
wrangler deploy --config wrangler.jsonc --dry-run
```
Then push, watch Deploy workflow green, spot-check live on `workers.dev`, `bash scripts/notify-indexnow.sh` if workflow didn't.