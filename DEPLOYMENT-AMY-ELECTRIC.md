# AMY Electric production deployment

## Verified state (checked 2026-09-27 against the Cloudflare API)

- Live Worker: **`amy-electric-site`**
- Live config: **`wrangler.jsonc`**
- Account: `a08528fe46962a4d732de2d8d30eeef5` (`a.m.y.electricalservice@gmail.com`)
- Deployed compatibility date: `2026-05-21`, flags `["nodejs_compat"]`
- Deployments on record: 10, **all with `source: "wrangler"`, none from Git**

That last line is the important one: **pushing to `main` does not deploy this site.** Workers Builds
has never run for this Worker, so every deploy has been a manual `wrangler deploy`. Earlier revisions
of this file referred to a `amy-electric-site-production` Worker and to the Revitaldaycare account;
neither is true of the site actually serving `amyelectric.com`, and both notes have been removed.

## Production boundary

- GitHub repository: `amyelectricalservice-ops/amy-electric-site`
- Production Worker: `amy-electric-site`
- Production hostname: `amyelectric.com` (plus the `www` redirect)
- Wrangler configuration: `wrangler.jsonc`
- Public assets are filtered by `.assetsignore`

`wrangler.jsonc` intentionally has no `account_id`, so the account comes from the authenticated
login rather than being committed.

`wrangler.production.jsonc` is retained as a hardened alternative. It is now equivalent to
`wrangler.jsonc` for `main`, `compatibility_date`, `compatibility_flags`, `observability`, `assets`
and host coverage, but it targets a different Worker name and sets `workers_dev: false`. It is not
what serves production today. Adopting it would require creating that Worker and moving the
`amyelectric.com` custom domain onto it.

## Deploying

```bash
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

## Optional: connecting Workers Builds

Nothing is connected today. To get automatic deploys on push, the zone owner would connect the Worker
to `main` in the Cloudflare Workers Builds settings with the deploy command
`npx wrangler deploy --config wrangler.jsonc`, then confirm a push produces a deployment whose
`source` is Git rather than `wrangler`.

That is a convenience, not a requirement — the direct `wrangler deploy` path is verified working.

## Post-deploy: edge cache

Edge HTML entries were historically served without `Accept` partitioning, so markdown/agent requests
could receive stale HTML (`cf-cache-status: HIT` with no `Vary` header). `worker.js` now emits
`Vary: Accept` on HTML responses, so entries partition correctly. The local OAuth token still lacks
the Cache Purge scope, so if stale content is ever observed, purge from the dashboard
(Caching → Purge Everything) or use an API token with Zone Cache Purge + Zone Settings:Read.
