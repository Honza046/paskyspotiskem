/**
 * Simple admin session cookies (HMAC-signed).
 *
 * Env:
 *   ADMIN_USERNAME
 *   ADMIN_PASSWORD
 *   ADMIN_SESSION_SECRET  – long random string
 */

const crypto = require('crypto');

const COOKIE_NAME = 'pasky_admin_session';
const MAX_AGE_SEC = 60 * 60 * 12; // 12 hours

function getCredentials() {
    const username = String(process.env.ADMIN_USERNAME || '').trim();
    const password = String(process.env.ADMIN_PASSWORD || '');
    const secret = String(process.env.ADMIN_SESSION_SECRET || '').trim();
    return { username, password, secret };
}

function isConfigured() {
    const { username, password, secret } = getCredentials();
    return Boolean(username && password && secret && secret.length >= 16);
}

function sign(payload, secret) {
    return crypto.createHmac('sha256', secret).update(payload).digest('hex');
}

function createSessionToken(username) {
    const { secret } = getCredentials();
    const exp = Math.floor(Date.now() / 1000) + MAX_AGE_SEC;
    const body = Buffer.from(JSON.stringify({ u: username, exp }), 'utf8').toString('base64url');
    const sig = sign(body, secret);
    return body + '.' + sig;
}

function verifySessionToken(token) {
    if (!token || typeof token !== 'string') return null;
    const { username, secret } = getCredentials();
    const parts = token.split('.');
    if (parts.length !== 2) return null;
    const [body, sig] = parts;
    const expected = sign(body, secret);
    const a = Buffer.from(sig);
    const b = Buffer.from(expected);
    if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
    try {
        const data = JSON.parse(Buffer.from(body, 'base64url').toString('utf8'));
        if (!data || data.u !== username) return null;
        if (!data.exp || data.exp < Math.floor(Date.now() / 1000)) return null;
        return data;
    } catch (e) {
        return null;
    }
}

function parseCookies(req) {
    const header = req.headers.cookie || '';
    const out = {};
    header.split(';').forEach(function (part) {
        const idx = part.indexOf('=');
        if (idx === -1) return;
        const key = part.slice(0, idx).trim();
        const val = part.slice(idx + 1).trim();
        out[key] = decodeURIComponent(val);
    });
    return out;
}

function sessionCookie(token, clear) {
    const secure = process.env.VERCEL || process.env.NODE_ENV === 'production' ? '; Secure' : '';
    if (clear) {
        return COOKIE_NAME + '=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0' + secure;
    }
    return (
        COOKIE_NAME +
        '=' +
        encodeURIComponent(token) +
        '; Path=/; HttpOnly; SameSite=Lax; Max-Age=' +
        MAX_AGE_SEC +
        secure
    );
}

function readSession(req) {
    if (!isConfigured()) return null;
    const cookies = parseCookies(req);
    return verifySessionToken(cookies[COOKIE_NAME]);
}

function requireAdmin(req, res) {
    if (!isConfigured()) {
        res.status(503).json({
            ok: false,
            error: 'Admin není nakonfigurován. Nastavte ADMIN_USERNAME, ADMIN_PASSWORD a ADMIN_SESSION_SECRET.',
        });
        return null;
    }
    const session = readSession(req);
    if (!session) {
        res.status(401).json({ ok: false, error: 'Nejste přihlášeni.' });
        return null;
    }
    return session;
}

function checkPassword(username, password) {
    const creds = getCredentials();
    if (!creds.username || !creds.password) return false;
    const userOk =
        username.length === creds.username.length &&
        crypto.timingSafeEqual(Buffer.from(username), Buffer.from(creds.username));
    const passBuf = Buffer.from(password);
    const expectBuf = Buffer.from(creds.password);
    const passOk =
        passBuf.length === expectBuf.length && crypto.timingSafeEqual(passBuf, expectBuf);
    return userOk && passOk;
}

module.exports = {
    COOKIE_NAME,
    MAX_AGE_SEC,
    isConfigured,
    createSessionToken,
    readSession,
    requireAdmin,
    checkPassword,
    sessionCookie,
    getCredentials,
};
