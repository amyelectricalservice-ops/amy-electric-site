/* AMY Electric — estimate lead attachment (07-estimate-lead.js).
 *
 * When a quote form's service select holds a mappable value, compute an
 * indicative range with the bundled AMY_ESTIMATE engine and attach it as a
 * hidden `estimate` field so it posts to /api/contact alongside the lead.
 * The payload is owner context, not a customer-facing quote: every number
 * carries labeled assumptions (200A service, ~30ft run, charger type TBD).
 * Unmappable services attach nothing; a stale hidden field is removed.
 *
 * Injection timing: select-change updates plus a capture-phase submit hook
 * (03-forms.js reads FormData in a bubble-phase listener, so capture runs
 * first even for last-second changes). No visual or UX change.
 */
(function () {
  'use strict';

  var ASSUMED_AMPERAGE = '200A';
  var ASSUMED_DISTANCE_FT = 30;

  function engine() {
    if (typeof AMY_ESTIMATE === 'undefined' || !AMY_ESTIMATE) return null;
    return AMY_ESTIMATE;
  }

  // Map a form service value to an engine spec, or null when the service
  // has no published pricing behind it.
  function specForService(value) {
    var E = engine();
    if (!E) return null;
    if (value === 'ev-charger') {
      return { kind: 'ev-span', serviceValue: value };
    }
    if (value === 'tesla-charger') {
      return { kind: 'single', serviceId: 'ev-tesla-wall', serviceValue: value };
    }
    if (value === 'panel-upgrade') {
      return { kind: 'single', serviceId: 'panel-200a-replacement', serviceValue: value };
    }
    if (value === 'rewiring') {
      return { kind: 'single', serviceId: 'rewiring-base', serviceValue: value };
    }
    if (value === 'lighting') {
      return { kind: 'single', serviceId: 'lighting-per-light', serviceValue: value };
    }
    if (value === 'generator') {
      return { kind: 'single', serviceId: 'generator-transfer-switch', serviceValue: value };
    }
    return null;
  }

  // EV span: min low to max high across the three charger subtypes, plus the
  // published permit line. Charger type is confirmed on site.
  function evSpan(E) {
    var ids = ['ev-tesla-wall', 'ev-nema-1450', 'ev-hardwired'];
    var low = Infinity;
    var high = -Infinity;
    for (var i = 0; i < ids.length; i++) {
      var s = E.getService(ids[i]);
      if (s.baseLow < low) low = s.baseLow;
      if (s.baseHigh > high) high = s.baseHigh;
    }
    var p = E.DATA.PERMITS[0];
    return { low: low + p.low, high: high + p.high };
  }

  function assumptionsFor(kind, serviceId) {
    var a = ['200A service assumed', '~30ft run assumed'];
    if (kind === 'ev-span') a.push('charger type (Tesla/NEMA/hardwired) confirmed on site');
    if (serviceId === 'rewiring-base') a.push('home size confirmed on site; range tiered by sqft');
    if (serviceId === 'lighting-per-light') a.push('per-light rate; fixture count confirmed on site');
    return a;
  }

  function permitNoteFor(serviceId) {
    if (serviceId === 'panel-200a-replacement') return 'permit fees included in range';
    if (serviceId === 'ev-span' || serviceId === 'ev-tesla-wall') return 'permit fees itemized above';
    return 'permit fees confirmed on site';
  }

  // Returns the lead payload object, or null when nothing mappable.
  function buildLeadEstimate(serviceValue) {
    var E = engine();
    if (!E) return null;
    var spec = specForService(serviceValue);
    if (!spec) return null;
    var key = spec.kind === 'ev-span' ? 'ev-span' : spec.serviceId;
    var out;
    if (spec.kind === 'ev-span') {
      var span = evSpan(E);
      out = { rangeLow: span.low, rangeHigh: span.high };
    } else {
      var r = E.calcEstimate({ serviceId: spec.serviceId, qty: 1, includePermit: true });
      out = { rangeLow: r.totalLow, rangeHigh: r.totalHigh };
    }
    return {
      service: serviceValue,
      rangeLow: out.rangeLow,
      rangeHigh: out.rangeHigh,
      currency: 'USD',
      assumptions: assumptionsFor(spec.kind, key === 'ev-span' ? 'ev-span' : spec.serviceId),
      permitNote: permitNoteFor(key),
      generatedBy: 'AMY_ESTIMATE v' + E.VERSION + ' (indicative; confirm on site)'
    };
  }

  function syncForm(form) {
    var sel = form.querySelector('select[name="service"]');
    if (!sel) return;
    var existing = form.querySelector('input[name="estimate"]');
    var payload = buildLeadEstimate(sel.value);
    if (!payload) {
      if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
      return;
    }
    if (!existing) {
      existing = document.createElement('input');
      existing.type = 'hidden';
      existing.name = 'estimate';
      form.appendChild(existing);
    }
    existing.value = JSON.stringify(payload);
  }

  function syncAll() {
    var forms = document.querySelectorAll('form[action="/api/contact"]');
    for (var i = 0; i < forms.length; i++) syncForm(forms[i]);
  }

  if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function () {
      syncAll();
      var sels = document.querySelectorAll('form[action="/api/contact"] select[name="service"]');
      for (var i = 0; i < sels.length; i++) {
        sels[i].addEventListener('change', syncAll);
      }
      document.addEventListener('submit', function (e) {
        var f = e.target;
        if (f && f.getAttribute && f.getAttribute('action') === '/api/contact') syncForm(f);
      }, true);
    });
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { specForService: specForService, buildLeadEstimate: buildLeadEstimate };
  } else if (typeof window !== 'undefined') {
    window.AMY_ESTIMATE_LEAD = { specForService: specForService, buildLeadEstimate: buildLeadEstimate };
  }
})();
