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
    assert.equal(r.priceRange.high, 900 + 400);
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
