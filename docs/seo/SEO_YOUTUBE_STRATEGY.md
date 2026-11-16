# AMY Electric — Month 6 YouTube SEO Strategy

**Purpose:** Build searchable, citation-friendly video assets around EV charging, electrical safety, panel capacity, emergency response, and Greater Los Angeles service intent. Publish one video every 2–3 weeks, then embed or link it from the closest relevant page.

## 12-video plan

| # | Working title and target intent | Key talking points (3–5) | CTA | Thumbnail / description direction |
|---|---|---|---|---|
| 1 | **EV Charger Installation in Los Angeles: What Homeowners Need to Know** — commercial investigation | Level 1 vs. Level 2; load calculation; permits and inspection; conduit and panel location; realistic project steps | Call **(818) 302-5614** for an EV charger assessment | Thumbnail: charger + “Ready for Home Charging?” Description: LA-specific installation checklist, links to `/ev-charger-installation.html` and `/#estimate`. |
| 2 | **Tesla Wall Connector vs. Plug-In EV Charger: Which Is Safer?** — comparison | Hardwired vs. receptacle; amperage; weather protection; convenience; when a dedicated circuit is required | Request a code-compliant charger quote | Thumbnail: split-screen connectors + “Hardwired or Plug-In?” Link `/tesla-charger-installation.html` and comparison article. |
| 3 | **Does Your Electrical Panel Need an Upgrade for an EV Charger?** — problem solving | Main-service rating; available capacity; tandem breakers; signs of overload; when a load calculation is needed | Book a panel and charger evaluation | Thumbnail: panel + EV icon + “Can Your Panel Handle It?” Link `/panel-upgrade.html`. |
| 4 | **5 Signs Your Los Angeles Electrical Panel Is Unsafe** — informational/high intent | Heat or discoloration; buzzing; repeated trips; obsolete Federal Pacific/Zinsco equipment; flicker and corrosion | Turn off unsafe equipment and call a licensed electrician | Thumbnail: warning triangle over panel + “5 Red Flags” | Link `/panel-upgrade.html` and `/federal-pacific-zinsco-panel-replacement.html`. |
| 5 | **100-Amp vs. 200-Amp Panel Upgrade: How to Choose** — comparison | Service capacity; HVAC/EV/ADU demand; permitting; future-proofing; why an electrician calculates rather than guesses | Get a documented capacity recommendation | Thumbnail: “100A vs 200A” with two panel labels | Link `/panel-100a-vs-200a.html` and `/panel-upgrade.html`. |
| 6 | **Emergency Electrical Repair: What to Do Before the Electrician Arrives** — urgent informational | Burning smell/smoke; safe main shutoff; water and electricity; downed lines; when to call 911/fire department | If there is fire, smoke, or live utility damage, leave and call emergency services; otherwise call AMY | Thumbnail: “Electrical Emergency?” with phone number | Link `/emergency-electrician.html` and `/emergency-electrical-repair-what-to-do.html`. |
| 7 | **Why Does My Breaker Keep Tripping? Safe Diagnosis for Homeowners** — troubleshooting | Overload vs. short circuit vs. ground fault; unplugging loads; GFCI reset; never upsizing a breaker; when to stop resetting | Schedule diagnosis instead of repeatedly resetting | Thumbnail: tripped breaker + “Don’t Keep Resetting” | Link `/breaker-tripping.html` and related guide. |
| 8 | **Electrical Safety Checklist for Older Los Angeles Homes** — informational/local | Knob-and-tube; ungrounded outlets; aluminum wiring; outdated panels; smoke/CO protection; inspection priorities | Arrange an older-home safety inspection | Thumbnail: older LA house + checklist | Link `/electrical-safety-inspections.html` and older-home blog guide. |
| 9 | **How Permits and Inspections Work for Electrical Projects in LA** — informational/compliance | When permits apply; LADBS/LADWP roles; plan and load information; inspection timing; why permits protect resale and safety | Ask AMY what your project requires before work starts | Thumbnail: permit + “Do I Need One?” | Link `/electrical-permit-cost-los-angeles.html` and `/ladwp-electrical-guide.html`. |
| 10 | **EV Charger Installation in Pasadena, Burbank, and the San Fernando Valley** — local transactional | Service-area examples; garage and driveway routing; panel constraints; city-specific permit questions; scheduling | Call for service in Greater LA and name your city | Thumbnail: LA map with charger pin | Link to the matching city/geo pages, e.g. `/ev-charger-installation-pasadena.html`. |
| 11 | **Behind the Job: A Code-Perfect Panel Upgrade in Los Angeles** — proof/E-E-A-T | Initial inspection; load calculation; equipment selection; labeling; testing and cleanup; customer handoff | See project photos and request an estimate | Thumbnail: before/after panel + “Job Walkthrough” | Link `/gallery.html`, `/testimonials.html`, and `/panel-upgrade.html`; use only consented, redacted footage. |
| 12 | **Electrical Fire Prevention: 10 Habits That Protect Your LA Home** — safety/local awareness | Extension-cord limits; hot outlets; overloaded strips; outdoor GFCI; dryer/EV circuits; smoke alarms; annual checks | Share the checklist and book an inspection if anything feels wrong | Thumbnail: “Prevent Electrical Fires” with 10 badge | Link `/blog/electrical-fire-prevention.html` and safety inspection page. |

## Production and publishing workflow

1. Record a clear licensed-electrician explanation; avoid diagnosing a viewer’s unseen installation.
2. Use a consistent opening: “AMY Electric serves Greater Los Angeles. I’m [name], and today…”
3. Add captions/transcript, chapters, location/service terms naturally, and a pinned CTA.
4. Link the relevant AMY page, phone number, and safety disclaimer in the description.
5. Embed videos only on pages where they answer the page’s primary question; do not create thin video pages.
6. Reuse each transcript as a short FAQ or internal-link opportunity, without duplicating the full transcript everywhere.

## VideoObject schema checklist

- [ ] `@context: https://schema.org` and `@type: VideoObject`
- [ ] Stable, canonical `name`, useful `description`, and `thumbnailUrl`
- [ ] `uploadDate` in ISO 8601; include `duration` when known
- [ ] Public `contentUrl` or `embedUrl` that Google can crawl
- [ ] `publisher` identifies AMY Electric and includes the site logo
- [ ] `author`/`creator` is accurate; do not invent credentials
- [ ] `potentialAction`/watch URL matches the actual video
- [ ] Video is visible on the page near the related copy and not hidden behind a click-only control
- [ ] Validate with Google Rich Results Test; keep schema synchronized after edits

**Measurement:** Track YouTube impressions, watch time, branded searches, referral clicks, calls/forms assisted by video, and indexed pages with video enhancements. No paid API or credential-dependent data is assumed in this plan.
