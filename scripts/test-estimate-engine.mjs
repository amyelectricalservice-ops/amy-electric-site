#!/usr/bin/env node
/* Tests for js/src/05-estimate-data.js + 06-estimate-engine.js,
 * plus JS/SQL parity with scripts/estimate-schema.sql.
 * Run: node --test scripts/test-estimate-engine.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const ctx = {};
vm.createContext(ctx);
for (const f of ['js/src/05-estimate-data.js', 'js/src/06-estimate-engine.js']) {
  vm.runInContext(readFileSync(join(root, f), 'utf8'), ctx, { filename: f });
}
const ENG = ctx.AMY_ESTIMATE;
const DATA = ctx.AMY_ESTIMATE_DATA;

describe('engine math', () => {
  it('panel base range, qty 1', () => {
    const r = ENG.calcEstimate({ serviceId: 'panel-200a-replacement' });
    assert.equal(r.totalLow, 2500);
    assert.equal(r.totalHigh, 4500);
    assert.equal(r.exclusions.length, 1); // unpublished permit
  });

  it('tesla + panel adder + permit', () => {
    const r = ENG.calcEstimate({
      serviceId: 'ev-tesla-wall',
      adderIds: ['adder-ev-panel-upgrade'],
      includePermit: true,
    });
    assert.equal(r.totalLow, 450 + 2500 + 150);
    assert.equal(r.totalHigh, 750 + 4500 + 400);
    assert.equal(r.exclusions.length, 0);
  });

  it('lighting qty 6', () => {
    const r = ENG.calcEstimate({ serviceId: 'lighting-per-light', qty: 6, includePermit: false });
    assert.equal(r.totalLow, 750);
    assert.equal(r.totalHigh, 1500);
  });

  it('rewiring tier by sqft', () => {
    const r = ENG.calcEstimate({ serviceId: 'rewiring-base', sizeSqft: 1600, includePermit: false });
    assert.equal(r.totalLow, 6000);
    assert.equal(r.totalHigh, 12000);
    assert.match(r.lines[0].name, /Medium home/);
  });

  it('material lines use unit pricing', () => {
    const r = ENG.calcEstimate({
      serviceId: 'ev-hardwired',
      materials: [{ id: 'evse-unit', qty: 1 }],
      includePermit: false,
    });
    assert.equal(r.totalLow, 500 + 400);
    assert.equal(r.totalHigh, 900 + 750);
  });

  it('unknown ids throw; bad qty throws', () => {
    assert.throws(() => ENG.calcEstimate({ serviceId: 'nope' }), /unknown SERVICES id/);
    assert.throws(() => ENG.calcEstimate({ serviceId: 'ev-nema-1450', qty: 0 }), /qty must be >= 1/);
    assert.throws(() => ENG.calcEstimate({ serviceId: 'ev-nema-1450', adderIds: ['nope'] }), /unknown ADDERS id/);
  });

  it('null-priced material is excluded, never zeroed', () => {
    const r = ENG.calcEstimate({
      serviceId: 'panel-200a-replacement',
      materials: [{ id: 'wire-thhn-per-ft', qty: 40 }],
      includePermit: false,
    });
    assert.equal(r.exclusions.length, 1);
    assert.match(r.exclusions[0].reason, /excluded from totals/);
    assert.equal(r.totalLow, 2500);
  });

  it('inapplicable adder is excluded', () => {
    const r = ENG.calcEstimate({
      serviceId: 'lighting-per-light', qty: 2,
      adderIds: ['adder-ev-panel-upgrade'],
      includePermit: false,
    });
    assert.equal(r.exclusions.length, 1);
    assert.equal(r.totalLow, 250);
  });

  it('credits are informational only', () => {
    const r = ENG.calcEstimate({ serviceId: 'ev-nema-1450', includePermit: false });
    assert.ok(r.credits.length >= 2);
    assert.equal(r.totalLow, 350); // no credit subtracted
  });
});

describe('relational integrity (JS side)', () => {
  it('ids unique per table; FK targets resolve', () => {
    for (const t of ['SERVICES', 'MATERIALS', 'ADDERS', 'PERMITS', 'CREDITS', 'SIZE_TIERS']) {
      const ids = DATA[t].map((r) => r.id);
      assert.equal(new Set(ids).size, ids.length, 'dup id in ' + t);
    }
    const svc = new Set(DATA.SERVICES.map((r) => r.id));
    for (const a of DATA.ADDERS) {
      assert.ok(a.appliesTo.length > 0, a.id);
      for (const s of a.appliesTo) assert.ok(svc.has(s), a.id + ' -> ' + s);
    }
    for (const t of DATA.SIZE_TIERS) assert.ok(svc.has(t.serviceId), t.id);
    for (const s of DATA.SERVICES) {
      if (s.permitId) assert.ok(DATA.PERMITS.some((p) => p.id === s.permitId), s.id);
    }
  });

  it('every row carries a source or an explicit pending status', () => {
    for (const t of ['SERVICES', 'ADDERS', 'PERMITS', 'CREDITS', 'SIZE_TIERS']) {
      for (const r of DATA[t]) assert.ok(r.source, t + '.' + r.id);
    }
    for (const m of DATA.MATERIALS) {
      assert.ok(m.source || m.status === 'pending-vendor', m.id);
    }
  });
});

describe('JS/SQL parity', () => {
  const sql = readFileSync(join(root, 'scripts/estimate-schema.sql'), 'utf8');
  const starts = [...sql.matchAll(/INSERT OR REPLACE INTO (\S+) /g)];
  const blockFor = (table) => {
    const i = starts.findIndex((m) => m[1] === table);
    assert.ok(i > -1, 'seed block for ' + table);
    const from = starts[i].index;
    const to = i + 1 < starts.length ? starts[i + 1].index : sql.length;
    return sql.slice(from, to);
  };
  const countSeeds = (table) => (blockFor(table).match(/\),\s*\n/g) || []).length + 1;
  it('seed row counts match JS table lengths', () => {
    assert.equal(countSeeds('estimate_services'), DATA.SERVICES.length);
    assert.equal(countSeeds('estimate_materials'), DATA.MATERIALS.length);
    assert.equal(countSeeds('estimate_adders'), DATA.ADDERS.length);
    assert.equal(countSeeds('estimate_permits'), DATA.PERMITS.length);
    assert.equal(countSeeds('estimate_credits'), DATA.CREDITS.length);
    assert.equal(countSeeds('estimate_size_tiers'), DATA.SIZE_TIERS.length);
  });

  it('service_adders join rows equal total appliesTo entries', () => {
    const expected = DATA.ADDERS.reduce((n, a) => n + a.appliesTo.length, 0);
    assert.equal(countSeeds('estimate_service_adders'), expected);
    for (const a of DATA.ADDERS) {
      for (const s of a.appliesTo) {
        assert.ok(sql.includes("('" + s + "', '" + a.id + "')"), s + '/' + a.id);
      }
    }
  });

  it('seed values match JS values', () => {
    for (const s of DATA.SERVICES) {
      assert.ok(sql.includes("('" + s.id + "', '" + s.name + "'"), s.id);
    }
    assert.ok(sql.includes('2500, 4500'), 'panel range in SQL');
  });
});
