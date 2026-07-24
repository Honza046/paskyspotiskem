/**
 * Info-banner config store (Vercel Blob or local file fallback).
 */

const fs = require('fs');
const path = require('path');

const BLOB_PATH = 'info-banner/config.json';
const LOCAL_PATH = path.join(process.cwd(), 'data', 'info-banner.live.json');

const DEFAULT_CONFIG = {
    enabled: true,
    updatedAt: null,
    updatedBy: null,
    messages: {
        cs: [
            'Srpen: výroba a logistika mají 3týdenní výluku. Objednávky s dodáním před výlukou zašlete nejpozději do <strong>10. 7. 2026</strong>.',
            'U objednávek z července a srpna platí dodací lhůta 3–4 týdny s dodáním v <strong>září 2026</strong>.',
        ],
        en: [
            'August: production and logistics will be shut down for 3 weeks. To receive delivery before the shutdown, place your order by <strong>10 July 2026</strong>.',
            'For July and August orders, the delivery time is 3–4 weeks with delivery in <strong>September 2026</strong>.',
        ],
        de: [
            'August: Produktion und Logistik sind 3 Wochen lang geschlossen. Bestellungen mit Lieferung vor der Schließung senden Sie bitte bis spätestens <strong>10. 7. 2026</strong>.',
            'Bei Bestellungen aus Juli und August gilt eine Lieferzeit von 3–4 Wochen mit Lieferung im <strong>September 2026</strong>.',
        ],
        it: [
            'Agosto: produzione e logistica saranno ferme per 3 settimane. Per la consegna prima della pausa, inviate l\'ordine entro il <strong>10 luglio 2026</strong>.',
            'Per gli ordini di luglio e agosto, i tempi di consegna sono di 3–4 settimane con consegna a <strong>settembre 2026</strong>.',
        ],
    },
};

function normalizeConfig(raw) {
    const base = JSON.parse(JSON.stringify(DEFAULT_CONFIG));
    if (!raw || typeof raw !== 'object') return base;

    base.enabled = raw.enabled !== false;
    base.updatedAt = raw.updatedAt || null;
    base.updatedBy = raw.updatedBy || null;

    ['cs', 'en', 'de', 'it'].forEach(function (lang) {
        const list = raw.messages && raw.messages[lang];
        if (Array.isArray(list)) {
            base.messages[lang] = list
                .map(function (m) {
                    return String(m == null ? '' : m).trim();
                })
                .filter(Boolean);
        }
        if (!base.messages[lang].length) {
            base.messages[lang] = DEFAULT_CONFIG.messages[lang].slice();
        }
    });

    return base;
}

function canUseBlob() {
    return Boolean(process.env.BLOB_READ_WRITE_TOKEN);
}

async function readFromBlob() {
    const { get } = require('@vercel/blob');
    const result = await get(BLOB_PATH, { access: 'private', useCache: false });
    if (!result || result.statusCode !== 200 || !result.stream) return null;

    const chunks = [];
    const reader = result.stream.getReader();
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(Buffer.from(value));
    }
    const text = Buffer.concat(chunks).toString('utf8');
    if (!text) return null;
    return JSON.parse(text);
}

async function writeToBlob(config) {
    const { put } = require('@vercel/blob');
    const body = JSON.stringify(config, null, 2);
    await put(BLOB_PATH, body, {
        access: 'private',
        contentType: 'application/json',
        addRandomSuffix: false,
        allowOverwrite: true,
    });
}

function readFromFile() {
    try {
        if (!fs.existsSync(LOCAL_PATH)) return null;
        return JSON.parse(fs.readFileSync(LOCAL_PATH, 'utf8'));
    } catch (e) {
        return null;
    }
}

function writeToFile(config) {
    fs.mkdirSync(path.dirname(LOCAL_PATH), { recursive: true });
    fs.writeFileSync(LOCAL_PATH, JSON.stringify(config, null, 2) + '\n', 'utf8');
}

async function getBannerConfig() {
    try {
        if (canUseBlob()) {
            const fromBlob = await readFromBlob();
            if (fromBlob) return normalizeConfig(fromBlob);
        }
    } catch (e) {
        console.error('banner blob read failed', e);
    }

    const fromFile = readFromFile();
    if (fromFile) return normalizeConfig(fromFile);
    return normalizeConfig(DEFAULT_CONFIG);
}

async function saveBannerConfig(config, meta) {
    const next = normalizeConfig(config);
    next.updatedAt = new Date().toISOString();
    next.updatedBy = (meta && meta.username) || null;

    if (canUseBlob()) {
        await writeToBlob(next);
    }
    // Always keep local copy for offline/dev and as fallback snapshot
    try {
        writeToFile(next);
    } catch (e) {
        if (!canUseBlob()) throw e;
        console.error('banner local write failed', e);
    }

    return next;
}

module.exports = {
    DEFAULT_CONFIG,
    normalizeConfig,
    getBannerConfig,
    saveBannerConfig,
    canUseBlob,
};
