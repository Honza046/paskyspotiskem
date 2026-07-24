/**
 * POST /api/admin/logout
 */

const { sessionCookie } = require('../../lib/admin-auth');

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }
    res.setHeader('Set-Cookie', sessionCookie('', true));
    return res.status(200).json({ ok: true });
};
