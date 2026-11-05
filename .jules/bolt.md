# Bolt's Performance Journal

Critical performance learnings and codebase-specific optimization insights.

## 2026-11-05 - Pre-serialize Static Well-Known Discovery Endpoints in Cloudflare Worker
**Learning:** Static discovery, specification, and agent metadata endpoints (`/.well-known/http-message-signatures-directory`, `/.well-known/agent-skills/index.json`, `/.well-known/mcp/server-card.json`, `/.well-known/api-catalog`, `/.well-known/agent.json`, `/openapi.json`, and `/api/docs`) previously instantiated large JS object trees and invoked `JSON.stringify(..., null, 2)` inside `fetch` on every request. Pre-serializing these payloads to constants at module scope eliminated object allocation and serialization overhead entirely, speeding up response generation from ~476ms to ~0.5ms per 50,000 requests with zero garbage collection churn on the edge runtime.
**Action:** Always pre-serialize static JSON specifications, agent cards, discovery schemas, and HTML documentation strings to module-scope constants in Cloudflare Workers edge routes.
