/* AMY ELECTRIC — Site Scripts */
/* Source: js/src/ — edit modules, not this file */
/* Run: python3 scripts/build-js.py */
(function () {
  'use strict';

  var ham = document.querySelector('.hamburger');
  var nav = document.querySelector('nav');
  if (ham && nav) {
    ham.setAttribute('aria-expanded', 'false');
    ham.addEventListener('click', function () {
      var isOpen = ham.classList.toggle('open');
      nav.classList.toggle('open');
      ham.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  // "More" dropdown: <details>/<summary> gives keyboard toggling for free,
  // but we still close it when the user clicks elsewhere or presses Escape.
  var more = document.querySelector('.nav-more');
  if (more) {
    document.addEventListener('click', function (e) {
      if (more.hasAttribute('open') && !more.contains(e.target)) {
        more.removeAttribute('open');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && more.hasAttribute('open')) {
        more.removeAttribute('open');
      }
    });
  }

  // Highlight the link that matches the current page.
  var links = document.querySelectorAll('nav a');
  var parts = window.location.pathname.split('/').filter(Boolean);
  var cur = parts.length ? parts[parts.length - 1] : 'index';
  if (cur === 'index.html' || cur === 'index') {
    if (parts.length > 1) cur = parts[parts.length - 2];
    else cur = 'index';
  }
  cur = cur.replace(/\.html$/, '');
  links.forEach(function (l) {
    var href = l.getAttribute('href');
    if (!href || href.indexOf('tel:') === 0) return;
    var segs = href.split('/').filter(Boolean);
    var clean = segs.length ? segs[segs.length - 1] : '';
    clean = clean.replace(/\.html$/, '');
    if (clean === '') clean = segs.length > 1 ? segs[segs.length - 2] : 'index';
    if (clean === cur) l.classList.add('active');
  });
})();

// Analytics tracking — AMY Electric website.
// Fires GA4 events when the GA4 Measurement ID (GA4_ID) Worker secret is set;
// otherwise the sendBeacon fallback runs without breaking the page.
// Event tracking is gated on window.gtag availability — all events are
// no-ops when gtag is undefined (Measurement ID not provisioned).

(function () {
  'use strict';

  // ============================================================
  // GA4 event firing — gated on window.gtag availability.
  // Without the GA4_ID secret (Worker), gtag is undefined and all
  // event calls are no-ops. This lets us write the code now so it
  // fires when the ID is provisioned, without breaking the site today.
  // ============================================================

  // ---- Core helper: fire a GA4 event if gtag is available ----
  function fireGtagEvent(name, extraParams = {}) {
    if (typeof window.gtag !== 'function') return;
    // Build the event payload — only send non-PII fields
    const payload = {
      event: name,
      page_path: window.location.pathname.slice(0, 200),
      ...extraParams,
    };
    // Remove undefined values so we don't send keys with no value
    Object.keys(payload).forEach(
      (k) => payload[k] === undefined && delete payload[k]
    );
    window.gtag('event', name, payload);
  }

  // ---- EVENT: phone_click ----
  // Fires when visitor clicks a tel: link.
  function onPhoneClick() {
    fireGtagEvent('phone_click', { event_category: 'Contact' });
  }

  // ---- EVENT: cta_click ----
  // Fires when visitor clicks a CTA link (estimate, contact, quote).
  function onCtaClick() {
    fireGtagEvent('cta_click', { event_category: 'Interaction' });
  }

  // ---- EVENT: form_submit ----
  // Fires when a lead form submits. The selector list is the contract: it
  // originally matched only #quote-form/#amy-quote-form/.quote-form, so the
  // contact page's #quick-form and #estimate-form fired nothing at all.
  function onFormSubmit(e) {
    fireGtagEvent('form_submit', { event_category: 'Form' });

    // ---- EVENT: form_submit_<segment> ----
    // The inquiry selector is the visitor's own intent signal, so report it
    // alongside form_submit rather than renaming the existing event (the GA4
    // dashboards key off form_submit). Values come from contact.html:
    // emergency / service (residential) / b2b / estimate.
    var form = e && e.target;
    var picked = form && form.querySelector
      ? form.querySelector('input[name="request_type"]:checked')
      : null;
    var segments = {
      emergency: 'form_submit_emergency',
      service: 'form_submit_residential',
      b2b: 'form_submit_b2b',
      estimate: 'form_submit_estimate'
    };
    var name = picked && segments[picked.value];
    if (name) {
      fireGtagEvent(name, { event_category: 'Form', form_type: picked.value });
    }
  }

  // ---- EVENT: quote_start ----
  // Fires when the quote widget opens (2-step flow: service+scope → contact).
  function onQuoteStart() {
    fireGtagEvent('quote_start', { event_category: 'Form' });
  }

  // ---- EVENT: quote_step_complete ----
  // Fires when either step of the 2-step quote completes
  // (service selection or contact info entered).
  function onQuoteStepComplete() {
    fireGtagEvent('quote_step_complete', { event_category: 'Form' });
  }

  // ---- EVENT: quote_submit ----
  // Fires on quote form submission (handled by widget submit handler).
  function onQuoteSubmit() {
    fireGtagEvent('quote_submit', { event_category: 'Form' });
  }

  // ---- EVENT: generate_lead ----
  // Fires after confirmed 200 OK from the Worker (the widget's submit
  // handler already does this; this is the centralized fallback for
  // other form types).
  function onLeadGenerated() {
    fireGtagEvent('generate_lead', {
      event_category: 'Form',
      service_type: (window.AMY_LAST_SUBMITTED_DATA && window.AMY_LAST_SUBMITTED_DATA.service)
        || 'unspecified',
      city: (window.AMY_LAST_SUBMITTED_DATA && window.AMY_LAST_SUBMITTED_DATA.city)
        || 'unspecified',
      page_location: window.location.pathname,
    });
  }

  // ---- EVENT: residential_lead ----
  // Fires when a residential-type lead is captured (vs. commercial).
  function onResidentialLead() {
    fireGtagEvent('residential_lead', {
      event_category: 'Lead',
      lead_type: 'residential',
    });
  }

  // ---- EVENT: commercial_lead ----
  // Fires when a commercial bid request lead is captured.
  function onCommercialLead() {
    fireGtagEvent('commercial_lead', {
      event_category: 'Lead',
      lead_type: 'commercial',
    });
  }

  // ---- EVENT: ev_assessment_start ----
  // Fires when the EV charger feasibility assessment begins.
  function onEvAssessmentStart() {
    fireGtagEvent('ev_assessment_start', {
      event_category: 'Estimation',
      assessment_type: 'ev_charger',
    });
  }

  // ---- EVENT: ev_assessment_complete ----
  // Fires when the EV charger feasibility assessment completes.
  function onEvAssessmentComplete() {
    fireGtagEvent('ev_assessment_complete', {
      event_category: 'Estimation',
      assessment_type: 'ev_charger',
    });
  }

  // ---- EVENT: file_upload ----
  // Fires when a project document/file is uploaded via the lead API.
  function onFileUpload() {
    fireGtagEvent('file_upload', { event_category: 'Document' });
  }

  // ---- EVENT: estimate_sent ----
  // Fires when an estimate PDF is sent to the customer.
  function onEstimateSent() {
    fireGtagEvent('estimate_sent', { event_category: 'Estimation' });
  }

  // ---- EVENT: estimate_accepted ----
  // Fires when an estimate is accepted by the customer.
  function onEstimateAccepted() {
    fireGtagEvent('estimate_accepted', { event_category: 'Estimation' });
  }

  // ---- Event binders (run on DOMContentLoaded) ----

  document.addEventListener('DOMContentLoaded', function () {
    // Phone links
    document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
      link.addEventListener('click', onPhoneClick);
    });

    // CTA links (estimate, contact, quote)
    document.querySelectorAll('a[href*="estimate"], a[href*="contact"], a[href*="quote"], a[href*="#get-"]').forEach(function (link) {
      link.addEventListener('click', onCtaClick);
    });

    // Form submissions
    document.querySelectorAll('#quote-form, #amy-quote-form, .quote-form, #quick-form, #estimate-form, #lf-form').forEach(function (form) {
      form.addEventListener('submit', onFormSubmit);
    });

    // Quote widget 2-step flow — these would be triggered from
    // js/estimator-widget.js window handlers:
    window.fireQuoteStart = onQuoteStart;
    window.fireQuoteStepComplete = onQuoteStepComplete;
    window.fireQuoteSubmit = onQuoteSubmit;

    // EV assessment handlers (would be called from ev-feasibility widget)
    window.fireEvAssessmentStart = onEvAssessmentStart;
    window.fireEvAssessmentComplete = onEvAssessmentComplete;

    // File upload handler (called from lead-files handler)
    window.fireFileUpload = onFileUpload;

    // Estimate sent/accepted (called from estimate PDF generation flow)
    window.fireEstimateSent = onEstimateSent;
    window.fireEstimateAccepted = onEstimateAccepted;
  });

  // -----------------------------------------------------------------
  // Analytics beacon endpoint — receives JSON payloads from the client.
  // The Worker processes these into Workers Logs so they survive without
  // any third-party tracker being active.
  // -----------------------------------------------------------------

})();
(function () {
  'use strict';

  // Seed render timestamps for the server-side timing trap on every form
  // that carries the hidden field (handled or not).
  document.querySelectorAll('input[name="_timestamp"]').forEach(function (ts) {
    if (!ts.value) ts.value = new Date().toISOString();
  });

  var MAX_FILES = 5;
  var MAX_BYTES = 10 * 1024 * 1024;
  var ALLOWED = /^(image\/(jpeg|png|webp|heic|heif)|application\/pdf)$/i;

  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') {
      return window.crypto.randomUUID();
    }
    return 't-' + Date.now() + '-' + Math.random().toString(16).slice(2, 12);
  }

  // Attribution travels with the lead: landing page, referrer, UTM and click IDs.
  function seedAttribution(form) {
    var params = new URLSearchParams(window.location.search);
    var fields = {
      source_page: window.location.pathname,
      referrer: document.referrer || '',
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_term: params.get('utm_term') || '',
      utm_content: params.get('utm_content') || '',
      gclid: params.get('gclid') || '',
      fbclid: params.get('fbclid') || ''
    };
    Object.keys(fields).forEach(function (name) {
      if (!fields[name] || form.querySelector('input[name="' + name + '"]')) return;
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = name;
      input.value = fields[name];
      form.appendChild(input);
    });
  }

  function fileInput(form) {
    return form.querySelector('input[type="file"][data-upload-input]');
  }

  function listUploads(form) {
    return form.querySelector('[data-upload-list]');
  }

  function validateFiles(files) {
    if (files.length > MAX_FILES) {
      return 'Please choose up to ' + MAX_FILES + ' files.';
    }
    for (var i = 0; i < files.length; i += 1) {
      var f = files[i];
      if (f.size > MAX_BYTES) {
        return 'Each file must be 10 MB or smaller (' + f.name + ').';
      }
      if (f.type && !ALLOWED.test(f.type)) {
        return 'Please upload a JPG, PNG, WebP, HEIC or PDF file.';
      }
    }
    return '';
  }

  function uploadOne(file, token) {
    var fd = new FormData();
    fd.append('file', file);
    fd.append('upload_token', token);
    return fetch('/api/lead-files', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: fd
    }).then(function (r) {
      return r.json().then(function (res) {
        if (!r.ok || !res.success) throw new Error(res.message || 'Upload failed');
        return res.file;
      });
    });
  }

  // Uploads run BEFORE the lead POST so a storage failure never loses the lead.
  // The empty result must match the {token, files} shape the caller reads —
  // resolving with a bare [] threw on `upload.files.length` and aborted every
  // lead from a form without a file input (the homepage quote form included).
  function uploadFiles(form, onProgress) {
    var input = fileInput(form);
    if (!input || !input.files || !input.files.length) return Promise.resolve({ token: '', files: [] });
    var files = Array.prototype.slice.call(input.files);
    var problem = validateFiles(files);
    if (problem) return Promise.reject(new Error(problem));

    var token = uuid();
    var uploaded = [];
    var chain = Promise.resolve();
    files.forEach(function (file, index) {
      chain = chain.then(function () {
        if (onProgress) onProgress('Uploading ' + (index + 1) + ' of ' + files.length + '…');
        return uploadOne(file, token).then(function (meta) { uploaded.push(meta); });
      });
    });
    return chain.then(function () {
      return { token: token, files: uploaded };
    });
  }

  function renderUploadList(form, files) {
    var list = listUploads(form);
    if (!list) return;
    list.innerHTML = '';
    Array.prototype.forEach.call(files, function (f) {
      var li = document.createElement('li');
      li.textContent = f.name + ' · ' + Math.round(f.size / 1024) + ' KB';
      list.appendChild(li);
    });
  }

  function wireUploadUi(form) {
    var input = fileInput(form);
    if (!input) return;
    input.addEventListener('change', function () {
      var problem = validateFiles(Array.prototype.slice.call(input.files || []));
      var note = form.querySelector('[data-upload-error]');
      if (note) {
        note.textContent = problem;
        note.style.display = problem ? 'block' : 'none';
      }
      if (problem) input.value = '';
      renderUploadList(form, input.files || []);
    });
  }

  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    if (!form) return;

    seedAttribution(form);
    wireUploadUi(form);

    var errorBox = document.getElementById(formId + '-error');

    function showError(message) {
      if (errorBox) {
        errorBox.textContent = message;
        errorBox.style.display = 'block';
      }
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (errorBox) errorBox.style.display = 'none';
      var btn = form.querySelector('.form-submit');
      var originalText = btn.textContent;
      btn.textContent = 'Sending\u2026';
      btn.disabled = true;

      function resetBtn() {
        btn.textContent = originalText;
        btn.disabled = false;
      }

      uploadFiles(form, function (msg) { btn.textContent = msg; })
        .then(function (upload) {
          var fd = new FormData(form);
          fd.delete('uploads'); // never send raw files to the lead endpoint
          if (upload && upload.files && upload.files.length) {
            fd.set('files', JSON.stringify(upload.files.map(function (f) { return f.id; })));
            fd.set('upload_token', upload.token);
          }
          btn.textContent = 'Sending\u2026';
          return fetch('/api/contact', {
            method: 'POST',
            headers: { 'Accept': 'application/json' },
            body: fd
          });
        })
        .then(function (r) {
          return r.json().then(function (res) {
            if (res.success) {
              form.style.display = 'none';
              document.getElementById(successId).style.display = 'block';
            } else if (r.status === 400) {
              // Server-side validation failure: show inline, stay on page.
              showError(res.message || 'Please check the highlighted fields and try again.');
              resetBtn();
            } else {
              throw new Error(res.message);
            }
          });
        })
        .catch(function (err) {
          // Network, upload or server failure: the lead never reached us.
          // Never pretend it sent — show an honest error and leave the form
          // visible so the visitor can retry or use the phone/email fallback.
          showError((err && err.message && /^Uploading|file|Upload/.test(err.message))
            ? err.message + ' You can also call (818) 302-5614.'
            : "Couldn't send — please try again, or email info@amyelectric.com or call (818) 302-5614.");
          resetBtn();
        });
    });
  }

  // The homepage runs one two-step quote widget (js/estimator-widget.js) that
  // replaced the separate quick form and the <details> detailed form. The
  // widget only collects answers and the live range; submitting happens here
  // so every lead keeps the same attribution, honeypot, upload and honest
  // error handling. The widget must not register its own submit listener.
  handleForm('quote-form', 'quote-form-success');

  // Open estimator when linked from other pages
  if (window.location.hash === '#estimator') {
    document.getElementById('estimator') && document.getElementById('estimator').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('quote-estimator') && document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();

/* AMY Electric — estimate data tables (05-estimate-data.js).
 *
 * Every row carries a `source` naming the site page (or decision) its numbers
 * come from. Rows with unitLow null are PLACEHOLDERS for vendor-quoted parts:
 * the engine must surface them as exclusions, never price them at zero.
 *
 * RELATIONAL MAP — this file is the denormalized view of scripts/estimate-schema.sql:
 *   services(id PK, name, unit, base_low, base_high, permit_id FK NULL, permit_handling, source)
 *   materials(id PK, name, unit, unit_low NULL, unit_high NULL, status, source)
 *   adders(id PK, name, low, high, source)
 *   service_adders(service_id FK, adder_id FK)  -- the appliesTo arrays, normalized
 *   size_tiers(id PK, service_id FK, min_sqft, max_sqft NULL, low, high, label, source)
 *   permits(id PK, name, low, high, source)
 *   credits(id PK, name, kind, amount, source, note)
 * scripts/test-estimate-engine.mjs asserts the JS tables and the SQL seed agree.
 */

var AMY_ESTIMATE_DATA = (function () {
  'use strict';

  // permitHandling is what the published range does with permit fees — it must
  // NOT be inferred from permitId (which only points at a priced permit row):
  //   'included'    base range already covers the permit (no permit line, no exclusion)
  //   'separate'    permit row (permitId) is added as its own priced line
  //   'unpublished' permit cost is not published for this scope: surfaced as an
  //                 exclusion, never guessed
  var SERVICES = [
    { id: 'panel-200a-replacement', name: '200A Panel Replacement', unit: 'job', baseLow: 2500, baseHigh: 4500, permitId: null, permitHandling: 'included', source: 'panel-upgrade.html ("including permits and inspection"), owner range decision 2026-10-08' },
    { id: 'panel-main-service-upgrade', name: 'Main Service Upgrade', unit: 'job', baseLow: 3000, baseHigh: 6000, permitId: null, permitHandling: 'unpublished', source: 'panel-upgrade.html' },
    { id: 'panel-subpanel-add', name: 'Sub-Panel Add', unit: 'job', baseLow: 1200, baseHigh: 2500, permitId: null, permitHandling: 'unpublished', source: 'panel-upgrade.html' },
    { id: 'panel-100a-like-for-like', name: '100A Panel Replacement (like-for-like)', unit: 'job', baseLow: 1500, baseHigh: 2500, permitId: null, permitHandling: 'unpublished', source: 'panel-100a-vs-200a.html' },
    { id: 'ev-nema-1450', name: 'NEMA 14-50 Outlet Install', unit: 'job', baseLow: 350, baseHigh: 600, permitId: 'permit-ev', permitHandling: 'separate', source: 'ev-charger-installation.html; owner "use the higher price" decision 2026-10-12 (high $550 -> $600)' },
    { id: 'ev-tesla-wall', name: 'Tesla Wall Connector Install', unit: 'job', baseLow: 500, baseHigh: 1200, permitId: null, permitHandling: 'included', source: 'tesla-charger-installation.html ($500-$1,200 incl. 60A circuit, mounting, permit); unchanged by the 2026-10-12 higher-price pass' },
    { id: 'ev-hardwired', name: 'Hardwired EVSE Install', unit: 'job', baseLow: 500, baseHigh: 1200, permitId: 'permit-ev', permitHandling: 'separate', source: 'ev-charger-installation.html; owner "use the higher price" decision 2026-10-12 (high $900 -> $1,200)' },
    { id: 'ev-fleet-station', name: 'Commercial EV Fleet Station', unit: 'station', baseLow: 1500, baseHigh: 6000, permitId: null, permitHandling: 'unpublished', source: 'commercial-ev-fleet-charging.html' },
    { id: 'lighting-per-light', name: 'Recessed Lighting', unit: 'light', baseLow: 125, baseHigh: 250, permitId: null, permitHandling: 'unpublished', source: 'llms.txt' },
    { id: 'rewiring-base', name: 'Whole-Home Rewiring', unit: 'job', baseLow: 8000, baseHigh: 18000, permitId: null, permitHandling: 'unpublished', source: 'whole-home-rewiring.html, llms.txt' },
    { id: 'rewiring-partial', name: 'Partial Rewiring / Remediation', unit: 'job', baseLow: 800, baseHigh: 3000, permitId: null, permitHandling: 'unpublished', source: 'whole-home-rewiring.html' },
    { id: 'rewiring-per-circuit', name: 'Rewire (per circuit)', unit: 'circuit', baseLow: 300, baseHigh: 600, permitId: null, permitHandling: 'unpublished', source: 'whole-home-rewiring.html' },
    { id: 'generator-transfer-switch', name: 'Automatic Transfer Switch Install', unit: 'job', baseLow: 800, baseHigh: 1500, permitId: null, permitHandling: 'unpublished', source: 'generator-transfer-switch.html' },
    { id: 'generator-manual-switch', name: 'Manual Transfer Switch Install', unit: 'job', baseLow: 400, baseHigh: 800, permitId: null, permitHandling: 'unpublished', source: 'generator-transfer-switch.html' }
  ];

  var SIZE_TIERS = [
    { id: 'rewiring-small', serviceId: 'rewiring-base', minSqft: 0, maxSqft: 1200, low: 3000, high: 7000, label: 'Small home (1-2 BR, ~1,000 sq ft)', source: 'whole-home-rewiring.html' },
    { id: 'rewiring-medium', serviceId: 'rewiring-base', minSqft: 1201, maxSqft: 1750, low: 6000, high: 12000, label: 'Medium home (3 BR, ~1,500 sq ft)', source: 'whole-home-rewiring.html' },
    { id: 'rewiring-large', serviceId: 'rewiring-base', minSqft: 1751, maxSqft: null, low: 10000, high: 15000, label: 'Large home (4+ BR, 2,000+ sq ft)', source: 'whole-home-rewiring.html' }
  ];

  var MATERIALS = [
    { id: 'permit-ev', name: 'EV Permit Fees', unit: 'job', unitLow: 150, unitHigh: 400, status: 'published', source: 'ev-charger-installation.html' },
    { id: 'evse-unit', name: 'Level 2 Charger Unit', unit: 'unit', unitLow: 400, unitHigh: 750, status: 'published', source: 'ev-charger-installation geo pages' },
    { id: 'panel-200a-equipment', name: '200A Panel + Main Breaker Equipment', unit: 'job', unitLow: null, unitHigh: null, status: 'pending-vendor', source: '' },
    { id: 'branch-breaker-2p', name: '2-Pole Branch Breaker', unit: 'breaker', unitLow: null, unitHigh: null, status: 'pending-vendor', source: '' },
    { id: 'wire-thhn-per-ft', name: 'THHN Wire + Conduit (per ft installed run)', unit: 'ft', unitLow: null, unitHigh: null, status: 'pending-vendor', source: '' }
  ];

  var ADDERS = [
    { id: 'adder-ev-panel-upgrade', name: 'Panel Upgrade with EV Install', low: 2500, high: 4500, appliesTo: ['ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'ev-charger-installation.html' },
    { id: 'adder-trenching', name: 'Trenching for Underground Service', low: 800, high: 2500, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade', 'ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'panel-upgrade.html' },
    { id: 'adder-service-mast', name: 'Service Mast / Weatherhead Replacement', low: 200, high: 600, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade'], source: 'panel-upgrade.html' },
    { id: 'adder-grounding', name: 'Grounding Electrodes (code-required)', low: 200, high: 500, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade'], source: 'panel-upgrade.html' },
    { id: 'adder-meter-socket', name: 'Meter Socket Replacement', low: 300, high: 700, appliesTo: ['panel-200a-replacement', 'panel-main-service-upgrade'], source: 'panel-upgrade.html' },
    { id: 'adder-distance-medium', name: 'Medium Wire Run (25-50 ft)', low: 100, high: 150, appliesTo: ['ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'legacy estimator distAdjust' },
    { id: 'adder-distance-long', name: 'Long Wire Run (50 ft+)', low: 200, high: 300, appliesTo: ['ev-nema-1450', 'ev-tesla-wall', 'ev-hardwired'], source: 'legacy estimator distAdjust' }
  ];

  var PERMITS = [
    { id: 'permit-ev', name: 'EV Charger Permit Fees', low: 150, high: 400, source: 'ev-charger-installation.html' }
  ];

  var CREDITS = [
    { id: 'credit-ladwp-ev', name: 'LADWP EV Rebate', kind: 'fixed-up-to', amount: 1000, source: 'ev-charger-installation.html', note: 'Residential customers; informational only, not subtracted from totals.' },
    { id: 'credit-fed-30c', name: 'Federal Section 30C Tax Credit', kind: 'percent', amount: 30, source: 'ev-charger-installation.html', note: '30% of equipment cost; informational only, not subtracted from totals.' }
  ];

  return {
    VERSION: '1.0.0',
    SERVICES: SERVICES,
    SIZE_TIERS: SIZE_TIERS,
    MATERIALS: MATERIALS,
    ADDERS: ADDERS,
    PERMITS: PERMITS,
    CREDITS: CREDITS
  };
})();

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
 * informational and never subtracted. Permit lines follow the service's
 * `permitHandling` ('separate' adds a priced line, 'included' is already in
 * the base range, 'unpublished' is an exclusion).
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
      // Permit treatment comes from svc.permitHandling, never from permitId
      // alone: permitId NULL means both "already inside the base range" (panel
      // replacement) and "never published" (rewiring), and those must not be
      // reported the same way.
      var handling = svc.permitHandling || 'unpublished';
      if (handling === 'separate' && svc.permitId) {
        var p = find('PERMITS', svc.permitId);
        lines.push({ kind: 'permit', id: p.id, name: p.name, qty: 1, unit: 'job', low: p.low, high: p.high });
      } else if (handling === 'included') {
        notes.push('Permit fees included in the base range.');
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

  // EV span: min low to max high across the three charger subtypes, permit
  // handling included per subtype (Tesla's published range already covers its
  // permit; NEMA/hardwired itemize one). Charger type is confirmed on site.
  // Totals come from the engine so the span can never disagree with a single
  // service's estimate.
  function evSpan(E) {
    var ids = ['ev-tesla-wall', 'ev-nema-1450', 'ev-hardwired'];
    var low = Infinity;
    var high = -Infinity;
    for (var i = 0; i < ids.length; i++) {
      var r = E.calcEstimate({ serviceId: ids[i], qty: 1, includePermit: true });
      if (r.totalLow < low) low = r.totalLow;
      if (r.totalHigh > high) high = r.totalHigh;
    }
    return { low: low, high: high };
  }

  function assumptionsFor(kind, serviceId) {
    var a = [ASSUMED_AMPERAGE + ' service assumed', '~' + ASSUMED_DISTANCE_FT + 'ft run assumed'];
    if (kind === 'ev-span') a.push('charger type (Tesla/NEMA/hardwired) confirmed on site');
    if (serviceId === 'rewiring-base') a.push('home size confirmed on site; range tiered by sqft');
    if (serviceId === 'lighting-per-light') a.push('per-light rate; fixture count confirmed on site');
    return a;
  }

  // Permit wording is derived from the data table so it can never contradict
  // what calcEstimate actually did with the permit.
  function permitNoteFor(E, spec) {
    if (spec.kind === 'ev-span') return 'permit fees included in range';
    var svc = E.getService(spec.serviceId);
    if (svc.permitHandling === 'included') return 'permit fees included in range';
    if (svc.permitHandling === 'separate' && svc.permitId) {
      var rows = E.DATA.PERMITS;
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].id === svc.permitId) {
          return 'permit fees added to range ($' + rows[i].low + '-$' + rows[i].high + ')';
        }
      }
    }
    return 'permit fees confirmed on site';
  }

  // Returns the lead payload object, or null when nothing mappable.
  function buildLeadEstimate(serviceValue) {
    var E = engine();
    if (!E) return null;
    var spec = specForService(serviceValue);
    if (!spec) return null;
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
      assumptions: assumptionsFor(spec.kind, spec.serviceId),
      permitNote: permitNoteFor(E, spec),
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

/* AMY Electric — geo personalization consumer (08-geo-personalize.js).
 *
 * worker.js personalizes the landing page for GEO_TARGET_AREAS visitors: it
 * injects `data-service-city` on <header> and sets window.AMY_GEO, and marks
 * the response private/no-store because the edge cannot Vary on cf.city.
 * That cache opt-out only buys something if a visitor can actually see their
 * city — this module is that consumer. Without it, matched visitors paid the
 * no-store penalty for a byte-identical page.
 *
 * It rewrites the existing hero eyebrow in place (same node, same position)
 * so there is no layout shift, and it no-ops everywhere else: pages without
 * window.AMY_GEO — every page except / — are untouched.
 *
 * Timing: worker.js injects the config inline before </body>, which runs
 * during parse, before deferred site.min.js and before DOMContentLoaded.
 */
(function () {
  'use strict';

  function cityOf() {
    if (typeof window === 'undefined' || !window.AMY_GEO) return null;
    var g = window.AMY_GEO;
    if (!g.matched || typeof g.city !== 'string' || !g.city) return null;
    return g.city;
  }

  function apply() {
    var city = cityOf();
    if (!city) return;
    if (typeof document === 'undefined' || !document.querySelector) return;
    var eyebrow = document.querySelector('.hero-eyebrow');
    if (!eyebrow) return;
    // Replace, never append: keeps the line one row tall (no CLS) and keeps
    // "Los Angeles" available in the h1 / hero copy below it.
    eyebrow.textContent = city + ' \u00b7 Residential & Commercial';
  }

  if (typeof document !== 'undefined' && document.addEventListener) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', apply);
    } else {
      apply();
    }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { apply: apply, cityOf: cityOf };
  } else if (typeof window !== 'undefined') {
    window.AMY_GEO_VISUAL = { apply: apply, cityOf: cityOf };
  }
})();
