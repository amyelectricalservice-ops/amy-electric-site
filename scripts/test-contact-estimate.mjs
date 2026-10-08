#!/usr/bin/env node
/* Server-side tests: the estimate attachment to POST /api/contact.
 * - valid estimate JSON is accepted and forwarded (GHL webhook + email text)
 * - garbage/absurd estimates are dropped WITHOUT failing the lead
 * - leads without estimate behave exactly as before
 * Never submits anything real: fetch is stubbed, env has no credentials.
 * Run: node --test scripts/test-contact-estimate.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
let src = readFileSync(join(root, 'contact-handler.js'), 'utf8');
src = src.replace(
  'export async function handleContact',
  'const handleContact = async function handleContact'
);
src += '\nthis.__C = { handleContact };';

const calls = [];
const ctx = {
  Response,
  URLSearchParams,
  console,
  fetch: async (url, opts) => {
    calls.push({ url: String(url), body: opts && opts.body });
    return { json: async () => ({ success: true }) };
  },
};
vm.createContext(ctx);
vm.runInContext(src, ctx, { filename: 'contact-handler.js' });
const handleContact = ctx.__C.handleContact;

const GOOD_ESTIMATE = JSON.stringify({
  service: 'panel-upgrade',
  rangeLow: 2500,
  rangeHigh: 4500,
  currency: 'USD',
  assumptions: ['200A service assumed'],
  permitNote: 'permit fees included in range',
});

function postForm(fields, env) {
  const fd = new FormData();
  for (const [k, v] of Object.entries(fields)) fd.append(k, v);
  const req = new Request('https://amyelectric.com/api/contact', { method: 'POST', body: fd });
  const pending = [];
  const waitUntil = (p) => { pending.push(p); };
  return { req, env: env || {}, waitUntil, pending };
}

describe('estimate attachment', () => {
  it('valid estimate is forwarded to GHL and email', async () => {
    calls.length = 0;
    const t = postForm(
      { name: 'Test User', phone: '(818) 302-5614', service: 'panel-upgrade', estimate: GOOD_ESTIMATE },
      { GHL_WEBHOOK_URL: 'https://example.test/hook' }
    );
    const res = await handleContact(t.req, t.env, t.waitUntil);
    assert.equal(res.status, 200);
    assert.equal((await res.json()).success, true);
    await Promise.all(t.pending);
    const ghl = calls.find((c) => c.url === 'https://example.test/hook');
    assert.ok(ghl, 'GHL webhook called');
    const payload = JSON.parse(ghl.body);
    assert.equal(JSON.parse(payload.estimate).rangeLow, 2500);
  });

  it('email text carries the range line', async () => {
    calls.length = 0;
    const t = postForm({ name: 'Test User', phone: '(818) 302-5614', estimate: GOOD_ESTIMATE }, {});
    const res = await handleContact(t.req, t.env, t.waitUntil);
    assert.equal(res.status, 200);
    await Promise.all(t.pending);
    const mc = calls.find((c) => c.url.includes('mailchannels'));
    assert.ok(mc, 'MailChannels called');
    assert.ok(mc.body.includes('Estimate: $2500'), 'range in email text');
    assert.ok(mc.body.includes('200A service assumed'), 'assumptions in email text');
  });

  it('garbage estimate is dropped without failing the lead', async () => {
    for (const bad of ['{nope', '[1,2', JSON.stringify({ rangeLow: -5, rangeHigh: 10 }), JSON.stringify({ rangeLow: 900, rangeHigh: 100 }), 'x'.repeat(5000)]) {
      calls.length = 0;
      const t = postForm(
        { name: 'Test User', phone: '(818) 302-5614', estimate: bad },
        { GHL_WEBHOOK_URL: 'https://example.test/hook' }
      );
      const res = await handleContact(t.req, t.env, t.waitUntil);
      assert.equal(res.status, 200, 'lead survives: ' + bad.slice(0, 20));
      assert.equal((await res.json()).success, true);
      await Promise.all(t.pending);
      const ghl = calls.find((c) => c.url === 'https://example.test/hook');
      assert.equal(JSON.parse(ghl.body).estimate, '', 'dropped, not forwarded');
    }
  });

  it('leads without estimate are unchanged', async () => {
    calls.length = 0;
    const t = postForm(
      { name: 'Test User', phone: '(818) 302-5614', service: 'panel-upgrade' },
      { GHL_WEBHOOK_URL: 'https://example.test/hook' }
    );
    const res = await handleContact(t.req, t.env, t.waitUntil);
    assert.equal((await res.json()).success, true);
    await Promise.all(t.pending);
    const ghl = calls.find((c) => c.url === 'https://example.test/hook');
    assert.equal(JSON.parse(ghl.body).estimate, '');
  });
});
