/**
 * Vercel Web Analytics – static HTML sites.
 * Requires Web Analytics enabled in the Vercel project dashboard.
 */
(function () {
    'use strict';

    window.va = window.va || function () {
        (window.vaq = window.vaq || []).push(arguments);
    };

    if (document.querySelector('script[src="/_vercel/insights/script.js"]')) {
        return;
    }

    var script = document.createElement('script');
    script.defer = true;
    script.src = '/_vercel/insights/script.js';
    (document.head || document.documentElement).appendChild(script);
})();
