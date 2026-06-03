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

  var links = document.querySelectorAll('nav a');
  var cur = window.location.pathname.split('/').pop() || 'index.html';
  links.forEach(function (l) {
    if (l.getAttribute('href') === cur || l.getAttribute('href') === './' + cur) {
      l.classList.add('active');
    }
  });

  function handleForm(formId, successId) {
    var form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('.form-submit');
      btn.textContent = 'Sending\u2026';
      btn.disabled = true;

      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form),
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.success) {
            form.style.display = 'none';
            document.getElementById(successId).style.display = 'block';
          } else {
            throw new Error(res.message);
          }
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

  function loadGA() {
    if (window.gaLoaded) return;
    window.gaLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-QVSNBR7PTS';
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-QVSNBR7PTS');
  }

  if ('requestIdleCallback' in window) {
    requestIdleCallback(loadGA, { timeout: 2000 });
  } else {
    setTimeout(loadGA, 2000);
  }

})();
