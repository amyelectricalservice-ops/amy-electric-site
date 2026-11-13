# Website audit — 2026-11-13

**Scope:** production Worker (`amyelectric.com` / workers.dev), all sitemap
pages, repo validators, Lighthouse mobile, security headers, redirects, lead
path and CRM delivery.
**Method:** repo scripts + full HTTP crawl (322 URLs) + Lighthouse 13.4.1
(mobile, simulated throttling) + Playwright network capture.
**Read-only except the fixes listed in §2**, which are deployed (PR #52).

---

## 1. Headline

| Area | Result |
|---|---|
| Pages in sitemap | 322 — **322/322 return 200** |
| Broken internal links | **0** of 133 unique targets |
| Canonical mismatches | **0** |
| Pages without exactly one H1 | **0** |
| Missing image alt / dimensions | **0** |
| Duplicate element IDs | **0** (2 fixed) |
| Invalid JSON-LD | **0** |
| Thin pages (<250 words) | **0** |
| Title/description duplicates | **0** |
| Security headers | **All present**; security smoke test passes |
| Accessibility (Lighthouse) | **100** on every audited page |
| SEO (Lighthouse, apex) | **100** |
| Lead path | Healthy; EspoCRM sync running, queue empty |

The site is in good shape. The remaining work is one Core Web Vital
(font-swap CLS) and a tracking/privacy decision.

---

## 2. Fixed during this audit (deployed)

| # | Finding | Fix |
|---|---|---|
| 1 | Upload inputs on `/contact` and `/residential-electrician` had no accessible name — a11y **94** | `aria-label` on all three file inputs → a11y **100** |
| 2 | `id="estimate"` appeared twice on `/generator-installation` and `/electrical-troubleshooting` | trailing CTA band renamed `estimate-cta` |
| 3 | `/blog/whole-home-rewiring-guide` meta description 179 chars | shortened to 145 |
| 4 | Microsoft UET (`bat.bing.com`, loaded by Cloudflare Zaraz) blocked by CSP on every page → console error | allowed `bat.bing.com` / `c.bing.com` in CSP |
| 5 | `injectSchema` skipped any page that merely mentioned "electrician"; 5 case-study pages had only BreadcrumbList | now keyed on `@type` (Electrician/LocalBusiness); case studies get the business entity |
| 6 | `audit-site.py` truncated descriptions at apostrophes (`it's` → 43 chars) | quote-aware regex |

Post-fix crawl: **322/322 pages, 0 issues in every category.**

---

## 3. Lighthouse (mobile, simulated 4× CPU)

Measured on the workers.dev host to avoid Cloudflare's bot challenge, which
distorts lab numbers on the apex.

| Page | Perf | A11y | Best prac. | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| `/` | 93 | 100 | 96 | 2.5 s | 20 ms | 0 |
| `/residential-electrician` | 96 | 100 | 96 | 2.4 s | 0 ms | 0 |
| `/contact` | 93 | 100 | 96 | 2.7 s | 70 ms | 0.069 |
| `/tesla-charger-installation` | 86 | 100 | 96 | 2.5 s | 0 ms | **0.196** |
| `/gallery` | 85 | 100 | 96 | **3.4 s** | 310 ms | 0 |
| `/book` | **70** | 100 | 96 | 1.6 s | 240 ms | **0.293** |

`Best practices` is 96 because of the known `/cdn-cgi/rum` 405 on the
workers.dev host (no analytics pipeline there) — an artifact, not a site error.
On the apex, SEO is 100 and console errors are now zero.

**Run-to-run variance is significant** under simulated throttling (homepage
TBT measured 20 / 110 / 540 ms across runs). Treat CLS and LCP as reliable,
TBT as directional.

---

## 4. Remaining findings

### P1 — CLS from web-font swap (only "poor" metric)

- `/book` **0.293** (poor, >0.25); `/tesla-charger-installation` **0.196**
  (needs improvement); `/contact` 0.069 (good).
- Lighthouse attributes the shifts to `BarlowCondensed-600/700.woff2` and
  `SourceSerif4-400italic.woff2` swapping in after first paint. All fonts are
  already preloaded and cached for a year, so field CLS is likely lower than
  lab — but there is no CrUX field data yet to confirm.
- Fix options:
  1. **Metric-compatible fallback** — keep `font-display: swap`, add a
     fallback `@font-face` with `size-adjust` / `ascent-override` /
     `descent-override` matched to the real font. Best visual result.
  2. `font-display: optional` — zero CLS, but first visits on slow connections
     may keep the fallback until the next navigation.
- Recommended: option 1 on the two Barlow weights + Source Serif italic.

### P2 — Gallery LCP 3.4 s

- Page weight 551 KiB, image-heavy by design. The first image is already
  eager/high-priority with a preload.
- Worth testing 600w variants and confirming the LCP element is the first
  image (not a later row) before changing the pipeline.

### P2 — Microsoft UET via Cloudflare Zaraz

- Zaraz injects `/cdn-cgi/zaraz/s.js`, which calls `bat.bing.com` for Microsoft
  Advertising. The CSP was blocking it; it is now allowed so the owner's
  configured tracking works.
- **Decision needed:** if Bing/Microsoft Ads is not in use (the plan in
  `seo-workspace/ads/` is Google Ads + LSA), remove the Zaraz tool — it costs
  requests/main-thread time and adds a third party. If it is in use, keep it
  and consider a consent/idle trigger in Zaraz.

### P3 — Smaller items

- `legacy-javascript-insight`: ~10 KiB of transpiled helpers in `site.min.js`;
  only worth revisiting if the browser target is raised.
- `cache-insight`: HTML is `max-age=300, s-maxage=60` by design (edge strips
  ETag); not a defect.
- No CrUX field data yet — lab only. Re-check PageSpeed after traffic grows.

---

## 5. SEO / technical checks

- **Sitemap**: 322 URLs, all 200, `<lastmod>` present, no priority/changefreq.
- **Canonicals**: every page self-canonical, extensionless, apex host.
- **Robots**: `index, follow` on apex; `x-robots-tag: noindex` only on the
  workers.dev host (intentional).
- **robots.txt**: allows content, blocks `/api/`, `/reports/`, `/partials/`;
  explicitly allows AI crawlers.
- **Redirects**: http→https 301, www→apex 301, `.html`→extensionless 301.
- **404**: returns 404 (not a soft 200).
- **llms.txt / llms-full.txt**: 200 (7.6 KB / 13 KB), linked via `Link`
  headers.
- **Schema**: all pages valid; case studies now carry the Electrician entity.
- **Content**: no thin pages; titles and descriptions unique.

## 6. Security

`scripts/security-check.sh` passes on production:

- HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, CSP present.
- `/admin` and `/api/admin/*` reject anonymous (401).
- Upload endpoint rejects a disguised file.
- `/api/contact` rejects GET (405).
- Admin token, CRM credentials and R2 objects remain private.

## 7. Lead path

- `/api/health`: all bindings present (`crm_db`, `lead_files`, `ai`, …).
- EspoCRM cron: last run clean, no pending leads.
- Lead scoring, de-dupe, uploads and CRM sync verified end-to-end on
  2026-11-12 (Contact + Lead + Task + Opportunity, then removed).

---

## 8. Suggested order

1. Font metric overrides (CLS) — `/book`, `/tesla`.
2. Decide Bing/Zaraz (remove or keep deliberately).
3. Gallery LCP experiment.
4. Start collecting CrUX field data; re-audit in 4–6 weeks.

---

## 9. Follow-up shipped (2026-11-13, after the first pass)

An external homepage review prompted a re-check. Three of its claims were
verified and fixed; three were not accurate for this site.

**Fixed**

| Finding | Detail |
|---|---|
| Quote widget dead end | Choosing "Other Electrical" hid the lead form **and** the phone number, so rewiring and repair leads vanished. The widget also had no source file. Rebuilt as `js/estimator-widget.js` → `scripts/build-estimator.py` → `js/estimator.min.js`, with a fourth service (Whole-Home Rewiring, priced by home size from `05-estimate-data` tiers) and a custom-quote path that always shows the form. |
| `.qe-field label` leaked onto radio labels | The group-heading rule applied to every `<label>` nested inside, forcing radio options to `display:block` with a 250px-wide dot. Scoped to `.qe-field > label`. |
| Honeypot not hidden from assistive tech | `aria-hidden:true` sat inside a `style` attribute on 483 wrappers across 242 pages, so browsers discarded it. Moved to the attribute; `scripts/fix-honeypot-aria.py` + an `audit-site.py` rule prevent regressions. |
| Stale LADWP rebate figure | 84 mentions across ~40 pages said "up to $500"; ladwp.com's current residential figure is **up to $1,000** (+$500 income-qualified). Swept; the estimate engine's `CREDITS` row corrected from 500 to 1000. |

**Not accurate**

- "Three stacked lead-capture flows" — the detailed form is already collapsed
  inside `<details>`. There are two visible flows, not three.
- "Astro" — the site is static HTML on Workers + Assets; no framework.
- "Build dedicated city and service landing pages" — 112 city pages and 64 geo
  service pages already exist.
- "Replace illustrative case studies with real jobs" — the gallery has 387 real
  photos, but publishing a case study needs job-specific facts (address,
  permit sign-off, timeline) that only the owner can supply. Inventing them
  would be a false claim, so the disclaimer stays until that data arrives.
