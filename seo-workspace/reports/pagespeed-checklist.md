# PageSpeed / Core Web Vitals — Field Check Checklist (owner)

**Goal:** compare real-user (CrUX) and lab metrics on amyelectric.com against targets, and log regressions. Run after every deploy that touches CSS/JS/images/HTML.

**Targets (from AGENTS.md):** LCP < 2.5s · INP < 200ms · CLS < 0.1 · mobile Lighthouse performance ≥ 90.

## 1. URLs to test (run all, in this order)

| # | URL | Why |
|---|---|---|
| 1 | https://amyelectric.com/ | Highest traffic; hero LCP |
| 2 | https://amyelectric.com/book | Booking widget; flatpickr bundle |
| 3 | https://amyelectric.com/tesla-charger-installation | Heavy page (TBT 390ms lab) |
| 4 | https://amyelectric.com/panel-upgrade | Wide tables + sidebar grid |
| 5 | https://amyelectric.com/gallery | LCP candidate (image grid) |
| 6 | https://amyelectric.com/city-burbank | Representative city hub |
| 7 | https://amyelectric.com/blog/whole-home-rewiring-guide | Blog LCP after async-CSS change |
| 8 | https://amyelectric.com/same-day-electrical-repair | Emergency cluster (P0) |

## 2. How to run (no login needed)

1. Open **https://pagespeed.web.dev/** in a normal browser (not an agent — apex serves bot challenges).
2. Paste each URL, click **Analyze**. Wait for both "Discover what your real users are experiencing" (CrUX field data) and "Diagnose performance issues" (lab) sections.
3. Record into the table in §4 (one row per URL × run).
4. For CrUX: if "No Data" (low traffic), note it — CrUX needs ≥~1k visits/month per URL. Use the origin-level CrUX in that case.
5. For lab: use the **mobile** tab (default). Record LCP, INP (or TBT as proxy), CLS, FCP, Speed Index, total byte weight.

## 3. What to look for (red flags)

- **LCP > 2.5s (field or lab)** → check the LCP element (image? text?). Hero image preload (`img/hero-electrician-400.webp` / `560x420.webp`) must stay `fetchpriority="high"` + `loading="eager"`. Re-run after any image/CSS change.
- **INP > 200ms (field)** → check `js/site.min.js` execution and inline scripts on the page. Use Chrome DevTools Performance tab locally.
- **CLS > 0.1** → usually a late-loading font or image without dimensions. Verify all `<img>` have `width`/`height` (audit-site.py checks this).
- **Mobile performance < 90** → check render-blocking resources (should be none now), unused CSS (advisory), image delivery.
- **TTFB > 800ms** → Worker cold start or edge cache miss; check `cf-cache-status` header (should be HIT).
- **Total byte weight > 500 KB** on a single page → usually an unoptimized image; run `seo-images` skill.

## 4. Results log (copy/paste, one block per run)

```
Run date: YYYY-MM-DD  ·  Deploy SHA: ______  ·  Tester: ______

| URL | CrUX LCP | CrUX INP | CrUX CLS | Lab LCP | Lab TBT | Lab CLS | Lab SI | Bytes | Mobile perf | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| / | | | | | | | | | | |
| /book | | | | | | | | | | |
| /tesla-charger-installation | | | | | | | | | | |
| /panel-upgrade | | | | | | | | | | |
| /gallery | | | | | | | | | | |
| /city-burbank | | | | | | | | | | |
| /blog/whole-home-rewiring-guide | | | | | | | | | | |
| /same-day-electrical-repair | | | | | | | | | | |

Regressions (any metric worse than previous run): ____________________
Action taken: ____________________
```

## 5. Baseline (from this audit, 2026-11-12, local Lighthouse mobile, 4× CPU throttle)

| URL | Lab LCP | Lab TBT | Lab CLS | Mobile perf |
|---|---|---|---|---|
| / | 2.8s | 280ms | ~0 | 100 |
| /book | 2.6s | 20ms | ~0 | 100 |
| /tesla-charger-installation | 2.5s | 390ms | ~0 | 100 |
| /panel-upgrade | 2.8s | 210ms | ~0 | 100 |
| /gallery | 5.6s | 310ms | ~0 | 100 |
| /city-burbank | 2.2s | 50ms | ~0 | 100 |
| /blog/whole-home-rewiring-guide | 2.4s | 240ms | ~0 | 100 |
| /same-day-electrical-repair | 2.5s | 360ms | ~0 | 100 |

Note: TBT/FID figures are 4×-CPU-throttle artifacts; real-device INP is expected to be far lower. CrUX field data is the source of truth — record it first.

## 6. When to re-run

- After any deploy that touches `css/`, `js/`, `img/`, `worker.js`, or any HTML.
- After adding/removing a page (sitemap changes).
- Monthly, even with no changes, to catch CrUX drift.

## 7. Where to log

Append results to `seo-workspace/reports/pagespeed-log.md` (create if missing). Keep the last 3 runs; archive older ones. Cross-reference with `seo-workspace/reports/improvement-plan-2026-11-12.md` §2 P1.1 (hero compression) and P1.7 (flatpickr lazy-load) — those are the only items expected to move LCP/TBT materially.