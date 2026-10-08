/* AMY Electric — estimate engine (06-estimate-engine.js).
 *
 * Pure calculation layer over AMY_ESTIMATE_DATA. No DOM access, no network,
 * no side effects: given an input spec it returns line items plus low/high
 * totals. Safe to unit-test in Node (see scripts/test-estimate-engine.mjs)
 * and to bundle into site.min.js for the quote forms.
 *
 * Input spec:
 *   { serviceId, qty = 1, sizeSqft = null,
 *     materials = [{ id, qty }], adderIds = [], includePermit = true }
 * Output:
 *   { version, serviceId, lines: [{ kind, id, name, qty, unit, low, high }],
 *     totalLow, totalHigh, credits: [...], exclusions: [...], notes: [...] }
 * Rules: unknown ids throw; qty < 1 throws; null-priced materials and
 * inapplicable adders land in `exclusions`, never in totals; credits are
 * informational and never subtracted.
 */

var AMY_ESTIMATE = (function () {
  'use strict';

  function table(name) {
    var t = AMY_ESTIMATE_DATA[name];
    if (!t) throw new Error('AMY_ESTIMATE: unknown table ' + name);
    return t;
  }

  function find(tableName, id) {
    var rows = table(tableName);
    for (var i = 0; i < rows.length; i++) {
      if (rows[i].id === id) return rows[i];
    }
    throw new Error('AMY_ESTIMATE: unknown ' + tableName + ' id ' + id);
  }

  function checkQty(qty, what) {
    if (typeof qty !== 'number' || !(qty >= 1)) {
      throw new Error('AMY_ESTIMATE: qty must be >= 1 for ' + what);
    }
  }

  function pickTier(serviceId, sizeSqft) {
    var tiers = table('SIZE_TIERS');
    var scoped = [];
    for (var i = 0; i < tiers.length; i++) {
      if (tiers[i].serviceId === serviceId) scoped.push(tiers[i]);
    }
    if (!scoped.length) return null;
    for (var j = 0; j < scoped.length; j++) {
      var max = scoped[j].maxSqft === null ? Infinity : scoped[j].maxSqft;
      if (sizeSqft >= scoped[j].minSqft && sizeSqft <= max) return scoped[j];
    }
    return null;
  }

  function formatUSD(n) {
    var r = Math.round(n);
    var s = String(r);
    var out = '';
    while (s.length > 3) {
      out = ',' + s.slice(-3) + out;
      s = s.slice(0, -3);
    }
    return '$' + s + out;
  }

  function calcEstimate(spec) {
    if (!spec || !spec.serviceId) throw new Error('AMY_ESTIMATE: spec.serviceId is required');
    var qty = spec.qty === undefined ? 1 : spec.qty;
    checkQty(qty, spec.serviceId);
    var svc = find('SERVICES', spec.serviceId);
    var materials = spec.materials || [];
    var adderIds = spec.adderIds || [];
    var includePermit = spec.includePermit === undefined ? true : !!spec.includePermit;

    var lines = [];
    var exclusions = [];
    var notes = [];

    var low = svc.baseLow * qty;
    var high = svc.baseHigh * qty;
    var lineName = svc.name;
    if (spec.sizeSqft !== undefined && spec.sizeSqft !== null) {
      var tier = pickTier(svc.id, spec.sizeSqft);
      if (tier) {
        low = tier.low * qty;
        high = tier.high * qty;
        lineName = svc.name + ' — ' + tier.label;
        notes.push('Sized by area: ' + tier.label + ' (' + tier.id + ').');
      } else {
        notes.push('No size tier covers ' + spec.sizeSqft + ' sq ft; fell back to base range.');
      }
    }
    lines.push({ kind: 'service', id: svc.id, name: lineName, qty: qty, unit: svc.unit, low: low, high: high });

    for (var m = 0; m < materials.length; m++) {
      var item = materials[m];
      var mat = find('MATERIALS', item.id);
      checkQty(item.qty === undefined ? 1 : item.qty, item.id);
      var mq = item.qty === undefined ? 1 : item.qty;
      if (mat.unitLow === null || mat.unitHigh === null) {
        exclusions.push({ id: mat.id, name: mat.name, reason: 'unit price not published (' + mat.status + '); obtain vendor quote, excluded from totals' });
        continue;
      }
      lines.push({ kind: 'material', id: mat.id, name: mat.name, qty: mq, unit: mat.unit, low: mat.unitLow * mq, high: mat.unitHigh * mq });
    }

    for (var a = 0; a < adderIds.length; a++) {
      var ad = find('ADDERS', adderIds[a]);
      var ok = false;
      for (var k = 0; k < ad.appliesTo.length; k++) {
        if (ad.appliesTo[k] === svc.id) { ok = true; break; }
      }
      if (!ok) {
        exclusions.push({ id: ad.id, name: ad.name, reason: 'not applicable to ' + svc.id + '; excluded from totals' });
        continue;
      }
      lines.push({ kind: 'adder', id: ad.id, name: ad.name, qty: 1, unit: 'job', low: ad.low, high: ad.high });
    }

    if (includePermit) {
      if (svc.permitId) {
        var p = find('PERMITS', svc.permitId);
        lines.push({ kind: 'permit', id: p.id, name: p.name, qty: 1, unit: 'job', low: p.low, high: p.high });
      } else {
        exclusions.push({ id: svc.id, name: 'Permit fees', reason: 'permit cost not published for this service; excluded from totals' });
      }
    }

    var totalLow = 0;
    var totalHigh = 0;
    for (var l = 0; l < lines.length; l++) {
      totalLow += lines[l].low;
      totalHigh += lines[l].high;
    }

    return {
      version: AMY_ESTIMATE_DATA.VERSION,
      serviceId: svc.id,
      lines: lines,
      totalLow: totalLow,
      totalHigh: totalHigh,
      totalLabel: formatUSD(totalLow) + '–' + formatUSD(totalHigh),
      credits: table('CREDITS').slice(),
      exclusions: exclusions,
      notes: notes
    };
  }

  function listServices() {
    var out = [];
    var rows = table('SERVICES');
    for (var i = 0; i < rows.length; i++) {
      out.push({ id: rows[i].id, name: rows[i].name, unit: rows[i].unit });
    }
    return out;
  }

  var api = {
    VERSION: AMY_ESTIMATE_DATA.VERSION,
    DATA: AMY_ESTIMATE_DATA,
    formatUSD: formatUSD,
    listServices: listServices,
    getService: function (id) { return find('SERVICES', id); },
    calcEstimate: calcEstimate
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else if (typeof window !== 'undefined') {
    window.AMY_ESTIMATE = api;
  }

  return api;
})();
