/**
 * Vercel Speed Insights – static HTML sites.
 * Requires Speed Insights enabled in the Vercel project dashboard.
 */
(function () {
    'use strict';

    if (document.querySelector('script[src*="/_vercel/speed-insights/script"]')) {
        return;
    }

    var script = document.createElement('script');
    script.defer = true;
    script.src = '/_vercel/speed-insights/script.js';
    (document.head || document.documentElement).appendChild(script);
})();
