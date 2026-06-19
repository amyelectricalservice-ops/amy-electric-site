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
})();
