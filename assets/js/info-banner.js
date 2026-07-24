/**
 * Rotate info-banner messages – one element, fade out → swap → fade in.
 * Priority: live /api/info-banner → i18n JSON → DEFAULT_TEXTS.
 */
(function () {
    'use strict';

    var DEFAULT_TEXTS = [
        'Srpen: výroba a logistika mají 3týdenní výluku. Objednávky s dodáním před výlukou zašlete nejpozději do <strong>10. 7. 2026</strong>.',
        'U objednávek z července a srpna platí dodací lhůta 3–4 týdny s dodáním v <strong>září 2026</strong>.',
    ];

    var DISPLAY_MS = 5500;
    var FADE_MS = 450;

    var el = document.querySelector('.info-banner__message');
    var viewport = el && el.parentElement;
    var banner = document.querySelector('.info-banner');
    if (!el || !viewport) {
        return;
    }

    var TEXTS = DEFAULT_TEXTS.slice();
    var index = 0;
    var busy = false;
    var timer = null;
    var started = false;
    var liveLoaded = false;

    function currentLang() {
        if (window.paskyI18n && typeof window.paskyI18n.getLang === 'function') {
            return window.paskyI18n.getLang();
        }
        var htmlLang = (document.documentElement.lang || 'cs').toLowerCase();
        if (htmlLang.indexOf('en') === 0) return 'en';
        if (htmlLang.indexOf('de') === 0) return 'de';
        if (htmlLang.indexOf('it') === 0) return 'it';
        return 'cs';
    }

    function getI18nTexts() {
        if (window.paskyI18n && typeof window.paskyI18n.get === 'function') {
            var msgs = window.paskyI18n.get('info_banner.messages');
            if (Array.isArray(msgs) && msgs.length) {
                return msgs.slice();
            }
        }
        return DEFAULT_TEXTS.slice();
    }

    function applyAriaLabel() {
        if (!banner) {
            return;
        }
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            banner.setAttribute('aria-label', window.paskyI18n.t('info_banner.aria_label', 'Důležité informace'));
        }
    }

    function setBannerVisible(on) {
        if (!banner) return;
        banner.hidden = !on;
        banner.style.display = on ? '' : 'none';
        if (typeof window.paskyonlineSyncSiteTopHeight === 'function') {
            window.paskyonlineSyncSiteTopHeight();
        }
        if (typeof window.paskyonlineLockHeroLayout === 'function') {
            window.paskyonlineLockHeroLayout();
        }
    }

    function prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function clearTimer() {
        if (timer) {
            window.clearTimeout(timer);
            timer = null;
        }
    }

    function setViewportHeight() {
        if (!TEXTS.length) {
            viewport.style.minHeight = '0px';
            return;
        }
        var measure = document.createElement('p');
        measure.className = 'info-banner__message';
        measure.setAttribute('aria-hidden', 'true');
        measure.style.cssText = 'position:absolute;visibility:hidden;pointer-events:none;left:0;right:0;padding:0;margin:0;';
        viewport.appendChild(measure);

        var maxHeight = 0;
        TEXTS.forEach(function (text) {
            measure.innerHTML = text;
            maxHeight = Math.max(maxHeight, measure.offsetHeight);
        });

        viewport.removeChild(measure);
        viewport.style.minHeight = maxHeight + 'px';
        if (typeof window.paskyonlineSyncSiteTopHeight === 'function') {
            window.paskyonlineSyncSiteTopHeight();
        }
        if (typeof window.paskyonlineLockHeroLayout === 'function') {
            window.paskyonlineLockHeroLayout();
        }
    }

    function waitForOpacityTransition(done) {
        var finished = false;

        function complete() {
            if (finished) return;
            finished = true;
            el.removeEventListener('transitionend', onEnd);
            done();
        }

        function onEnd(e) {
            if (e.target === el && e.propertyName === 'opacity') {
                complete();
            }
        }

        el.addEventListener('transitionend', onEnd);
        window.setTimeout(complete, FADE_MS + 100);
    }

    function scheduleNext() {
        clearTimer();
        if (TEXTS.length <= 1) {
            return;
        }
        timer = window.setTimeout(cycle, DISPLAY_MS);
    }

    function cycle() {
        if (busy || TEXTS.length <= 1) {
            return;
        }
        busy = true;

        if (prefersReducedMotion()) {
            index = (index + 1) % TEXTS.length;
            el.innerHTML = TEXTS[index];
            busy = false;
            scheduleNext();
            return;
        }

        el.classList.add('is-fading');

        waitForOpacityTransition(function () {
            index = (index + 1) % TEXTS.length;
            el.innerHTML = TEXTS[index];
            void el.offsetHeight;

            requestAnimationFrame(function () {
                requestAnimationFrame(function () {
                    el.classList.remove('is-fading');

                    waitForOpacityTransition(function () {
                        busy = false;
                        scheduleNext();
                    });
                });
            });
        });
    }

    function showCurrent() {
        if (!TEXTS.length) {
            el.innerHTML = '';
            setViewportHeight();
            return;
        }
        index = 0;
        el.innerHTML = TEXTS[0];
        setViewportHeight();
    }

    function restart(texts, enabled) {
        clearTimer();
        busy = false;
        TEXTS = Array.isArray(texts) && texts.length ? texts.slice() : [];
        applyAriaLabel();
        if (enabled === false || !TEXTS.length) {
            setBannerVisible(false);
            return;
        }
        setBannerVisible(true);
        showCurrent();
        scheduleNext();
    }

    function applyLiveConfig(data) {
        if (!data || !data.ok) return false;
        liveLoaded = true;
        var lang = currentLang();
        var messages = null;
        if (Array.isArray(data.messages) && data.lang) {
            messages = data.messages;
        } else if (data.messages && Array.isArray(data.messages[lang])) {
            messages = data.messages[lang];
        } else if (data.messages && Array.isArray(data.messages.cs)) {
            messages = data.messages.cs;
        }
        restart(messages || [], data.enabled !== false);
        return true;
    }

    function fetchLive() {
        var lang = currentLang();
        var url = '/api/info-banner?lang=' + encodeURIComponent(lang) + '&t=' + Date.now();
        return fetch(url, { credentials: 'omit', cache: 'no-store' })
            .then(function (res) {
                if (!res.ok) throw new Error('banner http ' + res.status);
                return res.json();
            })
            .then(function (data) {
                applyLiveConfig(data);
            })
            .catch(function () {
                if (!liveLoaded) {
                    restart(getI18nTexts(), true);
                }
            });
    }

    function boot() {
        if (started) {
            if (liveLoaded) {
                fetchLive();
            } else {
                restart(getI18nTexts(), true);
                fetchLive();
            }
            return;
        }
        started = true;
        applyAriaLabel();
        restart(getI18nTexts(), true);
        window.addEventListener('resize', setViewportHeight);
        fetchLive();
    }

    document.addEventListener('pasky:i18n-ready', boot);
    document.addEventListener('pasky:i18n-pages-applied', function () {
        if (started) fetchLive();
    });

    if (window.paskyI18n) {
        boot();
    } else {
        window.setTimeout(function () {
            if (!started) {
                boot();
            }
        }, 2500);
    }

    window.paskyonlineReloadInfoBanner = fetchLive;
})();
