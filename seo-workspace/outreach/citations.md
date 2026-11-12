# AMY Electric — Citation Drafts (Staged, Owner-Submitted)

*Staged 2026-11-08 · source: `scripts/site_data.py` BUSINESS · roadmap 2.5 / SEO-STRATEGY.md Phase 3.3 · status: **DRAFT — do not submit until owner reviews NAP + photos***
*Previous blockers: Yelp / Apple Maps / Bing Places were BLOCKED as owner-submitted in `IMPLEMENTATION-ROADMAP.md:2.5`. These drafts queue the work; submission still requires the owner's Google/Business account.*

> **Rule:** every field below is copied verbatim from the repo canonical. If any field is wrong on a live listing, paste the *existing wrong value* into the correction request — never guess.

---

## Canonical NAP block (copy-paste exact — every citation must match)

```
Business name:  AMY Electric
Legal name:     AMY Electric
Street:         20628 Londelius St
City / State / ZIP:  Winnetka, CA 91306
Country:        US
Phone (display): (818) 302-5614
Phone (machine): +1-818-302-5614
Email:          info@amyelectric.com
Website:        https://amyelectric.com
Google Maps:    https://maps.app.goo.gl/nzyuaFkAMGZdbbuj6
Geo:            34.22281, -118.58241
Hours:          Mon–Fri 07:00–17:00 · Sat 08:00–14:00 · Sun Closed
License:        C-10 #981578 (CSLB)
Certification:  EVITP #4051604
Founded:        2012
Price range:    $$
Image (OG):     https://amyelectric.com/img/og-home.jpg
Hero:           https://amyelectric.com/img/hero-electrician.jpg
```

**Description (use verbatim; 1–2 sentences depending on field limit):**
> Licensed C-10 electrical contractor in Los Angeles specializing in EV charger installation, panel upgrades, electrical repairs, and commercial electrical work. C-10 #981578 · EVITP #4051604 — serving Greater Los Angeles from Winnetka since 2012.

**Long description (where the platform allows 400–750 chars):**
> AMY Electric is a licensed C-10 electrical contractor (CSLB #981578) and EVITP-certified (EVITP #4051604) serving Greater Los Angeles from Winnetka. We install Level 2 EV chargers (Tesla, NEMA, hardwired), perform 200A panel upgrades, whole-home rewiring, lighting, and commercial electrical — including permit coordination and utility paperwork. Licensed & insured. Free estimates at https://amyelectric.com/book.

**Categories (apply in this priority order):**
1. Electrician *(primary everywhere)*
2. EV Charger Installer / Electric Vehicle Charging Station Contractor *(secondary where available)*
3. Electrical Installation Service / Lighting Contractor *(tertiary)*

**sameAs to include where the platform has a "links" or "social" field:**
- https://www.yelp.com/biz/amy-electric-los-angeles
- https://g.page/r/CVdK9ZAvNBrZEAI/review
- https://maps.app.goo.gl/WTNSkHRUgULPBHpc9
- https://maps.app.goo.gl/nzyuaFkAMGZdbbuj6

**Photos to upload (pick 3 — all captioned, all in `img/gallery/`, 4 variants each):**
- `gallery-commercial-garage-ev-charger` — EV charger in commercial garage (proves EVITP work) — `img/gallery/gallery-commercial-garage-ev-charger-1200w.webp`
- `gallery-panel-subpanel-labeled` — labeled subpanel in framed space, Sherman Oaks — `img/gallery/gallery-panel-subpanel-labeled-1200w.webp`
- `gallery-panel-siemens-stucco` — Siemens panel on stucco, Los Angeles — `img/gallery/gallery-panel-siemens-stucco-1200w.webp`
- *Alternates if a platform wants a 4th:* `gallery-commercial-switchgear-200a`, `gallery-roughin-framing-conduit`, `photo-20231010-01-v2` (Siemens panel interior + surge device)

> Photo hygiene: every gallery photo has been through `redact-photos.py` (face/text/license-plate redaction). Do not upload raw from `/home/amram/Pictures/Electric Work/`.

---

## 1) Yelp — https://biz.yelp.com

**Submit here:** https://biz.yelp.com — *Claim or Add Business* → search "AMY Electric, Winnetka, CA" → claim existing or create new.
**Reference (already in schema `sameAs`):** https://www.yelp.com/biz/amy-electric-los-angeles — verify this is the correct listing before creating a duplicate. If it resolves to AMY, **claim** it; do not create a second.

| Field | Value |
|---|---|
| Business name | AMY Electric |
| Address | 20628 Londelius St, Winnetka, CA 91306 |
| Phone | (818) 302-5614 |
| Website | https://amyelectric.com |
| Hours | Mon–Fri 7:00 AM – 5:00 PM, Sat 8:00 AM – 2:00 PM, Sun Closed |
| Categories | Electricians, EV Charging Station Contractors *(if available)* |
| Licenses | C-10 #981578 · EVITP #4051604 (add to "Licenses" / "Credentials" field) |
| Description | Use *Description* block above (Yelp truncates ~500 chars; use the short 2-sentence version) |
| Photos | Upload the 3 slugs listed above |
| Attributes | Licensed, Insured, Free Estimates, EVITP Certified, Commercial + Residential |
| Service area | Greater Los Angeles (Yelp uses address + radius; set 25–30 mi) |

**After claiming:** request the Yelp review link and add it to `sameAs` in `scripts/site_data.py` if Yelp issues a new canonical URL. Keep `reviewCount` canonical at 87 in `site_data.py` (GBP count) — Yelp's count is separate.

---

## 2) Apple Maps — Apple Business Connect — https://mapsconnect.apple.com (now https://businessconnect.apple.com)

**Submit here:** https://businessconnect.apple.com — *Add a new business* → search AMY Electric, Winnetka, CA → claim/add. Also reachable via https://mapsconnect.apple.com (redirects).
**Why it matters:** Siri, Spotlight, and iPhone Maps pull from this — iOS users never see GBP directly.

| Field | Value |
|---|---|
| Business name | AMY Electric |
| Address | 20628 Londelius St, Winnetka, CA 91306 |
| Phone | (818) 302-5614 |
| Website | https://amyelectric.com |
| Hours | Mon–Fri 07:00–17:00, Sat 08:00–14:00, Sun Closed (Apple uses structured hours + "Closed" for Sunday) |
| Categories | Electrician *(primary)*, Electric Vehicle Charging Station Contractor *(add if available)* |
| Description | Use *Long description* block (Apple allows ~500+ chars) |
| Photos | Upload the 3 slugs above (Apple crops to 1:1 and 16:9 — pick the 1200w variant, center-crop safe) |
| Logo | https://amyelectric.com/img/og-home.jpg |
| Place Card / Showcases | Add one Showcase: "EV Charger Installation — Tesla & NEMA" linking to https://amyelectric.com/ev-charger-installation |

**Verification:** Apple verifies by phone or document upload. Have CSLB license PDF + EVITP cert ready.

---

## 3) Bing Places — https://www.bingplaces.com

**Submit here:** https://www.bingplaces.com — *Add new business* or **Import from Google Business Profile** (one-click sync if GBP is already claimed).
**Why it matters:** Bing powers DuckDuckGo, Yahoo, ChatGPT browsing, and Windows search. Bing Places syncs from GBP so any GBP fix propagates — but a direct Bing claim is still needed for verification.

| Field | Value |
|---|---|
| Business name | AMY Electric |
| Address | 20628 Londelius St, Winnetka, CA 91306 |
| Phone | (818) 302-5614 |
| Website | https://amyelectric.com |
| Hours | Mon–Fri 7:00 AM – 5:00 PM, Sat 8:00 AM – 2:00 PM, Sun Closed (Bing uses the same structured-hours model as GBP) |
| Categories | Electrician *(primary)*, Electric Vehicle Charging Station Contractor |
| Description | Use *Long description* block |
| Photos | Upload the 3 slugs above |
| Service area | Greater Los Angeles — add the same 16 cities used in GBP: Los Angeles, Sherman Oaks, Studio City, Encino, Woodland Hills, Burbank, Glendale, Pasadena, North Hollywood, Hollywood, Beverly Hills, West LA, Santa Monica, Calabasas, Van Nuys, Culver City |
| Social links | Add sameAs URLs where Bing has a links field |

**Fast path if GBP is live:** use *Import from Google* at https://www.bingplaces.com → review imported NAP/hours/photos before publishing — Bing's import sometimes drops secondary categories and truncates photos.

---

## 4) BuildZoom — Reference (already exists, claim it) — https://www.buildzoom.com/contractor/a-m-y-electric

**Reference:** https://www.buildzoom.com/contractor/a-m-y-electric — page already exists for AMY Electric. **Do not create a new listing — claim this one.**
**Submit/claim here:** open the URL → *Claim this business* / *Are you this contractor?* → verify via phone (818) 302-5614 or license #981578.

| Field | Verify / correct to |
|---|---|
| Business name | AMY Electric |
| Address | 20628 Londelius St, Winnetka, CA 91306 |
| Phone | (818) 302-5614 |
| Website | https://amyelectric.com (some BuildZoom pages link to a generic — ensure it points to amyelectric.com) |
| License | C-10 #981578 — confirm BuildZoom shows Active (cross-check at https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=981578) |
| Certifications | Add EVITP #4051604 in the description/credentials area if the form allows free text |
| Categories | Electrical, EV Charger Installation, Panel Upgrade |
| Description | Use *Description* block above |
| Photos | Upload the 3 slugs above (BuildZoom compresses aggressively — upload 1200w WebP, it will transcode) |
| Service area | Greater Los Angeles |

**Note:** BuildZoom is a **reference/claim** — it already ranks for `AMY Electric` branded searches. Claiming it fixes NAP drift and unlocks the "Contact" CTA. No new URL is created.

---

## Tier 2 — Local Chambers (optional, after the 4 core are live)

Same NAP block for every chamber — copy the canonical block at the top verbatim. Chambers are **P2** per SEO-STRATEGY.md Phase 3.3; pursue after Yelp/Apple/Bing/BuildZoom are verified.

### Winnetka Chamber of Commerce

- **Prospect:** Winnetka Chamber of Commerce (Valley) — AMY's home ZIP 91306.
- **Why:** home-city chamber is the most defensible citation; also the address on the site.
- **Submit here:** search "Winnetka Chamber of Commerce" + "member directory" — verify current URL before submitting (chamber sites migrate). If Winnetka has no standalone chamber, use the **Canoga Park–Winnetka Chamber** or the **Valley Industry & Commerce Association (VICA)** as the valley-wide equivalent.
- **Category:** Electrical Contractor / Electrician
- **Pitch (1 sentence):** "Winnetka-based C-10 electrician (CSLB #981578, EVITP #4051604) serving the Valley — requesting a member directory listing."

### Sherman Oaks Chamber of Commerce

- **Prospect:** Sherman Oaks Chamber of Commerce — https://shermanoakschamber.org
- **Why:** Sherman Oaks is in the 16-city GBP service area and has a `city-sherman-oaks.html` page with LADWP territory.
- **Submit here:** https://shermanoakschamber.org → Membership → Join / Business Directory.
- **Category:** Electrical Contractor / Electrician
- **Pitch:** "Sherman Oaks–serving EVITP-certified electrician requesting a directory listing — we serve Sherman Oaks from Winnetka and carry a Sherman Oaks city page at https://amyelectric.com/city-sherman-oaks."

### Encino Chamber of Commerce

- **Prospect:** Encino Chamber of Commerce — https://encinochamber.org
- **Why:** Encino is LADWP territory with a `city-encino.html` page; Encino is contiguous to Winnetka/Sherman Oaks.
- **Submit here:** https://encinochamber.org → Membership / Directory.
- **Category:** Electrical Contractor / Electrician
- **Pitch:** same as Sherman Oaks, swapped city.

**Chamber hygiene:**
- All three chambers charge dues — treat as **paid citation + business development**, label as member/sponsor if the listing is marked sponsored (per `prospects.md` guardrails).
- After any chamber listing goes live, add its URL to `sameAs` in `scripts/site_data.py` only if the listing is public and indexable.
- Confirm each chamber's current domain before paying — chamber domains change; the URLs above are directional.

---

## Submission checklist (owner)

- [ ] Verify canonical NAP block against the live site footer + `scripts/site_data.py` BUSINESS before submitting anything.
- [ ] Yelp: claim https://www.yelp.com/biz/amy-electric-los-angeles — do not duplicate.
- [ ] Apple Business Connect: create/claim at https://businessconnect.apple.com — verify via phone/document.
- [ ] Bing Places: https://www.bingplaces.com — prefer Import from GBP if GBP is already live.
- [ ] BuildZoom: claim https://www.buildzoom.com/contractor/a-m-y-electric — do not create a new page.
- [ ] Upload the same 3 gallery photos to each platform (1200w WebP).
- [ ] After each platform verifies, record the live listing URL and paste it into `sameAs` in `scripts/site_data.py` (then run `schema-tool.py validate` + `audit-site.py`).
- [ ] Tier 2 chambers: only after the 4 core are verified; verify each chamber's current membership URL before paying.

## Sources

- `scripts/site_data.py` BUSINESS — name, address, phone, email, url, description, sameAs, hasMap, geo, openingHours, credentials, priceRange [repo: scripts/site_data.py]
- `seo-workspace/outreach/local-seo-gbp-action-plan.md` — GBP NAP/hours/categories/service-area framing [repo: seo-workspace/outreach/local-seo-gbp-action-plan.md]
- `seo-workspace/outreach/prospects.md` — prior outreach matrix, guardrails, paid-vs-free discipline [repo: seo-workspace/outreach/prospects.md]
- `seo-workspace/outreach/templates.md` — prior draft shape ([confirm] tags, directory inclusion) [repo: seo-workspace/outreach/templates.md]
- `SEO-STRATEGY.md` §5–§6 — Phase 2.5 / Phase 3.3 context, chamber list (Winnetka, Sherman Oaks, Encino) + EVITP + gallery asset [repo: SEO-STRATEGY.md]
- `IMPLEMENTATION-ROADMAP.md` — 2.5 BLOCKED status that this file queues [repo: seo-workspace/IMPLEMENTATION-ROADMAP.md]
- `scripts/photo-manifest.csv` + `img/gallery/` — 545 photos ×4 variants; 3 suggested slugs verified on disk: gallery-commercial-garage-ev-charger, gallery-panel-subpanel-labeled, gallery-panel-siemens-stucco [repo: scripts/photo-manifest.csv, img/gallery/]
