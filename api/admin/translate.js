/**
 * POST /api/admin/translate – translate CS messages → EN/DE/IT.
 * Body: { messages: string[] }
 */

const { requireAdmin } = require('../../lib/admin-auth');
const { translateMessagesFromCs } = require('../../lib/translate');

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }

    const session = requireAdmin(req, res);
    if (!session) return;

    try {
        const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
        const messages = Array.isArray(body.messages) ? body.messages : [];
        const cleaned = messages.map(function (m) { return String(m || '').trim(); }).filter(Boolean);
        if (!cleaned.length) {
            return res.status(400).json({ ok: false, error: 'Zadejte alespoň jednu českou zprávu.' });
        }
        if (cleaned.length > 5) {
            return res.status(400).json({ ok: false, error: 'Maximum je 5 zpráv.' });
        }

        const translated = await translateMessagesFromCs(cleaned);
        return res.status(200).json({
            ok: true,
            messages: translated,
            engine: process.env.OPENAI_API_KEY ? 'openai' : 'mymemory',
        });
    } catch (e) {
        console.error(e);
        return res.status(500).json({
            ok: false,
            error: 'Překlad selhal: ' + String(e.message || e),
        });
    }
};
