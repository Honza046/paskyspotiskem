/**
 * Footer credit easter egg — hover Jan Sedlář for a surprise.
 */
(function () {
    'use strict';

    var DEFAULT = 'Jan Sedlář';
    var MESSAGES = [
        'lepil i tento web',
        'kód · káva · lepidlo',
        'certifikováno Ctrl+S',
        'potisk A+ ✓',
        'hot melt edition',
        'made with 🧡 a lepidlem',
    ];

    function pickMessage() {
        return MESSAGES[Math.floor(Math.random() * MESSAGES.length)];
    }

    function spawnTape(x, y) {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        for (var i = 0; i < 4; i += 1) {
            var tape = document.createElement('span');
            tape.className = 'footer-credit__tape';
            tape.style.left = x + 'px';
            tape.style.top = y + 'px';
            tape.style.setProperty('--tape-rot', (Math.random() * 40 - 20) + 'deg');
            tape.style.setProperty('--tape-dx', (Math.random() * 24 - 12) + 'px');
            tape.style.setProperty('--tape-dy', (-24 - Math.random() * 20) + 'px');
            document.body.appendChild(tape);
            window.setTimeout(function (node) {
                node.remove();
            }, 900, tape);
        }
    }

    function initCredit(button) {
        var textEl = button.querySelector('.footer-credit__text');
        if (!textEl) {
            return;
        }

        var swapTimer = null;

        function restore() {
            window.clearTimeout(swapTimer);
            button.classList.remove('is-swapping', 'is-active');
            textEl.textContent = DEFAULT;
        }

        button.addEventListener('mouseenter', function (event) {
            button.classList.add('is-active');
            button.classList.add('is-swapping');
            spawnTape(event.clientX, event.clientY);

            swapTimer = window.setTimeout(function () {
                textEl.textContent = pickMessage();
                button.classList.remove('is-swapping');
            }, 160);
        });

        button.addEventListener('mouseleave', restore);
    }

    function boot() {
        document.querySelectorAll('.footer-credit').forEach(initCredit);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
