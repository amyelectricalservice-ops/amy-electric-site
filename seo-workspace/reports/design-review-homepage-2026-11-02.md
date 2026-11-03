# Design review — homepage (`/`)

**Date:** 2026-11-02
**Scope:** visual + layout + hierarchy critique of the live homepage. Not a code review, not an SEO audit.
**Method:** live render on `amy-electric-site.a-m-y-electricalservice.workers.dev` (apex serves bot challenges). Two viewports: **1440×900 desktop** and **iPhone 13 / 390 CSS px mobile**. All numbers below are measured from the rendered DOM, not estimated from screenshots.

---

## Verdict

The visual language is coherent and confident — condensed display type, navy/gold palette, strong photography. What lets it down is **structure, not styling**: the page is a flat stack of 11 sections, four of which duplicate each other, arranged in grids whose item counts don't fit their column counts. Several blocks read as unfinished because a value is missing or a placeholder never got replaced.

The single highest-leverage change is not cosmetic: **cut the homepage roughly in half** by removing the duplicate blog and testimonial sections and tightening the card grids. Every other finding is cheaper to fix but smaller in impact.

---

## Shipped 2026-11-02 (top five)

| Fix | Before | After |
|---|---|---|
| `--navy3` / `--navy1` defined | avatar circle invisible on 29 pages (`rgba(0,0,0,0)`) | raised disc `#22406e`, 1.55:1 on `--navy2` |
| Footer 5th column | `2fr 1fr 1fr 1fr`, `Company` orphaned on its own row, 1,292px | `1.6fr repeat(4,1fr)`, 5 across, **809px** |
| Duplicate sections | 13 sections, 2 blog + 2 testimonial blocks | 11 sections; one of each |
| Hero photo ≤900px | `display:none`, `<img>` 0×0 | full-width 16:10 below the CTAs, 342×257 at 390px |
| Credential band | 6 items in 4 cols → 4+2, 987px tall on mobile | 3×2 desktop / 2×3 mobile, **328px / 428px** |

**Page height: 13,081px → 10,016px desktop (−23%), 24,563px → 18,503px mobile (−25%).**

Two content decisions taken while doing it:

- The lower "Electrical Guides & Tips" block was **32 cards containing 3 duplicate pairs** (`la-electrical-safety-tips`, `smart-home-electrical-upgrades`, `panel-upgrade-signs` each linked twice). It was replaced by the curated 6-card block from the top of the page, moved to the bottom — so the page now opens hero → services instead of hero → blog, and the 3×2 grid kills the orphan row.
- The 4-card testimonial block absorbed the position of the 3-card one (proof right after "Why AMY Electric"), keeping the gold-left-border treatment, the Google rating line, and both CTAs. Its `auto-fit/minmax(300px)` grid is now `repeat(4,1fr)` → 2-up ≤900px → 1-up ≤600px.

Not touched (still open): nav IA, emoji icons, hero copy length, section-header alignment, project-profile empty panels, `.trust-bar` strip wrapping 5+1 at 1440, footer heading styles (three 20px white headings vs one 13px grey uppercase one).

---

## What already works

- **Type pairing is right.** Barlow Condensed 800 for display + Source Serif 4 for body is a genuine editorial pairing, not a default. H1 64/67.2, H2 46/50.6 — tight leading that suits condensed caps.
- **Palette is disciplined.** `--navy #0b1628`, `--navy2 #122040`, `--gold #f5a623`. Gold is used as accent only, not as decoration.
- **Trust signals are unusually strong** for a contractor site: C-10 number, EVITP number, CSLB verify link, insurance, permit claim, star rating, response promise.
- **Hero photo** is real work, correctly cropped, `fetchpriority=high`, 546×409 with proper dimensions.
- **The estimate widget** is the most differentiated asset on the page and deserves more prominence than it gets.

---

## Findings

### P0 — reads as broken

**1. Founder avatar circle is invisible (site-wide).**
The "Meet Amram" block renders a 160px circle with `background: var(--navy3)`, but **`--navy3` is never defined** — only `--navy` and `--navy2` exist in `css/src/01-*.css`. The background resolves to transparent, so the circle disappears and a bare gold "A" floats in the middle of the page. Measured: avatar background `rgba(0,0,0,0)` against section `#122040`, contrast ratio 1.31.

Same markup appears in **29 files** (`grep -rl 'var(--navy3)' --include=*.html` — 28 blog bylines + homepage). Every one is a floating letter with no frame.
*Fix:* define `--navy3` (or swap to `--navy2` + a `1px solid rgba(245,166,35,.25)` ring). One-line CSS change fixes all 29 pages.

**2. Trust bar is a 4-column grid holding 6 items.**
Measured `grid-template-columns: 249px ×4`, 6 children, 270px tall. Result: a full-width yellow band with four items on row 1 and two on row 2, leaving two-thirds of the second row as empty yellow. The band is also the loudest surface on the page — it competes with the `Call Now` button for attention.
*Fix:* either 3×2 or 6 columns (6 works at ≥1200px), or drop to the four strongest claims and move `4.9★ / 87 reviews` and the phone into the hero badges where they already exist.

**3. Trust bar is 987px tall on mobile.**
Same 6 items stack one per row inside the yellow band. That is more than one full screen of solid yellow between the FAQ and the founder bio. Mobile should show at most 2 rows — 2×3 grid or a single horizontal scroller.

**4. Footer's 5th column wraps to its own row.**
`.footer-grid` is `408px 204px 204px 204px` with **five** children (`footer-brand` + 4 `footer-col`). The fifth (`Company`, 11 links) drops to row 2, and because the grid stretches rows, columns 2–4 stay 623px tall while `Company` sits alone in a 443px row with three empty columns beside it. Desktop footer: **1,292px**. Mobile footer: **2,315px**.
*Fix:* 5-column template at ≥1100px (`minmax(240px,1.6fr) repeat(4, minmax(150px,1fr))`), or move `Company` into the brand column.

**5. Hero photo disappears on every screen ≤900px.**
`css/src/10-responsive.css:4` sets `.hero-img { display: none }`. At 390px the `<img>` measures **0×0**. The `.why-img` is hidden by the same rule. So the mobile homepage — where most contractor traffic lands — has **zero photography**, on a site with 387 gallery photos.
*Fix:* keep the photo, drop it below the CTAs at ≤900px, `aspect-ratio: 16/10`, full-bleed. It is the cheapest credibility win available.

**6. Emoji are used as icons — 46 instances on the homepage.**
⚡ 🔧 👷 🔌 📘 🏅 💰 🕐 📋 💬 🛠️ 🏢 💡 🚨 📍 ★ appear as service icons, guide icons, project-profile art, and review stars. They render differently on macOS / Windows / Android / iOS, cannot inherit brand color, and sit next to one high-quality photo — which makes the contrast obvious.
*Fix:* the gallery already has panel, EV, and rewiring photos. Project profiles especially need photos, not a wrench glyph in a 245px empty panel.

**7. Project-profile cards are 40% empty panel.**
Each card is a ~245px navy block containing one centered emoji, then the copy. On mobile the section is **2,307px** for four cards, three of which are the same shape.
*Fix:* swap the emoji block for a photo, or delete the block entirely and let the copy lead.

---

### P1 — structure and hierarchy

**8. The nav is a link dump: 24 items, 3 rows, 161px sticky.**
`Services, Home, EV Chargers, Panel Upgrades, Repairs, Commercial, Lighting, Tesla Charger, Rewiring, Generators, Surge Protection, Reviews, Gallery, Emergency, EV Charger vs Panel, Hardwired vs Plug-In, Blog, Is Your Home EV Ready?, Rewiring Cost, EV Charger Cost, Service Areas, Get a Quote, Book Online, Call Now`.

At 1440px this occupies three rows and **161px of a 900px viewport (18%)** — permanently, because the header is sticky above 680px. No visual grouping separates primary services from comparison pages from cost pages from utility pages; `Call Now` floats at the end of row 3 with a gap before it.
*Fix:* 5–7 primary items + a "Services" menu. Everything currently in rows 2–3 belongs in that menu or in the footer.

**9. The logo lockup is misaligned.**
`AMY` sits on one line, `Electric` on the next, the `AE` badge is absolutely positioned over the left edge spanning both, and `LOS ANGELES ELECTRICIANS` breaks to two 11px lines below. The result reads as three stacked fragments rather than a mark. At 1440 there is also a 60px dead gap between the mark and the first nav item.
*Fix:* one-line lockup — badge + `AMY Electric` on a single baseline, sub-line on one line at 11px with 0.08em tracking.

**10. Four of eleven sections duplicate each other.**
Section order: Guides → Services → Why → Testimonials → Estimator → Quote form → FAQ → Profiles → Testimonials again → Trust bar → Founder → Guides again.
- Two blog sections (`Electrical Guides for LA Homeowners` at 768px, `Electrical Guides & Tips` at 1,757px).
- Two testimonial sections (`What Our Customers Say` at 589px, `Trusted by Los Angeles Homeowners` at 975px) **with two different card treatments** — navy cards with a hairline border vs. charcoal cards with a 3px gold left border.
- Two `estimate-section` blocks back to back (691px + 743px).

*Fix:* keep one blog block (the lower one, which has the better `Resources` eyebrow), keep one testimonial block (pick the gold-left-border treatment — it scans faster), merge the estimator and quote form into a single section.

**11. Page length.**
**13,081px desktop / 24,563px mobile (~29 screens).** Fixing #10 removes roughly 2,500px desktop and 4,500px mobile. The remaining bulk is card grids that stack to one column on mobile: services **3,088px**, guides 1,474px, profiles 2,307px.

**12. Grid item counts don't fit column counts.**
- Guides: 6 cards in a 4-column grid → 4 + 2 with a large hole (mobile 1,474px).
- Profiles: 4 cards in 3 columns → 3 + 1 orphan.
- Testimonials (lower): 4 cards in 3 columns → 3 + 1 orphan.
- Trust bar: 6 in 4 columns (see #2).
- Footer: 5 in 4 columns (see #4).
*Fix:* 3-column grid for 6 guides, 2×2 for 4 profiles, 3+1 with the fourth card spanning or a "read all reviews" tile filling slot 4.

**13. Section-header alignment is inconsistent.**
Hero left, Services left, Why left, Testimonials centered, Estimator centered, FAQ centered, Profiles centered, Founder left, Guides centered. There is no rule the reader can learn.
*Fix:* pick one. Left-aligned is the better fit for the condensed display face and matches the hero.

**14. Hero copy is too long to be a hero.**
`.hero-desc` is 18px/29.7px and runs **7 lines at 1440 and 7 lines at 390** — it carries the licence number, the EVITP number, the pricing for two services, the permit claim, and the phone number in one paragraph. On mobile it pushes every CTA below the fold.
*Fix:* 2 lines — who you are, where, and what to do next. Move pricing to the badges row or the estimator, which already exists.

**15. Estimator is a 1,007px mobile section for a 3-option chooser.**
Three cards stack at ~330px each. The step indicator (`SERVICE / CHARGER / SETUP / QUOTE`) is 12px with heavy tracking and the inactive dots are `#122040` on `#0b1628` — effectively invisible progress.
*Fix:* compact cards on mobile (icon left, label + one-line description right, ~72px), and lighten inactive dots to `rgba(244,241,235,.25)`.

---

### P2 — polish

**16.** H1 breaks as `Los Angeles / Electrician — / Safe, Code-Compliant / Electrical Work` at 1440, leaving a dangling em dash at the end of line 2. Use a `<br>` after `Electrician` or `text-wrap: balance`.

**17.** Hero photo top edge sits **150px below** the H1 top edge at 1440 (`h1 y=330`, `img y=480`), so the two columns read as unrelated. Align the image top with the eyebrow, or vertically center it against the copy block.

**18.** The `LADWP rebate` callout is a gold-bordered alert box placed **above** the `See Your Price Instantly` H2. The alert outranks the heading. Move it under the widget's first step.

**19.** 51 text nodes are under 13px on mobile. Worst offenders: `.logo-sub` 11px, `.section-label` 12px/1.68px tracking, `.topbar` 14px, `nav a` 15px. The 12px eyebrow labels are legible; the 11px two-line logo sub-line is not.

**20.** Footer links are underlined 15px serif. Underlined serif in a dense 16-link column reads as a list of footnotes. Drop the underline, use `rgba(244,241,235,.72)` with a gold hover.

**21.** Desktop nav links measure 41px tall — 3px under the 44px target in `10-responsive.css`. The mobile touch-target work covers ≤767px; desktop pointer users are fine, but the rule and the render disagree.

**22.** The trust bar uses `<h3>C-10 Licensed</h3>` with no `<h2>` above it, so the document outline goes H2 → H3 with no parent. Either promote it to H2 or demote to a `<p>`/`<div>` — it is a claim, not a section.

---

## Suggested order of work

| # | Change | Effort | Impact |
|---|---|---|---|
| 1 | Define `--navy3` (fixes 29 pages) | 1 line | Removes a visible placeholder |
| 2 | Footer 5-column template | 1 rule | −850px desktop, −1,400px mobile |
| 3 | Delete duplicate blog + testimonial sections | content edit | −2,500px desktop |
| 4 | Restore hero photo ≤900px | 1 rule | Mobile credibility |
| 5 | Trust bar → 3×2 / 6-up, mobile 2 rows | 1 rule | Removes 700px of yellow on mobile |
| 6 | Fix grid item counts (guides, profiles, reviews) | CSS | Removes 3 orphan holes |
| 7 | Nav: 7 primary + menu | markup | −100px sticky header |
| 8 | Photos in project profiles | assets | Biggest perceived-quality gain |
| 9 | Hero copy to 2 lines | copy | CTA above the fold on mobile |
| 10 | Logo lockup, H1 break, estimator compaction | CSS/copy | Polish |

---

## Captures

Session screenshots (desktop 1296/1440, iPhone 13 390) were taken against the live `workers.dev` host and reviewed section by section: hero, guides, services, why, testimonials, estimator, quote form, FAQ, profiles, reviews, trust bar, founder, guides-2, footer, plus the open mobile menu. Key measurements are quoted inline above so the report stands without the images.
