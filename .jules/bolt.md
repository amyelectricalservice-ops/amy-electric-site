# Bolt's Performance Journal

Critical performance learnings and codebase-specific optimization insights.

## 2026-11-03 - Pre-serialize Static Endpoints in Cloudflare Worker Edge Handler
**Learning:** Static discovery and documentation endpoints (`/openapi.json`, `/.well-known/agent.json`, `/.well-known/api-catalog`, `/api/docs`) previously regenerated complex JavaScript object structures and ran `JSON.stringify(..., null, 2)` inside the request fetch handler on every request. Pre-serializing these static payloads to constants at module scope eliminated object allocation and JSON serialization overhead, cutting response generation time from ~697ms down to ~296ms per 20,000 requests (~58% faster) with zero heap churn per request.
**Action:** Always pre-serialize static JSON and HTML payloads to module-scope constants when serving static specifications, manifests, or documentation from Cloudflare Workers edge routes.
