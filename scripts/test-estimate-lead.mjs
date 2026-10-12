#!/usr/bin/env node
/* Tests for js/src/07-estimate-lead.js (pure mapping + payload builder).
 * DOM wiring is guarded and untested here; AMY_ESTIMATE comes from 05+06.
 * Run: node --test scripts/test-estimate-lead.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const ctx = { module: { exports: {} } };
vm.createContext(ctx);
for (const f of ['js/src/05-estimate-data.js', 'js/src/06-estimate-engine.js', 'js/src/07-estimate-lead.js']) {
  vm.runInContext(readFileSync(join(root, f), 'utf8'), ctx, { filename: f });
}
const L = ctx.module.exports;

describe('specForService', () => {
  it('maps priced services, nulls the rest', () => {
    assert.ok(L.specForService('ev-charger'));
    assert.ok(L.specForService('tesla-charger'));
    assert.ok(L.specForService('panel-upgrade'));
    assert.ok(L.specForService('rewiring'));
    assert.ok(L.specForService('lighting'));
    assert.ok(L.specForService('generator'));
    assert.equal(L.specForService('electrical-repair'), null);
    assert.equal(L.specForService('commercial'), null);
    assert.equal(L.specForService('surge-protection'), null);
    assert.equal(L.specForService(''), null);
    assert.equal(L.specForService('__proto__'), null);
  });
});

describe('buildLeadEstimate', () => {
  it('ev-charger spans subtypes plus permit', () => {
    const p = L.buildLeadEstimate('ev-charger');
    assert.equal(p.rangeLow, 350 + 150);
    assert.equal(p.rangeHigh, 1200 + 400);
    assert.equal(p.currency, 'USD');
    assert.ok(p.assumptions.some((a) => a.includes('200A')));
    assert.ok(p.assumptions.some((a) => a.includes('30ft')));
  });

  it('single-service payloads carry engine totals', () => {
    assert.deepEqual(
      [L.buildLeadEstimate('panel-upgrade').rangeLow, L.buildLeadEstimate('panel-upgrade').rangeHigh],
      [2500, 4500]
    );
    // Matches the published Tesla page ($500-$1,200 incl. permit) and the
    // homepage estimator widget, not the older EV-page-only range.
    assert.deepEqual(
      [L.buildLeadEstimate('tesla-charger').rangeLow, L.buildLeadEstimate('tesla-charger').rangeHigh],
      [500, 1200]
    );
    assert.equal(L.buildLeadEstimate('tesla-charger').permitNote, 'permit fees included in range');
    assert.deepEqual(
      [L.buildLeadEstimate('generator').rangeLow, L.buildLeadEstimate('generator').rangeHigh],
      [800, 1500]
    );
  });

  it('permit notes never contradict the engine', () => {
    // Panel: permit is inside the published range (panel-upgrade.html).
    assert.equal(L.buildLeadEstimate('panel-upgrade').permitNote, 'permit fees included in range');
    // Unpublished scopes say "confirmed on site", never "included".
    for (const svc of ['rewiring', 'lighting', 'generator']) {
      assert.equal(L.buildLeadEstimate(svc).permitNote, 'permit fees confirmed on site');
    }
    // The EV span always contains permit (added for NEMA/hardwired, built into
    // Tesla), so its note reflects the total, not a missing line item.
    assert.equal(L.buildLeadEstimate('ev-charger').permitNote, 'permit fees included in range');
  });

  it('unmapped services yield null (stale fields must be removed)', () => {
    assert.equal(L.buildLeadEstimate('electrical-repair'), null);
    assert.equal(L.buildLeadEstimate('dedicated-circuit'), null);
    assert.equal(L.buildLeadEstimate(''), null);
  });

  it('payload is JSON-safe and labeled indicative', () => {
    const p = L.buildLeadEstimate('rewiring');
    assert.equal(p.rangeLow, 8000);
    JSON.parse(JSON.stringify(p));
    assert.match(p.generatedBy, /indicative/);
    assert.ok(p.permitNote.length > 0);
  });
});
