/**
 * Admin UI – info-banner editor with login + auto-translate.
 */
(function () {
    'use strict';

    var LANGS = ['cs', 'en', 'de', 'it'];
    var state = {
        authenticated: false,
        username: '',
        config: null,
        storage: '',
    };

    var loginView = document.getElementById('admin-login');
    var editorView = document.getElementById('admin-editor');
    var bootError = document.getElementById('boot-error');
    var loginForm = document.getElementById('login-form');
    var loginError = document.getElementById('login-error');
    var loginSubmit = document.getElementById('login-submit');
    var logoutBtn = document.getElementById('logout-btn');
    var adminUser = document.getElementById('admin-user');
    var enabledInput = document.getElementById('banner-enabled');
    var bannerMeta = document.getElementById('banner-meta');
    var addMessageBtn = document.getElementById('add-message');
    var translateBtn = document.getElementById('translate-btn');
    var saveBtn = document.getElementById('save-btn');
    var saveStatus = document.getElementById('save-status');

    function api(path, options) {
        options = options || {};
        options.credentials = 'same-origin';
        options.headers = Object.assign(
            { Accept: 'application/json' },
            options.headers || {}
        );
        if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(options.body);
        }
        return fetch(path, options).then(function (res) {
            return res.json().catch(function () {
                return { ok: false, error: 'Neplatná odpověď serveru (' + res.status + ').' };
            }).then(function (data) {
                data._status = res.status;
                return data;
            });
        });
    }

    function show(el, on) {
        if (!el) return;
        el.hidden = !on;
    }

    function setStatus(text, kind) {
        if (!saveStatus) return;
        saveStatus.textContent = text || '';
        saveStatus.className = 'admin-status' + (kind ? ' is-' + kind : '');
    }

    function sanitizeHtml(html) {
        var wrap = document.createElement('div');
        wrap.innerHTML = String(html || '');

        function walk(node) {
            var children = Array.prototype.slice.call(node.childNodes);
            children.forEach(function (child) {
                if (child.nodeType === 3) return;
                if (child.nodeType !== 1) {
                    node.removeChild(child);
                    return;
                }
                var tag = child.tagName.toLowerCase();
                if (tag === 'br') return;
                if (tag === 'b' || tag === 'strong' || tag === 'i' || tag === 'em' || tag === 'u') {
                    walk(child);
                    return;
                }
                if (tag === 'div' || tag === 'p' || tag === 'span') {
                    // unwrap block/span: keep children + line break between div/p
                    while (child.firstChild) {
                        node.insertBefore(child.firstChild, child);
                    }
                    if (tag === 'div' || tag === 'p') {
                        node.insertBefore(document.createElement('br'), child);
                    }
                    node.removeChild(child);
                    return;
                }
                // drop unknown tags but keep text
                while (child.firstChild) {
                    node.insertBefore(child.firstChild, child);
                }
                node.removeChild(child);
            });
        }

        walk(wrap);

        // normalize b→strong, i→em
        wrap.querySelectorAll('b').forEach(function (el) {
            var strong = document.createElement('strong');
            while (el.firstChild) strong.appendChild(el.firstChild);
            el.parentNode.replaceChild(strong, el);
        });
        wrap.querySelectorAll('i').forEach(function (el) {
            var em = document.createElement('em');
            while (el.firstChild) em.appendChild(el.firstChild);
            el.parentNode.replaceChild(em, el);
        });

        return wrap.innerHTML
            .replace(/(<br\s*\/?>\s*)+$/gi, '')
            .replace(/&nbsp;/g, ' ')
            .trim();
    }

    function collectLang(lang) {
        var root = document.getElementById('messages-' + lang);
        if (!root) return [];
        return Array.prototype.map.call(root.querySelectorAll('[data-rich-editor]'), function (ed) {
            return sanitizeHtml(ed.innerHTML);
        }).filter(Boolean);
    }

    function execFormat(cmd) {
        document.execCommand(cmd, false, null);
    }

    function buildToolbar(editor) {
        var bar = document.createElement('div');
        bar.className = 'admin-rte__toolbar';
        bar.setAttribute('role', 'toolbar');
        bar.setAttribute('aria-label', 'Formátování textu');

        [
            { cmd: 'bold', label: 'B', title: 'Tučné', className: 'is-bold' },
            { cmd: 'italic', label: 'I', title: 'Kurzíva', className: 'is-italic' },
            { cmd: 'underline', label: 'U', title: 'Podtržené', className: 'is-underline' },
        ].forEach(function (btn) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'admin-rte__btn ' + btn.className;
            b.title = btn.title;
            b.setAttribute('aria-label', btn.title);
            b.textContent = btn.label;
            b.addEventListener('mousedown', function (e) {
                e.preventDefault(); // keep selection in editor
                editor.focus();
                execFormat(btn.cmd);
            });
            bar.appendChild(b);
        });

        return bar;
    }

    function renderLang(lang, messages) {
        var root = document.getElementById('messages-' + lang);
        if (!root) return;
        root.innerHTML = '';
        var list = Array.isArray(messages) && messages.length ? messages : [''];
        list.forEach(function (text, index) {
            var row = document.createElement('div');
            row.className = 'admin-message';

            var label = document.createElement('div');
            label.className = 'admin-message__label';
            label.textContent = 'Zpráva ' + (index + 1);

            var rte = document.createElement('div');
            rte.className = 'admin-rte';

            var editor = document.createElement('div');
            editor.className = 'admin-rte__editor';
            editor.setAttribute('data-rich-editor', '1');
            editor.setAttribute('contenteditable', 'true');
            editor.setAttribute('role', 'textbox');
            editor.setAttribute('aria-multiline', 'true');
            editor.setAttribute(
                'aria-label',
                lang === 'cs' ? 'Text info baru' : 'Překlad'
            );
            editor.dataset.placeholder = lang === 'cs' ? 'Text info baru…' : 'Translation…';
            editor.innerHTML = text || '';

            editor.addEventListener('paste', function (e) {
                e.preventDefault();
                var plain = (e.clipboardData || window.clipboardData).getData('text/plain');
                document.execCommand('insertText', false, plain);
            });

            rte.appendChild(buildToolbar(editor));
            rte.appendChild(editor);

            row.appendChild(label);
            row.appendChild(rte);

            if (lang === 'cs') {
                var remove = document.createElement('button');
                remove.type = 'button';
                remove.className = 'admin-message__remove';
                remove.textContent = 'Odebrat';
                remove.addEventListener('click', function () {
                    row.remove();
                    if (!root.querySelector('.admin-message')) {
                        renderLang('cs', ['']);
                    }
                });
                row.appendChild(remove);
            }

            root.appendChild(row);
        });
    }

    function applyConfig(config) {
        state.config = config;
        enabledInput.checked = config.enabled !== false;
        LANGS.forEach(function (lang) {
            renderLang(lang, (config.messages && config.messages[lang]) || []);
        });
        var meta = [];
        if (config.updatedAt) meta.push('Naposledy uloženo: ' + new Date(config.updatedAt).toLocaleString('cs-CZ'));
        if (config.updatedBy) meta.push('uživatel: ' + config.updatedBy);
        if (state.storage) meta.push('úložiště: ' + state.storage);
        bannerMeta.textContent = meta.join(' · ');
    }

    function readConfigFromForm() {
        return {
            enabled: !!enabledInput.checked,
            messages: {
                cs: collectLang('cs'),
                en: collectLang('en'),
                de: collectLang('de'),
                it: collectLang('it'),
            },
            updatedAt: state.config && state.config.updatedAt,
            updatedBy: state.config && state.config.updatedBy,
        };
    }

    function showLogin() {
        state.authenticated = false;
        show(loginView, true);
        show(editorView, false);
        show(bootError, false);
    }

    function showEditor() {
        state.authenticated = true;
        show(loginView, false);
        show(editorView, true);
        show(bootError, false);
        adminUser.textContent = state.username || '';
    }

    function loadBanner() {
        return api('/api/admin/banner').then(function (data) {
            if (!data.ok) throw new Error(data.error || 'Načtení banneru selhalo.');
            state.storage = data.storage || '';
            applyConfig(data.config);
        });
    }

    function boot() {
        api('/api/admin/me').then(function (data) {
            if (data._status === 503 || data.configured === false) {
                show(loginView, false);
                show(editorView, false);
                show(bootError, true);
                bootError.textContent =
                    'Admin ještě není nastavený. Doplňte ADMIN_USERNAME, ADMIN_PASSWORD a ADMIN_SESSION_SECRET (min. 16 znaků) — lokálně do .env.local, na produkci ve Vercel Environment Variables. Pro live ukládání na Vercelu také BLOB_READ_WRITE_TOKEN.';
                return;
            }
            if (data.authenticated) {
                state.username = data.username || '';
                showEditor();
                return loadBanner().catch(function (err) {
                    setStatus(err.message || 'Chyba načtení', 'error');
                });
            }
            showLogin();
        }).catch(function () {
            show(bootError, true);
            bootError.textContent = 'API adminu není dostupné. Spusťte „npm run dev“ (lokální API + web), nebo nasaďte projekt na Vercel.';
        });
    }

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        loginError.hidden = true;
        loginSubmit.disabled = true;
        loginSubmit.textContent = 'Přihlašuji…';
        api('/api/admin/login', {
            method: 'POST',
            body: {
                username: document.getElementById('login-username').value,
                password: document.getElementById('login-password').value,
            },
        }).then(function (data) {
            loginSubmit.disabled = false;
            loginSubmit.textContent = 'Přihlásit se';
            if (!data.ok) {
                loginError.hidden = false;
                loginError.textContent = data.error || 'Přihlášení selhalo.';
                return;
            }
            state.username = data.username || '';
            showEditor();
            return loadBanner();
        }).catch(function () {
            loginSubmit.disabled = false;
            loginSubmit.textContent = 'Přihlásit se';
            loginError.hidden = false;
            loginError.textContent = 'Síťová chyba při přihlášení.';
        });
    });

    logoutBtn.addEventListener('click', function () {
        api('/api/admin/logout', { method: 'POST' }).finally(function () {
            showLogin();
        });
    });

    addMessageBtn.addEventListener('click', function () {
        var current = collectLang('cs');
        if (current.length >= 5) {
            setStatus('Maximum je 5 zpráv.', 'error');
            return;
        }
        current.push('');
        renderLang('cs', current);
    });

    translateBtn.addEventListener('click', function () {
        var cs = collectLang('cs');
        if (!cs.length) {
            setStatus('Nejdřív vyplňte českou zprávu.', 'error');
            return;
        }
        translateBtn.disabled = true;
        translateBtn.textContent = 'Překládám…';
        setStatus('Překládám do EN / DE / IT…', '');
        api('/api/admin/translate', {
            method: 'POST',
            body: { messages: cs },
        }).then(function (data) {
            translateBtn.disabled = false;
            translateBtn.textContent = 'Přeložit z češtiny';
            if (!data.ok) {
                setStatus(data.error || 'Překlad selhal.', 'error');
                return;
            }
            renderLang('en', data.messages.en);
            renderLang('de', data.messages.de);
            renderLang('it', data.messages.it);
            setStatus('Překlad hotový (' + (data.engine || 'auto') + '). Zkontrolujte a uložte.', 'ok');
        }).catch(function () {
            translateBtn.disabled = false;
            translateBtn.textContent = 'Přeložit z češtiny';
            setStatus('Síťová chyba při překladu.', 'error');
        });
    });

    saveBtn.addEventListener('click', function () {
        var config = readConfigFromForm();
        if (!config.messages.cs.length) {
            setStatus('Česká zpráva je povinná.', 'error');
            return;
        }

        function doSave(finalConfig) {
            saveBtn.disabled = true;
            saveBtn.textContent = 'Ukládám…';
            setStatus('Publikuji na web…', '');
            return api('/api/admin/banner', {
                method: 'PUT',
                body: { config: finalConfig },
            }).then(function (data) {
                saveBtn.disabled = false;
                saveBtn.textContent = 'Uložit a publikovat';
                if (!data.ok) {
                    setStatus(data.error || 'Uložení selhalo.', 'error');
                    return;
                }
                state.storage = data.storage || state.storage;
                applyConfig(data.config);
                setStatus('Uloženo. Info bar je live na webu.', 'ok');
            }).catch(function () {
                saveBtn.disabled = false;
                saveBtn.textContent = 'Uložit a publikovat';
                setStatus('Síťová chyba při ukládání.', 'error');
            });
        }

        // Auto-translate empty target langs before save
        var needsTranslate =
            !config.messages.en.length ||
            !config.messages.de.length ||
            !config.messages.it.length ||
            config.messages.en.length !== config.messages.cs.length ||
            config.messages.de.length !== config.messages.cs.length ||
            config.messages.it.length !== config.messages.cs.length;

        if (!needsTranslate) {
            doSave(config);
            return;
        }

        saveBtn.disabled = true;
        saveBtn.textContent = 'Překládám…';
        setStatus('Nejdřív překládám chybějící jazyky…', '');
        api('/api/admin/translate', {
            method: 'POST',
            body: { messages: config.messages.cs },
        }).then(function (data) {
            if (!data.ok) {
                saveBtn.disabled = false;
                saveBtn.textContent = 'Uložit a publikovat';
                setStatus(data.error || 'Překlad před uložením selhal.', 'error');
                return;
            }
            config.messages.en = data.messages.en;
            config.messages.de = data.messages.de;
            config.messages.it = data.messages.it;
            renderLang('en', config.messages.en);
            renderLang('de', config.messages.de);
            renderLang('it', config.messages.it);
            return doSave(config);
        }).catch(function () {
            saveBtn.disabled = false;
            saveBtn.textContent = 'Uložit a publikovat';
            setStatus('Síťová chyba při překladu.', 'error');
        });
    });

    boot();
})();
