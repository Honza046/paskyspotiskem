/**
 * Homepage product carousel – dots + autoplay (pause/resume), seamless loop.
 */
(function () {
    'use strict';

    var root = document.querySelector('[data-product-carousel]');
    if (!root) return;

    var track = root.querySelector('[data-carousel-track]');
    var dotsWrap = root.querySelector('[data-carousel-dots]');
    if (!track || !dotsWrap) return;

    var originalSlides = Array.prototype.slice.call(
        track.querySelectorAll('.product-carousel__slide:not([data-carousel-clone])')
    );
    if (!originalSlides.length) return;

    var autoplayMs = 4500;
    var timer = null;
    var currentPage = 0;
    var pageCount = 1;
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var ignoreScrollSync = false;
    var ignoreScrollTimer = null;
    var wrapJumpTimer = null;
    var looping = false;
    var remainingMs = autoplayMs;
    var segmentStartedAt = 0;
    var paused = false;

    function slideStep() {
        var first = originalSlides[0];
        if (!first) return 280;
        var style = window.getComputedStyle(track);
        var gap = parseFloat(style.columnGap || style.gap) || 20;
        return first.getBoundingClientRect().width + gap;
    }

    function gapSize() {
        var style = window.getComputedStyle(track);
        return parseFloat(style.columnGap || style.gap) || 20;
    }

    function wrapScrollLeft() {
        return Math.max(0, originalSlides.length * slideStep() - gapSize());
    }

    function maxScrollOriginal() {
        return Math.max(0, wrapScrollLeft() - track.clientWidth);
    }

    function computePageCount() {
        var step = slideStep();
        var max = maxScrollOriginal();
        if (step <= 0 || max <= 4) return 1;
        return Math.max(1, Math.round(max / step) + 1);
    }

    function pageFromScroll() {
        var step = slideStep();
        if (step <= 0) return 0;
        var raw = Math.round(track.scrollLeft / step);
        if (raw >= pageCount) return 0;
        return Math.max(0, Math.min(pageCount - 1, raw));
    }

    function clearClones() {
        Array.prototype.slice.call(track.querySelectorAll('[data-carousel-clone]')).forEach(function (node) {
            node.parentNode.removeChild(node);
        });
    }

    function ensureClones() {
        clearClones();
        looping = pageCount > 1 && !reducedMotion;
        if (!looping) return;

        originalSlides.forEach(function (slide) {
            var clone = slide.cloneNode(true);
            clone.setAttribute('data-carousel-clone', '1');
            clone.setAttribute('aria-hidden', 'true');
            clone.setAttribute('tabindex', '-1');
            track.appendChild(clone);
        });
    }

    function activeFill() {
        return dotsWrap.querySelector('.product-carousel__dot.is-active .product-carousel__dot-fill');
    }

    function canAnimateFill() {
        return !reducedMotion && !dotsWrap.classList.contains('is-picking') && !paused;
    }

    function restartFill() {
        var fill = activeFill();
        if (!fill) return;
        fill.style.animationPlayState = '';
        fill.style.width = '';
        fill.classList.remove('is-filling');
        void fill.offsetWidth;
        if (!reducedMotion && !dotsWrap.classList.contains('is-picking')) {
            fill.classList.add('is-filling');
            if (paused) {
                fill.style.animationPlayState = 'paused';
            }
        }
        remainingMs = autoplayMs;
        segmentStartedAt = Date.now();
    }

    function syncDots(restart) {
        var dots = dotsWrap.querySelectorAll('.product-carousel__dot');
        dots.forEach(function (dot, idx) {
            var on = idx === currentPage;
            var wasOn = dot.classList.contains('is-active');
            dot.classList.toggle('is-active', on);
            var fill = dot.querySelector('.product-carousel__dot-fill');
            if (!fill) return;

            if (!on) {
                fill.classList.remove('is-filling');
                fill.style.animationPlayState = '';
                fill.style.width = '';
                return;
            }

            if (!restart && wasOn) {
                return;
            }

            fill.style.animationPlayState = '';
            fill.style.width = '';
            fill.classList.remove('is-filling');
            void fill.offsetWidth;
            if (!reducedMotion && !dotsWrap.classList.contains('is-picking')) {
                fill.classList.add('is-filling');
                if (paused) {
                    fill.style.animationPlayState = 'paused';
                }
            }
            remainingMs = autoplayMs;
            segmentStartedAt = Date.now();
        });
    }

    function lockScrollSync(ms) {
        ignoreScrollSync = true;
        if (ignoreScrollTimer) {
            window.clearTimeout(ignoreScrollTimer);
        }
        ignoreScrollTimer = window.setTimeout(function () {
            ignoreScrollSync = false;
            ignoreScrollTimer = null;
        }, ms || 600);
    }

    function jumpToStart() {
        var prev = track.style.scrollBehavior;
        track.style.scrollBehavior = 'auto';
        track.scrollLeft = 0;
        track.style.scrollBehavior = prev;
    }

    function scrollToPage(page, behavior) {
        var step = slideStep();
        var left = Math.min(maxScrollOriginal(), Math.max(0, page * step));

        lockScrollSync(600);
        track.scrollTo({ left: left, behavior: behavior || 'smooth' });
        currentPage = page;
        syncDots(true);
    }

    function wrapForward() {
        if (!looping) {
            scrollToPage(0, 'smooth');
            return;
        }

        if (wrapJumpTimer) {
            window.clearTimeout(wrapJumpTimer);
            wrapJumpTimer = null;
        }

        lockScrollSync(900);
        currentPage = 0;
        syncDots(true);

        var target = wrapScrollLeft();
        track.scrollTo({ left: target, behavior: reducedMotion ? 'auto' : 'smooth' });

        wrapJumpTimer = window.setTimeout(function () {
            wrapJumpTimer = null;
            jumpToStart();
            ignoreScrollSync = false;
        }, reducedMotion ? 30 : 520);
    }

    function goNext() {
        if (currentPage >= pageCount - 1) {
            wrapForward();
        } else {
            scrollToPage(currentPage + 1, 'smooth');
        }
    }

    function normalizeAfterUserScroll() {
        if (!looping) return;
        var wrapAt = wrapScrollLeft();
        if (track.scrollLeft >= wrapAt - 8) {
            lockScrollSync(100);
            jumpToStart();
            currentPage = 0;
            syncDots(true);
        }
    }

    function buildDots() {
        pageCount = computePageCount();
        ensureClones();

        dotsWrap.innerHTML = '';
        dotsWrap.hidden = pageCount <= 1;
        for (var i = 0; i < pageCount; i++) {
            (function (page) {
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'product-carousel__dot';
                btn.setAttribute('aria-label', 'Skupina pásek ' + (page + 1));
                var fill = document.createElement('span');
                fill.className = 'product-carousel__dot-fill';
                btn.appendChild(fill);
                btn.addEventListener('click', function () {
                    if (page === 0 && currentPage === pageCount - 1 && looping) {
                        wrapForward();
                    } else {
                        scrollToPage(page, 'smooth');
                    }
                    remainingMs = autoplayMs;
                    startAutoplay(true);
                });
                dotsWrap.appendChild(btn);
            })(i);
        }
        currentPage = pageFromScroll();
        syncDots(true);
    }

    function clearTimer() {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
    }

    function pauseAutoplay() {
        if (paused) return;
        paused = true;
        clearTimer();

        if (segmentStartedAt && remainingMs > 0) {
            var elapsed = Date.now() - segmentStartedAt;
            remainingMs = Math.max(150, remainingMs - elapsed);
        }

        var fill = activeFill();
        if (fill && fill.classList.contains('is-filling')) {
            fill.style.animationPlayState = 'paused';
        }
    }

    function scheduleAdvance(delay) {
        clearTimer();
        segmentStartedAt = Date.now();
        timer = window.setTimeout(function () {
            timer = null;
            if (document.hidden || paused) return;
            goNext();
            remainingMs = autoplayMs;
            if (!paused) {
                scheduleAdvance(autoplayMs);
            }
        }, delay);
    }

    function startAutoplay(forceRestart) {
        if (reducedMotion || pageCount <= 1) return;

        paused = false;

        var fill = activeFill();
        if (forceRestart || !fill || !fill.classList.contains('is-filling')) {
            remainingMs = autoplayMs;
            restartFill();
        } else {
            fill.style.animationPlayState = 'running';
        }

        scheduleAdvance(remainingMs);
    }

    function stopAutoplay() {
        pauseAutoplay();
    }

    var scrollTick = false;
    track.addEventListener('scroll', function () {
        if (ignoreScrollSync || scrollTick) return;
        scrollTick = true;
        window.requestAnimationFrame(function () {
            scrollTick = false;
            if (ignoreScrollSync) return;
            var page = pageFromScroll();
            if (page !== currentPage) {
                currentPage = page;
                syncDots(true);
                remainingMs = autoplayMs;
                if (!paused) {
                    scheduleAdvance(autoplayMs);
                }
            }
            normalizeAfterUserScroll();
        });
    }, { passive: true });

    track.addEventListener('pointerenter', pauseAutoplay);
    track.addEventListener('pointerleave', function () {
        startAutoplay(false);
    });

    if (finePointer) {
        dotsWrap.addEventListener('mouseenter', function () {
            pauseAutoplay();
            dotsWrap.classList.add('is-picking');
        });
        dotsWrap.addEventListener('mouseleave', function () {
            dotsWrap.classList.remove('is-picking');
            startAutoplay(false);
        });
        dotsWrap.addEventListener('focusin', function () {
            pauseAutoplay();
            dotsWrap.classList.add('is-picking');
        });
        dotsWrap.addEventListener('focusout', function (e) {
            if (dotsWrap.contains(e.relatedTarget)) return;
            dotsWrap.classList.remove('is-picking');
            startAutoplay(false);
        });
    }

    var resizeTimer = null;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            buildDots();
            remainingMs = autoplayMs;
            startAutoplay(true);
        }, 120);
    });

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) pauseAutoplay();
        else startAutoplay(false);
    });

    buildDots();
    startAutoplay(true);
})();
