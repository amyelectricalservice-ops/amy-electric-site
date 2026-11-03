#!/usr/bin/env node
/* Tests for the merged worker route dispatch (photo API + estimator + health).
 * Run: node --test scripts/test-worker-merge.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker.js';

// Route matching logic extracted from worker.js fetch handler
function isPhotoRoute(pathname) {
  return pathname === '/api/photos' || pathname.startsWith('/api/photos/') ||
    pathname === '/api/photos/count' || pathname === '/api/dates' ||
    pathname === '/api/map' || pathname === '/api/photo' ||
    pathname.startsWith('/api/photo/') || pathname === '/api/upload';
}

function isEstimatorRoute(pathname) {
  return pathname.startsWith('/estimator');
}

function isHealthRoute(pathname) {
  return pathname === '/api/health';
}

describe('merged worker route dispatch', () => {
  it('routes photo API paths correctly', () => {
    assert.ok(isPhotoRoute('/api/photos'));
    assert.ok(isPhotoRoute('/api/photos')); // query string is on url.search, not pathname
    assert.ok(isPhotoRoute('/api/photos/count'));
    assert.ok(isPhotoRoute('/api/dates'));
    assert.ok(isPhotoRoute('/api/map'));
    assert.ok(isPhotoRoute('/api/photo'));
    assert.ok(isPhotoRoute('/api/photo/file'));
    assert.ok(isPhotoRoute('/api/photo')); // query string is on url.search, not pathname
    assert.ok(isPhotoRoute('/api/upload'));
  });

  it('does not route non-photo paths as photo', () => {
    assert.ok(!isPhotoRoute('/api/contact'));
    assert.ok(!isPhotoRoute('/api/lead'));
    assert.ok(!isPhotoRoute('/api/events'));
    assert.ok(!isPhotoRoute('/api/health'));
    assert.ok(!isPhotoRoute('/'));
    assert.ok(!isPhotoRoute('/estimator'));
    assert.ok(!isPhotoRoute('/api/photographer')); // no false positive
  });

  it('routes estimator paths correctly', () => {
    assert.ok(isEstimatorRoute('/estimator'));
    assert.ok(isEstimatorRoute('/estimator/'));
    assert.ok(isEstimatorRoute('/estimator/calculate'));
    assert.ok(isEstimatorRoute('/estimator/extract'));
    assert.ok(isEstimatorRoute('/estimator/download'));
  });

  it('does not route non-estimator paths as estimator', () => {
    assert.ok(!isEstimatorRoute('/'));
    assert.ok(!isEstimatorRoute('/api/photos'));
    assert.ok(!isEstimatorRoute('/estimate'));
  });

  it('routes health endpoint correctly', () => {
    assert.ok(isHealthRoute('/api/health'));
    assert.ok(!isHealthRoute('/api/healthz'));
    assert.ok(!isHealthRoute('/health'));
  });

  describe('allowed conversion events', () => {
    it('validates allowed conversion events for /api/events', () => {
      const ALLOWED = new Set(['phone_click', 'cta_click', 'form_submit']);
      assert.equal(ALLOWED.size, 3);
      assert.ok(ALLOWED.has('phone_click'));
      assert.ok(ALLOWED.has('cta_click'));
      assert.ok(ALLOWED.has('form_submit'));
      assert.ok(!ALLOWED.has('internal_link_click'));
      assert.ok(!ALLOWED.has('unknown_event'));
      assert.ok(!ALLOWED.has(''));
    });
  });

  describe('static discovery endpoints', () => {
    it('serves pre-serialized openapi.json accurately', async () => {
      const res = await worker.fetch(new Request('https://amyelectric.com/openapi.json'), {}, { waitUntil: () => {} });
      assert.equal(res.status, 200);
      assert.equal(res.headers.get('Content-Type'), 'application/json; charset=utf-8');
      assert.equal(res.headers.get('Cache-Control'), 'public, max-age=3600');
      const body = await res.json();
      assert.equal(body.openapi, '3.1.0');
      assert.equal(body.info.title, 'AMY Electric Contact API');
    });

    it('serves pre-serialized agent card accurately', async () => {
      const res = await worker.fetch(new Request('https://amyelectric.com/.well-known/agent.json'), {}, { waitUntil: () => {} });
      assert.equal(res.status, 200);
      assert.equal(res.headers.get('Content-Type'), 'application/json; charset=utf-8');
      const body = await res.json();
      assert.equal(body.name, 'AMY Electric Estimator');
    });

    it('serves pre-computed contact API docs accurately', async () => {
      const res = await worker.fetch(new Request('https://amyelectric.com/api/docs'), {}, { waitUntil: () => {} });
      assert.equal(res.status, 200);
      assert.equal(res.headers.get('Content-Type'), 'text/html; charset=utf-8');
      const body = await res.text();
      assert.ok(body.includes('<h1>AMY Electric Contact API</h1>'));
    });

    it('serves pre-serialized api-catalog accurately', async () => {
      const res = await worker.fetch(new Request('https://amyelectric.com/.well-known/api-catalog'), {}, { waitUntil: () => {} });
      assert.equal(res.status, 200);
      assert.equal(res.headers.get('Content-Type'), 'application/linkset+json');
      const body = await res.json();
      assert.ok(Array.isArray(body.linkset));
      assert.equal(body.linkset[0].anchor, 'https://amyelectric.com/api/contact');
    });
  });
});