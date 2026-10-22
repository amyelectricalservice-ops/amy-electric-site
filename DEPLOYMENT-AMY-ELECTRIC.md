# AMY Electric production deployment

## Verified state (checked 2026-10-18 against the Cloudflare API)

Production is **one** Worker:

- **`amy-electric-site`** — config `wrangler.jsonc`. The site/assets/API Worker, and the owner of the
  zone's single `amyelectric.com/*` route: it serves the domain directly. `workers_dev` is on, which
  is what the deploy smoke tests use.
- Account: `a08528fe46962a4d732de2d8d30eeef5` (`a.m.y.electricalservice@gmail.com`)
- Deployed compatibility date: `2026-10-14`, flags `["nodejs_compat"]`

An **`amy-electric-seo`** edge wrapper used to own the zone routes and front this Worker through an
`ORIGIN` service binding. It had been deployed out-of-band (via the Cloudflare API, not from this
repository), so nothing in git said it existed. It was recovered into `seo-worker/`, found to be
shadowing the site's own pages and serving a smaller sitemap, and retired on 2026-10-18: the
`amyelectric.com/*` route was reassigned to `amy-electric-site` and the wrapper Worker and its 11
redundant sub-patterns were deleted.

Earlier revisions of this file described a single Worker serving `amyelectric.com` (true again since
2026-10-18) and a `amy-electric-site-production` Worker in the Revitaldaycare account (never true).

## Production boundary

- GitHub repository: `amyelectricalservice-ops/amy-electric-site`
- Production hostname: `amyelectric.com` (plus the `www` redirect, a zone-level rule outside the Worker)
- Route owner: **`amy-electric-site`** — the single `amyelectric.com/*`
- Wrangler configuration: `wrangler.jsonc`
- Public assets are filtered by `.assetsignore`

The config does not commit an `account_id`, so the account comes from the authenticated login rather
than being committed.

`wrangler.production.jsonc` is retained as a hardened alternative for the Worker but is unused: it
targets a different Worker name (`amy-electric-site-production`) and repeats the `amyelectric.com`
custom domain. Adopting it would mean renaming the Worker.

## Deploying

```bash
wrangler deploy --dry-run --config wrangler.jsonc   # validates bundle + asset list + route
wrangler deploy --config wrangler.jsonc             # publishes, prints Version ID
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

Two workflows share two repository secrets, which are deliberately not in the repo:

- `CLOUDFLARE_API_TOKEN` — an API token with **Account > Workers Scripts > Edit** (and **Zone >
  Workers Routes > Read** for the route audit)
- `CLOUDFLARE_ACCOUNT_ID` — the account that owns the amyelectric.com zone

- `.github/workflows/deploy.yml` deploys the Worker (`wrangler.jsonc`) on every push to `main`
  (pull requests validate and upload a preview version instead), notifies IndexNow, and smoke-tests
  production. Because `wrangler.jsonc` now declares the `amyelectric.com/*` route, the deploy is what
  keeps the zone's route table in step with git.
- `.github/workflows/cloudflare-routes.yml` compares the committed route table with the live zone
  (`scripts/audit-cloudflare-routes.py`). A weekly schedule runs it strictly, so a route changed in
  the dashboard without reaching git is reported instead of silently standing; on a push or pull
  request the same audit only warns, because the deploy that follows is about to reconcile the zone.

Both are inert until the secrets exist: each job fails at an explicit preflight step that names the
missing secret, rather than failing obscurely inside wrangler.

Cloudflare's own Workers Builds Git integration remains unconnected and is not required; if it is ever
enabled, disable the matching workflow so they do not both deploy on the same push.

## Post-deploy: edge cache

Edge HTML entries were historically served without `Accept` partitioning, so markdown/agent requests
could receive stale HTML (`cf-cache-status: HIT` with no `Vary` header). `worker.js` now emits
`Vary: Accept` on HTML responses, so entries partition correctly. The local OAuth token still lacks
the Cache Purge scope, so if stale content is ever observed, purge from the dashboard
(Caching → Purge Everything) or use an API token with Zone Cache Purge + Zone Settings:Read.
