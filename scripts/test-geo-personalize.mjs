#!/usr/bin/env node
/* Tests for js/src/08-geo-personalize.js — the consumer for the
 * window.AMY_GEO injection worker.js makes on the landing page. The injection
 * forces private/no-store for matched visitors; this module is what makes
 * that cache opt-out visible instead of free cost.
 * Run: node --test scripts/test-geo-personalize.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const file = 'js/src/08-geo-personalize.js';
const code = readFileSync(join(root, file), 'utf8');
const DEFAULT_EYEBROW = 'Los Angeles \u00b7 Residential & Commercial';

// Loads the module against a stub DOM. The module applies immediately when
// readyState is not 'loading', so the return value reflects what a visitor
// would see. eyebrow === false simulates a page without the hero.
function load(geo, { withHero = true, readyState = 'complete' } = {}) {
  const state = { textContent: DEFAULT_EYEBROW };
  const ctx = {
    module: { exports: {} },
    window: {},
    document: {
      readyState,
      addEventListener() {},
      querySelector: (sel) => (sel === '.hero-eyebrow' && withHero ? state : null),
    },
  };
  if (geo !== undefined) ctx.window.AMY_GEO = geo;
  vm.createContext(ctx);
  vm.runInContext(code, ctx, { filename: file });
  return { M: ctx.module.exports, state };
}

describe('cityOf', () => {
  it('returns the city only when the worker marked a match', () => {
    assert.equal(load({ city: 'Winnetka', matched: true }).M.cityOf(), 'Winnetka');
    assert.equal(load({ city: 'Winnetka', matched: false }).M.cityOf(), null);
    assert.equal(load({ matched: true }).M.cityOf(), null);
    assert.equal(load().M.cityOf(), null);
  });
});

describe('apply', () => {
  it('rewrites the hero eyebrow for a matched visitor', () => {
    const { state } = load({ city: 'Northridge', matched: true });
    assert.equal(state.textContent, 'Northridge \u00b7 Residential & Commercial');
  });

  it('keeps the default copy when there is no geo config', () => {
    for (const geo of [undefined, {}, { city: 'Sherman Oaks', matched: false }]) {
      assert.equal(load(geo).state.textContent, DEFAULT_EYEBROW);
    }
  });

  it('is a no-op on pages without the hero (no throw)', () => {
    const { state, M } = load({ city: 'Canoga Park', matched: true }, { withHero: false });
    assert.equal(state.textContent, DEFAULT_EYEBROW);
    assert.equal(M.cityOf(), 'Canoga Park');
  });
});
