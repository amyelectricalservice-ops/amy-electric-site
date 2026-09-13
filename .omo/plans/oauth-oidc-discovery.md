# oauth-oidc-discovery - Work Plan

## TL;DR (For humans)
<!-- Fill this LAST, after the detailed plan below is written, so it summarizes the REAL plan. -->
<!-- Plain English for a non-engineer: NO file paths, NO todo numbers, NO wave/agent/tool names. -->

**What you'll get:** A working OAuth/OIDC Discovery endpoint at https://amyelectric.com/.well-known/openid-configuration that returns valid OpenID Connect metadata for agent-readiness compliance.

**Why this approach:** Using Cloudflare Access as the identity provider is the natural choice for a CF-hosted site. Publishing discovery metadata at the domain level (not the CF Access subdomain) satisfies isitagentready.com validation requirements.

**What it will NOT do:** This will NOT implement actual authentication, login systems, or OAuth flows. It only publishes discovery metadata for compliance.

**Effort:** Quick
**Risk:** Low - Simple file creation and worker configuration, no authentication logic
**Decisions to sanity-check:** Cloudflare Access as IdP, issuer URL as https://amyelectric.com

Your next move: Approve this plan, then run `/start-work` to execute. Full execution detail follows below.

---

> TL;DR (machine): <1 line - effort, risk, deliverables>

## Scope
### Must have
- Create `.well-known/openid-configuration` JSON file with required OIDC fields
- Configure worker to serve the file with correct Content-Type: application/json
- Include all required fields: issuer, authorization_endpoint, token_endpoint, jwks_uri, response_types_supported, subject_types_supported, id_token_signing_alg_values_supported
- Include recommended fields: grant_types_supported, scopes_supported
- Use Cloudflare Access endpoints for authorization_endpoint, token_endpoint, and jwks_uri
- Set issuer to https://amyelectric.com

### Must NOT have (guardrails, anti-slop, scope boundaries)
- No actual authentication implementation (no login system)
- No Cloudflare Access configuration (user must do this in CF dashboard)
- No client registration or OAuth flow implementation
- No additional security headers beyond what exists
- No modifications to existing routes or contact form functionality

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: tests-after + curl validation
- Evidence: .omo/evidence/oauth-oidc-discovery/task-<N>.json

## Execution strategy
### Parallel execution waves
> Target 5-8 todos per wave. Fewer than 3 (except the final) means you under-split.

**Wave 1:** Create discovery metadata file (Todo 1)
**Wave 2:** Configure worker to serve metadata (Todo 2)
**Wave 3:** Validate endpoint (Todo 3)

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1 | None | 2 | None |
| 2 | 1 | 3 | None |
| 3 | 2 | None | None |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->
- [ ] 1. Create .well-known/openid-configuration JSON file
  What to do / Must NOT do: Create a new file at `.well-known/openid-configuration` with the required OpenID Connect Discovery metadata. The file MUST include: issuer, authorization_endpoint, token_endpoint, jwks_uri, response_types_supported, subject_types_supported, id_token_signing_alg_values_supported. Include recommended fields: grant_types_supported, scopes_supported. Use Cloudflare Access endpoints for authorization_endpoint, token_endpoint, and jwks_uri. Set issuer to https://amyelectric.com. Do NOT add any actual authentication logic.
  Parallelization: Wave 1 | Blocked by: None | Blocks: 2
  References (executor has NO interview context - be exhaustive): OpenID Connect Discovery 1.0 spec (https://openid.net/specs/openid-connect-discovery-1_0.html), Cloudflare Access OIDC docs, .well-known/security.txt (existing file in same directory)
  Acceptance criteria (agent-executable): File exists at .well-known/openid-configuration, contains valid JSON with all required fields, Content-Type will be application/json when served
  QA scenarios (name the exact tool + invocation): happy: read file and verify JSON structure, failure: file missing or invalid JSON, Evidence attemptDir/task-1-oauth-oidc-discovery.json
  Commit: Y | feat(oidc): add OpenID Connect Discovery metadata

- [ ] 2. Configure worker to serve discovery metadata with correct Content-Type
  What to do / Must NOT do: Modify worker.js to intercept requests to /.well-known/openid-configuration and serve the JSON file with Content-Type: application/json. The worker should check if the request path matches and return the file with correct headers. Do NOT modify any other routes or add authentication logic.
  Parallelization: Wave 2 | Blocked by: 1 | Blocks: 3
  References (executor has NO interview context - be exhaustive): worker.js (current implementation), .well-known/openid-configuration (created in step 1)
  Acceptance criteria (agent-executable): GET /.well-known/openid-configuration returns JSON with Content-Type: application/json, all required fields present
  QA scenarios (name the exact tool + invocation): happy: curl -H "Accept: application/json" https://amyelectric.com/.well-known/openid-configuration returns valid JSON, failure: returns HTML or 404, Evidence attemptDir/task-2-oauth-oidc-discovery.json
  Commit: Y | feat(worker): serve OIDC discovery metadata

- [ ] 3. Validate endpoint returns correct JSON structure
  What to do / Must NOT do: Test the endpoint by making a request and verifying the response contains all required OIDC fields. Check that issuer matches https://amyelectric.com, authorization_endpoint and token_endpoint point to Cloudflare Access, jwks_uri is valid. Do NOT attempt to actually authenticate or use the endpoints.
  Parallelization: Wave 3 | Blocked by: 2 | Blocks: None
  References (executor has NO interview context - be exhaustive): OpenID Connect Discovery 1.0 spec, Cloudflare Access OIDC docs
  Acceptance criteria (agent-executable): Response contains all required fields, issuer is https://amyelectric.com, endpoints point to Cloudflare Access
  QA scenarios (name the exact tool + invocation): happy: all required fields present and valid, failure: missing fields or invalid URLs, Evidence attemptDir/task-3-oauth-oidc-discovery.json
  Commit: N/A (validation only)

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [ ] F1. Plan compliance audit - Verify all required OIDC fields are present and valid
- [ ] F2. Code quality review - Verify worker.js changes are clean and follow existing patterns
- [ ] F3. Real manual QA - Test endpoint with curl and verify JSON response
- [ ] F4. Scope fidelity - Confirm no authentication logic was added

## Commit strategy
- Commit 1: `feat(oidc): add OpenID Connect Discovery metadata` - Create .well-known/openid-configuration
- Commit 2: `feat(worker): serve OIDC discovery metadata` - Update worker.js to serve the file
- Both commits should be atomic and follow existing commit message conventions

## Success criteria
- GET https://amyelectric.com/.well-known/openid-configuration returns valid JSON
- Response contains all required OIDC fields: issuer, authorization_endpoint, token_endpoint, jwks_uri, response_types_supported, subject_types_supported, id_token_signing_alg_values_supported
- Issuer is https://amyelectric.com
- authorization_endpoint and token_endpoint point to Cloudflare Access
- Content-Type header is application/json
- isitagentready.com validation passes (checks.discovery.oauthDiscovery.status = "pass")
