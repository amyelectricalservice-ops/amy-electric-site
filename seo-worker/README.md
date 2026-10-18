# `amy-electric-seo` — edge SEO wrapper

This Worker sits in front of `amy-electric-site` on production. Requests to
`amyelectric.com/*` hit this Worker, which forwards them to the origin Worker
and only steps in when the origin has no page at that path.

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

`amy-electric-site` owns the content and is the source of truth, so every
request is proxied to it first. **A real page always wins.** The wrapper
synthesises a page only when the origin answers `404` for a path it knows how to
build: `/faq`, `/electrician-<city>`, `/<service>` and `/<service>-<city>`. Any
other 404 is passed through untouched, and the origin's HTML is returned
verbatim — the wrapper does not rewrite it.

`sitemap.xml`, `robots.txt` and `llms.txt` are **never** generated here; the
site owns those files and serves them itself.

An earlier revision broke both of those rules and this was the production bug it
caused:

- it generated its own `sitemap.xml` (233 URLs), `robots.txt` and `llms.txt`,
  shadowing the site's static files — so the site's 306-URL sitemap never
  reached crawlers;
- it generated its own `/ev-charger-installation`, `/panel-upgrade`,
  `/lighting-installation`, `/electrician-<city>` and `/<service>-<city>` pages
  over the site's real ones; and
- it rewrote every proxied HTML page's `<title>` to one identical string and
  appended a second canonical/description/OG set, so ~300 pages shared a title
  and carried duplicate canonical tags.

Behaviour is covered by `scripts/test-seo-wrapper.mjs` (`node --test
scripts/test-seo-wrapper.mjs`).
