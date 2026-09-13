---
slug: oauth-oidc-discovery
status: approved
intent: clear
review_required: false
pending-action: execute plan via /start-work
approach: Create static JSON file at .well-known/openid-configuration, configure worker to serve it with correct content type
---

# Draft: oauth-oidc-discovery

## Components (topology ledger)
<!-- Lock the SHAPE before depth. One row per top-level component that can succeed or fail independently. -->
<!-- id | outcome (one line) | status: active|deferred | evidence path -->
| 1 | Create .well-known/openid-configuration JSON file | active | .well-known/ directory exists |
| 2 | Configure worker to serve discovery metadata | active | worker.js handles routes |
| 3 | Validate endpoint returns correct JSON | active | POST to isitagentready.com |

## Open assumptions (announced defaults)
<!-- Record any default you adopt instead of asking, so the user can veto it at the gate. -->
<!-- assumption | adopted default | rationale | reversible? -->
| Use Cloudflare Access as IdP | Cloudflare Access | Most common for CF-hosted sites; free tier available | Yes |
| Issuer URL | https://amyelectric.com | Domain matches site; standard OIDC convention | Yes |
| Grant types | authorization_code, implicit | Standard for web apps; matches OpenID spec | Yes |
| Response types | code, id_token, id_token token | Standard for OIDC; covers authorization code + implicit flows | Yes |

## Findings (cited - path:lines)

### OpenID Connect Discovery 1.0 Specification
- **Source**: https://openid.net/specs/openid-connect-discovery-1_0.html
- **Required fields**: issuer, authorization_endpoint, token_endpoint, jwks_uri, response_types_supported, subject_types_supported, id_token_signing_alg_values_supported
- **Optional fields**: grant_types_supported, scopes_supported, userinfo_endpoint, registration_endpoint, etc.
- **Endpoint path**: `/.well-known/openid-configuration` on the issuer URL
- **Content-Type**: application/json

### Cloudflare Access OIDC Support
- **Source**: Cloudflare docs on Generic OIDC
- **Discovery endpoint**: `https://<team-name>.cloudflareaccess.com/cdn-cgi/access/sso/oidc/<client-id>/.well-known/openid-configuration`
- **Issuer**: `https://<team-name>.cloudflareaccess.com/cdn-cgi/access/sso/oidc/<client-id>`
- **Token endpoint**: `https://<team-name>.cloudflareaccess.com/cdn-cgi/access/sso/oidc/<client-id>/token`

### Current Site Architecture
- **Source**: AGENTS.md, worker.js
- **Hosting**: Cloudflare Workers + Assets
- **Worker**: Simple fetch handler with HTTPS redirect + contact API
- **Well-known**: .well-known/security.txt exists
- **No authentication**: Site is static HTML with no login system

## Decisions (with rationale)

### Decision 1: Use Cloudflare Access as Identity Provider
**Rationale**: Cloudflare Access is the natural choice for CF-hosted sites. It provides:
- Free tier for up to 50 users
- OIDC support with discovery endpoints
- Integration with Cloudflare Zero Trust
- No additional infrastructure needed

### Decision 2: Publish Discovery Metadata at Domain Level
**Rationale**: The user wants `https://amyelectric.com/.well-known/openid-configuration` to serve the metadata, not the Cloudflare Access subdomain. This is for agent-readiness compliance.

### Decision 3: Minimal Configuration for Agent-Readiness
**Rationale**: The site doesn't have actual authentication needs. The discovery metadata is for compliance with agent-readiness standards (isitagentready.com validation).

## Scope IN

1. Create `.well-known/openid-configuration` JSON file with required fields
2. Configure worker to serve the file with correct Content-Type
3. Include all required OIDC fields: issuer, authorization_endpoint, token_endpoint, jwks_uri, response_types_supported, subject_types_supported, id_token_signing_alg_values_supported
4. Include recommended fields: grant_types_supported, scopes_supported
5. Validate endpoint returns correct JSON

## Scope OUT (Must NOT have)

1. No actual authentication implementation (no login system)
2. No Cloudflare Access configuration (user must do this in CF dashboard)
3. No client registration or OAuth flow implementation
4. No additional security headers beyond what exists

## Open questions

1. **Identity Provider**: Should this use Cloudflare Access as the IdP, or a custom implementation? (Answer: Cloudflare Access)
2. **Issuer URL**: What should the issuer be? (Answer: https://amyelectric.com)
3. **Purpose**: Is this for agent-readiness compliance, or actual authentication needs? (Answer: Agent-Readiness Compliance)

## Approval gate
status: awaiting-approval
<!-- When exploration is exhausted and unknowns are answered, set status: awaiting-approval. -->
<!-- That durable record is the loop guard: on a later turn read it and resume at the gate instead of re-running exploration. -->
