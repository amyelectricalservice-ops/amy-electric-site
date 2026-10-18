#!/usr/bin/env node
/* Tests for seo-worker/worker.js -- the edge wrapper in front of
 * amy-electric-site. The site Worker owns every page, sitemap and file; this
 * wrapper only forwards. It must never generate a page or rewrite the HTML.
 *
 * These guard the regressions a first deployed build caused:
 *   1. it generated /sitemap.xml, /robots.txt and /llms.txt itself, so the
 *      site's 306-URL sitemap never reached crawlers, and it generated its own
 *      /ev-charger-installation, /panel-upgrade, /lighting-installation,
 *      /electrician-<city> pages over the site's real ones, and
 *   2. it rewrote every proxied HTML page's <title> to one identical string
 *      and appended a second canonical/description/OG set.
 *
 * env.ORIGIN is the service binding to amy-electric-site; it is stubbed here so
 * the routing can be exercised without a live Worker.
 * Run: node --test scripts/test-seo-wrapper.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { default: wrapper } = await import(pathToFileURL(join(root, 'seo-worker/worker.js')).href);

// A stand-in for one of the site's real pages: one title, one description, one
// canonical, exactly as the site publishes it.
const REAL_PAGE = '<!DOCTYPE html><html lang="en"><head>'
  + '<title>About AMY Electric | Licensed C-10 Electrician Los Angeles</title>'
  + '<meta name="description" content="Learn about AMY Electric.">'
  + '<link rel="canonical" href="https://amyelectric.com/about"></head>'
  + '<body><h1>About</h1></body></html>';

const GENERIC_TITLE = 'AMY Electric | Los Angeles Electrician | EV Charger, Panel Upgrade & Rewiring';

// Stubbed ORIGIN binding. Paths in `missing` answer with the site's 404 page and
// status 404; every other path answers with `body`.
function stubOrigin(body, missing = []) {
  return {
    fetch: async (request) => {
      const path = new URL(request.url).pathname;
      if (missing.includes(path)) {
        return new Response('<!DOCTYPE html><html><head><title>404</title></head>'
          + '<body>Page not found</body></html>',
        { status: 404, headers: { 'Content-Type': 'text/html;charset=utf-8' } });
      }
      return new Response(body, { status: 200, headers: { 'Content-Type': 'text/html;charset=utf-8' } });
    },
  };
}

const get = (path, env) => wrapper.fetch(new Request('https://amyelectric.com' + path), env);

describe('seo-wrapper: it forwards, the site decides', () => {
  it('passes a real page through untouched', async () => {
    const resp = await get('/about', { ORIGIN: stubOrigin(REAL_PAGE) });
    const body = await resp.text();
    assert.equal(resp.status, 200);
    assert.match(body, /<title>About AMY Electric \| Licensed C-10 Electrician Los Angeles<\/title>/);
  });

  it('does not replace the title with the old generic string', async () => {
    const body = await (await get('/about', { ORIGIN: stubOrigin(REAL_PAGE) })).text();
    assert.ok(!body.includes(GENERIC_TITLE), 'generic title leaked into a real page');
  });

  it('does not append a duplicate canonical / description / OG set', async () => {
    const body = await (await get('/about', { ORIGIN: stubOrigin(REAL_PAGE) })).text();
    assert.equal((body.match(/rel="canonical"/g) || []).length, 1);
    assert.equal((body.match(/name="description"/g) || []).length, 1);
    assert.equal((body.match(/property="og:title"/g) || []).length, 0);
  });

  it('serves the site\'s own sitemap.xml', async () => {
    const sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset><url><loc>https://amyelectric.com/</loc></url></urlset>';
    const resp = await get('/sitemap.xml', { ORIGIN: stubOrigin(sitemap) });
    assert.equal(await resp.text(), sitemap);
  });

  it('never synthesises a sitemap, robots.txt or llms.txt', async () => {
    for (const path of ['/sitemap.xml', '/robots.txt', '/llms.txt']) {
      const resp = await get(path, { ORIGIN: stubOrigin(REAL_PAGE, [path]) });
      assert.equal(resp.status, 404, path + ' was synthesised');
    }
  });

  it('does not shadow the site\'s service and city pages', async () => {
    const paths = [
      '/ev-charger-installation', '/panel-upgrade', '/lighting-installation',
      '/electrician-pasadena', '/ev-charger-installation-sherman-oaks',
      '/panel-upgrade-burbank',
    ];
    for (const path of paths) {
      const body = await (await get(path, { ORIGIN: stubOrigin(REAL_PAGE) })).text();
      assert.match(body, /<title>About AMY Electric/, path + ' was shadowed');
    }
  });

  it('does not generate the pages only the old build had', async () => {
    // Nothing links these and no sitemap listed them; they now fall through to
    // the site, which 404s them with its own 404 page.
    const paths = [
      '/faq', '/rewiring', '/troubleshooting', '/electrical-inspection',
      '/electrician-sherman-oaks', '/panel-upgrade-northridge',
    ];
    for (const path of paths) {
      const resp = await get(path, { ORIGIN: stubOrigin(REAL_PAGE, [path]) });
      assert.equal(resp.status, 404, path + ' was generated');
    }
  });

  it('leaves the site\'s 404 alone', async () => {
    const path = '/no-such-page-xyz';
    const resp = await get(path, { ORIGIN: stubOrigin(REAL_PAGE, [path]) });
    assert.equal(resp.status, 404);
    assert.match(await resp.text(), /Page not found/);
  });

  it('keeps the CORS headers on API responses', async () => {
    const resp = await get('/api/health', { ORIGIN: stubOrigin('{"ok":true}') });
    assert.equal(resp.headers.get('Access-Control-Allow-Origin'), 'https://amyelectric.com');
    assert.equal(resp.headers.get('Access-Control-Allow-Methods'), 'GET, POST, OPTIONS');
  });
});
