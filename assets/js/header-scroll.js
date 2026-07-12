/**
 * Hide sticky header on scroll down, reveal on scroll up only (homepage hero only).
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

    var isHomeHero = !!document.getElementById('uvod');
    var fullSiteTopHeight = 0;
    var lastY = 0;
    var ticking = false;
    var hidden = false;
    var canHide = false;
    var anchorNavigating = false;
    var hideAccum = 0;
    var showAccum = 0;
    var MIN_SCROLL = 80;
    var SCROLL_THRESHOLD = 40;
    var NOISE = 3;
    var ENABLE_DELAY_MS = 800;
    var ANCHOR_GRACE_MS = 1400;

    document.documentElement.style.scrollBehavior = 'auto';
    document.documentElement.style.overscrollBehaviorY = 'none';

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

    function measureFullSiteTopHeight() {
        var siteTop = document.querySelector('.site-top');
        if (!siteTop) {
            return;
        }
        var wasHidden = hidden;
        showHeader();
        fullSiteTopHeight = siteTop.offsetHeight;
        if (wasHidden && isHomeHero) {
            setHidden(true);
        }
    }

    function syncSiteTopHeight() {
        var siteTop = document.querySelector('.site-top');
        if (!siteTop) {
            return;
        }
        var height = isHomeHero && fullSiteTopHeight > 0
            ? fullSiteTopHeight
            : siteTop.offsetHeight;
        document.documentElement.style.setProperty('--site-top-height', height + 'px');
    }

    /** Lock hero block height – recalc when site-top size changes (i18n banner text, etc.). */
    function lockHeroLayout() {
        var uvod = document.getElementById('uvod');
        if (!uvod) {
            return;
        }
        var siteTop = document.querySelector('.site-top');
        if (!siteTop) {
            return;
        }
        var topOffset = siteTop.offsetHeight;
        var viewportH = window.visualViewport ? window.visualViewport.height : window.innerHeight;
        var heroH = Math.max(320, Math.ceil(viewportH - topOffset));
        document.documentElement.style.setProperty('--hero-top-offset', topOffset + 'px');
        document.documentElement.style.setProperty('--hero-height', heroH + 'px');
    }

    var resizeTimer;
    function onWindowResize() {
        if (isHomeHero) {
            measureFullSiteTopHeight();
        }
        syncHeaderShellHeight();
        syncSiteTopHeight();
        clearTimeout(resizeTimer);
        resizeTimer = window.setTimeout(lockHeroLayout, 150);
    }

    function syncHeaderShellHeight() {
        if (hidden) {
            return;
        }
        var h = header.offsetHeight;
        if (h > 0) {
            shell.style.setProperty('--site-header-height', h + 'px');
        }
    }

    function initSiteTopHeight() {
        measureFullSiteTopHeight();
        syncHeaderShellHeight();
        lockHeroLayout();
        syncSiteTopHeight();
        var siteTop = document.querySelector('.site-top');
        if (siteTop && typeof ResizeObserver !== 'undefined') {
            new ResizeObserver(function () {
                if (isHomeHero) {
                    if (!hidden) {
                        measureFullSiteTopHeight();
                    }
                    lockHeroLayout();
                }
                syncHeaderShellHeight();
                syncSiteTopHeight();
            }).observe(siteTop);
        }
        window.addEventListener('resize', onWindowResize);
        window.paskyonlineSyncSiteTopHeight = syncSiteTopHeight;
    }

    function setHidden(shouldHide) {
        if (!isHomeHero || hidden === shouldHide) {
            return;
        }
        if (shouldHide) {
            syncHeaderShellHeight();
        }
        hidden = shouldHide;
        shell.classList.toggle('is-collapsed', shouldHide);
        header.setAttribute('aria-hidden', shouldHide ? 'true' : 'false');
        if (shouldHide) {
            closeMobileNav();
            hideAccum = 0;
            showAccum = 0;
        }
    }

    function showHeader() {
        shell.classList.remove('is-collapsed');
        hidden = false;
        header.setAttribute('aria-hidden', 'false');
        hideAccum = 0;
        showAccum = 0;
        window.requestAnimationFrame(function () {
            syncHeaderShellHeight();
            if (!isHomeHero) {
                syncSiteTopHeight();
            }
        });
    }

    function enableHide() {
        if (!isHomeHero) {
            return;
        }
        canHide = true;
        lastY = window.scrollY;
        hideAccum = 0;
        showAccum = 0;
    }

    function beginAnchorNavigation() {
        if (!isHomeHero) {
            return;
        }
        anchorNavigating = true;
        canHide = false;
        showHeader();
        window.setTimeout(function () {
            anchorNavigating = false;
            lastY = window.scrollY;
            hideAccum = 0;
            showAccum = 0;
            if (window.scrollY > MIN_SCROLL) {
                canHide = true;
            }
        }, ANCHOR_GRACE_MS);
    }

    function bindAnchorNavLinks() {
        if (!isHomeHero) {
            return;
        }
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
        if (!isHomeHero) {
            ticking = false;
            return;
        }

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

        var delta = y - lastY;

        if (delta > NOISE) {
            showAccum = 0;
            hideAccum += delta;
            if (hideAccum >= SCROLL_THRESHOLD && y > MIN_SCROLL) {
                setHidden(true);
            }
        } else if (delta < -NOISE) {
            hideAccum = 0;
            showAccum += -delta;
            if (showAccum >= SCROLL_THRESHOLD) {
                setHidden(false);
            }
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
        if (isHomeHero) {
            window.setTimeout(enableHide, ENABLE_DELAY_MS);
        }
    }

    if (isHomeHero) {
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
    }

    window.addEventListener('pageshow', function () {
        boot();
    });

    window.addEventListener('load', function () {
        showHeader();
        syncHeaderShellHeight();
        lockHeroLayout();
        if (isHomeHero) {
            measureFullSiteTopHeight();
        }
        syncSiteTopHeight();
        lastY = window.scrollY;
        if (isHomeHero && window.location.hash) {
            beginAnchorNavigation();
        }
    });

    window.paskyonlineBeginAnchorNavigation = beginAnchorNavigation;
    window.paskyonlineLockHeroLayout = lockHeroLayout;

    document.addEventListener('pasky:i18n-ready', function () {
        window.requestAnimationFrame(function () {
            if (isHomeHero) {
                measureFullSiteTopHeight();
                lockHeroLayout();
            }
            syncSiteTopHeight();
        });
    });

    boot();
})();
