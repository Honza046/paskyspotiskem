/**
 * Translate HTML-ish banner strings CS → EN/DE/IT.
 * Prefers OpenAI when OPENAI_API_KEY is set, else MyMemory free API.
 */

const TARGETS = ['en', 'de', 'it'];

function protectTags(html) {
    const tags = [];
    const protectedText = String(html || '').replace(/<\/?[a-zA-Z][^>]*>/g, function (tag) {
        const idx = tags.length;
        tags.push(tag);
        return ' [[TAG' + idx + ']] ';
    });
    return { text: protectedText, tags: tags };
}

function restoreTags(text, tags) {
    return String(text || '')
        .replace(/\s*\[\[\s*TAG\s*(\d+)\s*\]\]\s*/gi, function (_, n) {
            const i = Number(n);
            return tags[i] != null ? tags[i] : '';
        })
        .replace(/\s{2,}/g, ' ')
        .trim();
}

async function translateWithOpenAI(text, targetLang) {
    const key = process.env.OPENAI_API_KEY;
    if (!key) return null;

    const langNames = { en: 'English', de: 'German', it: 'Italian' };
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            Authorization: 'Bearer ' + key,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: process.env.OPENAI_TRANSLATE_MODEL || 'gpt-4o-mini',
            temperature: 0.2,
            messages: [
                {
                    role: 'system',
                    content:
                        'You translate short website announcement texts from Czech. ' +
                        'Keep placeholders like [[TAG0]] exactly unchanged. Keep meaning, tone and brevity. ' +
                        'Return only the translation, no quotes.',
                },
                {
                    role: 'user',
                    content: 'Translate to ' + langNames[targetLang] + ':\n\n' + text,
                },
            ],
        }),
    });

    if (!res.ok) {
        const errText = await res.text();
        throw new Error('OpenAI translate failed: ' + res.status + ' ' + errText.slice(0, 200));
    }
    const data = await res.json();
    const out = data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
    return out ? String(out).trim() : null;
}

async function translateWithMyMemory(text, targetLang) {
    const url =
        'https://api.mymemory.translated.net/get?q=' +
        encodeURIComponent(text) +
        '&langpair=' +
        encodeURIComponent('cs|' + targetLang);
    const res = await fetch(url);
    if (!res.ok) throw new Error('MyMemory failed: ' + res.status);
    const data = await res.json();
    const translated = data && data.responseData && data.responseData.translatedText;
    if (!translated) throw new Error('MyMemory returned empty translation');
    return String(translated).trim();
}

async function translateOne(html, targetLang) {
    const packed = protectTags(html);
    let translated = null;
    try {
        translated = await translateWithOpenAI(packed.text, targetLang);
    } catch (e) {
        console.error(e);
    }
    if (!translated) {
        translated = await translateWithMyMemory(packed.text, targetLang);
    }
    return restoreTags(translated, packed.tags);
}

async function translateMessagesFromCs(csMessages) {
    const list = Array.isArray(csMessages) ? csMessages.map(String) : [];
    const out = { cs: list.slice(), en: [], de: [], it: [] };

    for (let i = 0; i < list.length; i++) {
        const source = list[i];
        for (let t = 0; t < TARGETS.length; t++) {
            const lang = TARGETS[t];
            out[lang][i] = await translateOne(source, lang);
        }
    }

    return out;
}

module.exports = {
    TARGETS,
    translateMessagesFromCs,
    translateOne,
};
