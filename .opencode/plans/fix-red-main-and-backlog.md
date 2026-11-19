# Plan: get `main` green, then work the SEO/conversion backlog

Status: proposed · 2026-11-19 · base `44e79257` (`origin/main`)
Scope: unbreak the contact API and the two red CI workflows, fix the nav generator drift, then execute the P0–P3 backlog in dependency order.

## Guardrails (read before touching anything)

- Branch + PR, never push to `main`. Rebase over the `[skip ci]` lastmod commit the deploy bot writes back.
- `python3 scripts/audit-skills.py` parses **every backticked lowercase-kebab token in `AGENTS.md`** as a skill id. Use full filenames/paths in backticks there.
- Do not change canonical prices by editing page copy alone. `js/src/05-estimate-data.js` + `scripts/estimate-schema.sql` + `scripts/test-estimator.mjs` move together.
- Never bulk-run `scripts/inject-layout.py` or `scripts/sync-nav.py` without reading the diff first (both currently regress the header — see Phase 2).
- Never run `scripts/sync-faq-schema.py --apply`. Never add a §30C claim.
- Every phase ends with `python3 scripts/audit-site.py` + `node --test scripts/test-*.mjs` + `wrangler deploy --dry-run` before the PR is opened.

## Phase 0 — PR 1: restore the contact handler (blocks everything)

**Why:** `44e79257` deleted five module-local helpers (`parseEstimate`, `badRequest`, `successResponse`, `formatLeadText`) from `contact-handler.js` while still calling them. Every `POST /api/contact` throws a `ReferenceError`, is caught by the outer `try`, and returns a generic 400. Deploy has been blocked by the 4 failing tests since 2026-11-18.

### Task 0.1 — revert the file to the last working revision

```bash
git checkout -b fix/contact-handler-helpers
git checkout HEAD~1 -- contact-handler.js
node --test scripts/test-contact-estimate.mjs   # verified: 4/4 pass
node --test scripts/test-*.mjs                  # expect 132 tests, 0 fail
```

This is the whole fix. It also drops the inline D1 block the same commit added, which is correct: persistence belongs to `contact-enrich.js` → `lead-store.js`. Leaving that block in place (once helpers are restored) would write a second, unscored, UTM-less row for every lead.

Verify by hand (the test stubs `fetch`, so it cannot prove the worker wiring):

```bash
printf 'name=Test&phone=(818)302-5614&message=panel+upgrade+please' > /tmp/f.txt
# after deploy, on the workers.dev host only:
curl -sS -o /dev/null -w '%{http_code}\n' -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data @/tmp/f.txt https://amy-electric-site.a-m-y-electricalservice.workers.dev/api/contact
```

Done when: 200 `{"success":true}`, D1 gains exactly one `leads` row (not two), and the deploy workflow's `Test the Worker` step is green.

### Task 0.2 — add a guard so this cannot ship again

In `scripts/test-contact-estimate.mjs`, the suite already imports the real module, so the deletion was caught — it shipped because the deploy gate ran after a cherry-pick that never ran tests locally. No new test needed; instead add to the PR description that `node --test scripts/test-*.mjs` is the gate.

## Phase 1 — PR 2: unbreak `audit-site.py` / the Quality workflow

Current failures (measured): 4 pages missing from sitemap, 4 missing `js/site.min.js`, 4 missing the sticky bar, 4 broken `index.html` links.

### Task 1.1 — make the four new `electrician-*.html` pages aliases (matches the established pattern)

`electrician-{los-angeles,pasadena,woodland-hills}.html` are `noindex, follow` **and** canonical to their `city-*` page, which is why they are legitimately absent from `sitemap.xml`. The four added in `4d38f79b` (`burbank`, `glendale`, `santa-monica`, `sherman-oaks`) are `index, follow` and self-canonical, so both CI sitemap checks demand entries for them.

```python
# one-off, run from repo root
for city in ('burbank','glendale','santa-monica','sherman-oaks'):
    f = f'electrician-{city}.html'
    t = open(f).read()
    t = t.replace('<meta name="robots" content="index, follow">',
                  '<meta name="robots" content="noindex, follow">', 1)
    t = t.replace(f'<link rel="canonical" href="https://amyelectric.com/electrician-{city}">',
                  f'<link rel="canonical" href="https://amyelectric.com/city-{city}">', 1)
    open(f, 'w').write(t)
```

Verified: this alone takes `Pages missing from sitemap: 4 → 0`.

> Owner decision (see bottom): if these four should stay indexable instead, skip the `noindex` line, add canonical-self entries to `sitemap.xml`, and accept four near-duplicates of the `city-*` pages.

### Task 1.2 — give those four pages the site bundle and the sticky bar

They are a different, minimal template (378 lines) than the 574-line alias pages. Insert before `</body>`, with no `../` prefix (they are root files):

```html
<div class="sticky-bar"><a class="sticky-btn sticky-call" href="tel:18183025614" aria-label="Call AMY Electric at (818) 302-5614"><span class="sticky-icon" aria-hidden="true">📞</span><span class="sticky-label">Call Now</span></a><a class="sticky-btn sticky-text" href="sms:+18183025614?body=Hi%20AMY%20Electric%2C%20I%27m%20inquiring%20about%20electrical%20work.%20Sending%20a%20photo%20of%20my%20panel%2Foutlet%20now." aria-label="Text AMY Electric"><span class="sticky-icon" aria-hidden="true">💬</span><span class="sticky-label">Text Us</span></a><a class="sticky-btn sticky-estimate" href="book"><span class="sticky-icon" aria-hidden="true">📋</span><span class="sticky-label">Get Estimate</span></a></div>
<script src="js/site.min.js" defer></script>
```

Copy the `.sticky-*` rules from `css/src/09-sticky-bar.css` into their inline `<style>` block (they do not load the stylesheet).

### Task 1.3 — remove the placeholder analytics block

Each of the four ships this, which is worse than no tracking:

```html
<script async src="https://googletagmanager.com/gtag/js"></script>
<script>... gtag('config', 'G-XXXXXXXXXX'); ...</script>
```

Delete the block. `js/site.min.js` (`js/src/02-analytics.js`) already fires `phone_click` and is gated on the real `GA4_ID` secret. Keeping both also duplicates the call event under a second name (`click_to_call` vs `phone_click`), which Phase 5 has to reconcile.

### Task 1.4 — fix the schema city

All four carry `"description": "Licensed C-10 electrical contractor serving Agoura Hills, CA. ..."` in the `Electrician` JSON-LD. Replace `Agoura Hills` with the page's city in each.

### Task 1.5 — the four dead `case-studies/*` links

`index.html` lines ~968–1007 link to `case-studies/{glendale-ev-charger,sherman-oaks-panel-upgrade,multi-unit-ev-subpanel,winnetka-service-release}`, none of which exist. Recommended: create the four pages, because the card titles are localized proof (`200A Panel Upgrade in Sherman Oaks`) and the sibling pages are short and explicitly illustrative.

- Clone `case-studies/residential-ev-ready-garage.html` (101 lines: canonical + inline CSS + one `main` block + sticky bar + `../js/site.min.js`).
- Change title, description, canonical, `<h1>`, breadcrumb, the three section headings, the related-service link, and keep the "Illustrative project profile … no identifying customer" framing in the description.
- Add a card to `case-studies/index.html` for each.
- Add 4 `<url>` entries to `sitemap.xml` (directory URLs stay as-is; no `<priority>`/`<changefreq>`) with today's `<lastmod>`.

Cheap fallback if the copy is not wanted: repoint the four cards to the four existing case studies and delete the duplicate titles.

Done when: `audit-site.py` prints `0` for every issue line, the deploy workflow's inline sitemap-parity script passes, and the page/sitemap counts in `AGENTS.md` are updated (366 → 370 pages, 323 → 327 sitemap URLs if Task 1.5 creates pages).

## Phase 2 — PR 3: one canonical header

`partials/{nav,nav-blog,footer}.html` + `scripts/inject-layout.py` and `scripts/sync-nav.py` disagree with each other and with the deployed pages:

| generator | measured effect today |
|---|---|
| `inject-layout.py` | 367 files; replaces `class="main-nav"` with bare `<nav>`, deletes the entire "More" panel and the Book CTA, reverts to the 15-link menu |
| `sync-nav.py` | 365 files; drops the "Residential Electrician" link, repoints two guide links to `-cost-la` URLs that `_redirects` 301s away |

1. Treat the deployed nav (7 primary items + "More" panel, as served by `/`) as the target.
2. Patch `scripts/sync-nav.py`: add `residential-electrician` back into the More → Services column, and use `blog/ev-charger-installation-cost-los-angeles` / `blog/whole-home-rewiring-cost-los-angeles`.
3. Run `python3 scripts/sync-nav.py`, then `git diff --stat` and eyeball 3 pages (root, `blog/*`, `case-studies/*` for the `../` prefix).
4. Regenerate `partials/nav.html` from the result so `inject-layout.py` can no longer regress the header — or delete the `inject-layout` path and document `sync-nav.py` as the only source.
5. Add `python3 scripts/sync-nav.py --check` as a step in `.github/workflows/audit.yml`.

Done when `sync-nav.py --check` exits 0 on a clean tree and the rendered header on `/`, `/blog/`, and `/case-studies/` is identical.

## Phase 3 — PR 4: pricing and license accuracy (backlog TASK-01/02)

Do **not** apply the backlog's round numbers. Measure first:

| service | values in the tree today |
|---|---|
| panel upgrade | `$1,800–$4,500` on 19 pages, `$2,500–$4,500` on 26 pages, `$1,800–$3,500` on 1 |
| EV charger | `$500–$1,200` (install only, canonical) on 16 pages, `$800–$2,500` (likely unit included) on 17 |
| diagnostic / service call | `$125–$185` in FAQ schema, `$150–$350` in the backlog, no row in `05-estimate-data.js` |

1. **Owner decision required** (see bottom) on panel range and on whether `$800–$2,500` means "installed with charger". Write the answer into `js/src/05-estimate-data.js` first if it is a real scope change.
2. Sweep only the agreed literal, page by page, with a script that prints every replacement — not a blind `sed`.
3. Add the disclaimer under pricing blocks: *"Final pricing depends on existing panel capacity, conduit/trenching distance, and LADWP/LADBS permit requirements."*
4. Extend `scripts/audit-price-drift.py` to panel ranges (it currently reads only EV canonicals, which is why it reports `Flagged page/range pairs: 0` while panel copy disagrees with itself on 45 pages).
5. **TASK-02 copy fix:** `licensed-electrician-los-angeles.html` and `tesla-charger-installation.html` say "all 16 major communities we specifically serve" — replace with statewide-license wording (`CSLB C-10 #981578`, permits + LADWP/LADBS coordination across Greater LA).
6. Verify CSLB `#981578` and `EVITP #4051604` appear in the topbar/footer of every page (`grep -L` sweep).

## Phase 4 — PR 5: LADWP / ADU authority + inquiry routing (TASK-03/04)

Most of TASK-03 already exists — extend rather than rebuild:

- Existing: `ev-charger-installation-los-angeles.html`, `adu-electrical.html`, `ladwp-electrical-guide.html`, `panel-upgrade-los-angeles.html`, 65 geo service pages; "meter spot" on 6 pages, CALeVIP on 5.
- Missing: **Charge Up LA** (0 pages), **LADBS Express Permit** (1 page), a consolidated "200A+ / meter spot / overhead-to-underground / ADU subpanel load-sharing" block.
- Add the block to `panel-upgrade.html` + `panel-upgrade-los-angeles.html`, and a rebate-navigation block to the EV hub. H2s must name Valley cities already covered by `GEO_TARGET_AREAS`.

TASK-04 form work — the fields already exist (`city`, optional uploads on `contact.html` lines ~457/542, UTM capture in `contact-enrich.js:attribution()`). Only the selector is missing:

1. Add the three inquiry types to the `request_type` radiogroup on `contact.html`; keep `request_type` as the field name so `contact-enrich`/`lead-store` keep working.
2. Extend `COMMERCIAL_RE` / emergency regexes in `lead-store.js` to recognise the new values, or B2B leads score as residential.
3. Emergency type must also render a prominent `tel:` CTA and set `follow_up_at` inside 15 minutes.
4. Do not re-add `<label for="request_type">` (no element has that id; 252 pages rely on `aria-labelledby="request-type-label"`).

## Phase 5 — PR 6/7: B2B page, schema, tracking (TASK-05/06/07)

- **TASK-05** `/contractors-commercial` does not exist at all — the only genuinely new page in this backlog. Build it as a root `contractors-commercial.html` with the standard template (JSON-LD, OG, sticky bar, `js/site.min.js`), add it to `sitemap.xml`, the `sync-nav.py` More panel, and link it from `commercial-electrical.html`.
- **TASK-06** schema: the site already emits `Electrician` + `identifier` (`981578`, `4051604`) on some pages; `injectSchema()` only fills pages with no `Electrician`/`LocalBusiness` block. Add `areaServed` from `GEO_TARGET_AREAS` and the 112 `city-*` pages in the canonical block in `scripts/site_data.py`, not per page. Review tags: add service/neighborhood labels in the review component and keep `reviewCount` at 87.
- **TASK-07** tracking: rename nothing until the dashboards exist. Today `js/src/02-analytics.js` fires `phone_click`, `form_submit`, `quote_submit`, `estimate_sent`, …; the backlog asks for `click_to_call`, `form_submit_emergency`, `form_submit_residential`, `form_submit_b2b`, `download_capability_sheet`. Add the missing ones **alongside** the existing names, and only after `GA4_ID` is actually set as a Worker secret — otherwise every event stays a no-op and you cannot verify it.
- UTM tagging for GBP/LSA is a Google-side configuration task; the server already persists `utm_source`/`utm_medium` per lead, so verify with `/admin` rather than changing code.

## Sequencing and dependencies

```
PR1 (Phase 0) ──► PR2 (Phase 1) ──► PR3 (Phase 2) ──► PR4 (Phase 3) ──► PR5 (Phase 4) ──► PR6/7 (Phase 5)
   unblocks CI        green             nav stable        copy/price         content          new page/tracking
```

PR1 and PR2 are the only ones that must land before anything else; PR3 should land before PR5 because new pages get appended to the nav.

## Open owner decisions (block specific tasks)

1. **Panel range:** `$1,800–$4,500` (19 pages) or `$2,500–$4,500` (26 pages)? Pick one and update `05-estimate-data.js` + SQL + test.
2. **EV range scope:** is `$800–$2,500` "installed with the charger unit" and `$500–$1,200` "installation only"? If yes, both stay and the copy must label the scope; if no, one is wrong.
3. **Diagnostic price:** adopt `$150–$350` (there is no canonical row today, so this needs a new estimate-data entry).
4. **The four `electrician-*` pages:** alias (`noindex`, canonical to `city-*`, recommended) or indexable with sitemap entries.
5. **Case studies:** create the four illustrative profiles, or repoint the cards at the existing four.
6. **Email delivery:** still blocked — `env.EMAIL` is unbound and MailChannels silently fails. No phase above should promise email in visitor copy.

## Definition of done

```bash
python3 scripts/schema-tool.py validate
python3 scripts/audit-site.py            # 0 issues
python3 scripts/audit-skills.py          # PASS
node --test scripts/test-*.mjs           # 132 pass
python3 scripts/sync-nav.py --check      # 0 drift (after Phase 2)
python3 scripts/build-css.py && python3 scripts/build-js.py \
  && python3 scripts/build-estimator.py && python3 scripts/build-leadform.py
git diff --exit-code css/style.min.css js/site.min.js js/estimator.min.js \
  js/lead-estimator.js js/lead-estimator.min.js css/lead-form.min.css
wrangler deploy --dry-run
```

Then: merge, watch Deploy + Quality workflows go green, spot-check `https://amy-electric-site.a-m-y-electricalservice.workers.dev/{,city-arleta,panel-upgrade,blog/}`, submit a real test lead through `/contact` and confirm one D1 row + `/admin` visibility, and finally delete the "Known-broken on `main`" section from `AGENTS.md`.
