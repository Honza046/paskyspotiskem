/**
 * GET /api/info-banner – public live info-banner config.
 * Optional ?lang=cs|en|de|it returns only that language's messages.
 */

const { getBannerConfig } = require('../lib/banner-store');

module.exports = async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Cache-Control', 'public, max-age=30, stale-while-revalidate=60');

    if (req.method === 'OPTIONS') {
        res.status(204).end();
        return;
    }

    if (req.method !== 'GET') {
        res.setHeader('Allow', 'GET');
        return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }

    try {
        const config = await getBannerConfig();
        const lang = String((req.query && req.query.lang) || '').toLowerCase();
        if (lang && config.messages[lang]) {
            return res.status(200).json({
                ok: true,
                enabled: config.enabled,
                updatedAt: config.updatedAt,
                lang: lang,
                messages: config.messages[lang],
            });
        }
        return res.status(200).json({ ok: true, ...config });
    } catch (e) {
        console.error(e);
        return res.status(500).json({ ok: false, error: 'Nepodařilo se načíst info bar.' });
    }
};
