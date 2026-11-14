#!/usr/bin/env node
/* Guard: Worker modules living at the repo root must not be public assets.
 *
 * The ASSETS binding serves `directory: "."`, so every root-level file is
 * public unless .assetsignore excludes it. On 2026-11-14 worker.js and
 * contact-handler.js were excluded but eleven other modules were not — their
 * full source (admin API shape, lead scoring, EspoCRM field mapping, GBP
 * schedule) came back with a 200 from /crm-handler.js, /lead-store.js and
 * friends.
 *
 * Run: node --test scripts/test-assets-ignore.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

function patterns() {
  return readFileSync(join(ROOT, '.assetsignore'), 'utf8')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line && !line.startsWith('#'));
}

function matches(entry, pattern) {
  if (!pattern.includes('*')) return entry === pattern;
  const rx = new RegExp(
    '^' + pattern.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*') + '$'
  );
  return rx.test(entry);
}

describe('assets exposure', () => {
  it('excludes every root-level Worker module from public assets', () => {
    const pats = patterns();
    const modules = readdirSync(ROOT).filter(f => /\.(js|ts|mjs)$/.test(f));
    assert.ok(modules.length > 0, 'expected Worker modules at the repo root');

    const exposed = modules.filter(f => !pats.some(p => matches(f, p)));
    assert.deepEqual(exposed, [], `add to .assetsignore: ${exposed.join(', ')}`);
  });

  it('does not exclude the public site bundles', () => {
    const pats = patterns();
    for (const asset of ['js/site.min.js', 'js/estimator.min.js', 'css/style.min.css']) {
      assert.ok(!pats.some(p => matches(asset, p)), `${asset} must stay public`);
    }
  });
});
