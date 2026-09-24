import { handleContact } from './contact-handler.js';

const oidcDiscovery = (clientId) => ({
  "issuer": "https://amyelectric.com",
  "authorization_endpoint": `https://amyelectric.cloudflareaccess.com/cdn-cgi/access/sso/oidc/${clientId}/authorize`,
  "token_endpoint": `https://amyelectric.cloudflareaccess.com/cdn-cgi/access/sso/oidc/${clientId}/token`,
  "jwks_uri": `https://amyelectric.cloudflareaccess.com/cdn-cgi/access/sso/oidc/${clientId}/jwks`,
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
});

function decodeMarkdownEntities(s) {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&middot;/g, '·')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)));
}

function metaContent(html, name, property) {
  let m = html.match(new RegExp('<meta\\s+name="' + name + '"\\s+content="([^"]*)"', 'i'));
  if (m) return m[1];
  m = html.match(new RegExp('<meta\\s+property="' + property + '"\\s+content="([^"]*)"', 'i'));
  return m ? m[1] : '';
}

function inlineMarkdown(fragment, pageUrl) {
  let s = fragment;
  s = s.replace(/<img\b[^>]*alt="([^"]*)"[^>]*src="([^"]*)"[^>]*>/gi, (_, alt, src) => {
    try { src = new URL(src, pageUrl).toString(); } catch { /* keep relative */ }
    return '![' + alt + '](' + src + ')';
  });
  s = s.replace(/<img\b[^>]*src="([^"]*)"[^>]*>/gi, (_, src) => {
    try { src = new URL(src, pageUrl).toString(); } catch { /* keep relative */ }
    return '![](' + src + ')';
  });
  s = s.replace(/<a\b[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, (_, href, text) => {
    const clean = text.replace(/<[^>]+>/g, '').trim();
    if (!clean || href.startsWith('#') || href.startsWith('javascript:')) return clean;
    let absolute = href;
    try { absolute = new URL(href, pageUrl).toString(); } catch { /* keep as-is */ }
    return '[' + clean + '](' + absolute + ')';
  });
  s = s.replace(/<(strong|b)\b[^>]*>([\s\S]*?)<\/(strong|b)>/gi, '**$2**');
  s = s.replace(/<(em|i)\b[^>]*>([\s\S]*?)<\/(em|i)>/gi, '*$2*');
  s = s.replace(/<br\s*\/?>/gi, '\n');
  s = s.replace(/<[^>]+>/g, '');
  return decodeMarkdownEntities(s);
}

function htmlToMarkdown(html, pageUrl) {
  const title = metaContent(html, 'title', 'og:title') || (html.match(/<title>([^<]*)<\/title>/i) || [])[1] || '';
  const description = metaContent(html, 'description', 'og:description');
  const image = metaContent(html, '', 'og:image');

  const jsonLd = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)]
    .map(m => m[1].trim())
    .filter(Boolean);

  let bodyMatch = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  let body = bodyMatch ? bodyMatch[1] : (html.match(/<body\b[^>]*>([\s\S]*?)<\/body>/i) || [])[1] || html;
  body = body.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '');
  body = body.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '');
  body = body.replace(/<(nav|header|footer)\b[^>]*>[\s\S]*?<\/\1>/gi, '');

  body = body.replace(/<details\b[^>]*>\s*<summary\b[^>]*>([\s\S]*?)<\/summary>([\s\S]*?)<\/details>/gi,
    (_, q, a) => '\n\n**' + inlineMarkdown(q, pageUrl).trim() + '**\n\n' + inlineMarkdown(a, pageUrl).trim() + '\n\n');

  body = body.replace(/<table\b[^>]*>([\s\S]*?)<\/table>/gi, (_, table) => {
    const rows = [...table.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/gi)].map(r =>
      [...r[1].matchAll(/<(th|td)\b[^>]*>([\s\S]*?)<\/(th|td)>/gi)].map(c => inlineMarkdown(c[2], pageUrl).replace(/\|/g, '\\|').trim())
    ).filter(r => r.length);
    if (!rows.length) return '';
    const headerSep = rows[0].map(() => '---');
    return '\n\n' + [rows[0].join(' | '), headerSep.join(' | '), ...rows.slice(1).map(r => r.join(' | '))].join('\n') + '\n\n';
  });

  body = body.replace(/<(ul|ol)\b[^>]*>([\s\S]*?)<\/\1>/gi, (_, tag, list) => {
    let n = 0;
    const items = [...list.matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/gi)].map(m => {
      n += 1;
      return (tag.toLowerCase() === 'ol' ? n + '. ' : '- ') + inlineMarkdown(m[1], pageUrl).trim();
    });
    return '\n\n' + items.join('\n') + '\n\n';
  });

  body = body.replace(/<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi,
    (_, level, text) => '\n\n' + '#'.repeat(Number(level)) + ' ' + inlineMarkdown(text, pageUrl).trim() + '\n\n');
  body = body.replace(/<(p|div|section|article|li|blockquote|figcaption)\b[^>]*>/gi, '\n\n');
  body = body.replace(/<\/(p|div|section|article|li|blockquote|figcaption|ul|ol|table|tr|details)>/gi, '\n\n');
  body = inlineMarkdown(body, pageUrl);
  body = body.split('\n').map(l => l.replace(/[ \t]+$/g, '')).join('\n');
  body = body.replace(/\n{3,}/g, '\n\n').trim();

  let out = '';
  if (title || description || image) {
    out += '---\n';
    if (title) out += 'title: ' + title.trim() + '\n';
    if (description) out += 'description: ' + description.trim() + '\n';
    if (image) out += 'image: ' + image.trim() + '\n';
    out += '---\n\n';
  }
  out += body;
  if (jsonLd.length) {
    out += '\n\n```json\n' + jsonLd.join('\n') + '\n```\n';
  }
  return out;
}

const a2aTasks = new Map();

function a2aAgentCard() {
  return {
    name: 'AMY Electric Estimator',
    description: 'Answer questions about residential and commercial electrical work in Greater Los Angeles (services, pricing ranges, licensing, permits, rebates) and guide estimate requests. Operated by AMY Electric, C-10 #981578.',
    url: 'https://amyelectric.com/a2a',
    version: '1.0.0',
    supportedInterfaces: [{ url: 'https://amyelectric.com/a2a', protocol: 'JSONRPC' }],
    capabilities: { streaming: true, pushNotifications: false, stateTransitionHistory: true },
    defaultInputModes: ['text'],
    defaultOutputModes: ['text'],
    skills: [
      { id: 'answer-faq', name: 'Answer electrical questions', description: 'Pricing ranges, licensing, permits, LADWP rebates, and service guidance for LA electrical work.', tags: ['electrical', 'pricing', 'faq'] },
      { id: 'guide-estimate', name: 'Guide an estimate request', description: 'Collect service type, city, and contact details, then direct the customer to booking channels.', tags: ['estimate', 'lead'] }
    ]
  };
}

function a2aAnswer(text) {
  const t = text.toLowerCase();
  const has = (...words) => words.some(w => t.includes(w));
  if (has('license', 'licensed', 'c-10', 'c10', 'insured', 'legit')) {
    return 'AMY Electric holds California C-10 Electrical Contractor license #981578, verifiable at cslb.ca.gov, plus EVITP certification #4051604 for charging infrastructure. We carry general liability and workers compensation insurance. California requires a C-10 license for electrical jobs over $500 — always verify before signing.';
  }
  if (has('rebate', 'credit', 'ladwp', 'incentive', '30c')) {
    return 'Two incentives stack on most installs: the LADWP rebate up to $500 for qualifying Level 2 chargers, and the 30 percent federal 30C tax credit up to $1,000 through 2032. Combined they can bring a standard $900 install under $200 net. LADWP jobs need a licensed contractor, permit, and inspection — our standard process.';
  }
  if (has('price', 'cost', 'much', 'quote', 'estimate', 'charge')) {
    if (has('panel', 'upgrade', '200a', '200 amp', 'amp')) return 'A 100A to 200A panel upgrade in Los Angeles runs $2,500 to $4,500 including permit, labor, materials, and inspection, over a four to eight hour power-off day. Federal Pacific or Zinsco replacements run $2,800 to $4,800. We quote firm itemized pricing after an on-site evaluation.';
    if (has('rewire', 'rewiring', 're-wire')) return 'Whole-home rewiring in Los Angeles runs $8,000 to $18,000 over three to seven days depending on size and access. Trigger signs: knob-and-tube or aluminum wiring, ungrounded two-prong outlets, and insurance restrictions.';
    if (has('tesla', 'wall connector')) return 'Tesla Wall Connector installation runs $500 to $1,200 including the dedicated 60A circuit, wiring, mounting, permit, and commissioning. The unit itself ($475) is purchased separately from Tesla.';
    return 'Typical Los Angeles ranges: Level 2 EV charger $350 to $900, panel upgrade $2,500 to $4,500, troubleshooting visits $150 to $350, whole-home rewiring $8,000 to $18,000. Every project gets an itemized written estimate after an on-site load calculation — call (818) 302-5614.';
  }
  if (has('permit')) {
    return 'Most LA electrical work — panel upgrades, EV chargers, new circuits, rewiring — requires an LADBS e-permit plus city inspection to California Electrical Code, with LADWP coordination where service work is involved. We submit permits, schedule and attend inspections, and deliver final records. Unpermitted work must be disclosed at sale.';
  }
  if (has('emergency', 'spark', 'burning', 'outage', 'urgent')) {
    return 'For sparking outlets, burning smells, or power loss affecting only your home, call (818) 302-5614 immediately — we dispatch same-day for emergencies when crews are available. Stop using the affected circuit and do not keep resetting a tripping breaker.';
  }
  if (has('ev', 'charger', 'tesla', 'chargepoint', 'nema')) {
    return 'Most LA homeowners install a 40A or 48A Level 2 charger ($350 to $900 installed) after a free load calculation confirms panel capacity; 100A services often need the $2,500 to $4,500 upgrade first. We install Tesla, ChargePoint, and universal stations, permitted and inspected, and prepare LADWP rebate paperwork up to $500.';
  }
  return null;
}

function a2aTaskNew(text) {
  const id = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2);
  return {
    id, contextId: id,
    status: { state: 'submitted', timestamp: new Date().toISOString() },
    history: [{ messageId: id + '-u1', role: 'user', parts: [{ kind: 'text', text }] }],
    artifacts: []
  };
}

function a2aComplete(task, answer) {
  const now = new Date().toISOString();
  task.history.push({ messageId: task.id + '-a' + task.history.length, role: 'agent', parts: [{ kind: 'text', text: answer }] });
  task.artifacts.push({ artifactId: task.id + '-art1', name: 'answer', parts: [{ kind: 'text', text: answer }] });
  task.status = { state: 'completed', timestamp: now };
  return task;
}

function a2aRpcError(id, code, message) {
  return new Response(JSON.stringify({ jsonrpc: '2.0', id: id === undefined ? null : id, error: { code, message } }), {
    status: 200,
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

function a2aRpcResult(id, result) {
  return new Response(JSON.stringify({ jsonrpc: '2.0', id, result }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

async function a2aHandler(request) {
  if (request.method === 'GET') {
    return new Response(JSON.stringify({ error: 'Use POST with a JSON-RPC body. Agent card: /.well-known/agent.json' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', Allow: 'POST' }
    });
  }
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return a2aRpcError(null, -32700, 'Parse error: invalid JSON');
  }
  if (!body || body.jsonrpc !== '2.0' || typeof body.method !== 'string') {
    return a2aRpcError(body && body.id, -32600, 'Invalid Request');
  }
  const id = body.id === undefined ? null : body.id;

  if (body.method === 'message/send') {
    const msg = body.params && body.params.message;
    const text = msg && Array.isArray(msg.parts)
      ? msg.parts.filter(p => p.kind === 'text' && typeof p.text === 'string').map(p => p.text).join('\n')
      : '';
    if (!text.trim()) return a2aRpcError(id, -32602, 'Invalid params: message.parts with text content required');
    let task = null;
    const ctxId = msg.contextId;
    if (ctxId && a2aTasks.has(ctxId)) {
      task = a2aTasks.get(ctxId);
      if (task.status.state === 'canceled' || task.status.state === 'failed' || task.status.state === 'completed') task = null;
    }
    if (!task) {
      task = a2aTaskNew(text);
      a2aTasks.set(task.contextId, task);
    } else {
      task.history.push({ messageId: task.id + '-u' + task.history.length, role: 'user', parts: [{ kind: 'text', text }] });
    }
    const answer = a2aAnswer(text);
    if (answer) return a2aRpcResult(id, a2aComplete(task, answer));
    const clarify = 'I can help with AMY Electric services, pricing ranges, licensing, permits, and rebates across Greater Los Angeles — or guide an estimate request. Tell me the service you need and your city (for humans: (818) 302-5614). Which project are you planning?';
    task.history.push({ messageId: task.id + '-a' + task.history.length, role: 'agent', parts: [{ kind: 'text', text: clarify }] });
    task.status = { state: 'input-required', timestamp: new Date().toISOString() };
    return a2aRpcResult(id, task);
  }

  if (body.method === 'message/stream') {
    const msg = body.params && body.params.message;
    const text = msg && Array.isArray(msg.parts)
      ? msg.parts.filter(p => p.kind === 'text' && typeof p.text === 'string').map(p => p.text).join('\n')
      : '';
    if (!text.trim()) return a2aRpcError(id, -32602, 'Invalid params: message.parts with text content required');
    const task = a2aTaskNew(text);
    a2aTasks.set(task.contextId, task);
    const answer = a2aAnswer(text) || 'Tell me the service you need and your city, or call (818) 302-5614 for an immediate quote.';
    const working = { jsonrpc: '2.0', id, result: { ...task, status: { state: 'working', timestamp: new Date().toISOString() } } };
    const done = { jsonrpc: '2.0', id, result: a2aComplete(task, answer) };
    const stream = new ReadableStream({
      start(controller) {
        controller.enqueue(new TextEncoder().encode('data: ' + JSON.stringify(working) + '\n\n'));
        controller.enqueue(new TextEncoder().encode('data: ' + JSON.stringify(done) + '\n\n'));
        controller.close();
      }
    });
    return new Response(stream, {
      headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-store' }
    });
  }

  if (body.method === 'tasks/get') {
    const taskId = body.params && (body.params.id || body.params.taskId);
    const task = [...a2aTasks.values()].find(t => t.id === taskId || t.contextId === taskId);
    if (!task) return a2aRpcError(id, -32002, 'Task not found');
    return a2aRpcResult(id, task);
  }

  if (body.method === 'tasks/cancel') {
    const taskId = body.params && (body.params.id || body.params.taskId);
    const task = [...a2aTasks.values()].find(t => t.id === taskId || t.contextId === taskId);
    if (!task) return a2aRpcError(id, -32002, 'Task not found');
    if (task.status.state === 'completed') return a2aRpcError(id, -32003, 'Task already completed');
    task.status = { state: 'canceled', timestamp: new Date().toISOString() };
    return a2aRpcResult(id, task);
  }

  return a2aRpcError(id, -32601, 'Method not found');
}

function contactApiSpec() {
  return {
    openapi: '3.1.0',
    info: {
      title: 'AMY Electric Contact API',
      version: '1.0.0',
      description: 'Submit estimate requests and service inquiries to AMY Electric, licensed C-10 electrical contractor (#981578) in Los Angeles. Backed by spam protection (honeypot, timing check, optional Turnstile).'
    },
    servers: [{ url: 'https://amyelectric.com' }],
    paths: {
      '/api/contact': {
        post: {
          summary: 'Submit a contact or estimate request',
          requestBody: {
            required: true,
            content: {
              'application/json': { schema: { $ref: '#/components/schemas/Lead' } },
              'application/x-www-form-urlencoded': { schema: { $ref: '#/components/schemas/Lead' } },
              'multipart/form-data': { schema: { $ref: '#/components/schemas/Lead' } }
            }
          },
          responses: {
            200: { description: 'Accepted', content: { 'application/json': { schema: { $ref: '#/components/schemas/Success' } } } },
            400: { description: 'Validation or processing failure' },
            405: { description: 'Method not allowed (POST only)' }
          }
        }
      },
      '/api/health': {
        get: {
          summary: 'Service health check',
          responses: {
            200: { description: 'Service operating normally' }
          }
        }
      }
    },
    components: {
      schemas: {
        Lead: {
          type: 'object',
          properties: {
            name: { type: 'string', description: 'Full name' },
            phone: { type: 'string', description: 'Callback phone number' },
            email: { type: 'string', description: 'Email address' },
            service: { type: 'string', description: 'Requested service (e.g. EV Charger Installation, Panel Upgrade)' },
            city: { type: 'string', description: 'Service area city' },
            message: { type: 'string', description: 'Project details' },
            request_type: { type: 'string', description: 'Alternative to service for request classification' },
            website: { type: 'string', description: 'Honeypot anti-spam field. Leave empty.' },
            _timestamp: { type: 'string', description: 'Form render timestamp for timing checks' },
            'cf-turnstile-response': { type: 'string', description: 'Turnstile token when CAPTCHA is enabled' }
          }
        },
        Success: {
          type: 'object',
          required: ['success', 'message'],
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: "Thank you! We'll be in touch shortly." }
          }
        }
      }
    }
  };
}

function contactApiDocs() {
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    + '<meta name="viewport" content="width=device-width, initial-scale=1">'
    + '<title>Contact API Docs | AMY Electric</title>'
    + '<meta name="description" content="Documentation for the AMY Electric contact and estimate request API.">'
    + '</head><body><main>'
    + '<h1>AMY Electric Contact API</h1>'
    + '<p>Submit estimate requests and service inquiries to our licensed C-10 electrical team (#981578). '
    + 'Machine-readable description: <a href="/openapi.json">openapi.json</a>. '
    + 'Discovery catalog: <a href="/.well-known/api-catalog">api-catalog</a>. '
    + 'Health: <a href="/api/health">api/health</a>.</p>'
    + '<h2>POST /api/contact</h2>'
    + '<p>Accepts <code>application/json</code>, <code>application/x-www-form-urlencoded</code>, or '
    + '<code>multipart/form-data</code>. Fields: <code>name</code>, <code>phone</code>, <code>email</code>, '
    + '<code>service</code>, <code>city</code>, <code>message</code>, <code>request_type</code>. '
    + 'Leave the <code>website</code> honeypot field empty. Returns <code>{"success": true}</code> on acceptance; '
    + '<code>405</code> for non-POST methods. Prefer a human? Call <a href="tel:18183025614">(818) 302-5614</a>.</p>'
    + '<h2>GET /api/health</h2>'
    + '<p>Returns <code>{"ok": true}</code> when the service is operating normally.</p>'
    + '</main></body></html>';
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.protocol === 'http:' || request.headers.get('x-forwarded-proto') === 'http') {
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }

    if (url.hostname === 'www.amyelectric.com') {
      url.hostname = 'amyelectric.com';
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === '/api/contact') {
      return handleContact(request, env, ctx.waitUntil.bind(ctx));
    }

    if (url.pathname === '/.well-known/openid-configuration') {
      const clientId = env.OIDC_CLIENT_ID || 'not-configured';
      return new Response(JSON.stringify(oidcDiscovery(clientId), null, 2), {
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Cache-Control': 'no-store',
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

    if (url.pathname === '/.well-known/agent-skills/index.json') {
      const agentSkills = {
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "skills": [
          {
            "name": "amy-electric",
            "type": "skill-md",
            "description": "Interact with AMY Electric for electrical services, estimates, and business information in Greater Los Angeles",
            "url": "/.well-known/agent-skills/SKILL.md",
            "digest": "sha256:2bd5819ac20ede6f5e4c34325e56c77b310cf181f63d54c732603ba5ce03e420"
          }
        ]
      };
      return new Response(JSON.stringify(agentSkills, null, 2), {
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
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

    if ((url.pathname === '/.well-known/agent.json' || url.pathname === '/.well-known/agent-card.json') && request.method === 'GET') {
      return new Response(JSON.stringify(a2aAgentCard(), null, 2), {
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=3600' }
      });
    }

    if (url.pathname === '/a2a') {
      return a2aHandler(request);
    }

    if (url.pathname === '/api/health') {
      return new Response(JSON.stringify({ ok: true, service: 'amy-electric-site', time: new Date().toISOString() }), {
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
      });
    }

    if (url.pathname === '/openapi.json') {
      return new Response(JSON.stringify(contactApiSpec(), null, 2), {
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=3600' }
      });
    }

    if (url.pathname === '/api/docs') {
      return new Response(contactApiDocs(), {
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=3600' }
      });
    }

    if (url.pathname === '/.well-known/api-catalog') {
      const catalog = {
        linkset: [
          {
            anchor: 'https://amyelectric.com/api/contact',
            'service-desc': [{ href: 'https://amyelectric.com/openapi.json' }],
            'service-doc': [{ href: 'https://amyelectric.com/api/docs' }],
            status: [{ href: 'https://amyelectric.com/api/health' }]
          },
          {
            anchor: 'https://amyelectric.com/api/health',
            'service-desc': [{ href: 'https://amyelectric.com/openapi.json' }],
            'service-doc': [{ href: 'https://amyelectric.com/api/docs' }]
          }
        ]
      };
      return new Response(JSON.stringify(catalog, null, 2), {
        headers: { 'Content-Type': 'application/linkset+json', 'Cache-Control': 'public, max-age=3600' }
      });
    }

    const accept = request.headers.get('Accept') || '';
    if (accept.includes('text/markdown')) {
      const markdownPaths = {
        '/': '/markdown/home.md',
        '/index.html': '/markdown/home.md',
        '/about.html': '/markdown/about.md',
        '/services.html': '/markdown/services.md',
        '/contact.html': '/markdown/contact.md'
      };

      const mdPath = markdownPaths[url.pathname];
      if (mdPath) {
        const mdResponse = await env.ASSETS.fetch(new Request(
          new URL(mdPath, request.url).toString(),
          request
        ));
        if (mdResponse.ok) {
          return new Response(mdResponse.body, {
            headers: {
              'Content-Type': 'text/markdown; charset=utf-8',
              'Cache-Control': 'public, max-age=3600',
              'Vary': 'Accept'
            }
          });
        }
      }

      // Markdown for Agents output layout (frontmatter, body, JSON-LD block).
      const htmlResponse = await env.ASSETS.fetch(new Request(
        url.toString(),
        { headers: { 'Accept': 'text/html' } }
      ));
      const htmlType = htmlResponse.headers.get('Content-Type') || '';
      if (htmlResponse.ok && htmlType.includes('text/html')) {
        const html = await htmlResponse.text();
        const markdown = htmlToMarkdown(html, url.toString());
        return new Response(markdown, {
          headers: {
            'Content-Type': 'text/markdown; charset=utf-8',
            'Cache-Control': 'public, max-age=3600',
            'Vary': 'Accept',
            'x-markdown-tokens': String(Math.ceil(markdown.length / 4)),
            'x-original-tokens': String(Math.ceil(html.length / 4))
          }
        });
      }

      return htmlResponse;
    }

    const response = await env.ASSETS.fetch(request);

    if (url.pathname === '/' || url.pathname === '/index.html') {
      const headers = new Headers(response.headers);
      headers.append('Link', '</.well-known/mcp/server-card.json>; rel="service-desc"');
      headers.append('Link', '</.well-known/openid-configuration>; rel="describedby"');
      headers.append('Link', '</.well-known/http-message-signatures-directory>; rel="api-catalog"');
      headers.append('Link', '</robots.txt>; rel="service-doc"');
      headers.append('Vary', 'Accept');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    }

    const responseType = response.headers.get('Content-Type') || '';
    if (responseType.includes('text/html')) {
      const headers = new Headers(response.headers);
      headers.append('Vary', 'Accept');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    }

    return response;
  },
};
