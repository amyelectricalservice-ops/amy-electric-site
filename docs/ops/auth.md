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
needs no API key, OAuth client, enrollment, or sign-up form. There is no
self-serve signup portal. Automated clients
should identify with a descriptive `User-Agent` string. For high-volume
or commercial agent integrations, contact [info@amyelectric.com](mailto:info@amyelectric.com) to arrange
allowlisting and a direct coordination channel.

## How to register an agent integration

Although no key or enrollment is required to start, production agent
integrations should register so we can allowlist your traffic and notify
you of API changes. Registration is a short email exchange:

1. Register with the estimate form at https://amyelectric.com/#estimator
   (put `Agent registration` in the project details), or email
   [info@amyelectric.com](mailto:info@amyelectric.com) with subject `Agent registration`.
2. Include your `User-Agent` string, the endpoints you call
   (`/.well-known/api-catalog`, `/openapi.json`, `/a2a`), and expected
   request volume.
3. We reply within two business days confirming allowlisting, plus a
   contact channel for breaking-change notices.

Registered integrations are listed for abuse-triage purposes only; there
are no fees, tiers, or credential issuance.

## Contact

AMY Electric, C-10 #981578 · (818) 302-5614 · info@amyelectric.com · 20628 Londelius St, Winnetka, CA 91306
