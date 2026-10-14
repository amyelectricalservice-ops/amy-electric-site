#!/usr/bin/env node
/* Tests for the worker.js image-optimization block (WebP negotiation,
 * ?w= responsive widths, Images-binding transform, static fallback).
 * Run: node --test scripts/test-worker-images.mjs
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
src = src.replace(/^import .*$/gm, '');
src += '\nconst handleLead = async () => new Response("stubbed", { status: 500 });'
  + '\nconst handleContact = async () => new Response("stubbed", { status: 500 });';
src = src.replace('export default', 'const __EXPORT_DEFAULT =');
src += '\nthis.__T = { fetch: __EXPORT_DEFAULT.fetch, isImagePath, clientSupportsWebP, snapWidth, variantCandidates, serveImage, IMG_WIDTHS, IMG_CACHE_CONTROL };';

const ctx = { URL, Response, Headers, Request, console, TextEncoder, TextDecoder, crypto: webcrypto };
vm.createContext(ctx);
vm.runInContext(src, ctx, { filename: 'worker.js' });
const T = ctx.__T;

// Static asset set mimicking the repo's mixed naming (-400 vs -400w).
const FILES = new Map([
  ['/img/hero-electrician.jpg', { body: 'JPG-FULL', type: 'image/jpeg' }],
  ['/img/hero-electrician-400.webp', { body: 'WEBP-400', type: 'image/webp' }],
  ['/img/hero-electrician-400.jpg', { body: 'JPG-400', type: 'image/jpeg' }],
  ['/img/hero-electrician-800w.webp', { body: 'WEBP-800', type: 'image/webp' }],
  ['/img/hero-electrician-800w.jpg', { body: 'JPG-800', type: 'image/jpeg' }],
  ['/img/hero-electrician.webp', { body: 'WEBP-FULL', type: 'image/webp' }],
  ['/img/gallery/g-1200w.jpg', { body: 'G-JPG', type: 'image/jpeg' }],
  ['/img/gallery/g-400w.webp', { body: 'G-WEBP-400', type: 'image/webp' }],
]);

function stubEnvNoImages() {
  return {
    ASSETS: {
      fetch: async (req) => {
        const path = new URL(req.url).pathname;
        const f = FILES.get(path);
        if (!f) return new Response('nf', { status: 404 });
        return new Response(f.body, { status: 200, headers: { 'Content-Type': f.type } });
      },
    },
  };
}

function req(path, accept) {
  return new Request('https://amyelectric.com' + path, {
    headers: accept ? { Accept: accept } : {},
  });
}
const IMG_ACCEPT = 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8';
const ctxStub = { waitUntil() {} };

describe('isImagePath', () => {
  it('accepts /img/* raster files including gallery', () => {
    assert.equal(T.isImagePath('/img/hero-electrician.jpg'), true);
    assert.equal(T.isImagePath('/img/gallery/g-1200w.jpg'), true);
    assert.equal(T.isImagePath('/img/a.PNG'), true);
  });
  it('rejects non-img paths, traversal, and non-raster suffixes', () => {
    assert.equal(T.isImagePath('/css/style.min.css'), false);
    assert.equal(T.isImagePath('/img/../worker.js'), false);
    assert.equal(T.isImagePath('/img/photo.svg'), false);
    assert.equal(T.isImagePath(null), false);
  });
});

describe('clientSupportsWebP', () => {
  it('detects webp and avif (avif browsers decode webp)', () => {
    assert.equal(T.clientSupportsWebP(req('/x', IMG_ACCEPT)), true);
    assert.equal(T.clientSupportsWebP(req('/x', 'image/avif,*/*;q=0.8')), true);
    assert.equal(T.clientSupportsWebP(req('/x', 'image/webp')), true);
  });
  it('rejects legacy accept headers', () => {
    assert.equal(T.clientSupportsWebP(req('/x', 'image/jpeg')), false);
    assert.equal(T.clientSupportsWebP(req('/x')), false);
  });
});

describe('snapWidth', () => {
  it('snaps up to the nearest pre-generated width', () => {
    assert.equal(T.snapWidth('100'), 400);
    assert.equal(T.snapWidth('400'), 400);
    assert.equal(T.snapWidth('500'), 800);
    assert.equal(T.snapWidth('1200'), 1200);
  });
  it('clamps to 100..1200 and rejects garbage', () => {
    assert.equal(T.snapWidth('1'), 400);
    assert.equal(T.snapWidth('2000'), 1200);
    assert.equal(T.snapWidth('abc'), null);
    assert.equal(T.snapWidth(null), null);
  });
});

describe('serveImage static fallback (no IMAGES binding)', () => {
  it('serves sibling .webp when the client supports it', async () => {
    const res = await T.serveImage(req('/img/hero-electrician.jpg', IMG_ACCEPT), stubEnvNoImages(), ctxStub);
    assert.ok(res, 'expected a variant response');
    assert.equal(await res.text(), 'WEBP-FULL');
    assert.equal(res.headers.get('Content-Type'), 'image/webp');
    assert.equal(res.headers.get('Cache-Control'), T.IMG_CACHE_CONTROL);
    assert.equal(res.headers.get('Vary'), 'Accept');
  });

  it('returns null for legacy clients so the original passes through', async () => {
    const res = await T.serveImage(req('/img/hero-electrician.jpg', 'image/jpeg'), stubEnvNoImages(), ctxStub);
    assert.equal(res, null);
  });

  it('?w=500 snaps to 800 and prefers the -800w webp variant', async () => {
    const res = await T.serveImage(req('/img/hero-electrician.jpg?w=500', IMG_ACCEPT), stubEnvNoImages(), ctxStub);
    assert.ok(res);
    assert.equal(await res.text(), 'WEBP-800');
  });

  it('?w=300 without webp falls back to the same-format -400 file (mixed -400 naming)', async () => {
    const res = await T.serveImage(req('/img/hero-electrician.jpg?w=300', 'image/jpeg'), stubEnvNoImages(), ctxStub);
    assert.ok(res);
    assert.equal(await res.text(), 'JPG-400');
  });

  it('returns null when no variant exists (caller serves the original)', async () => {
    const res = await T.serveImage(req('/img/missing.jpg?w=400', IMG_ACCEPT), stubEnvNoImages(), ctxStub);
    assert.equal(res, null);
  });

  it('ignores non-img paths and traversal', async () => {
    assert.equal(await T.serveImage(req('/worker.js', IMG_ACCEPT), stubEnvNoImages(), ctxStub), null);
    assert.equal(await T.serveImage(req('/img/../worker.js', IMG_ACCEPT), stubEnvNoImages(), ctxStub), null);
  });
});

describe('serveImage with IMAGES binding', () => {
  function imagesEnv(seen) {
    const base = stubEnvNoImages();
    return {
      ...base,
      IMAGES: {
        input(buf) {
          seen.bytes = buf.byteLength;
          return {
            transform(opts) {
              seen.opts = opts;
              return { output: () => ({ response: () => new Response('TRANSFORMED', { headers: { 'Content-Type': 'image/webp' } }) }) };
            },
          };
        },
      },
    };
  }

  it('transforms arbitrary widths with format:auto + scale-down, cached immutable', async () => {
    const seen = {};
    const res = await T.serveImage(req('/img/hero-electrician.jpg?w=600', IMG_ACCEPT), imagesEnv(seen), ctxStub);
    assert.ok(res);
    assert.equal(await res.text(), 'TRANSFORMED');
    assert.equal(seen.opts.width, 800, '600 snaps to 800');
    assert.equal(seen.opts.format, 'auto');
    assert.equal(seen.opts.fit, 'scale-down');
    assert.equal(res.headers.get('Cache-Control'), T.IMG_CACHE_CONTROL);
  });

  it('falls back to static variants when the transform throws', async () => {
    const base = stubEnvNoImages();
    const env = {
      ...base,
      IMAGES: { input() { throw new Error('5403 transform failed'); } },
    };
    const res = await T.serveImage(req('/img/hero-electrician.jpg', IMG_ACCEPT), env, ctxStub);
    assert.ok(res);
    assert.equal(await res.text(), 'WEBP-FULL');
  });
});

describe('fetch wiring', () => {
  it('image responses bypass the HTML beacon path', async () => {
    const res = await T.fetch(req('/img/hero-electrician.jpg', IMG_ACCEPT), stubEnvNoImages(), ctxStub);
    assert.equal(res.status, 200);
    assert.equal(res.headers.get('Content-Type'), 'image/webp');
    assert.ok(!(await res.text()).includes('beacon.min.js'), 'no RUM beacon in images');
  });
});
