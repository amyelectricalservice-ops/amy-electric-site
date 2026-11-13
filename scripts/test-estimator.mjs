#!/usr/bin/env node
/* Tests for js/estimator.js, plus value parity with js/src/05-estimate-data.js
 * for the services both cover.
 * Run: node --test scripts/test-estimator.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

function loadStandalone(path) {
  const code = readFileSync(join(root, path), 'utf8');
  const sb = { module: { exports: {} } };
  vm.createContext(sb);
  vm.runInContext(code + '\nthis.__M = module.exports;', sb, { filename: path });
  return sb.__M;
}

function loadEngineData() {
  const sb = {};
  vm.createContext(sb);
  vm.runInContext(readFileSync(join(root, 'js/src/05-estimate-data.js'), 'utf8'), sb);
  return sb.AMY_ESTIMATE_DATA;
}

const E = loadStandalone('js/estimator.js');
const DATA = loadEngineData();

describe('panel-upgrade', () => {
  it('200A returns the canonical range with permit included', () => {
    const r = E.estimateProject({ projectType: 'panel-upgrade', serviceAmperage: '200A', linearDistance: 40 });
    assert.equal(r.priceRange.low, 2500);
    assert.equal(r.priceRange.high, 4500);
    assert.equal(r.priceRange.currency, 'USD');
    assert.equal(r.distanceBand, 'medium');
    assert.equal(r.permit.required, true);
    assert.ok(r.materials.some((m) => m.qty === 40 && m.unit === 'ft'), 'wire qty tracks distance');
    assert.ok(r.exclusions.length > 0, 'unpriced parts surfaced');
  });

  it('100A like-for-like uses its own range', () => {
    const r = E.estimateProject({ projectType: 'panel-upgrade', serviceAmperage: '100A', linearDistance: 10 });
    assert.equal(r.priceRange.low, 1500);
    assert.equal(r.priceRange.high, 2500);
    assert.equal(r.distanceBand, 'short');
  });
});

describe('ev-charger', () => {
  it('base excludes permit; permit itemized; unit customer-supplied', () => {
    const r = E.estimateProject({ projectType: 'ev-charger', serviceAmperage: '200A', linearDistance: 20 });
    assert.equal(r.priceRange.low, 350 + 150);
    assert.equal(r.priceRange.high, 1200 + 400);
    assert.equal(r.labor.low, 350);
    const unit = r.materials.find((m) => m.item === 'Level 2 charger unit');
    assert.equal(unit.scope, 'customer-supplied');
    assert.ok(!r.exclusions.some((e) => e.item === 'Level 2 charger unit'), 'priced unit is not an exclusion');
  });

  it('100A service flags the possible panel-upgrade adder', () => {
    const r = E.estimateProject({ projectType: 'ev-charger', serviceAmperage: '100A', linearDistance: 60 });
    assert.equal(r.distanceBand, 'long');
    assert.equal(r.priceRange.low, 350 + 150 + 200);
    const adder = r.possibleAdders.find((a) => a.low === 2500);
    assert.ok(adder, 'panel-upgrade adder listed with condition, not totalled');
  });
});

describe('subpanel-installation', () => {
  it('range + unpublished-permit exclusion', () => {
    const r = E.estimateProject({ projectType: 'subpanel-installation', serviceAmperage: '200A', linearDistance: 30 });
    assert.equal(r.priceRange.low, 1200);
    assert.equal(r.priceRange.high, 2500);
    assert.equal(r.permit.required, true);
    assert.ok(r.exclusions.some((e) => e.item === 'Permit fees'), 'unpublished permit flagged');
    assert.ok(r.materials.some((m) => m.qty === 30 && m.unit === 'ft'), 'feeder qty tracks distance');
  });
});

describe('validation', () => {
  it('rejects bad input with valid-value errors', () => {
    assert.throws(() => E.estimateProject({ projectType: 'solar', serviceAmperage: '200A', linearDistance: 10 }), /valid: panel-upgrade/);
    assert.throws(() => E.estimateProject({ projectType: 'panel-upgrade', serviceAmperage: '400A', linearDistance: 10 }), /valid: 100A, 200A/);
    assert.throws(() => E.estimateProject({ projectType: 'panel-upgrade', serviceAmperage: '200A', linearDistance: -5 }), /non-negative/);
    assert.throws(() => E.estimateProject(null), /input object/);
  });

  it('distance bands at the documented thresholds', () => {
    assert.equal(E.distanceBand(25).band, 'short');
    assert.equal(E.distanceBand(26).band, 'medium');
    assert.equal(E.distanceBand(50).band, 'medium');
    assert.equal(E.distanceBand(51).band, 'long');
  });
});

describe('parity with the bundled engine data', () => {
  const byId = (id) => DATA.SERVICES.find((s) => s.id === id);
  it('shared service ranges agree', () => {
    assert.equal(byId('panel-200a-replacement').baseLow, 2500);
    assert.equal(byId('panel-200a-replacement').baseHigh, 4500);
    const r = E.estimateProject({ projectType: 'subpanel-installation', serviceAmperage: '200A', linearDistance: 0 });
    assert.equal(r.priceRange.low, byId('panel-subpanel-add').baseLow);
    assert.equal(r.priceRange.high, byId('panel-subpanel-add').baseHigh);
  });

  it('shared adder/credit/permit values agree', () => {
    const trench = DATA.ADDERS.find((a) => a.id === 'adder-trenching');
    assert.deepEqual([trench.low, trench.high], [800, 2500]);
    const p = DATA.PERMITS.find((x) => x.id === 'permit-ev');
    assert.deepEqual([p.low, p.high], [150, 400]);
  });
});

/* js/estimator.js is not loaded by any page — the homepage widget lazy-loads
 * js/estimator.min.js, which is BUILT from js/estimator-widget.js by
 * scripts/build-estimator.py. These assertions compare the widget source
 * against the engine so the two price tables cannot drift apart again
 * (the tesla 450-750 vs 500-1200 split this repo shipped for a while). */
describe('widget source parity with the engine', () => {
  const W = loadStandalone('js/estimator-widget.js');
  const byId = (id) => DATA.SERVICES.find((s) => s.id === id);

  it('charger rows match the engine', () => {
    const tesla = W.PRICES['tesla-wall'];
    assert.deepEqual([tesla.baseLow, tesla.baseHigh], [byId('ev-tesla-wall').baseLow, byId('ev-tesla-wall').baseHigh]);
    const hardwired = W.PRICES.hardwired;
    assert.deepEqual([hardwired.baseLow, hardwired.baseHigh], [byId('ev-hardwired').baseLow, byId('ev-hardwired').baseHigh]);
  });

  it('NEMA row covers the engine range (widget quotes the wider circuit scope)', () => {
    // Outlet-only install publishes at $350-$600 (ev-charger-installation) and
    // the charger-circuit scope at $350-$900 (geo pages), so the widget's upper
    // bound is legitimately higher — but never below the engine's.
    const nema = W.PRICES['nema14-50'];
    assert.equal(nema.baseLow, byId('ev-nema-1450').baseLow);
    assert.ok(nema.baseHigh >= byId('ev-nema-1450').baseHigh, 'widget NEMA high ' + nema.baseHigh);
  });

  it('panel row matches the engine', () => {
    assert.deepEqual([W.PANEL.low, W.PANEL.high],
      [byId('panel-200a-replacement').baseLow, byId('panel-200a-replacement').baseHigh]);
  });

  it('rewiring tiers match the engine size tiers', () => {
    for (const key of ['small', 'medium', 'large']) {
      const tier = DATA.SIZE_TIERS.find((t) => t.id === 'rewiring-' + key);
      assert.ok(tier, 'engine tier rewiring-' + key);
      assert.deepEqual([W.REWIRING_TIERS[key].low, W.REWIRING_TIERS[key].high], [tier.low, tier.high]);
    }
  });
});

describe('widget quotes', () => {
  const W = loadStandalone('js/estimator-widget.js');

  it('EV: adders stack in the published order', () => {
    const q = W.buildQuote({ service: 'ev-charger', charger: 'tesla-wall', panel: '100a', distance: 'long', location: 'outdoor' });
    assert.equal(q.kind, 'estimate');
    assert.equal(q.low, 500 + 200 + 50 + 2500);
    assert.equal(q.high, 1200 + 300 + 150 + 4500);
    assert.equal(q.parts.length, 4);
  });

  it('EV: a 200A panel with a short indoor run adds nothing', () => {
    const q = W.buildQuote({ service: 'ev-charger', charger: 'nema14-50', panel: '200a', distance: 'short', location: 'indoor' });
    assert.deepEqual([q.low, q.high], [350, 900]);
  });

  it('panel upgrade and rewiring return real ranges', () => {
    assert.deepEqual([W.buildQuote({ service: 'panel-upgrade' }).low, W.buildQuote({ service: 'panel-upgrade' }).high], [2500, 4500]);
    const rw = W.buildQuote({ service: 'rewiring', size: 'large' });
    assert.deepEqual([rw.low, rw.high], [10000, 15000]);
  });

  it('"Other" returns a custom quote instead of a dead end', () => {
    // Regression guard: the old bundle returned null here, which hid the lead
    // form AND the phone number, so rewiring/repair leads vanished silently.
    const q = W.buildQuote({ service: 'other' });
    assert.equal(q.kind, 'custom');
    assert.ok(q.reason && q.reason.length > 20);
  });
});

describe('built bundle is in sync with the source', () => {
  it('js/estimator.min.js exposes the same version and prices', () => {
    const src = loadStandalone('js/estimator-widget.js');
    const min = loadStandalone('js/estimator.min.js');
    assert.equal(min.VERSION, src.VERSION);
    assert.deepEqual(
      JSON.parse(JSON.stringify(min.PRICES)),
      JSON.parse(JSON.stringify(src.PRICES))
    );
    assert.equal(typeof min.mount, 'function');
    assert.equal(typeof min.buildQuote, 'function');
  });
});
