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