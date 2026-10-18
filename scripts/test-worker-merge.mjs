#!/usr/bin/env node
/* Tests for the merged worker route dispatch (photo API + estimator + health).
 * Run: node --test scripts/test-worker-merge.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

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
});