/**
 * Hide sticky header on scroll down, reveal on scroll up only.
 * Info banner stays visible; only the main header collapses.
 */
(function () {
    'use strict';

    function wrapHeader(header) {
        if (!header) {
            return null;
        }
        if (header.parentElement && header.parentElement.classList.contains('site-header-shell')) {
            return header.parentElement;
        }
        var shell = document.createElement('div');
        shell.className = 'site-header-shell';
        header.parentNode.insertBefore(shell, header);
        shell.appendChild(header);
        return shell;
    }

    var header = document.querySelector('header.site-header');
    var shell = wrapHeader(header);
    if (!header || !shell) {
        return;
    }

    var lastY = 0;
    var ticking = false;
    var hidden = false;
    var canHide = false;
    var anchorNavigating = false;
    var MIN_SCROLL = 80;
    var DELTA = 18;
    var ENABLE_DELAY_MS = 800;
    var ANCHOR_GRACE_MS = 1400;

    function closeMobileNav() {
        var mobileNav = document.getElementById('mobile-nav');
        var menuToggle = document.getElementById('menu-toggle');
        if (mobileNav && !mobileNav.classList.contains('hidden')) {
            mobileNav.classList.add('hidden');
            if (menuToggle) {
                menuToggle.setAttribute('aria-expanded', 'false');
                if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
                    menuToggle.setAttribute('aria-label', window.paskyI18n.t('nav.menu'));
                } else {
                    menuToggle.setAttribute('aria-label', 'Otevřít menu');
                }
            }
        }
    }

    function syncSiteTopHeight() {
        var siteTop = document.querySelector('.site-top');
        if (siteTop) {
            document.documentElement.style.setProperty('--site-top-height', siteTop.offsetHeight + 'px');
        }
    }

    function initSiteTopHeight() {
        syncSiteTopHeight();
        var siteTop = document.querySelector('.site-top');
        if (siteTop && typeof ResizeObserver !== 'undefined') {
            new ResizeObserver(syncSiteTopHeight).observe(siteTop);
        } else {
            window.addEventListener('resize', syncSiteTopHeight);
        }
        window.paskyonlineSyncSiteTopHeight = syncSiteTopHeight;
    }

    function setHidden(shouldHide) {
        if (hidden === shouldHide) {
            return;
        }
        hidden = shouldHide;
        shell.classList.toggle('is-collapsed', shouldHide);
        header.setAttribute('aria-hidden', shouldHide ? 'true' : 'false');
        if (shouldHide) {
            closeMobileNav();
        }
        window.requestAnimationFrame(syncSiteTopHeight);
    }

    function showHeader() {
        shell.classList.remove('is-collapsed');
        hidden = false;
        header.setAttribute('aria-hidden', 'false');
        window.requestAnimationFrame(syncSiteTopHeight);
    }

    function enableHide() {
        canHide = true;
        lastY = window.scrollY;
    }

    function beginAnchorNavigation() {
        anchorNavigating = true;
        canHide = false;
        showHeader();
        window.setTimeout(function () {
            anchorNavigating = false;
            lastY = window.scrollY;
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
            lastY = y;
            ticking = false;
            return;
        }

        if (!canHide) {
            lastY = y;
            ticking = false;
            return;
        }

        if (y > lastY + DELTA && y > MIN_SCROLL) {
            setHidden(true);
        } else if (y < lastY - DELTA) {
            setHidden(false);
        }

        lastY = y;
        ticking = false;
    }

    function boot() {
        canHide = false;
        initSiteTopHeight();
        showHeader();
        lastY = window.scrollY;
        bindAnchorNavLinks();
        window.setTimeout(enableHide, ENABLE_DELAY_MS);
    }

    window.addEventListener('hashchange', function () {
        beginAnchorNavigation();
    });

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
        lastY = window.scrollY;
        if (window.location.hash) {
            beginAnchorNavigation();
        }
    });

    window.paskyonlineBeginAnchorNavigation = beginAnchorNavigation;

    boot();
})();
