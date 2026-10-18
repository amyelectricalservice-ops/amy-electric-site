# `amy-electric-seo` — edge SEO wrapper

This Worker sits in front of `amy-electric-site` on production. Requests to
`amyelectric.com/*` hit this Worker, which forwards them to the origin Worker
unchanged. `amy-electric-site` owns every page, sitemap and file; this wrapper
generates nothing.

- **Route owner:** every `amyelectric.com` zone route (see `wrangler.jsonc`).
- **Origin:** `amy-electric-site`, reached through the `ORIGIN` service binding.
- **Not** reachable on workers.dev (`workers_dev: false`).

## Provenance

The Worker was originally deployed out-of-band (via the Cloudflare API, not from
this repository), so it existed only as a deployed bundle. `worker.js` here is
that deployed source, recovered on 2026-10-18 and committed unchanged so the
layer is version-controlled. If you edit it, redeploy with:

```bash
wrangler deploy --dry-run --config seo-worker/wrangler.jsonc   # validate
wrangler deploy --config seo-worker/wrangler.jsonc             # publish
```

The site Worker (`../wrangler.jsonc`) deliberately declares **no** zone routes,
so deploying it cannot take the routes back from this wrapper.

## Behaviour

`amy-electric-site` owns the content and is the source of truth. Every request
is proxied to it, and its response — including a 404 — is returned as-is; the
HTML is never rewritten. The wrapper's only addition is the CORS headers
cross-origin callers need on `/api/` responses.

It generates nothing of its own. `sitemap.xml`, `robots.txt`, `llms.txt` and
every page come from the site, and a path the site does not have gets the site's
own 404 page.

An earlier revision did the opposite, and this was the production bug it caused:

- it answered its own `sitemap.xml` (233 URLs), `robots.txt` and `llms.txt`
  before contacting the origin, shadowing the site's static files — so the
  site's 306-URL sitemap never reached crawlers;
- it answered its own `/ev-charger-installation`, `/panel-upgrade`,
  `/lighting-installation`, `/electrician-<city>` and `/<service>-<city>` pages
  over the site's real ones;
- it rewrote every proxied HTML page's `<title>` to one identical string and
  appended a second canonical/description/OG set, so ~300 pages shared a title
  and carried duplicate canonical tags; and
- the ~200 pages only it had (`/faq`, `/rewiring`, `/troubleshooting`,
  `/electrical-inspection`, 27 city pages, the service-city pairs the site
  lacks) were linked from nowhere and listed in no sitemap. Those paths now 404.

Behaviour is covered by `scripts/test-seo-wrapper.mjs` (`node --test
scripts/test-seo-wrapper.mjs`), which `cloudflare-sync.yml` runs before it
publishes this Worker.
