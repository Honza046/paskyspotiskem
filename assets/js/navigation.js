(function () {
    'use strict';

    var toggle = document.querySelector('.toggle-categories-menu');
    var menu = document.getElementById('menu');

    if (!toggle || !menu) {
        return;
    }

    toggle.addEventListener('click', function () {
        var isOpen = menu.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
})();
