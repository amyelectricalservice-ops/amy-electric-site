# Auth.md — Authentication for AMY Electric

> How authentication and abuse protection work on amyelectric.com. No customer-facing login exists.

## Public access (no authentication)

- Website pages, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`: public, no credentials.
- Discovery documents (`/.well-known/api-catalog`, `/openapi.json`, `/api/docs`, `/api/health`, MCP server card, agent skills index): public, no credentials.
- Contact and estimate API (`POST /api/contact`): public by design — it powers the website quote forms. No API keys. Abuse is handled server-side instead.

## Contact API abuse protection

- Honeypot form field plus form-timing checks reject automated spam silently (accepted as success to avoid signaling bots).
- Optional Cloudflare Turnstile verification when enabled.
- Rate handling via Cloudflare edge; repeated abuse can be blocked at the WAF.

## Internal access

- Staff tooling sits behind Cloudflare Access (see `/.well-known/openid-configuration`). Nothing customer-facing requires login or OAuth tokens.

## Agent registration

No registration is required: every agent-facing endpoint on this site
(API catalog, OpenAPI spec, API docs, health, MCP server card, agent
skills index, A2A agent card, markdown representations) is public and
needs no API key, OAuth client, or enrollment step. Automated clients
should identify with a descriptive `User-Agent` string. For high-volume
or commercial agent integrations, contact info@amyelectric.com to arrange
allowlisting and a direct coordination channel.

## Contact

AMY Electric, C-10 #981578 · (818) 302-5614 · info@amyelectric.com · 20628 Londelius St, Winnetka, CA 91306
