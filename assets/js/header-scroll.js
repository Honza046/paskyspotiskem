/**
 * Sticky site-top: always-visible glass header, homepage hero lock,
 * and --site-top-height / --site-header-height sync for scroll-padding.
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

    document.documentElement.style.scrollBehavior = 'auto';
    document.documentElement.style.overscrollBehaviorY = 'none';
    if (isHomeHero) {
        document.documentElement.classList.add('home-hero');
    }

    /* Always visible — clear any leftover collapsed state from older scripts. */
    shell.classList.remove('is-collapsed');
    header.setAttribute('aria-hidden', 'false');

    function measureFullSiteTopHeight() {
        var siteTop = document.querySelector('.site-top');
        if (!siteTop) {
            return;
        }
        fullSiteTopHeight = siteTop.offsetHeight;
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
        var h = header.offsetHeight;
        if (h > 0) {
            shell.style.setProperty('--site-header-height', h + 'px');
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
            syncHeaderShellHeight();
            syncSiteTopHeight();
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

    /* Kept for nav-active / hash clicks — header no longer hides. */
    function beginAnchorNavigation() {}

    function boot() {
        initLayout();
    }

    window.addEventListener('pageshow', boot);
    window.addEventListener('load', boot);
    window.paskyonlineBeginAnchorNavigation = beginAnchorNavigation;
    window.paskyonlineLockHeroLayout = lockHeroLayout;

    document.addEventListener('pasky:i18n-ready', function () {
        window.requestAnimationFrame(function () {
            refreshLayout(true);
        });
    });

    boot();
})();
