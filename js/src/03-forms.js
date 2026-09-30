(function () {
  'use strict';

  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    if (!form) return;

    // Seed the render timestamp for the server-side timing trap.
    var ts = form.querySelector('input[name="_timestamp"]');
    if (ts && !ts.value) ts.value = new Date().toISOString();

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
          var data = Object.fromEntries(new FormData(form));
          var body = '';
          for (var k in data) {
            if (data.hasOwnProperty(k)) body += k + ': ' + data[k] + '\n';
          }
          window.location.href = 'mailto:info@amyelectric.com?subject=AMY%20Electric%20-%20' + encodeURIComponent(data.name || 'New Lead') + '&body=' + encodeURIComponent(body);
          form.style.display = 'none';
          document.getElementById(successId).style.display = 'block';
        });
    });
  }

  handleForm('quick-form', 'quick-form-success');
  handleForm('estimate-form', 'estimate-form-success');

  // Open estimator when linked from other pages
  if (window.location.hash === '#estimator') {
    document.getElementById('estimator') && document.getElementById('estimator').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('quote-estimator') && document.getElementById('quote-estimator').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
