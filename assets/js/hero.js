(function () {
    'use strict';

    var slider = document.querySelector('[data-hero-slider]');

    if (!slider) {
        return;
    }

    var slides = slider.querySelectorAll('[data-slide]');
    var dots = slider.querySelectorAll('[data-slide-dot]');
    var current = 0;
    var interval = 6000;
    var timer;

    function goTo(index) {
        if (!slides.length) {
            return;
        }

        current = (index + slides.length) % slides.length;

        slides.forEach(function (slide, i) {
            slide.classList.toggle('is-active', i === current);
        });

        dots.forEach(function (dot, i) {
            var active = i === current;
            dot.classList.toggle('is-active', active);
            dot.setAttribute('aria-selected', active ? 'true' : 'false');
        });
    }

    function next() {
        goTo(current + 1);
    }

    function start() {
        stop();
        timer = window.setInterval(next, interval);
    }

    function stop() {
        if (timer) {
            window.clearInterval(timer);
        }
    }

    dots.forEach(function (dot) {
        dot.addEventListener('click', function () {
            goTo(parseInt(dot.getAttribute('data-slide-dot'), 10));
            start();
        });
    });

    slider.addEventListener('mouseenter', stop);
    slider.addEventListener('mouseleave', start);

    goTo(0);
    start();
})();
