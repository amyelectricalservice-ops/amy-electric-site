/* ── AMY Wizard UI controller ──
 *
 * 3-step flow: 1) project type → 2) technical variables → 3) locked estimate
 * gated on name + email + phone. Uses window.AMY_ESTIMATE (engine). No DOM
 * work until #lead-wizard exists. CSP-safe (no inline eval).
 */

(function () {
  'use strict';

  /* Geo city string injected by the Cloudflare edge worker (see worker.js
   * injectGeoCity): window.AMY_GEO_CITY, e.g. "Burbank". Falls back to the
   * data attribute, then "Los Angeles". Never blank in the headline. */
  function geoCity() {
    if (typeof window.AMY_GEO_CITY === 'string' && window.AMY_GEO_CITY.trim()) {
      return window.AMY_GEO_CITY.trim();
    }
    var el = document.querySelector('[data-geo-city-default]');
    if (el && el.getAttribute('data-geo-city-default')) {
      return el.getAttribute('data-geo-city-default');
    }
    return 'Los Angeles';
  }

  function applyGeoHeadline() {
    var city = geoCity();
    document.querySelectorAll('[data-geo-city]').forEach(function (el) {
      el.textContent = city;
    });
  }

  /* serviceId → which Step-2 variable groups to show */
  var STEP2_CONFIG = {
    'ev-nema-1450': { title: 'Charger & run details', groups: ['charger-kind', 'distance'] },
    'ev-tesla-wall': { title: 'Charger & run details', groups: ['charger-kind', 'distance'] },
    'ev-hardwired': { title: 'Charger & run details', groups: ['charger-kind', 'distance'] },
    'ev-fleet-station': { title: 'Station details', groups: ['qty'] },
    'panel-200a-replacement': { title: 'Service details', groups: ['amps'] },
    'panel-main-service-upgrade': { title: 'Service details', groups: ['amps'] },
    'panel-subpanel-add': { title: 'Service details', groups: ['amps'] },
    'panel-100a-like-for-like': { title: 'Service details', groups: ['amps'] },
    'lighting-per-light': { title: 'Lighting details', groups: ['qty'] },
    'rewiring-base': { title: 'Home size', groups: ['size'] },
    'rewiring-partial': { title: 'Scope details', groups: ['size'] },
    'rewiring-per-circuit': { title: 'Scope details', groups: ['qty'] },
    'generator-transfer-switch': { title: 'Switch details', groups: ['switch-kind'] },
    'generator-manual-switch': { title: 'Switch details', groups: ['switch-kind'] }
  };

  var PROJECT_CARDS = [
    { serviceId: 'ev-tesla-wall', icon: '&#9889;', name: 'EV Charger', desc: 'Tesla, universal & fleet' },
    { serviceId: 'panel-200a-replacement', icon: '&#128268;', name: 'Panel Upgrade', desc: '200A service & sub-panels' },
    { serviceId: 'rewiring-base', icon: '&#127968;', name: 'Rewiring', desc: 'Whole-home & partial' },
    { serviceId: 'lighting-per-light', icon: '&#128161;', name: 'Lighting', desc: 'Recessed & retrofit' },
    { serviceId: 'generator-transfer-switch', icon: '&#128267;', name: 'Generator Switch', desc: 'Auto & manual transfer' }
  ];

  var state = {
    step: 1,
    serviceId: 'ev-tesla-wall',
    chargerKind: 'tesla-wall',
    switchKind: 'automatic',
    amps: '200',
    sizeSqft: 1500,
    qty: 1,
    distance: 'short',
    needPanelUpgrade: false,
    unlocked: false,
    result: null
  };

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function showStep(n) {
    state.step = n;
    $all('[data-wizard-step]').forEach(function (s) {
      s.classList.toggle('lf-active', Number(s.getAttribute('data-wizard-step')) === n);
    });
    $all('.lf-dot').forEach(function (d, i) {
      d.classList.toggle('lf-active', i + 1 <= n);
    });
    $all('.lf-step-label').forEach(function (l, i) {
      l.classList.toggle('lf-active', i + 1 === n);
    });
    var wiz = $('#lead-wizard');
    if (wiz) wiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function showStepError(step, msg) {
    var box = $('#wizard-error-' + step);
    if (!box) return;
    box.textContent = msg;
    box.classList.add('lf-show');
  }

  function clearStepError(step) {
    var box = $('#wizard-error-' + step);
    if (!box) return;
    box.textContent = '';
    box.classList.remove('lf-show');
  }

  /* Build the Step-2 variable groups for the chosen service. */
  function renderStep2() {
    var cfg = STEP2_CONFIG[state.serviceId] || { title: 'Project details', groups: [] };
    $('#wizard-step2-title').textContent = cfg.title;
    $all('[data-var-group]').forEach(function (g) {
      g.style.display = cfg.groups.indexOf(g.getAttribute('data-var-group')) !== -1 ? '' : 'none';
    });
  }

  function currentSpec() {
    var spec = { serviceId: state.serviceId, includePermit: true };
    if (state.serviceId === 'lighting-per-light' || state.serviceId === 'rewiring-per-circuit' || state.serviceId === 'ev-fleet-station') {
      spec.qty = Math.max(1, Number(state.qty) || 1);
    }
    if (state.serviceId === 'rewiring-base' || state.serviceId === 'rewiring-partial') {
      spec.sizeSqft = Number(state.sizeSqft) || 1500;
    }
    if (state.serviceId === 'ev-nema-1450' || state.serviceId === 'ev-tesla-wall' || state.serviceId === 'ev-hardwired') {
      if (state.distance === 'medium') spec.adderIds = ['adder-distance-medium'];
      if (state.distance === 'long') spec.adderIds = ['adder-distance-long'];
      if (state.needPanelUpgrade) (spec.adderIds = spec.adderIds || []).push('adder-ev-panel-upgrade');
    }
    return spec;
  }

  function money(n) { return window.AMY_ESTIMATE.formatUSD(n); }

  /* Render the locked estimate preview (blurred totals) + unlock form. */
  function renderLockedEstimate() {
    try {
      state.result = window.AMY_ESTIMATE.calcEstimate(currentSpec());
    } catch (e) {
      showStepError(2, 'Could not price that combination — please adjust and try again.');
      return false;
    }
    var r = state.result;
    $('#locked-range').textContent = r.totalLabel;
    $('#locked-service').textContent = r.lines[0].name;
    showStep(3);
    return true;
  }

  /* Replace the blur with the full line-item summary after valid contact. */
  function renderUnlockedSummary() {
    var r = state.result;
    var html = '<ul class="lf-breakdown">';
    r.lines.forEach(function (l) {
      html += '<li><span style="color:var(--gold);flex-shrink:0;">&#10003;</span><span>' +
        escapeHtml(l.name) + (l.qty > 1 ? ' &times; ' + l.qty : '') +
        ': ' + money(l.low) + '–' + money(l.high) + '</span></li>';
    });
    html += '</ul>';
    if (r.exclusions.length) {
      html += '<p class="lf-text-xs lf-text-muted lf-mt-4">Not included (quoted separately): ' +
        r.exclusions.map(function (e) { return escapeHtml(e.name); }).join('; ') + '.</p>';
    }
    html += '<p class="lf-text-xs lf-text-muted lf-mt-2">Licensed C-10 #981578 · EVITP #4051604 · Serving ' +
      escapeHtml(geoCity()) + ' and Greater Los Angeles.</p>';
    $('#summary-lines').innerHTML = html;
    $('#summary-total').textContent = r.totalLabel;
    $('#estimate-locked').style.display = 'none';
    $('#estimate-unlocked').style.display = '';
    state.unlocked = true;
  }

  function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }
  function validPhone(v) { return (v.replace(/\D/g, '').length) >= 7; }

  function bindCards(container, attr, onPick) {
    $all('[data-pick]', container).forEach(function (btn) {
      btn.addEventListener('click', function () {
        $all('[data-pick]', container).forEach(function (b) { b.classList.remove('lf-selected'); });
        btn.classList.add('lf-selected');
        onPick(btn.getAttribute(attr), btn);
        clearStepError(state.step);
      });
    });
  }

  function init() {
    var wiz = document.getElementById('lead-wizard');
    if (!wiz || !window.AMY_ESTIMATE) return;

    applyGeoHeadline();

    /* Seed timestamp trap (same contract as 03-forms.js). */
    var ts = document.querySelector('#lf-form input[name="_timestamp"]');
    if (ts && !ts.value) ts.value = new Date().toISOString();

    /* Step 1: project cards (built from PROJECT_CARDS). */
    var grid = $('#project-grid');
    PROJECT_CARDS.forEach(function (c, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'lf-card' + (i === 0 ? ' lf-selected' : '');
      b.setAttribute('data-pick', '');
      b.setAttribute('data-service', c.serviceId);
      b.innerHTML = '<span style="font-size:2rem;line-height:1">' + c.icon + '</span>' +
        '<span class="lf-font-cond lf-font-bold">' + c.name + '</span>' +
        '<span class="lf-text-xs lf-text-muted">' + c.desc + '</span>';
      grid.appendChild(b);
    });
    bindCards(grid, 'data-service', function (v) { state.serviceId = v; });

    $('#wizard-next-1').addEventListener('click', function () {
      clearStepError(1);
      if (!state.serviceId) { showStepError(1, 'Please choose a project type to continue.'); return; }
      renderStep2();
      showStep(2);
    });

    /* Step 2: technical variables. */
    bindCards($('#var-charger-kind'), 'data-value', function (v) {
      state.serviceId = v === 'outlet' ? 'ev-nema-1450' : (v === 'universal' ? 'ev-hardwired' : 'ev-tesla-wall');
      state.chargerKind = v;
    });
    bindCards($('#var-switch-kind'), 'data-value', function (v) {
      state.serviceId = v === 'manual' ? 'generator-manual-switch' : 'generator-transfer-switch';
      state.switchKind = v;
    });
    bindCards($('#var-amps'), 'data-value', function (v) { state.amps = v; });
    bindCards($('#var-distance'), 'data-value', function (v) { state.distance = v; });

    var sizeSel = $('#var-size');
    if (sizeSel) sizeSel.addEventListener('change', function () { state.sizeSqft = Number(sizeSel.value); });
    var qtyInput = $('#var-qty');
    if (qtyInput) qtyInput.addEventListener('input', function () { state.qty = Number(qtyInput.value); });
    var panelChk = $('#var-panel-upgrade');
    if (panelChk) panelChk.addEventListener('change', function () { state.needPanelUpgrade = panelChk.checked; });

    $('#wizard-back-2').addEventListener('click', function () { showStep(1); });
    $('#wizard-next-2').addEventListener('click', function () {
      clearStepError(2);
      if (state.serviceId === 'lighting-per-light' || state.serviceId === 'rewiring-per-circuit' || state.serviceId === 'ev-fleet-station') {
        if (!(Number(state.qty) >= 1)) { showStepError(2, 'Please enter a quantity of at least 1.'); return; }
      }
      renderLockedEstimate();
    });

    /* Step 3: unlock form → CRM-first POST to /api/lead (same-origin proxy;
     * secret webhook URL never touches the browser), /api/contact fallback
     * server-side. Success → confirmation + downloadable project summary. */
    $('#wizard-back-3').addEventListener('click', function () { showStep(2); });
    $('#lf-form').addEventListener('submit', function (e) {
      e.preventDefault();
      clearStepError(3);
      var name = $('#lf-name').value.trim();
      var email = $('#lf-email').value.trim();
      var phone = $('#lf-phone').value.trim();
      var city = $('#lf-city') ? $('#lf-city').value.trim() : '';
      if (!name) { showStepError(3, 'Please enter your name.'); return; }
      if (!validEmail(email)) { showStepError(3, 'Please enter a valid email address.'); return; }
      if (!validPhone(phone)) { showStepError(3, 'Please enter a valid phone number.'); return; }
      if (!state.result) { showStepError(3, 'Please go back and choose your project details first.'); return; }

      var btn = $('#lf-submit');
      var original = btn.textContent;
      btn.textContent = 'Sending…';
      btn.disabled = true;

      var spec = currentSpec();
      var r = state.result;
      var payload = {
        website: ($('#lf-website') && $('#lf-website').value) || '',
        _timestamp: ($('#lf-timestamp') && $('#lf-timestamp').value) || '',
        name: name,
        email: email,
        phone: phone,
        city: city,
        geoCity: geoCity(),
        serviceId: state.serviceId,
        spec: spec,
        estimateLabel: r.totalLabel,
        estimateLow: r.totalLow,
        estimateHigh: r.totalHigh,
        lines: r.lines,
        exclusions: r.exclusions
      };

      fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (resp) {
          return resp.json().then(function (res) {
            if (res.success) {
              renderUnlockedSummary();
              renderConfirmation(res.crm);
            } else if (resp.status === 400) {
              showStepError(3, res.message || 'Please check the highlighted fields and try again.');
              btn.textContent = original;
              btn.disabled = false;
            } else { throw new Error(res.message); }
          });
        })
        .catch(function () {
          showStepError(3, 'Connection issue — please check your connection and try again, or call (818) 302-5614.');
          btn.textContent = original;
          btn.disabled = false;
        });
    });

    /* Confirmation panel + client-downloadable project summary (.txt). */
    function renderConfirmation(crm) {
      var panel = $('#wizard-confirmation');
      if (panel) {
        var note = $('#confirmation-note');
        if (note) {
          note.textContent = crm === 'fallback'
            ? 'Received! Our CRM is briefly unreachable, so your request was saved through our backup channel — a licensed electrician will still follow up within a few hours.'
            : 'Received! A licensed electrician will follow up within a few hours to confirm your exact price.';
        }
        panel.style.display = '';
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      var dl = $('#summary-download');
      if (dl) {
        dl.style.display = '';
        dl.addEventListener('click', function () {
          downloadSummary();
        }, { once: true });
      }
    }

    function summaryText() {
      var r = state.result;
      var spec = currentSpec();
      var name = $('#lf-name').value.trim();
      var lines = [];
      lines.push('AMY ELECTRIC — PROJECT SUMMARY');
      lines.push('Licensed C-10 #981578 · EVITP #4051604 · (818) 302-5614');
      lines.push('Generated: ' + new Date().toLocaleString());
      lines.push('');
      lines.push('CUSTOMER');
      lines.push('  Name:  ' + name);
      lines.push('  Email: ' + $('#lf-email').value.trim());
      lines.push('  Phone: ' + $('#lf-phone').value.trim());
      if ($('#lf-city') && $('#lf-city').value.trim()) lines.push('  City:  ' + $('#lf-city').value.trim());
      lines.push('  Service area: ' + geoCity() + ', Greater Los Angeles');
      lines.push('');
      lines.push('PROJECT');
      lines.push('  Service: ' + r.lines[0].name + ' (' + state.serviceId + ')');
      lines.push('  Spec: ' + JSON.stringify(spec));
      lines.push('');
      lines.push('ESTIMATE: ' + r.totalLabel);
      r.lines.forEach(function (l) {
        lines.push('  - ' + l.name + (l.qty > 1 ? ' x ' + l.qty : '') +
          ': ' + money(l.low) + '–' + money(l.high));
      });
      if (r.exclusions.length) {
        lines.push('');
        lines.push('NOT INCLUDED (quoted separately):');
        r.exclusions.forEach(function (x) { lines.push('  - ' + x.name + ': ' + x.reason); });
      }
      if (r.notes.length) {
        lines.push('');
        r.notes.forEach(function (n) { lines.push('Note: ' + n); });
      }
      lines.push('');
      lines.push('This is a planning estimate, not a fixed bid. Final price confirmed on site visit.');
      return lines.join('\n');
    }

    function downloadSummary() {
      var blob = new Blob([summaryText()], { type: 'text/plain;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'amy-electric-project-summary.txt';
      document.body.appendChild(a);
      a.click();
      setTimeout(function () {
        URL.revokeObjectURL(a.href);
        a.remove();
      }, 1000);
    }
  }

  window.AMY_WIZARD = { init: init, getState: function () { return state; } };

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
  }
})();
