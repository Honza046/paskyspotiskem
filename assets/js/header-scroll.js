/**
 * Hide sticky header on scroll down, reveal on scroll up.
 * Always visible on page load / refresh until the user scrolls down.
 */
(function () {
    'use strict';

    var header = document.querySelector('header.site-header');
    if (!header) {
        return;
    }

    var lastY = 0;
    var ticking = false;
    var hidden = false;
    var canHide = false;
    var anchorNavigating = false;
    var MIN_SCROLL = 120;
    var DELTA = 10;
    var ENABLE_DELAY_MS = 800;
    var ANCHOR_GRACE_MS = 1400;

    function scrollTopInstant() {
        if (window.location.hash) {
            return;
        }
        var html = document.documentElement;
        var prev = html.style.scrollBehavior;
        html.style.scrollBehavior = 'auto';
        html.scrollTop = 0;
        document.body.scrollTop = 0;
        window.scrollTo(0, 0);
        html.style.scrollBehavior = prev;
    }

    function closeMobileNav() {
        var mobileNav = document.getElementById('mobile-nav');
        var menuToggle = document.getElementById('menu-toggle');
        if (mobileNav && !mobileNav.classList.contains('hidden')) {
            mobileNav.classList.add('hidden');
            if (menuToggle) {
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        }
    }

    function setHidden(shouldHide) {
        if (hidden === shouldHide) {
            return;
        }
        hidden = shouldHide;
        header.classList.toggle('-translate-y-full', shouldHide);
        header.setAttribute('aria-hidden', shouldHide ? 'true' : 'false');
        if (shouldHide) {
            closeMobileNav();
        }
    }

    function showHeader() {
        header.classList.remove('-translate-y-full');
        hidden = false;
        header.setAttribute('aria-hidden', 'false');
        lastY = window.scrollY;
    }

    function enableHide() {
        canHide = true;
    }

    function beginAnchorNavigation() {
        anchorNavigating = true;
        canHide = false;
        showHeader();
        window.setTimeout(function () {
            anchorNavigating = false;
            lastY = window.scrollY;
            showHeader();
            if (window.scrollY > MIN_SCROLL) {
                canHide = true;
            }
        }, ANCHOR_GRACE_MS);
    }

    function bindAnchorNavLinks() {
        var selector = '#main-nav a[href*="#"], #mobile-nav a[href*="#"]';
        document.querySelectorAll(selector).forEach(function (link) {
            link.addEventListener('click', function () {
                var href = link.getAttribute('href') || '';
                if (href.indexOf('#') === -1) {
                    return;
                }
                beginAnchorNavigation();
            });
        });
    }

    function onScroll() {
        var y = window.scrollY;

        if (anchorNavigating) {
            showHeader();
            lastY = y;
            ticking = false;
            return;
        }

        if (!canHide || y <= MIN_SCROLL) {
            showHeader();
            ticking = false;
            return;
        }

        if (y > lastY + DELTA) {
            setHidden(true);
        } else if (y < lastY - DELTA) {
            setHidden(false);
        }

        lastY = y;
        ticking = false;
    }

    function boot() {
        canHide = false;
        showHeader();
        bindAnchorNavLinks();

        window.setTimeout(enableHide, ENABLE_DELAY_MS);
    }

    window.addEventListener('hashchange', function () {
        beginAnchorNavigation();
    });

    window.addEventListener('scrollend', function () {
        if (window.location.hash) {
            showHeader();
        }
    }, { passive: true });

    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(onScroll);
            ticking = true;
        }
    }, { passive: true });

    window.addEventListener('wheel', enableHide, { once: true, passive: true });
    window.addEventListener('touchmove', enableHide, { once: true, passive: true });
    window.addEventListener('keydown', function (e) {
        if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Home', 'End', ' '].indexOf(e.key) > -1) {
            enableHide();
        }
    });

    window.addEventListener('pageshow', function () {
        boot();
    });

    window.addEventListener('load', function () {
        showHeader();
        if (window.location.hash) {
            beginAnchorNavigation();
        }
    });

    window.paskyonlineBeginAnchorNavigation = beginAnchorNavigation;

    boot();
})();
