/**
 * Mobile navigation – hamburger toggle (lg:hidden button, lg:block desktop nav).
 */
(function () {
    'use strict';

    var menuToggle = document.getElementById('menu-toggle');
    var mobileNav = document.getElementById('mobile-nav');
    if (!menuToggle || !mobileNav) {
        return;
    }

    function menuLabel(open) {
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            return window.paskyI18n.t(open ? 'nav.menu_close' : 'nav.menu');
        }
        return open ? 'Zavřít menu' : 'Otevřít menu';
    }

    function setOpen(open) {
        mobileNav.classList.toggle('hidden', !open);
        menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        menuToggle.setAttribute('aria-label', menuLabel(open));
    }

    function isOpen() {
        return !mobileNav.classList.contains('hidden');
    }

    menuToggle.addEventListener('click', function () {
        setOpen(!isOpen());
    });

    document.addEventListener('pasky:i18n-ready', function () {
        menuToggle.setAttribute('aria-label', menuLabel(isOpen()));
    });
})();
