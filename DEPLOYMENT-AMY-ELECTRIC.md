# AMY Electric production deployment

Production must be deployed from the Cloudflare account that owns the
`amyelectric.com` zone. The local Wrangler login is currently associated with
the unrelated Revitaldaycare account, so it is suitable only for the
temporary `amy-electric-site.revitaldaycare.workers.dev` preview.

## Production boundary

- GitHub repository: `amyelectricalservice-ops/amy-electric-site`
- Production Worker: `amy-electric-site-production`
- Production hostname: `amyelectric.com`
- Wrangler configuration: `wrangler.production.jsonc`
- Public assets are filtered by `.assetsignore`

The production config intentionally has no `account_id`. Wrangler should be
run only after authenticating to the account that owns the AMY Electric zone,
which prevents an account ID from being committed to the repository.

## One-time setup by the zone owner

1. Confirm that `amyelectric.com` is an active zone in the Cloudflare account.
2. Create or authorize the `amy-electric-site-production` Worker.
3. Connect the Worker to the GitHub repository and `main` branch through
   Workers Builds. Set its deploy command to
   `npx wrangler deploy --config wrangler.production.jsonc`, or use an
   account-scoped deployment token with that same config.
4. Configure the custom domain from `wrangler.production.jsonc`.
5. Confirm the intended `www` redirect separately; the custom domain matches
   only the exact hostname configured.
6. Keep the current `amy-electric-site` Worker in the Revitaldaycare account
   as a temporary preview until the production hostname is verified.

The production Worker includes the shared `/api/contact` handler. Do not use
an assets-only deployment for production, or form submissions will not be
processed.

## Deployment and verification

From the repository root, after logging in to the zone-owning account:

```bash
npx wrangler@latest deploy --config wrangler.production.jsonc --dry-run
npx wrangler@latest deploy --config wrangler.production.jsonc --message "Deploy AMY Electric production site"
```

Verify the production hostname before considering the cutover complete:

```bash
curl -fsSL https://amyelectric.com/licensed-electrician-los-angeles | grep -m1 '<title>'
curl -fsSL https://amyelectric.com/service-areas | grep -m1 'meta name="description"'
curl -fsSL -o /dev/null -w '%{http_code}\n' https://amyelectric.com/api/contact
```

Do not delete or transfer Revitaldaycare resources as part of this setup.
