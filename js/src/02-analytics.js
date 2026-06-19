(function () {
  'use strict';

  // GA4 event tracking
  function trackEvent(action, label) {
    if (typeof gtag === 'function') {
      gtag('event', action, { 'event_category': 'engagement', 'event_label': label });
    }
  }

  // Track phone clicks
  document.addEventListener('click', function (e) {
    var tel = e.target.closest('a[href^="tel:"]');
    if (tel) {
      trackEvent('phone_click', tel.getAttribute('href'));
    }
  });

  // Track CTA clicks (buttons with btn-gold, btn-outline, btn-navy)
  document.addEventListener('click', function (e) {
    var cta = e.target.closest('.btn, a.btn');
    if (cta) {
      var label = cta.textContent.trim().substring(0, 100);
      trackEvent('cta_click', label);
    }
  });
})();
