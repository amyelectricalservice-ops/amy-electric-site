import { handleContact } from './contact-handler.js';

const oidcDiscovery = {
  "issuer": "https://amyelectric.com",
  "authorization_endpoint": "https://amyelectric.cloudflareaccess.com/cdn-cgi/access/sso/oidc/PLACEHOLDER_CLIENT_ID/authorize",
  "token_endpoint": "https://amyelectric.cloudflareaccess.com/cdn-cgi/access/sso/oidc/PLACEHOLDER_CLIENT_ID/token",
  "jwks_uri": "https://amyelectric.cloudflareaccess.com/cdn-cgi/access/sso/oidc/PLACEHOLDER_CLIENT_ID/jwks",
  "response_types_supported": ["code", "id_token", "id_token token"],
  "subject_types_supported": ["public"],
  "id_token_signing_alg_values_supported": ["RS256"],
  "grant_types_supported": ["authorization_code", "implicit"],
  "scopes_supported": ["openid", "profile", "email"],
  "token_endpoint_auth_methods_supported": ["client_secret_basic", "client_secret_post"],
  "claims_supported": ["sub", "iss", "aud", "exp", "iat", "name", "email"],
  "service_documentation": "https://developers.cloudflare.com/cloudflare-one/identity/",
  "op_policy_uri": "https://amyelectric.com/privacy-policy.html",
  "op_tos_uri": "https://amyelectric.com/terms-of-service.html"
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.protocol === 'http:' || request.headers.get('x-forwarded-proto') === 'http') {
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === '/api/contact') {
      return handleContact(request, env, ctx.waitUntil.bind(ctx));
    }

    if (url.pathname === '/.well-known/openid-configuration') {
      return new Response(JSON.stringify(oidcDiscovery, null, 2), {
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Cache-Control': 'public, max-age=3600',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    if (url.pathname === '/.well-known/http-message-signatures-directory') {
      const jwks = {
        "keys": [
          {
            "kty": "OKP",
            "crv": "Ed25519",
            "x": "M4aJ5aIFHslCAjNWJFCZVrLaC3N_CpvmwJzFqUF1h58",
            "kid": "amy-electric-2026"
          }
        ]
      };
      return new Response(JSON.stringify(jwks, null, 2), {
        headers: {
          'Content-Type': 'application/http-message-signatures-directory+json',
          'Cache-Control': 'public, max-age=3600',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    if (url.pathname === '/.well-known/mcp/server-card.json') {
      const mcpServerCard = {
        "serverInfo": {
          "name": "amy-electric",
          "version": "1.0.0"
        },
        "endpoint": "/mcp",
        "capabilities": {
          "tools": [
            {
              "name": "getBusinessInfo",
              "description": "Get AMY Electric business information, hours, and service area"
            },
            {
              "name": "getServices",
              "description": "List available electrical services offered by AMY Electric"
            },
            {
              "name": "getContactInfo",
              "description": "Get contact details for AMY Electric"
            }
          ],
          "resources": [
            {
              "uri": "amy-electric://services",
              "name": "Services List",
              "description": "Complete list of electrical services offered"
            },
            {
              "uri": "amy-electric://locations",
              "name": "Service Locations",
              "description": "Areas served by AMY Electric"
            }
          ],
          "prompts": [
            {
              "name": "scheduleEstimate",
              "description": "Help schedule a free estimate appointment"
            }
          ]
        }
      };
      return new Response(JSON.stringify(mcpServerCard, null, 2), {
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Cache-Control': 'public, max-age=3600',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    return env.ASSETS.fetch(request);
  },
};
