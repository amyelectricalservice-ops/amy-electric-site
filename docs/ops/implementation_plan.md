# Implementation Plan — AMY Electric Website Audit & Improvement

**Date:** 2026-10-08 · **Baseline commit:** `ffc7f6d` (main, deployed, CI green)
**Audit method:** `seo-coach` + `web-perf` skills loaded; Lighthouse CLI against production (Chrome DevTools MCP not connected; PageSpeed API quota exhausted; Cloudflare MCP servers configured in `.vscode/mcp.json` but not connected this session); full local static analysis; GSC export `seo-workspace/gsc/amyelectric.com-Performance-on-Search-2026-09-05/`.

---

## Overview

Audit the 312-page AMY Electric site with MCP-assisted skills and produce a prioritized improvement program covering (a) remaining technical defects, (b) Core Web Vitals/performance, and (c) an on-page content plan driven by real GSC impressions. The foundation is strong — CI (schema validation, sitemap, CSS/JS builds, `audit-site.py`) is fully green, all JSON-LD parses, 0 broken internal links/fragments, Lighthouse SEO 100 / accessibility 100, homepage mobile performance 93. The remaining work is a long tail: 5 malformed blog pages, schema text-quality defects (junk-suffixed and unmarked FAQ questions), 22 indexable pages with no FAQPage schema, one under-performing gallery page (LCP 4.3 s / perf 81), sitewide TBT marginally over target (220–250 ms), and content depth for the highest-impression zero-click keywords (`whole home rewiring` 2,727 imp @ pos 41, `emergency electrician los angeles` 404 imp @ pos 17, six city `electrician {city}` queries).

**Scope decision (user-confirmed):** everything — technical fixes + performance + content plan for GSC keyword opportunities. **FAQ strategy (user-confirmed):** prefer *adding visible FAQ sections/content* over deleting schema. **GSC data (user-confirmed):** use the existing Sep 5 export; note refresh points in the plan.

**Important correction from investigation:** an initial scan appeared to show 16 "phantom" FAQ questions on `panel-upgrade-{city}` pages. After HTML-entity normalization (`&#8217;` → `'`) the true phantom count is **0** — the earlier report was a false positive in my comparison logic. The real FAQ defects are the *inverse* (visible but unmarked) plus junk-suffixed schema names, detailed below. Do not "fix" the phantom count; there is nothing to remove.

---

## Types

No compiled type system exists (vanilla HTML/CSS/JS + Python 3 scripts). The plan defines these data structures for new/modified scripts:

1. **FAQ sync record** (used by new `scripts/audit-faq-sync.py`):
   ```python
   {
     "file": str,            # e.g. "outlet-switch-installation.html"
     "kind": "unmarked" | "junk_name" | "missing_faqpage",
     "questions": [str],     # visible summary text or schema name, normalized
   }
   ```
2. **Normalized question text** — canonical form used for all comparisons:
   `normalize(s) = lower(strip(unescape(s), trailing glyphs [+▾▶…] and whitespace, curly apostrophes → straight))`, compared on the first 50 chars. Every future FAQ script must use this same normalization (the Sep-25 tooling's failure to unescape entities produced phantom results).
3. **Head-structure defect** — page where `<body>` occurs with no preceding `</head>` (5 pages today).
4. **Lighthouse result** — reuse existing JSON shape (`categories`, `audits`) as consumed by `scripts/parse-lighthouse.py`; new baselines saved to `audit/lighthouse/`.

---

## Files

### New files

| Path | Purpose |
|---|---|
| `scripts/audit-faq-sync.py` | Idempotent audit+fix CLI. Modes: `--check` (exit 1 on defects, prints table) and `--fix`. Detects: (1) visible `<summary>` question with no matching FAQPage entry → appends to schema; (2) schema `name` ending in `+`/`▾` → strips suffix; (3) indexable page with visible FAQ disclosure UI but no FAQPage block → reports (does not auto-generate content). Uses `normalize()` from Types §2. |
| `audit/faq-sync-baseline.json` | Machine-readable defect baseline produced by `--check`, so CI and future runs can diff. |
| `implementation_plan.md` | This document. |

### Existing files to modify

| Path | Change |
|---|---|
| `blog/electrical-panel-labeling-guide.html` | Insert `</head>` immediately before the `<body>` tag at line 157 (`<head>` opens line 2 and is never closed). |
| `blog/panel-upgrade-signs.html` | Same `</head>` fix (line 157). |
| `blog/signs-home-needs-rewiring.html` | Same `</head>` fix (line 157). |
| `blog/smart-home-electrical-upgrades.html` | Same `</head>` fix (line 157). |
| `blog/whole-home-rewiring-guide.html` | Same `</head>` fix (line 157). |
| `200-amp-panel-upgrade.html` | Strip trailing `" +"` from 5 FAQPage `mainEntity[].name` values (JSON-LD only; visible `<summary>` keeps its accordion glyph). |
| `electrical-permit-cost-los-angeles.html` | Strip trailing `" +"` from 5 FAQPage names. |
| `federal-pacific-zinsco-panel-replacement.html` | Strip trailing `" +"` from 5 FAQPage names. |
| `blog/emergency-electrical-repair-what-to-do.html` | Add 1 unmarked visible question to FAQPage schema. |
| `ev-charger-hardwired-vs-plug-in.html` | Add 1 unmarked visible question to FAQPage schema. |
| `outlet-switch-installation.html` | Add 2 unmarked visible questions to FAQPage schema. |
| `gallery.html` | **Perf (perf 81, LCP 4.3 s):** (1) fix image preload mismatch — line 28 preloads `gallery-panel-siemens-stucco-1200w.webp` (231 KB) while `<picture>` selects the 800w variant on viewports ≤1400px, so the preload is wasted *and* 800w is re-downloaded; replace with `<link rel="preload" as="image" imagesrcset="…" imagesizes="…" fetchpriority="high">` matching the first `<picture>` sourceset. (2) Change images 2–6 from `loading="eager"` to `loading="lazy"` (6 eager gallery images ≈ 570 KB before LCP settles). (3) Keep image 1 `fetchpriority="high"`. Re-measure; target perf ≥ 90, LCP < 2.5 s. |
| `scripts/schema-tool.py` | Extend `cmd_validate()` with 3 checks: **(a)** FAQPage `name` ends with junk glyph → `JUNK_FAQ_NAME`; **(b)** visible question-`<summary>` not present in FAQPage after `normalize()` → `UNMARKED_FAQ`; **(c)** `<body>` present without preceding `</head>` → `MISSING_HEAD_CLOSE`. Reuse entity-aware `normalize()` (do not port the buggy non-unescaping comparison). |
| `scripts/audit-site.py` | Add "missing `</head>`" counter to the summary table (cheap site-wide hygiene metric; complements schema-tool check (c)). |
| `js/src/` estimator module + `index.html` | **TBT 250 ms → <200 ms:** gate `js/estimator.min.js` heavy setup behind `requestIdleCallback` (fallback `setTimeout(…, 2000)`) or IntersectionObserver on `#estimator`. Keep `<script defer>` tag. Do **not** touch `js/site.min.js` core analytics. Rebuild via `python3 scripts/build-js.py`. |
| `js/webmcp.js` references (99 pages) | **Accepted, no change:** 7.5 KB, `defer`, exits immediately when `navigator.modelContext` is absent (all current browsers). Document as accepted in audit notes. |
| Content pages (Functions §content) | On-page SEO content blocks per GSC plan below. |

### Files NOT to touch

- `worker.js` caching config (`HTML_CACHE_CONTROL`) — protected by AGENTS.md.
- Font preloads, `font-display: optional` — retracted findings from the Sep-25 audit.
- `_redirects`, `robots.txt`, `sitemap.xml` — verified correct (307 URLs, fresh lastmod).
- Cloudflare `/cdn-cgi/challenge-platform` deprecation warnings — external script; **Best Practices 81 is caused by Cloudflare Bot Management's own JS (`StorageType.persistent` deprecation) and is not fixable from the repo**; document as accepted.

---

## Functions

### New

- `normalize_q(text: str) -> str` — in `scripts/schema-tool.py` (shared via `site_data.py` import if needed). Entity unescape + glyph strip + lowercase, compare first 50 chars. **Single source of truth;** `audit-faq-sync.py` imports it.
- `check_junk_faq_names(html: str) -> list[str]` — `scripts/schema-tool.py`; returns schema names ending in `[+▾▶]`.
- `check_unmarked_faqs(html: str) -> list[str]` — `scripts/schema-tool.py`; returns visible summary questions absent from FAQPage.
- `check_head_close(html: str) -> bool` — True if `<body>` has no preceding `</head>`.
- `fix_junk_names(html: str) -> str` and `add_unmarked_to_faqpage(html: str) -> str` — in `scripts/audit-faq-sync.py --fix`. The latter rebuilds the FAQPage block via `json.dumps(..., ensure_ascii=False, indent=2)` (same pattern as the 2026-10-08 ev-charger rebuild), **only appends; never removes questions**, and post-write asserts every JSON-LD block in the file still parses.

### Modified

- `cmd_validate()` (`scripts/schema-tool.py:133`) — call the three new checks per page; append to `issues`.
- `audit()` (`scripts/audit-site.py`) — add `missing_head_close` list + summary line, following the existing `sticky_bar_missing` pattern exactly.
- `audit()` (`scripts/audit-site.py`) — add `missing_head_close` list + summary line, following the existing `sticky_bar_missing` pattern exactly.

### Content edits (GSC-driven, not code functions)

Priority order from the Sep-5 GSC export (≥100 impressions):

| # | Query (imp @ pos) | Page(s) | Edit |
|---|---|---|---|
| C1 | `whole home rewiring` (2,727 @ 41.2), `home rewiring` (499 @ 23.2) | `whole-home-rewiring.html` | Align H1/title to "Whole-Home Rewiring in Los Angeles — Cost $8,000–$18,000"; add visible 4-question FAQ (cost, timeline, permits, knob-and-tube vs aluminum) + FAQPage schema; switch inbound anchors from the 17 `whole-home-rewiring-{city}.html` pages to keyword-rich anchor text. |
| C2 | `emergency electrician los angeles` (404 @ 17.1), `24/7 electrician` (214 @ 45.6), `24 hour electrician los angeles` (186 @ 40.3), `electrical emergency service` (123 @ 38.7), `power outage repair` (126 @ 40.7) | `emergency-electrician-los-angeles.html`, `emergency-electrical.html`, `power-outage-repair.html` | Titles leading with "24/7 Emergency Electrician Los Angeles" (≤70 chars); visible 3-question FAQ (response time, coverage, after-hours pricing) + schema; neighborhood anchor list to city pages. |
| C3 | `electrician sherman oaks` (296 @ 37), `electrician studio city` (192 @ 25.9), `electrician encino` (181 @ 55.2), `electrician woodland hills` (176 @ 54.1), `electrician van nuys` (170 @ 56), `electrician burbank` (152 @ 55.8) | `city-sherman-oaks.html`, `city-studio-city.html`, `city-encino.html`, `city-woodland-hills.html`, `city-van-nuys.html`, `city-burbank.html` | Differentiate from template: unique 60–90 word locality intro (landmarks, permit district, LADWP notes), 1 city-specific case-study blurb or review snippet, verify H1 = `Electrician in {City}, CA`, 1 locally-phrased visible FAQ + schema. Avoid near-duplicate boilerplate across the six. |
| C4 | `tesla charger installation` (338 @ 67.8) | `tesla-charger-installation.html` | Title/H1 → "Tesla Charger Installation in Los Angeles"; make the existing schema price data ($450–$750 Wall Connector installed) visible content + FAQ; hub link from `ev-charger-installation.html`. |
| C5 | `commercial electrician los angeles` (175 @ 77.1) | `commercial-electrical-los-angeles.html` | Visible services breakdown (TI, LED retrofit, fleet charging) with query-matched H2s + FAQ. |
| C6 | Refresh point | — | After C1–C5 deploy: export fresh GSC data into `seo-workspace/gsc/` and re-run this table. Positions 17–26 (C2/C3) are the fastest wins. |

---

## Classes

None. The codebase is procedural Python (scripts), vanilla JS (IIFE modules in `js/src/`), and static HTML. **Do not introduce classes** — follow the existing flat-function script pattern (`audit-site.py`, `schema-tool.py`, `fix-*.py`): module-level functions, `if __name__ == '__main__'`, idempotent behavior, `f'  - {file}'` bullet-style prints.

---

## Dependencies

- **No new packages.** Python stdlib only (`re`, `json`, `glob`, `html.unescape`, `xml.etree`) — matching existing scripts. `beautifulsoup4` is already used by `scripts/lighthouse-static-audit.py` if DOM-safe parsing is ever needed, but regex-in-file style is the repo convention for HTML edits.
- **Lighthouse CLI** at `/home/amram/.npm-global/bin/lighthouse` for before/after perf measurement (installed; `run_lighthouse_audit.sh` exists).
- **Cloudflare MCP / Chrome DevTools MCP** — configured in `.vscode/mcp.json` but not connected this session; plan does not require them. All CWV numbers here are lab/emulated; field data unavailable this session (stated per `web-perf` skill).
- **`gh` CLI** — authenticated; used for workflow monitoring.

---

## Testing

1. **Schema/structure gates (after every batch):**
   ```bash
   python3 scripts/schema-tool.py validate      # must stay "All pages pass validation."
   python3 scripts/audit-site.py                # 312 pages, 0 across all counters
   python3 scripts/build-css.py && python3 scripts/build-js.py && git diff --exit-code css/style.min.css js/site.min.js
   python3 scripts/audit-faq-sync.py --check    # new: 0 junk, 0 unmarked, 0 missing-head
   ```
2. **Sitemap integrity:** inline Python from `.github/workflows/audit.yml` → must print `Sitemap integrity check passed!`.
3. **JSON-LD parse sweep:** regex-extract every `application/ld+json` block across `*.html`, `blog/*.html`, `case-studies/*.html` → `json.loads` each (0 failures); FAQPage question count must equal visible question-`<summary>` count (delta 0 after fixes).
4. **Lighthouse (lab, mobile):** `gallery.html` perf **≥ 90** (from 81), LCP **< 2.5 s** (from 4.3 s) — primary success criterion; `index.html` TBT **< 200 ms** (from 250), perf ≥ 93, CLS stays 0; `city-burbank` perf ≥ 93, a11y 100, SEO 100 (no regressions). Save JSONs to `audit/lighthouse/`.
5. **Content checks:** every edited page — title ≤ 70 chars, meta 50–165 chars (`audit-site.py` enforces), new FAQs visible *and* in schema (`audit-faq-sync.py --check`), link/fragment sweep → 0 broken.
6. **Deployment verification:** push to `main` → `gh run watch --exit-status` for both workflows → live curl spot-checks (`/gallery`, `/whole-home-rewiring`, one `city-*`) → `bash scripts/notify-indexnow.sh`.
7. **Concurrency guard (learned 2026-10-08):** a second session (OpenCode) was editing/committing concurrently. Before every commit: `git status --short` + `git log --oneline -3`; stage only this plan's explicit paths (never `git add -A`); if unexpected files appear, stop and ask the user.

---

## Implementation Order

1. **Hygiene batch (mechanical, zero-risk):** add `</head>` to the 5 blog pages; strip `" +"` from 15 FAQ names on 3 pages; add the 4 unmarked visible questions to 3 pages' FAQPage — all via `scripts/audit-faq-sync.py --fix`, no hand edits.
2. **CI guardrails:** extend `scripts/schema-tool.py cmd_validate()` with checks (a)(b)(c); add the head counter to `scripts/audit-site.py`; write `audit/faq-sync-baseline.json`. Run Testing §1–2. **Commit** — locks fixes against the concurrent session's batches.
3. **Perf — `gallery.html`:** preload fix (`imagesrcset` matching first `<picture>`), lazy-load images 2–6; Lighthouse before/after; **commit** when perf ≥ 90 / LCP < 2.5 s.
4. **Perf — TBT:** gate estimator init behind `requestIdleCallback`/IntersectionObserver in `js/src/`, rebuild JS, homepage TBT < 200 ms; **commit**. If residual TBT is solely Cloudflare's challenge script, document as accepted — do not chase.
5. **Content C1** (whole-home rewiring — highest impressions, 3,226 combined): edit page, sync schema, gates, **commit**.
6. **Content C2** (emergency cluster — best position-to-effort, pos 17): **commit**.
7. **Content C3** (six city pages — template differentiation): one **commit** for all six (reviewable in one place).
8. **Content C4 + C5** (Tesla, commercial): **commit**.
9. **Deploy & IndexNow:** push (per-batch or grouped), watch CI with `gh run watch --exit-status`, live-verify, `bash scripts/notify-indexnow.sh`.
10. **Record & hand-off:** save Lighthouse baselines to `audit/lighthouse/`, append dated before/after results to this plan, note the GSC refresh point (C6) for the next cycle.

### Risk notes

- Step 1 touches the 5 blog pages the Sep-25 remediation "left alone deliberately" because `</head>` was missing pre-existing in git HEAD — fix is safe, but rebase-check before committing (concurrent session).
- FAQ append logic must never drop existing questions (2026-10-08 incident: a greedy regex ate 2 schema blocks on `ev-charger-installation.html`). All rebuilds must be block-scoped with a post-write `json.loads` assertion on **every** block in the file.
- `gallery.html` is 310 KB HTML with JS-lazy "Show More" — do not restructure gallery item markup; preload/lazy attributes only.
- Lab Lighthouse = throttled emulated mobile; field CWV is what GSC reports — treat lab gains as directional, confirm with Cloudflare Web Analytics (`events.rumPageloadEvents`) after deploy.

