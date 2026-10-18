# AMY Electric production deployment

## Verified state (checked 2026-10-18 against the Cloudflare API)

Production is two Workers, not one:

- **Edge wrapper Worker: `amy-electric-seo`** — config `seo-worker/wrangler.jsonc`. It owns every
  `amyelectric.com` zone route (`amyelectric.com/*` plus 11 sub-patterns) and proxies to the origin
  through an `ORIGIN` service binding. `workers_dev` is off.
- **Origin Worker: `amy-electric-site`** — config `wrangler.jsonc`. The site/assets/API Worker. It
  declares **no** zone routes; it is reached only through the wrapper's service binding (and its
  workers.dev subdomain).
- Account: `a08528fe46962a4d732de2d8d30eeef5` (`a.m.y.electricalservice@gmail.com`)
- Origin deployed compatibility date: `2026-10-14`, flags `["nodejs_compat"]`

The `amy-electric-seo` wrapper was originally deployed out-of-band (via the Cloudflare API, not from
this repository) and is now committed under `seo-worker/` so the layer is version-controlled.

Earlier revisions of this file described a single Worker serving `amyelectric.com`, and a
`amy-electric-site-production` Worker in the Revitaldaycare account; neither is true today.

## Production boundary

- GitHub repository: `amyelectricalservice-ops/amy-electric-site`
- Production hostname: `amyelectric.com` (plus the `www` redirect)
- Route owner: **`amy-electric-seo`** — `amyelectric.com/*` and its sub-patterns
- Origin Worker: **`amy-electric-site`**
- Wrangler configurations: `seo-worker/wrangler.jsonc` (wrapper), `wrangler.jsonc` (origin)
- Public assets are filtered by `.assetsignore`

Neither config commits an `account_id`, so the account comes from the authenticated login rather
than being committed.

`wrangler.production.jsonc` is retained as a hardened alternative for the origin Worker but is
unused: it targets a different Worker name (`amy-electric-site-production`) and claims the
`amyelectric.com` custom domain plus `www.amyelectric.com/*`, which now belong to the wrapper.
Adopting it would require moving those routes off `amy-electric-seo` first.

## Deploying

```bash
# edge wrapper (route owner)
wrangler deploy --dry-run --config seo-worker/wrangler.jsonc   # validates the bundle
wrangler deploy --config seo-worker/wrangler.jsonc             # publishes, prints Version ID

# origin site Worker
wrangler deploy --dry-run --config wrangler.jsonc   # validates bundle + asset list
wrangler deploy --config wrangler.jsonc            # publishes, prints Version ID
```

`wrangler login` must have been run against the zone-owning account. Deploys currently ride an
OAuth token that expires; if a deploy fails with `CLOUDFLARE_API_TOKEN` required, re-run it — that
is a token-refresh race, not a broken config.

Verify before considering a deploy complete:

```bash
curl -fsSL https://amyelectric.com/ | grep -m1 '<title>'
curl -sS -o /dev/null -w '%{http_code}\n' https://amyelectric.com/sitemap.xml
curl -sS -o /dev/null -w '%{http_code}\n' https://amyelectric.com/report.json   # expect 404
curl -sSI https://www.amyelectric.com/ | head -1                                # expect 301 to apex
```

The Worker includes the shared `/api/contact` handler. Do not use an assets-only deployment, or form
submissions will not be processed.

## Automatic deploys

`.github/workflows/deploy.yml` deploys the **origin** Worker on every push to `main`. It validates
structured data and sitemap integrity first, then runs `wrangler deploy --config wrangler.jsonc`,
notifies IndexNow, and smoke-tests production. It is inert until two repository secrets exist:

- `CLOUDFLARE_API_TOKEN` — an API token with **Account > Workers Scripts > Edit**
- `CLOUDFLARE_ACCOUNT_ID` — the account owning the amyelectric.com zone

The workflow does not deploy the `amy-electric-seo` wrapper; deploy that one manually (see above).
Because the origin declares no zone routes, a push to `main` can no longer take the
`amyelectric.com` routes back from the wrapper.

Until both are set the deploy job fails at an explicit preflight step that names the missing secret,
rather than failing obscurely inside wrangler.

Cloudflare's own Workers Builds Git integration remains unconnected and is not required; if it is ever
enabled, disable this workflow so the two do not both deploy on the same push.

## Post-deploy: edge cache

Edge HTML entries were historically served without `Accept` partitioning, so markdown/agent requests
could receive stale HTML (`cf-cache-status: HIT` with no `Vary` header). `worker.js` now emits
`Vary: Accept` on HTML responses, so entries partition correctly. The local OAuth token still lacks
the Cache Purge scope, so if stale content is ever observed, purge from the dashboard
(Caching → Purge Everything) or use an API token with Zone Cache Purge + Zone Settings:Read.
