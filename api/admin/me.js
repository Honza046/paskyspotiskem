/**
 * GET /api/admin/me – current admin session.
 */

const { isConfigured, readSession } = require('../../lib/admin-auth');

module.exports = async function handler(req, res) {
    if (req.method !== 'GET') {
        res.setHeader('Allow', 'GET');
        return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }

    if (!isConfigured()) {
        return res.status(503).json({ ok: false, configured: false, authenticated: false });
    }

    const session = readSession(req);
    if (!session) {
        return res.status(200).json({ ok: true, configured: true, authenticated: false });
    }

    return res.status(200).json({
        ok: true,
        configured: true,
        authenticated: true,
        username: session.u,
    });
};
