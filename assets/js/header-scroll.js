/**
 * Sticky site-top: locked homepage hero, solid header,
 * hide after hero (scroll down) / reveal on deliberate scroll up.
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
    var lockedHeroHeight = 0;
    var lastLayoutWidth = 0;
    var lastY = 0;
    var scrollTicking = false;
    var hidden = false;
    var anchorNavigating = false;
    var hideAccum = 0;
    var showAccum = 0;

    var NOISE = 3;
    var HIDE_THRESHOLD = 56;
    var SHOW_THRESHOLD = 140;
    var PAST_HERO_DEFAULT = 72;
    var ANCHOR_GRACE_MS = 1400;

    document.documentElement.style.scrollBehavior = 'auto';
    document.documentElement.style.overscrollBehaviorY = 'none';
    if (isHomeHero) {
        document.documentElement.classList.add('home-hero');
    }

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
        if (wasHidden) {
            setHidden(false);
        }
        fullSiteTopHeight = siteTop.offsetHeight;
        if (wasHidden && pastHeroZone()) {
            setHidden(true);
        }
    }

    function syncSiteTopHeight() {
        var siteTop = document.querySelector('.site-top');
        if (!siteTop) {
            return;
        }
        document.documentElement.style.setProperty('--site-top-height', siteTop.offsetHeight + 'px');
    }

    function lockHeroLayout(force) {
        var uvod = document.getElementById('uvod');
        if (!uvod) {
            return;
        }

        var layoutWidth = window.innerWidth;
        if (!force && lockedHeroHeight > 0 && layoutWidth === lastLayoutWidth) {
            return;
        }

        var siteTop = document.querySelector('.site-top');
        if (!siteTop) {
            return;
        }

        if (isHomeHero && fullSiteTopHeight <= 0) {
            measureFullSiteTopHeight();
        }

        var topOffset = isHomeHero && fullSiteTopHeight > 0
            ? fullSiteTopHeight
            : siteTop.offsetHeight;
        var viewportH = window.innerHeight;
        var heroH = Math.max(320, Math.ceil(viewportH - topOffset));

        lockedHeroHeight = heroH;
        lastLayoutWidth = layoutWidth;
        document.documentElement.style.setProperty('--hero-top-offset', topOffset + 'px');
        document.documentElement.style.setProperty('--hero-height', heroH + 'px');
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

    function pastHeroZone() {
        if (!isHomeHero) {
            return window.scrollY > PAST_HERO_DEFAULT;
        }
        var uvod = document.getElementById('uvod');
        if (!uvod) {
            return window.scrollY > PAST_HERO_DEFAULT;
        }
        return window.scrollY >= uvod.offsetTop + uvod.offsetHeight - 40;
    }

    function setHidden(shouldHide) {
        if (hidden === shouldHide) {
            return;
        }
        if (shouldHide && !pastHeroZone()) {
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
        window.requestAnimationFrame(syncSiteTopHeight);
    }

    function showHeader() {
        setHidden(false);
        hideAccum = 0;
        showAccum = 0;
        window.requestAnimationFrame(syncHeaderShellHeight);
    }

    function syncScrollState() {
        var y = window.scrollY;

        if (!pastHeroZone()) {
            showHeader();
            lastY = y;
            scrollTicking = false;
            return;
        }

        if (anchorNavigating) {
            lastY = y;
            scrollTicking = false;
            return;
        }

        var delta = y - lastY;

        if (delta > NOISE) {
            showAccum = 0;
            hideAccum += delta;
            if (hideAccum >= HIDE_THRESHOLD) {
                setHidden(true);
            }
        } else if (delta < -NOISE) {
            hideAccum = 0;
            showAccum += -delta;
            if (showAccum >= SHOW_THRESHOLD) {
                setHidden(false);
            }
        }

        lastY = y;
        scrollTicking = false;
    }

    function onScroll() {
        if (!scrollTicking) {
            scrollTicking = true;
            window.requestAnimationFrame(syncScrollState);
        }
    }

    function refreshLayout(forceHero) {
        if (isHomeHero) {
            if (forceHero) {
                fullSiteTopHeight = 0;
            }
            measureFullSiteTopHeight();
            lockHeroLayout(!!forceHero);
        }
        syncHeaderShellHeight();
        syncSiteTopHeight();
    }

    var resizeTimer;
    function onWindowResize() {
        refreshLayout(true);
        clearTimeout(resizeTimer);
        resizeTimer = window.setTimeout(function () {
            if (isHomeHero) {
                lockHeroLayout(true);
            }
            syncScrollState();
        }, 150);
    }

    function initLayout() {
        refreshLayout(true);

        var lastObservedWidth = window.innerWidth;
        window.addEventListener('resize', function () {
            if (window.innerWidth === lastObservedWidth) {
                return;
            }
            lastObservedWidth = window.innerWidth;
            onWindowResize();
        });
        window.paskyonlineSyncSiteTopHeight = syncSiteTopHeight;
    }

    function beginAnchorNavigation() {
        anchorNavigating = true;
        showHeader();
        window.setTimeout(function () {
            anchorNavigating = false;
            lastY = window.scrollY;
            hideAccum = 0;
            showAccum = 0;
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

    function boot() {
        initLayout();
        bindAnchorNavLinks();
        lastY = window.scrollY;
        syncScrollState();
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('hashchange', beginAnchorNavigation);
    }

    window.addEventListener('pageshow', boot);
    window.addEventListener('load', function () {
        boot();
        syncScrollState();
    });
    window.paskyonlineBeginAnchorNavigation = beginAnchorNavigation;
    window.paskyonlineLockHeroLayout = lockHeroLayout;

    document.addEventListener('pasky:i18n-ready', function () {
        window.requestAnimationFrame(function () {
            refreshLayout(true);
            syncScrollState();
        });
    });

    boot();
})();
