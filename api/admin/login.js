/**
 * POST /api/admin/login
 * Body: { username, password }
 */

const {
    isConfigured,
    checkPassword,
    createSessionToken,
    sessionCookie,
    getCredentials,
} = require('../../lib/admin-auth');

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }

    if (!isConfigured()) {
        return res.status(503).json({
            ok: false,
            error: 'Admin není nakonfigurován. Nastavte ADMIN_USERNAME, ADMIN_PASSWORD a ADMIN_SESSION_SECRET ve Vercel env.',
        });
    }

    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
    const username = String(body.username || '').trim();
    const password = String(body.password || '');

    if (!checkPassword(username, password)) {
        return res.status(401).json({ ok: false, error: 'Neplatné přihlašovací údaje.' });
    }

    const token = createSessionToken(getCredentials().username);
    res.setHeader('Set-Cookie', sessionCookie(token, false));
    return res.status(200).json({ ok: true, username: getCredentials().username });
};
