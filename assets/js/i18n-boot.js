/**
 * Early locale detect – hide body until i18n applies (prevents Czech flash on EN/DE/IT).
 * Also enables perf-lite mode when GPU acceleration is unavailable.
 * Must load synchronously in <head> before first paint.
 */
(function () {
    'use strict';

    function isSoftwareRenderer() {
        try {
            var canvas = document.createElement('canvas');
            var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (!gl) {
                return true;
            }
            var ext = gl.getExtension('WEBGL_debug_renderer_info');
            if (!ext) {
                return false;
            }
            var renderer = String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) || '').toLowerCase();
            return /swiftshader|llvmpipe|software|soft rasterizer|microsoft basic render/.test(renderer);
        } catch (err) {
            return false;
        }
    }

    function wantsPerfLite() {
        try {
            if (localStorage.getItem('pasky-perf-lite') === '1') {
                return true;
            }
            if (localStorage.getItem('pasky-perf-lite') === '0') {
                return false;
            }
        } catch (e) {}
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return true;
        }
        if (window.matchMedia('(prefers-reduced-transparency: reduce)').matches) {
            return true;
        }
        if (window.matchMedia('(update: slow)').matches) {
            return true;
        }
        return isSoftwareRenderer();
    }

    if (wantsPerfLite()) {
        document.documentElement.classList.add('perf-lite');
    }

    var SUPPORTED = ['cs', 'en', 'de', 'it'];
    var DEFAULT = 'cs';
    var STORAGE_KEY = 'paskyonline_lang';
    var I18N_VER = '40';

    function getLocale() {
        var params = new URLSearchParams(window.location.search);
        var lang = (params.get('lang') || '').toLowerCase();
        if (SUPPORTED.indexOf(lang) > -1) {
            return lang;
        }
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            if (stored && SUPPORTED.indexOf(stored) > -1) {
                return stored;
            }
        } catch (e) {}
        return DEFAULT;
    }

    var locale = getLocale();
    if (locale === DEFAULT) {
        return;
    }

    var style = document.createElement('style');
    style.id = 'i18n-boot-style';
    style.textContent =
        'html.i18n-pending{background-color:#f8fafc}' +
        'html.i18n-pending body{visibility:hidden}';
    document.head.appendChild(style);
    document.documentElement.classList.add('i18n-pending');

    var preload = document.createElement('link');
    preload.rel = 'preload';
    preload.as = 'fetch';
    preload.href = '/data/i18n/' + locale + '.json?v=' + I18N_VER;
    preload.crossOrigin = 'same-origin';
    document.head.appendChild(preload);
})();
