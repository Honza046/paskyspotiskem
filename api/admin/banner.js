/**
 * GET/PUT /api/admin/banner – read/save info-banner config (auth required).
 */

const { requireAdmin } = require('../../lib/admin-auth');
const { getBannerConfig, saveBannerConfig, canUseBlob } = require('../../lib/banner-store');

module.exports = async function handler(req, res) {
    const session = requireAdmin(req, res);
    if (!session) return;

    if (req.method === 'GET') {
        try {
            const config = await getBannerConfig();
            return res.status(200).json({
                ok: true,
                config: config,
                storage: canUseBlob() ? 'blob' : 'file',
            });
        } catch (e) {
            console.error(e);
            return res.status(500).json({ ok: false, error: 'Načtení selhalo.' });
        }
    }

    if (req.method === 'PUT' || req.method === 'POST') {
        try {
            const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
            const config = body.config || body;
            if (!config || typeof config !== 'object') {
                return res.status(400).json({ ok: false, error: 'Chybí konfigurace.' });
            }
            const saved = await saveBannerConfig(config, { username: session.u });
            return res.status(200).json({
                ok: true,
                config: saved,
                storage: canUseBlob() ? 'blob' : 'file',
            });
        } catch (e) {
            console.error(e);
            return res.status(500).json({
                ok: false,
                error:
                    'Uložení selhalo. Na Vercelu nastavte BLOB_READ_WRITE_TOKEN (Vercel Blob store). ' +
                    String(e.message || ''),
            });
        }
    }

    res.setHeader('Allow', 'GET, PUT, POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
};
