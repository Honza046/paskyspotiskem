/**
 * Cult UI–inspired interactions (vanilla JS ports).
 */
(function () {
    'use strict';

    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* --- Border beam wrap ------------------------------------------------ */
    function initBeamButtons() {
        var selector = [
            '#hero-cta-primary',
            '#sample-inquiry-cta',
            '#gform_submit_button_1',
            '.gform_next_button',
            'a[href*="gf_1"].bg-gradient-to-r',
            'a[href*="#gf_1"].bg-gradient-to-r',
        ].join(',');

        document.querySelectorAll(selector).forEach(function (el) {
            if (el.closest('.btn-beam-wrap') || el.classList.contains('btn-beam-skip')) {
                return;
            }

            var wrap = document.createElement('span');
            wrap.className = 'btn-beam-wrap';

            var radius = window.getComputedStyle(el).borderRadius || '9999px';
            var px = parseFloat(radius);
            if (el.classList.contains('rounded-full') || px >= 999 || isNaN(px)) {
                radius = '9999px';
            } else {
                radius = Math.max(px, 16) + 'px';
            }
            wrap.style.setProperty('--beam-radius', radius);
            el.style.borderRadius = radius === '9999px' ? '9999px' : radius;

            el.parentNode.insertBefore(wrap, el);
            wrap.appendChild(el);
            el.classList.add('btn-beam-inner');
        });
    }

    /* --- Animated numbers ------------------------------------------------ */
    function formatNumber(n, decimals) {
        return decimals > 0 ? n.toFixed(decimals) : String(Math.round(n));
    }

    function animateNumberEl(el) {
        if (el.dataset.animated === '1') {
            return;
        }
        el.dataset.animated = '1';
        el.classList.add('animate-number');

        var staticText = el.getAttribute('data-animate-static');
        if (staticText) {
            el.textContent = staticText;
            el.classList.add('is-visible');
            return;
        }

        var target = parseFloat(el.getAttribute('data-animate-value') || '0', 10);
        var suffix = el.getAttribute('data-animate-suffix') || '';
        var prefix = el.getAttribute('data-animate-prefix') || '';
        var decimals = parseInt(el.getAttribute('data-animate-decimals') || '0', 10);
        var duration = reducedMotion ? 0 : parseInt(el.getAttribute('data-animate-duration') || '1400', 10);

        el.classList.add('animate-number');

        if (reducedMotion || duration === 0 || isNaN(target)) {
            el.textContent = prefix + formatNumber(target, decimals) + suffix;
            el.classList.add('is-visible');
            return;
        }

        var start = null;
        function step(ts) {
            if (!start) start = ts;
            var p = Math.min((ts - start) / duration, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = prefix + formatNumber(target * eased, decimals) + suffix;
            if (p < 1) {
                requestAnimationFrame(step);
            } else {
                el.classList.add('is-visible');
            }
        }
        requestAnimationFrame(step);
    }

    function initAnimatedNumbers() {
        document.querySelectorAll('[data-animate-value], [data-animate-static]').forEach(function (el) {
            if (!('IntersectionObserver' in window)) {
                animateNumberEl(el);
                return;
            }
            var obs = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        animateNumberEl(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.35 });
            obs.observe(el);
        });
    }

    /* --- Direction-aware tabs (gallery type filter) ---------------------- */
    function initDirectionTabs() {
        var tabsRoot = document.querySelector('[data-dir-tabs]');
        if (!tabsRoot) return;

        var buttons = Array.prototype.slice.call(tabsRoot.querySelectorAll('[data-dir-tab]'));
        var indicator = tabsRoot.querySelector('.dir-tabs__indicator');
        var filterPanel = document.getElementById('gallery-filter');
        if (!buttons.length || !filterPanel) return;

        function moveIndicator(btn) {
            if (!indicator) return;
            indicator.style.width = btn.offsetWidth + 'px';
            indicator.style.left = btn.offsetLeft + 'px';
        }

        function setTypeFilter(typeTag) {
            if (typeof window.paskyGallerySetTypeFilter === 'function') {
                window.paskyGallerySetTypeFilter(typeTag || null);
            }
        }

        buttons.forEach(function (btn, i) {
            btn.addEventListener('click', function () {
                buttons.forEach(function (b) { b.setAttribute('aria-selected', 'false'); });
                btn.setAttribute('aria-selected', 'true');
                moveIndicator(btn);
                setTypeFilter(btn.getAttribute('data-type-filter') || '');
            });
            if (i === 0) {
                btn.setAttribute('aria-selected', 'true');
                requestAnimationFrame(function () { moveIndicator(btn); });
            }
        });

        window.addEventListener('resize', function () {
            var active = tabsRoot.querySelector('[aria-selected="true"]');
            if (active) moveIndicator(active);
        });

        document.addEventListener('pasky:gallery-type-cleared', function () {
            buttons.forEach(function (b, i) {
                b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
            });
            moveIndicator(buttons[0]);
        });
    }

    function init() {
        initAnimatedNumbers();
        initDirectionTabs();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
