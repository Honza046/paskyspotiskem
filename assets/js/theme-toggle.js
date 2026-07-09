/**
 * Dark / light theme toggle. Persists choice in localStorage (pasky-theme).
 */
(function () {
    'use strict';

    var STORAGE_KEY = 'pasky-theme';
    var btn = document.getElementById('theme-toggle');
    if (!btn) {
        return;
    }

    function setTheme(dark) {
        document.documentElement.classList.toggle('dark', dark);
        try {
            localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light');
        } catch (e) {}
    }

    function flashTransition() {
        document.documentElement.classList.add('theme-transition');
        window.setTimeout(function () {
            document.documentElement.classList.remove('theme-transition');
        }, 250);
    }

    btn.addEventListener('click', function () {
        flashTransition();
        setTheme(!document.documentElement.classList.contains('dark'));
    });
})();
