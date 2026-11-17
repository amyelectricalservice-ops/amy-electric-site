# Month 3 City Expansion Plan

This plan defines the next eight local landing pages for AMY Electric. It is a planning document, not a claim that AMY Electric has completed work in every listed city. City pages should be published only after the copy is reviewed for service availability, jurisdiction-specific permitting, and factual accuracy.

## Target cities and page briefs

| City | Recommended slug | Page title | Primary local intent | Secondary local intents | Internal-link targets |
|---|---|---|---|---|---|
| Long Beach | `city-long-beach.html` | Electrician in Long Beach, CA \| AMY Electric | licensed electrician Long Beach | panel upgrade, EV charger installation, electrical repair | `/panel-upgrade`, `/ev-charger-installation`, `/electrical-repair`, `/service-areas.html` |
| Torrance | `city-torrance.html` | Electrician in Torrance, CA \| AMY Electric | electrician Torrance CA | EV charger, electrical panel upgrade, lighting | `/ev-charger-installation`, `/panel-upgrade`, `/lighting-installation`, `/service-areas.html` |
| Redondo Beach | `city-redondo-beach.html` | Electrician in Redondo Beach, CA \| AMY Electric | electrician Redondo Beach | EV charger, panel upgrade, urgent repair | `/ev-charger-installation`, `/panel-upgrade`, `/electrical-repair`, `/service-areas.html` |
| Downey | `city-downey.html` | Electrician in Downey, CA \| AMY Electric | electrician Downey CA | electrical repair, panel upgrade, rewiring | `/electrical-repair`, `/panel-upgrade`, `/whole-home-rewiring`, `/service-areas.html` |
| Alhambra | `city-alhambra.html` | Electrician in Alhambra, CA \| AMY Electric | electrician Alhambra CA | panel upgrade, EV charger, older-home rewiring | `/panel-upgrade`, `/ev-charger-installation`, `/whole-home-rewiring`, `/service-areas.html` |
| Bellflower | `city-bellflower.html` | Electrician in Bellflower, CA \| AMY Electric | electrician Bellflower CA | electrical repair, EV charger, safety inspection | `/electrical-repair`, `/ev-charger-installation`, `/electrical-safety-inspections`, `/service-areas.html` |
| Santa Clarita | `city-santa-clarita.html` | Electrician in Santa Clarita, CA \| AMY Electric | electrician Santa Clarita | EV charger, panel upgrade, generator transfer switch | `/ev-charger-installation`, `/panel-upgrade`, `/generator-transfer-switch`, `/service-areas.html` |
| Inglewood | `city-inglewood.html` | Electrician in Inglewood, CA \| AMY Electric | electrician Inglewood CA | panel upgrade, EV charger, commercial electrical | `/panel-upgrade`, `/ev-charger-installation`, `/commercial-electrical`, `/service-areas.html` |

## Production notes

- Use the existing city-page structure and shared navigation; do not clone unsupported reviews, project stories, ZIP-code lists, response times, or city-specific code claims.
- Confirm the actual service area before publication. Use “serving” language only where AMY Electric accepts jobs.
- Keep one clear city intent in the title, H1, description, introductory copy, and Electrician/LocalBusiness `areaServed`.
- Link to the relevant root service pages and to `service-areas.html`; add a nearby-city link only when it is useful and factually appropriate.

## Quality checklist

- [ ] Unique title (about 50–60 characters) and description (about 140–160 characters).
- [ ] Canonical URL, Open Graph, and Twitter metadata match the final slug.
- [ ] One descriptive H1 and scannable service sections with no boilerplate city substitutions.
- [ ] Accurate LocalBusiness/Electrician JSON-LD with `areaServed`; no invented address, ratings, prices, or guarantees.
- [ ] FAQPage answers match visible FAQs and avoid unsupported city-specific claims.
- [ ] BreadcrumbList follows Home → Service Areas → City.
- [ ] Links to `service-areas.html` plus at least one relevant service page resolve.
- [ ] Phone CTA uses `tel:18183025614` and estimate CTA points to the real form.
- [ ] Images have meaningful alt text and lazy loading where appropriate.
- [ ] Validate HTML, JSON-LD, links, mobile layout, and sitemap entry before deployment.
