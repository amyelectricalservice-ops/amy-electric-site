# AMY Electric — SEO Workspace

This folder is the working source of truth for SEO notes, exports, briefs, outreach, and reports for `https://amyelectric.com`.

## Current priorities

1. Increase qualified calls and estimate requests.
2. Improve Greater Los Angeles local visibility and service-page rankings.
3. Establish reliable measurement before buying additional research or publishing more pages.

## Site context

- Static HTML site on Cloudflare Workers + Assets.
- English-language United States market focused on Greater Los Angeles.
- Core commercial topics: EV charger installation, panel upgrades, emergency electrical repair, rewiring, commercial electrical, lighting, and safety.
- Existing page groups include service pages, city pages, geo-service pages, blog content, and illustrative case studies.

## Next input needed

Export Google Search Console query and page reports and place them in `gsc/`, using names such as:

- `queries-last-3-months.csv`
- `pages-last-3-months.csv`
- `queries-last-16-months.csv`
- `pages-last-16-months.csv`

Use those exports to prioritize page improvements and keyword clustering. Do not treat older reports in this folder as live performance data unless their date and source are confirmed.

---

# Historical SEO Audit Report

**Date**: 2026-06-03
**Tool**: OpenSEO Agent Skills + Lighthouse + Manual Analysis
**Site**: https://amyelectric.com (42 pages)

---

## Scores

| Area | Score | Notes |
|---|---|---|
| Lighthouse Desktop | **96** | Performance |
| Lighthouse Mobile | **73** | Performance (GA4 overhead) |
| Accessibility | **100/100** | Perfect |
| Best Practices | **77** | Cloudflare challenge script warnings (not our code) |
| SEO | **100** | |

## Critical Issues

### 1. HTTP → HTTPS redirect broken
`http://amyelectric.com/` serves content directly over HTTP. Fix: Enable "Always Use HTTPS" in Cloudflare dashboard → SSL/TLS.

### 2. www.amyelectric.com DNS doesn't resolve
Returns NXDOMAIN. Add a CNAME record for `www` → `amyelectric.com` in Cloudflare DNS, then configure the Bulk Redirect rule.

### 3. City pages missing Electrician schema
All 16 city pages only have FAQPage JSON-LD. They need `@type: Electrician` with `areaServed` (city name, postal codes). This is the biggest local SEO gap.

### 4. Canonical/redirect mismatch
Canonical tags point to `.html` URLs, but `.html` URLs 307-redirect to clean URLs. Google gets conflicting signals. Fix: Update all canonical tags to clean URLs (no `.html`).

### 5. 307 redirects should be 301
All `.html` → clean URL redirects use temporary (307) redirects. Change to permanent (301).

## High Priority

### 6. Title tags too short (4 pages)
| Page | Current | Suggested |
|---|---|---|
| Homepage (40 chars) | "Electrician Los Angeles \| AMY Electric" | "Electrician Los Angeles \| Panel Upgrades, EV Chargers & Repairs" |
| City LA (42 chars) | "Electrician in Los Angeles \| AMY Electric" | "Los Angeles Electrician \| Panel Upgrades & EV Charger Installer" |
| Burbank (43 chars) | "Electrician in Burbank \| AMY Electric" | "Burbank Electrician \| Panel Upgrades & EV Charger Installer" |
| Testimonials (38 chars) | "AMY Electric Reviews \| Los Angeles" | "AMY Electric Reviews \| Los Angeles Electrical Contractor Testimonials" |

### 7. Meta descriptions too short (2 pages)
- **Testimonials**: 77 chars → expand to 150-160 with CTA
- **Blog post (EV charging benefits)**: 76 chars → expand

### 8. No `<img>` tags on any page
All images are CSS backgrounds. Add `<img>` tags with `alt` text and `loading="lazy"` for accessibility, SEO, and Core Web Vitals credit.

### 9. H1 missing primary keyword (homepage)
Current: "Powering LA With Safe, Code-Perfect Electrical Work"
Suggestion: "Los Angeles Electrician — Powering LA With Safe, Code-Perfect Electrical Work"

### 10. USPs missing from homepage meta description
Add a CTA like "Call (818) 302-5614 for a free estimate."

## Medium Priority

### 11. Copyright year 2025 → 2026
### 12. Remove "TO ACTIVATE" placeholder comments in production HTML
### 13. Footer broken HTML (3 `<a>` tags in 1 `<li>`)
### 14. Emergency pages missing Service/Electrician schema
### 15. Burbank FAQ references LADBS/LADWP → should reference Burbank's own departments

## Competitive Landscape

| vs Branover (255 pages) | AMY (42 pages) |
|---|---|
| 170 blog posts | 10 blog posts |
| 25+ city+service pages | 0 city+service pages (have 16 city pages only) |
| Yoast/Rank Math auto schema | Manual schema |
| Geo sitemap | No geo sitemap |
| Case studies/portfolio | No case studies |

## Recommended Next Steps (for you)

These need your account access:

1. **Google Business Profile**: Claim and verify at business.google.com
2. **Directory Citations**: NAP consistency on BBB, Angie's List, HomeAdvisor, Yelp, Nextdoor
3. **GoHighLevel**: Provide the form endpoint URL for lead capture
4. **Cloudflare Dashboard**: Enable "Always Use HTTPS", add www DNS record
5. **Google Search Console**: Export query/page CSVs for keyword research

## What I Can Fix Now

- [ ] Update canonical tags to clean URLs (all ~42 pages)
- [ ] Update title tags on 4+ short pages
- [ ] Expand meta descriptions on 2 short pages
- [ ] Update copyright 2025 → 2026 (all pages)
- [ ] Remove "TO ACTIVATE" placeholder comments (all pages)
- [ ] Add Electrician schema to city pages (16 pages)
- [ ] Add Service schema to emergency pages
- [ ] Fix footer broken HTML
- [ ] Fix Burbank FAQ references

Want me to start on the fixable items?
