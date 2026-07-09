/**
 * Rotate info-banner messages – one element, fade out → swap → fade in.
 */
(function () {
    'use strict';

    var TEXTS = [
        'Srpen: výroba a logistika mají 3týdenní výluku. Objednávky s dodáním před výlukou zašlete nejpozději do <strong>10. 7. 2026</strong>.',
        'U objednávek z července a srpna platí dodací lhůta 3–4 týdny s dodáním v <strong>září 2026</strong>.',
    ];

    var DISPLAY_MS = 5500;
    var FADE_MS = 450;

    var el = document.querySelector('.info-banner__message');
    var viewport = el && el.parentElement;
    if (!el || !viewport) {
        return;
    }

    var index = 0;
    var busy = false;
    var timer = null;

    function prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function setViewportHeight() {
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
        timer = window.setTimeout(cycle, DISPLAY_MS);
    }

    function cycle() {
        if (busy) {
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

    el.innerHTML = TEXTS[0];
    setViewportHeight();
    window.addEventListener('resize', setViewportHeight);
    scheduleNext();
})();
