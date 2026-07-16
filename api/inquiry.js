/**
 * POST /api/inquiry – odeslání poptávkového formuláře e-mailem (Resend).
 *
 * Env (Vercel → Settings → Environment Variables):
 *   RESEND_API_KEY          – API klíč z resend.com
 *   INQUIRY_FROM_EMAIL      – ověřená adresa odesílatele, např. "Poptávka <poptavka@paskyspotiskem.cz>"
 *   INQUIRY_TO_EMAILS       – volitelné přepsání, výchozí: vojtech + karel @alfain.eu
 */

/** Příjemci každé poptávky z formuláře */
const INQUIRY_RECIPIENTS = [
    'vojtech.petrak@alfain.eu',
    'karel.petrak@alfain.eu',
];

function escapeHtml(value) {
    return String(value == null ? '' : value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function row(label, value) {
    if (!value) return '';
    return (
        '<tr><td style="padding:6px 12px 6px 0;color:#64748b;vertical-align:top;white-space:nowrap;">' +
        escapeHtml(label) +
        '</td><td style="padding:6px 0;font-weight:600;color:#0f172a;">' +
        escapeHtml(value) +
        '</td></tr>'
    );
}

function buildEmailHtml(data) {
    const rows = [
        row('Materiál', data.materialLabel),
        row('Konkrétní páska', data.product),
        row('Typ lepidla', data.adhesive),
        data.acrylNoSilent ? row('Akryl varianta', 'Bez nehlučného činidla') : '',
        row('Podkladová barva', data.baseColor),
        row('Počet barev k tisku', data.printColors),
        row('Šíře pásky', data.widthMm ? data.widthMm + ' mm' : ''),
        row('Délka pásky', data.lengthM ? data.lengthM + ' m' : ''),
        row('Množství', data.quantity ? data.quantity + ' ks' : ''),
        row('Perioda objednávky', data.orderPeriod),
        row('Společnost', data.company),
        row('IČ', data.ico),
        row('Kontaktní osoba', data.contactName),
        row('E-mail', data.email),
        row('Telefon', data.phone),
        row('Poznámka', data.note),
    ].join('');

    return (
        '<div style="font-family:system-ui,sans-serif;max-width:640px;color:#334155;">' +
        '<h2 style="margin:0 0 16px;font-size:20px;color:#0f172a;">Nová poptávka z webu</h2>' +
        '<p style="margin:0 0 20px;font-size:14px;">Odesláno z formuláře na <strong>paskyspotiskem.cz</strong>.</p>' +
        '<table style="border-collapse:collapse;font-size:14px;line-height:1.5;">' +
        rows +
        '</table>' +
        '</div>'
    );
}

function buildPlainText(data) {
    const lines = [
        'Nová poptávka z webu paskyspotiskem.cz',
        '',
        data.materialLabel && 'Materiál: ' + data.materialLabel,
        data.product && 'Konkrétní páska: ' + data.product,
        data.adhesive && 'Typ lepidla: ' + data.adhesive,
        data.acrylNoSilent && 'Akryl: bez nehlučného činidla',
        data.baseColor && 'Podkladová barva: ' + data.baseColor,
        data.printColors && 'Počet barev: ' + data.printColors,
        data.widthMm && 'Šíře: ' + data.widthMm + ' mm',
        data.lengthM && 'Délka: ' + data.lengthM + ' m',
        data.quantity && 'Množství: ' + data.quantity + ' ks',
        data.orderPeriod && 'Perioda: ' + data.orderPeriod,
        '',
        data.company && 'Společnost: ' + data.company,
        data.ico && 'IČ: ' + data.ico,
        data.contactName && 'Kontakt: ' + data.contactName,
        data.email && 'E-mail: ' + data.email,
        data.phone && 'Telefon: ' + data.phone,
        data.note && 'Poznámka: ' + data.note,
    ].filter(Boolean);
    return lines.join('\n');
}

function parseRecipients() {
    const raw = process.env.INQUIRY_TO_EMAILS;
    if (!raw) {
        return INQUIRY_RECIPIENTS.slice();
    }
    return raw.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
}

function validatePayload(body) {
    const errors = [];
    if (!body.materialLabel) errors.push('Vyberte typ materiálu.');
    if (!body.adhesive) errors.push('Vyberte typ lepidla.');
    if (!body.baseColor) errors.push('Vyberte podkladovou barvu.');
    if (!body.quantity || Number(body.quantity) < 360) errors.push('Minimální množství je 360 ks.');
    if (!body.company) errors.push('Vyplňte název společnosti.');
    if (!body.ico) errors.push('Vyplňte IČ.');
    if (!body.contactName) errors.push('Vyplňte jméno kontaktní osoby.');
    if (!body.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email)) errors.push('Vyplňte platný e-mail.');
    if (!body.phone) errors.push('Vyplňte telefon.');
    if (!body.gdprConsent) errors.push('Potvrďte souhlas se zpracováním údajů.');
    return errors;
}

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }

    const apiKey = process.env.RESEND_API_KEY;
    const fromEmail = process.env.INQUIRY_FROM_EMAIL;

    if (!apiKey || !fromEmail) {
        return res.status(503).json({
            ok: false,
            error: 'E-mailová služba není nakonfigurována. Kontaktujte správce webu.',
        });
    }

    const body = req.body || {};

    if (body.website) {
        return res.status(200).json({ ok: true });
    }

    const errors = validatePayload(body);
    if (errors.length) {
        return res.status(400).json({ ok: false, error: errors.join(' ') });
    }

    const subject = 'Poptávka: ' + (body.company || 'webový formulář');
    const html = buildEmailHtml(body);
    const text = buildPlainText(body);
    const to = parseRecipients();

    try {
        const response = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                Authorization: 'Bearer ' + apiKey,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from: fromEmail,
                to: to,
                reply_to: body.email,
                subject: subject,
                html: html,
                text: text,
            }),
        });

        const result = await response.json().catch(function () { return {}; });

        if (!response.ok) {
            console.error('Resend error:', result);
            return res.status(502).json({
                ok: false,
                error: 'E-mail se nepodařilo odeslat. Zkuste to prosím později nebo napište přímo na karel.petrak@alfain.eu.',
            });
        }

        return res.status(200).json({ ok: true, id: result.id || null });
    } catch (err) {
        console.error('Inquiry send failed:', err);
        return res.status(500).json({
            ok: false,
            error: 'Došlo k chybě při odesílání. Zkuste to prosím znovu.',
        });
    }
};
