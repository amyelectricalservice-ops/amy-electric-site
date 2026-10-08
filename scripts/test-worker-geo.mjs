#!/usr/bin/env node
/* Tests for the worker.js geo-personalization block (GEO_TARGET_AREAS,
 * matchTargetCity, visitorCity, injectGeo, landing-only htmlResponse wiring).
 * request.cf.city is edge-supplied, so every branch is exercised with stub
 * requests instead of a live foundation.
 * Run: node --test scripts/test-worker-geo.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
let src = readFileSync(join(root, 'worker.js'), 'utf8');
src = src.replace(
  "import { handleContact } from './contact-handler.js';",
  'const handleContact = async () => new Response("stubbed", { status: 500 });'
);
src = src.replace('export default', 'const __EXPORT_DEFAULT =');
src += '\nthis.__T = { fetch: __EXPORT_DEFAULT.fetch, matchTargetCity, injectGeo, visitorCity, GEO_TARGET_AREAS, GEO_NO_STORE, HTML_CACHE_CONTROL };';

const ctx = { URL, Response, Headers, crypto: webcrypto, console, TextEncoder, TextDecoder };
vm.createContext(ctx);
vm.runInContext(src, ctx, { filename: 'worker.js' });
const T = ctx.__T;

const MIN_HTML = '<!DOCTYPE html><html><head><title>t</title></head>'
  + '<body><header><h1>hi</h1></header><p>x</p></body></html>';

function stubReq(path, city) {
  const headers = {
    get(n) {
      if (n === 'Accept') return 'text/html';
      return null;
    },
  };
  const req = { url: 'https://amyelectric.com' + path, headers, method: 'GET' };
  if (city !== undefined) req.cf = { city };
  return req;
}

function stubEnv(html) {
  return {
    ASSETS: {
      fetch: async () => new Response(html === undefined ? MIN_HTML : html, {
        status: 200,
        headers: { 'Content-Type': 'text/html' },
      }),
    },
  };
}

describe('matchTargetCity', () => {
  it('matches the three launch areas case-insensitively', () => {
    assert.equal(T.matchTargetCity('Northridge'), 'Northridge');
    assert.equal(T.matchTargetCity('winnetka'), 'Winnetka');
    assert.equal(T.matchTargetCity('  CANOGA PARK '), 'Canoga Park');
  });
  it('rejects everything else, including injection attempts', () => {
    assert.equal(T.matchTargetCity('Los Angeles'), null);
    assert.equal(T.matchTargetCity(''), null);
    assert.equal(T.matchTargetCity('   '), null);
    assert.equal(T.matchTargetCity('Northridge<script>alert(1)</script>'), null);
    assert.equal(T.matchTargetCity('Northridge, CA'), null);
    assert.equal(T.matchTargetCity(null), null);
    assert.equal(T.matchTargetCity(undefined), null);
    assert.equal(T.matchTargetCity(42), null);
  });
});

describe('visitorCity', () => {
  it('returns null without edge cf data (local dev)', () => {
    assert.equal(T.visitorCity(stubReq('/')), null);
    assert.equal(T.visitorCity({ url: 'https://amyelectric.com/', headers: { get: () => null } }), null);
  });
  it('passes cf.city through the allowlist', () => {
    assert.equal(T.visitorCity(stubReq('/', 'Winnetka')), 'Winnetka');
    assert.equal(T.visitorCity(stubReq('/', 'Burbank')), null);
  });
});

describe('injectGeo', () => {
  it('sets the header attribute and exposes window.AMY_GEO', () => {
    const out = T.injectGeo(MIN_HTML, 'Northridge');
    assert.ok(out.includes('<header data-service-city="Northridge">'), 'header attribute');
    assert.ok(out.includes('window.AMY_GEO={"city":"Northridge","matched":true'), 'config object');
    assert.ok(out.includes('"areas":["Northridge","Winnetka","Canoga Park"]'), 'areas list');
  });
  it('still injects the config when no <header> tag exists', () => {
    const out = T.injectGeo('<html><body><p>x</p></body></html>', 'Canoga Park');
    assert.ok(out.includes('window.AMY_GEO={"city":"Canoga Park"'), 'config object');
  });
  it('never emits raw input (canonical values only)', () => {
    const out = T.injectGeo(MIN_HTML, T.matchTargetCity('winnetka'));
    assert.ok(!out.includes('winnetka">'), 'lowercase raw form absent');
  });
});

describe('landing fetch wiring', () => {
  it('matched city on / gets injection + uncacheable response', async () => {
    const res = await T.fetch(stubReq('/', 'Canoga Park'), stubEnv());
    assert.equal(res.status, 200);
    const body = await res.text();
    assert.ok(body.includes('<header data-service-city="Canoga Park">'));
    assert.ok(body.includes('window.AMY_GEO='));
    const cc = res.headers.get('Cache-Control');
    assert.equal(cc, T.GEO_NO_STORE);
    assert.ok(!cc.includes('s-maxage'), 'no shared edge cache');
  });

  it('matched city on /index.html behaves the same', async () => {
    const res = await T.fetch(stubReq('/index.html', 'Northridge'), stubEnv());
    const body = await res.text();
    assert.ok(body.includes('data-service-city="Northridge"'));
    assert.equal(res.headers.get('Cache-Control'), T.GEO_NO_STORE);
  });

  it('non-target city keeps the shared cache policy with no injection', async () => {
    const res = await T.fetch(stubReq('/', 'Los Angeles'), stubEnv());
    const body = await res.text();
    assert.ok(!body.includes('data-service-city'));
    assert.ok(!body.includes('window.AMY_GEO'));
    assert.equal(res.headers.get('Cache-Control'), T.HTML_CACHE_CONTROL);
  });

  it('missing cf data keeps the shared cache policy', async () => {
    const res = await T.fetch(stubReq('/'), stubEnv());
    const body = await res.text();
    assert.ok(!body.includes('window.AMY_GEO'));
    assert.equal(res.headers.get('Cache-Control'), T.HTML_CACHE_CONTROL);
  });

  it('non-landing pages are never personalized', async () => {
    const res = await T.fetch(stubReq('/panel-upgrade', 'Northridge'), stubEnv());
    const body = await res.text();
    assert.ok(!body.includes('window.AMY_GEO'));
    assert.ok(!body.includes('data-service-city'));
    assert.equal(res.headers.get('Cache-Control'), T.HTML_CACHE_CONTROL);
  });
});
