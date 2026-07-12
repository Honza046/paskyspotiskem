/**
 * Active nav state: current page + scroll spy for home sections.
 */
(function () {
    'use strict';

    var STYLE_ID = 'nav-active-style';
    var HOME_SECTIONS = [
        { id: 'uvod', key: 'home' },
        { id: 'reference', key: 'reference' },
        { id: 'gf_1', key: 'contact' },
        { id: 'kontakt1', key: 'contact' },
    ];
    var navClickLock = null;
    var navClickLockTimer = null;

    function injectStyle() {
        if (document.getElementById(STYLE_ID)) {
            return;
        }
        var style = document.createElement('style');
        style.id = STYLE_ID;
        style.textContent = '#main-nav a.is-active,#mobile-nav a.is-active{color:#ea580c!important}';
        document.head.appendChild(style);
    }

    function scrollOffset() {
        var padding = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop);
        return Number.isFinite(padding) && padding > 0 ? padding : 88;
    }

    function sectionTop(el) {
        return el.getBoundingClientRect().top + window.scrollY;
    }

    function navKeyFromHref(href) {
        if (!href) {
            return null;
        }
        if (/galerie/i.test(href)) {
            return 'gallery';
        }
        if (/sortiment/i.test(href)) {
            return 'sortiment';
        }
        if (href === '#reference' || /#reference(?:$|[?#])/.test(href)) {
            return 'reference';
        }
        if (href === '#kontakt1' || /#kontakt/i.test(href)) {
            return 'contact';
        }
        if (/#uvod(?:$|[?#])/.test(href)) {
            return 'home';
        }
        return null;
    }

    function hashFromHref(href) {
        if (!href || href.indexOf('#') === -1) {
            return null;
        }
        return href.split('#').pop().split('?')[0] || null;
    }

    function pageKeyFromLocation() {
        var dataPage = document.body.getAttribute('data-page');
        if (dataPage === 'gallery') {
            return 'gallery';
        }
        if (dataPage === 'sortiment') {
            return 'sortiment';
        }
        if (dataPage === 'home') {
            return null;
        }

        var path = window.location.pathname || '';
        if (/galerie/i.test(path)) {
            return 'gallery';
        }
        if (/sortiment/i.test(path)) {
            return 'sortiment';
        }
        if (/index\.html$/i.test(path) || /\/$/.test(path)) {
            return null;
        }
        return null;
    }

    function allNavLinks() {
        return Array.prototype.slice.call(
            document.querySelectorAll('#main-nav a[href], #mobile-nav a[href]')
        );
    }

    function setActive(key) {
        allNavLinks().forEach(function (link) {
            var linkKey = navKeyFromHref(link.getAttribute('href'));
            link.classList.toggle('is-active', linkKey === key);
        });
    }

    function homeSectionKey() {
        var probe = window.scrollY + scrollOffset() + 1;
        var active = 'home';
        HOME_SECTIONS.forEach(function (section) {
            var el = document.getElementById(section.id);
            if (el && sectionTop(el) <= probe) {
                active = section.key;
            }
        });
        return active;
    }

    function clearNavClickLock() {
        navClickLock = null;
        if (navClickLockTimer) {
            window.clearTimeout(navClickLockTimer);
            navClickLockTimer = null;
        }
    }

    function lockNavClick(key) {
        navClickLock = key;
        if (navClickLockTimer) {
            window.clearTimeout(navClickLockTimer);
        }
        navClickLockTimer = window.setTimeout(clearNavClickLock, 1500);
    }

    function scrollToSection(hash) {
        var target = document.getElementById(hash);
        if (!target) {
            return false;
        }

        var top = Math.max(0, sectionTop(target) - scrollOffset());
        window.scrollTo(0, top);

        if (typeof window.paskyonlineBeginAnchorNavigation === 'function') {
            window.paskyonlineBeginAnchorNavigation();
        }

        return true;
    }

    function bindHomeNavClicks() {
        allNavLinks().forEach(function (link) {
            link.addEventListener('click', function (event) {
                var href = link.getAttribute('href') || '';
                var key = navKeyFromHref(href);
                var hash = hashFromHref(href);

                if (!key || !hash || !document.getElementById(hash)) {
                    return;
                }

                event.preventDefault();
                lockNavClick(key);
                setActive(key);

                if (window.location.hash !== '#' + hash) {
                    history.pushState(null, '', '#' + hash);
                }

                scrollToSection(hash);

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
            });
        });
    }

    function initHomeScrollSpy() {
        var ticking = false;

        function update() {
            setActive(navClickLock || homeSectionKey());
            ticking = false;
        }

        function onUserScrollIntent() {
            if (navClickLock) {
                clearNavClickLock();
                setActive(homeSectionKey());
            }
        }

        window.addEventListener('scroll', function () {
            if (!ticking) {
                window.requestAnimationFrame(update);
                ticking = true;
            }
        }, { passive: true });

        window.addEventListener('scrollend', function () {
            clearNavClickLock();
            setActive(homeSectionKey());
        }, { passive: true });

        window.addEventListener('wheel', onUserScrollIntent, { passive: true });
        window.addEventListener('touchstart', onUserScrollIntent, { passive: true });
        window.addEventListener('keydown', function (event) {
            if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Home', 'End', ' '].indexOf(event.key) > -1) {
                onUserScrollIntent();
            }
        });

        window.addEventListener('load', update);
        update();
    }

    function boot() {
        injectStyle();
        var pageKey = pageKeyFromLocation();
        if (pageKey) {
            setActive(pageKey);
            return;
        }
        if (document.getElementById('uvod') || document.body.getAttribute('data-page') === 'home') {
            bindHomeNavClicks();
            initHomeScrollSpy();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
