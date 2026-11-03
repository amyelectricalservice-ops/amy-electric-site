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
