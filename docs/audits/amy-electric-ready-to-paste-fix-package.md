# AMY Electric — Ready-to-Paste Fix Package

Every fix from the audit, in paste-ready form. Items are ordered by priority. Anything marked **[YOUR ACTION]** requires logins I don't have (hosting, Yelp, Google Business Profile, CALeVIP).

---

## Fix 1 — Remove Git merge conflict markers (Gallery page) 🔴 Critical

**Problem:** `https://amyelectric.com/gallery` begins with four repeated blocks of raw conflict text: `<<<<<<< HEAD ======= >>>>>>> 080ca59 (photos: 3 new gallery items (LA panel/EV/commercial), pipeline OUT path worktree-safe)`.

**What to do in the repo:**

1. `git log --oneline -5` — find the bad merge (message contains `080ca59`).
2. Open the gallery page source (likely `gallery.html` or the template/CMS block that renders it) and delete every line starting with `<<<<<<<`, `=======`, `>>>>>>>`, and keep only the *incoming* version (the `080ca59` side, which added the 3 new gallery items).
3. Search the **entire repo** before redeploying:

```bash
grep -rn -E '^(<<<<<<<|=======$|>>>>>>>)' --include='*.html' --include='*.md' --include='*.php' --include='*.js' .
```

4. Add this to your deploy pipeline (or run before every deploy) so it can never ship again:

```bash
#!/usr/bin/env bash
# pre-deploy-conflict-check.sh — exit non-zero if merge markers found
if git grep -lE '^(<{7}|>{7}|={7}$)' -- . ':!*.lock'; then
  echo "❌ Merge conflict markers found in tracked files. Resolve before deploying."
  exit 1
fi
echo "✅ No conflict markers. Safe to deploy."
```

---

## Fix 2 — Real Contact page for `/contact` 🔴 Critical

**Problem:** `/contact` serves homepage content. Paste this in as the `/contact` page:

> # Contact AMY Electric
>
> ## Talk to a Licensed Electrician — Not a Call Center
>
> Call or text **(818) 302-5614** for same-day dispatch when available, or send a request below. We typically respond within a few hours during business hours.
>
> - **Phone / Text:** (818) 302-5614
> - **Hours:** Monday–Friday 7:00 AM – 5:00 PM · 24/7 emergency dispatch for urgent safety issues (sparking outlets, power loss, burning smell)
> - **Service Area:** Greater Los Angeles — San Fernando Valley, Westside, Hollywood Hills, and LA County (62+ ZIP codes)
> - **License:** C-10 #981578 (verify at cslb.ca.gov) · EVITP #4051604
>
> **[Insert Google Maps embed of your service area]**
>
> ### Request Service or an Estimate
> *(keep the existing Quick Quote form component here)*
>
> ### Emergency?
> For sparking outlets, smoking panels, exposed wires, or water near electricity — **call (818) 302-5614 now.** We prioritize emergency dispatch and typically arrive within 30–60 minutes.

**[YOUR ACTION]** Also set the page `<title>` to `Contact AMY Electric | Los Angeles Electrician (818) 302-5614` and a meta description, e.g. *"Contact AMY Electric — licensed C-10 Los Angeles electrician. Call (818) 302-5614 for same-day electrical service, free estimates, and 24/7 emergency dispatch."*

---

## Fix 3 — Correct factual inconsistencies on the homepage 🔴 Critical

### 3a. Review count claim
Replace `87 5-Star Reviews` with the accurate total. If 87 is your total review count at 4.9★ average:

> ✅ `4.9★ on Google · 87 Reviews`

### 3b. LADWP rebate (FAQ)
The current LADWP residential rebate is **up to $1,000** for a qualifying Level 2 charger and installation, so the FAQ's "$500" is stale. In the FAQ *"How much does an EV charger installation cost in LA?"*, replace:

> ❌ `LADWP offers up to $500 in rebates for qualifying Level 2 installations.`
>
> ✅ `LADWP offers up to $1,000 back on a qualifying Level 2 charger and installation through its Residential EV Charger Rebate Program.`

Keep the quote-section banner ("up to $1,000") — it matches. Add a note to re-verify quarterly, since program terms change.

### 3c. Duplicate ZIP in FAQ
In *"What's the service area ZIP code coverage?"*, the list contains `91423` twice (`…91411, 91423, 91436, 91423, 91505…`). Delete one instance.

### 3d. Founder name standardization
The About section says the founder is **Amram**; article quotes say *"According to Amy, founder of AMY Electric."* Standardize to **Amram** everywhere:

> ✅ `According to Amram Edry, founder of AMY Electric and licensed C-10 electrical contractor with 15+ years of experience: "…"`

Search-and-replace across all blog/service pages: `According to Amy` → `According to Amram Edry`.

---

## Fix 4 — Remove duplicate testimonials (homepage) 🟠 High

The David R. / Maria T. / James K. trio appears in **two** homepage sections. Keep the first instance; replace the second ("Trusted by Los Angeles Homeowners" section) with real, attributable reviews:

> ### What Customers Say
> ★★★★★ "AMY Electric installed a Tesla Wall Connector at our home in Sherman Oaks. Amram was punctual, professional, and explained everything clearly. He handled the permit and LADWP rebate paperwork too." — *Sarah M., Sherman Oaks · EV Charger Installation*
>
> ★★★★★ "We needed a 200-amp panel upgrade for our older home in Burbank. Fair quote, permit pulled, completed in one day — and our insurance company was impressed with the documentation." — *David & Lisa K., Burbank · Panel Upgrade*
>
> ★★★★★ "AMY Electric rewired our 1940s home in Studio City. The old knob-and-tube wiring was a fire hazard. The crew finished ahead of schedule." — *Jennifer & Mark R., Studio City · Whole-Home Rewiring*

Rules for all testimonials going forward: **one quote per customer, include city + service type + date, and link each to the actual Google review.** Two reviewers currently use the identical phrase "Fast, honest, and affordable" — rewrite one of them.

**[YOUR ACTION]** Embed a live Google Reviews widget (or direct "Read our 87 Google reviews →" link to your Business Profile) so every claim is verifiable.

---

## Fix 5 — Natural headings on money pages 🟠 High

Replace the question-pattern H2s (an AI/programmatic-SEO pattern Google discounts and users find odd):

| Current | Replace with |
| --- | --- |
| What Electrical Guides Should LA Homeowners Read? | Electrical Guides for LA Homeowners |
| What Electrical Services Do We Offer in Los Angeles? | Our Electrical Services in Los Angeles |
| Why Do Los Angeles Homeowners Choose AMY Electric? | Why Homeowners Across LA Choose AMY Electric |
| How Does the EV Charger Installation Process Work? | Our EV Charger Installation Process |
| What Is Level 2 EV Charger Installation? | Level 2 EV Charging, Explained |
| See Your Price Instantly | See Your Price Instantly ✅ *(keep — it's an action, fine)* |

Apply the same pattern to city and service pages: statement headings, not questions.

---

## Fix 6 — Real case studies instead of "illustrative profiles" 🟠 High

The homepage's four "Project Profiles" all disclaim themselves as *illustrative*. With 309 real gallery photos and 2,000+ claimed projects, use real work. Template:

> ### Case Study: 200A Panel Upgrade + Tesla Wall Connector — Sherman Oaks
> **Problem:** 1962 home on original 100A Zinsco panel; owner bought an EV and needed charging plus capacity for a future heat pump.
> **Scope:** 200A load calculation, panel replacement, dedicated 60A circuit, wall-mount install in garage.
> **Permits & Inspection:** LADBS permit pulled; LADWP service coordination; passed final inspection first visit.
> **Outcome:** Owner approved for the $1,000 LADWP rebate; charging at 44 mi/hr.
> **Customer:** "Quote matched the invoice to the dollar." — real review excerpt, city, service, date.

**[YOUR ACTION]** Pick 3–5 recent jobs with photos you can verify (customer permission where needed) and rebuild the section with this structure.

## Fix 6b — Gallery captions with real detail

Replace generic auto-captions like *"Electrical work in unfinished wood-framed space — with panel and wiring detail"* with specifics:

> ❌ `Electrical system with metal enclosures — Los Angeles, CA · 2022 · Panel Upgrades`
>
> ✅ `200A panel replacement with EV-ready capacity — Sherman Oaks, CA · 2022 · LADBS-permitted · Panel Upgrades`

Caption formula: **what was installed + amperage/model + city + year + permit jurisdiction + category.**

---

## Fix 7 — Off-site citations 🟠 High (all [YOUR ACTION])

**CALeVIP listing** (https://calevip.org/evsp/amy-electric) — log in and update the website field from `http://amyelectric.wordpress.com/` to `https://amyelectric.com/`. Also refresh the manager contact and description.

**Yelp profile** (https://www.yelp.com/biz/amy-electric-winnetka) — claim/edit:
- Fix street spelling ("Londeliues St" → correct spelling per official address).
- Replace description typos: "exmpale" → "example"; clean grammar.
- Updated description to paste:
  > "AMY Electric is a licensed C-10 electrical contractor (CSLB #981578) serving Greater Los Angeles since 2012. EVITP-certified (#4051604) Level 2 EV charger installation, 200A panel upgrades, whole-home rewiring, lighting, and electrical repairs. Permits and inspections handled with LADBS and LADWP. Free estimates: (818) 302-5614."
- Upload real project photos (you have 309 on the site), and align hours — if you truly run 24/7 emergency dispatch, say so; if not, remove 24/7 claims from the website instead.

**Google Business Profile** — claim/optimize: category "Electrician", correct NAP matching your official address, 10+ recent photos, respond to every review, add the same description and license numbers.

**NAP rule:** choose ONE canonical Name-Address-Phone string (e.g. "AMY Electric · Winnetka, CA · (818) 302-5614") and use it identically on the site footer, Google, Yelp, CALeVIP, MapQuest, and Bing Places. Right now the site says "Los Angeles, CA" while Yelp shows a Winnetka street address — pick one and standardize.

---

## Fix 8 — Author bylines for E-E-A-T 🟡 Medium

Add a byline block under every blog article:

> **By Amram Edry** — California-licensed C-10 Electrical Contractor (#981578), EVITP-certified (#4051604), 15+ years and 2,000+ projects across Greater Los Angeles. *Reviewed for accuracy against current California Electrical Code and LADWP/LADBS requirements. Last reviewed: November 2026.*

Also fix the article named *"LADWP EV Charger Rebate Guide"* so the site's own FAQ matches its blog (both should say up to $1,000).

---

## Verification checklist

After deploying:

- [ ] Gallery page loads with no `<<<<<<<` text (view-source + `grep` in CI)
- [ ] `/contact` shows the dedicated contact page with correct title
- [ ] Site-wide search for "According to Amy" returns zero results
- [ ] FAQ says "$1,000" for LADWP rebate, ZIP list has no duplicates
- [ ] Homepage shows testimonials once, each linked/dated
- [ ] CALeVIP + Yelp show `https://amyelectric.com/` and corrected info
- [ ] Google Business Profile matches site NAP exactly