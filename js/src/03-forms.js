(function () {
  'use strict';

  // Seed render timestamps for the server-side timing trap on every form
  // that carries the hidden field (handled or not).
  document.querySelectorAll('input[name="_timestamp"]').forEach(function (ts) {
    if (!ts.value) ts.value = new Date().toISOString();
  });

  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    if (!form) return;

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

      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form),
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
        .catch(function () {
          // Network or server failure: the lead never reached /api/contact.
          // Never pretend it sent — show an honest error and leave the form
          // visible so the visitor can retry or use the phone/email fallback.
          showError("Couldn't send — please try again, or email info@amyelectric.com or call (818) 302-5614.");
          resetBtn();
        });
    });
  }

  handleForm('quick-form', 'quick-form-success');
  handleForm('estimate-form', 'estimate-form-success');
  // NOTE: qe-form is submitted by the legacy estimator engine
  // (js/estimator.min.js), which builds its own FormData. Registering it
  // here too would double-POST every estimator lead.

  // Open estimator when linked from other pages
  if (window.location.hash === '#estimator') {
    document.getElementById('estimator') && document.getElementById('estimator').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('quote-estimator') && document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
