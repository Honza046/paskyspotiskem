/**
 * Client-side i18n for static HTML pages (CS / EN / DE / IT).
 */
(function () {
    'use strict';

    var SUPPORTED = ['cs', 'en', 'de', 'it'];
    var DEFAULT = 'cs';
    var STORAGE_KEY = 'paskyonline_lang';
    var I18N_VER = '15';
    var HTML_LANG = { cs: 'cs', en: 'en', de: 'de', it: 'it' };
    var currentLocale = null;
    var localeCache = {};

    function getQueryLang() {
        var params = new URLSearchParams(window.location.search);
        var lang = (params.get('lang') || '').toLowerCase();
        return SUPPORTED.indexOf(lang) > -1 ? lang : '';
    }

    function getLocale() {
        var fromQuery = getQueryLang();
        if (fromQuery) {
            try { localStorage.setItem(STORAGE_KEY, fromQuery); } catch (e) {}
            return fromQuery;
        }
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            if (stored && SUPPORTED.indexOf(stored) > -1) {
                return stored;
            }
        } catch (e) {}
        if (window.paskyonlineI18n && window.paskyonlineI18n.locale) {
            return window.paskyonlineI18n.locale;
        }
        return DEFAULT;
    }

    function getByPath(obj, path) {
        if (!obj || !path) return undefined;
        var parts = path.split('.');
        var cur = obj;
        for (var i = 0; i < parts.length; i++) {
            if (cur == null || typeof cur !== 'object' || !(parts[i] in cur)) {
                return undefined;
            }
            cur = cur[parts[i]];
        }
        return cur;
    }

    function fetchJson(url) {
        return fetch(url, { credentials: 'same-origin' }).then(function (r) {
            if (!r.ok) throw new Error('i18n load failed: ' + url);
            return r.json();
        });
    }

    function jsonUrl(locale) {
        return '/data/i18n/' + locale + '.json?v=' + I18N_VER;
    }

    function loadLocaleTree(code) {
        if (localeCache[code]) {
            return Promise.resolve(localeCache[code]);
        }
        return fetchJson(jsonUrl(code)).then(function (tree) {
            localeCache[code] = tree;
            return tree;
        });
    }

    function prefetchLocales(active) {
        SUPPORTED.forEach(function (code) {
            if (code === active || localeCache[code]) {
                return;
            }
            fetchJson(jsonUrl(code)).then(function (tree) {
                localeCache[code] = tree;
            }).catch(function () {});
        });
    }

    function reveal() {
        requestAnimationFrame(function () {
            document.documentElement.classList.remove('i18n-pending');
        });
    }

    function applyText(root, tree) {
        root.querySelectorAll('[data-i18n]').forEach(function (el) {
            var key = el.getAttribute('data-i18n');
            var val = getByPath(tree, key);
            if (typeof val === 'string') {
                el.textContent = val;
            }
        });

        root.querySelectorAll('[data-i18n-html]').forEach(function (el) {
            var key = el.getAttribute('data-i18n-html');
            var val = getByPath(tree, key);
            if (typeof val === 'string') {
                el.innerHTML = val;
            }
        });

        root.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
            var key = el.getAttribute('data-i18n-placeholder');
            var val = getByPath(tree, key);
            if (typeof val === 'string') {
                el.setAttribute('placeholder', val);
            }
        });

        root.querySelectorAll('[data-i18n-attr]').forEach(function (el) {
            var spec = el.getAttribute('data-i18n-attr');
            spec.split(';').forEach(function (pair) {
                var bits = pair.split(':');
                if (bits.length !== 2) return;
                var attr = bits[0].trim();
                var key = bits[1].trim();
                var val = getByPath(tree, key);
                if (typeof val === 'string') {
                    el.setAttribute(attr, val);
                }
            });
        });
    }

    function updateMeta(tree) {
        var meta = tree.meta || {};
        var page = document.body.getAttribute('data-page') || 'home';
        var lang = HTML_LANG[tree._locale] || 'cs';
        document.documentElement.lang = meta.htmlLang || lang;
        if (page === 'gallery' && meta.gallery_title) {
            document.title = meta.gallery_title;
        } else if (page === 'sortiment' && meta.sortiment_title && !parseSortimentSlug()) {
            document.title = meta.sortiment_title;
        } else if (meta.home_title && (page === 'home' || !page)) {
            document.title = meta.home_title;
        } else if (meta.title) {
            document.title = meta.title;
        }
        var desc = document.querySelector('meta[name="description"]');
        var descKey = page === 'gallery' ? meta.gallery_description : (page === 'sortiment' ? meta.sortiment_description : meta.home_description);
        if (desc && descKey) {
            desc.setAttribute('content', descKey);
        }
    }

    function parseSortimentSlug() {
        var parts = window.location.pathname.split('/').filter(Boolean);
        return parts[0] === 'sortiment' && parts.length > 1;
    }

    function flagImg(code) {
        var img = document.createElement('img');
        img.src = '/images/flags/' + code + '.svg';
        img.alt = '';
        img.width = 20;
        img.height = 15;
        img.className = 'h-full w-full object-cover';
        img.setAttribute('aria-hidden', 'true');
        return img;
    }

    function switchLocale(code, newUrl) {
        if (code === currentLocale) return;
        try { localStorage.setItem(STORAGE_KEY, code); } catch (err) {}

        loadLocaleTree(code)
            .then(function (tree) {
                applyLocale(code, tree, { reveal: false });
                if (newUrl && window.history && history.replaceState) {
                    history.replaceState({ locale: code }, '', newUrl);
                }
                prefetchLocales(code);
            })
            .catch(function (err) {
                console.warn('i18n switch:', err);
            });
    }

    function updateLangSwitcherState(switcher, locale, tree) {
        var names = (tree.meta && tree.meta.langNames) || {
            cs: 'Čeština', en: 'English', de: 'Deutsch', it: 'Italiano'
        };
        switcher._locale = locale;

        var trigger = switcher.querySelector('button[aria-haspopup="listbox"]');
        var menu = switcher.querySelector('[role="listbox"]');
        if (!trigger || !menu) return;

        var flagWrap = trigger.querySelector('span.flex.h-5');
        if (flagWrap) {
            flagWrap.innerHTML = '';
            flagWrap.appendChild(flagImg(locale));
        }
        var label = trigger.querySelector('span.max-w-0');
        if (label) label.textContent = names[locale] || locale.toUpperCase();

        menu.querySelectorAll('[role="option"]').forEach(function (opt) {
            var code = opt.getAttribute('data-lang');
            var selected = code === locale;
            opt.className = 'flex w-full items-center gap-2.5 px-3 py-2 text-left text-sm transition-colors hover:bg-orange-50 hover:text-orange-700' +
                (selected ? ' bg-orange-50 font-semibold text-orange-700' : ' text-slate-700');
            if (selected) {
                opt.setAttribute('aria-selected', 'true');
            } else {
                opt.removeAttribute('aria-selected');
            }
        });
    }

    function buildLangLinks(locale, tree) {
        var switcher = document.querySelector('[data-lang-switcher]');
        if (!switcher) return;

        if (switcher.dataset.initialized === '1') {
            updateLangSwitcherState(switcher, locale, tree);
            return;
        }
        switcher.dataset.initialized = '1';
        switcher._locale = locale;

        var names = (tree.meta && tree.meta.langNames) || {
            cs: 'Čeština', en: 'English', de: 'Deutsch', it: 'Italiano'
        };
        var path = window.location.pathname;

        switcher.className = 'lang-dropdown relative shrink-0';
        switcher.setAttribute('aria-label', 'Language');
        switcher.innerHTML = '';

        var trigger = document.createElement('button');
        trigger.type = 'button';
        trigger.className = 'group/lang flex items-center rounded-md py-1 text-sm font-medium text-slate-600 transition-colors hover:text-slate-900';
        trigger.setAttribute('aria-expanded', 'false');
        trigger.setAttribute('aria-haspopup', 'listbox');

        var flagWrap = document.createElement('span');
        flagWrap.className = 'flex h-5 w-5 shrink-0 overflow-hidden rounded-full';
        flagWrap.appendChild(flagImg(locale));

        var label = document.createElement('span');
        label.className = 'max-w-0 overflow-hidden whitespace-nowrap opacity-0 transition-all duration-300 ease-out group-hover/lang:ml-2 group-hover/lang:max-w-[8rem] group-hover/lang:opacity-100';
        label.textContent = names[locale] || locale.toUpperCase();

        trigger.appendChild(flagWrap);
        trigger.appendChild(label);

        var menu = document.createElement('div');
        menu.className = 'lang-dropdown__menu absolute right-0 top-[calc(100%+0.375rem)] z-[90] hidden min-w-[11rem] origin-top-right rounded-xl border border-slate-200 bg-white py-1 shadow-lg ring-1 ring-black/5';
        menu.setAttribute('role', 'listbox');

        function navigateTo(code) {
            if (code === switcher._locale) return;
            var search = new URLSearchParams(window.location.search);
            search.delete('lang');
            search.set('lang', code);
            var qs = search.toString();
            var newUrl = path + (qs ? '?' + qs : '') + window.location.hash;
            switchLocale(code, newUrl);
        }

        function closeMenu() {
            menu.classList.add('hidden');
            trigger.setAttribute('aria-expanded', 'false');
            label.classList.remove('!ml-2', '!max-w-[8rem]', '!opacity-100');
        }

        SUPPORTED.forEach(function (code) {
            var opt = document.createElement('button');
            opt.type = 'button';
            opt.className = 'flex w-full items-center gap-2.5 px-3 py-2 text-left text-sm transition-colors hover:bg-orange-50 hover:text-orange-700' +
                (code === locale ? ' bg-orange-50 font-semibold text-orange-700' : ' text-slate-700');
            opt.setAttribute('role', 'option');
            opt.setAttribute('data-lang', code);
            if (code === locale) {
                opt.setAttribute('aria-selected', 'true');
            }

            var optFlag = document.createElement('span');
            optFlag.className = 'flex h-5 w-5 shrink-0 overflow-hidden rounded-full ring-1 ring-slate-200';
            optFlag.appendChild(flagImg(code));

            var optLabel = document.createElement('span');
            optLabel.textContent = names[code] || code.toUpperCase();

            opt.appendChild(optFlag);
            opt.appendChild(optLabel);
            opt.addEventListener('click', function (e) {
                e.stopPropagation();
                closeMenu();
                navigateTo(code);
            });
            menu.appendChild(opt);
        });

        function openMenu() {
            menu.classList.remove('hidden');
            trigger.setAttribute('aria-expanded', 'true');
            label.classList.add('!ml-2', '!max-w-[8rem]', '!opacity-100');
            prefetchLocales(switcher._locale);
        }

        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            if (menu.classList.contains('hidden')) {
                openMenu();
            } else {
                closeMenu();
            }
        });

        switcher.addEventListener('click', function (e) {
            e.stopPropagation();
        });

        document.addEventListener('click', closeMenu);
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                closeMenu();
            }
        });

        switcher.appendChild(trigger);
        switcher.appendChild(menu);
    }

    function patchHeroSlides(tree) {
        var slides = getByPath(tree, 'home.hero.slides');
        var hero = getByPath(tree, 'home.hero') || {};
        if (!Array.isArray(slides) || !window.__heroSlides) return;
        slides.forEach(function (s, i) {
            if (!window.__heroSlides[i]) return;
            if (s.title) window.__heroSlides[i].title = s.title;
            if (s.subtitle) window.__heroSlides[i].subtitle = s.subtitle;

            var isSampleSlide = i === slides.length - 1 && !!window.__heroSlides[i].ctaPrimary &&
                window.__heroSlides[i].ctaPrimary.inquirySample;
            var primaryText = s.cta_primary ||
                (isSampleSlide && hero.cta_sample ? hero.cta_sample : hero.cta_offer);
            var secondaryText = s.cta_secondary || hero.cta_quote;

            if (primaryText && window.__heroSlides[i].ctaPrimary) {
                window.__heroSlides[i].ctaPrimary.text = primaryText;
            }
            if (secondaryText && window.__heroSlides[i].ctaSecondary) {
                window.__heroSlides[i].ctaSecondary.text = secondaryText;
            }
        });
        if (typeof window.__heroRefresh === 'function') {
            window.__heroRefresh();
        }
    }

    function exposeApi(locale, tree) {
        tree._locale = locale;
        window.paskyI18n = {
            locale: locale,
            t: function (key, fallback) {
                var val = getByPath(tree, key);
                return typeof val === 'string' ? val : (fallback || key);
            },
            get: function (key) {
                return getByPath(tree, key);
            },
            strings: getByPath(tree, 'js') || {}
        };
        document.documentElement.setAttribute('data-locale', locale);
        document.dispatchEvent(new CustomEvent('pasky:i18n-ready', { detail: { locale: locale, tree: tree } }));
    }

    function applyLocale(locale, tree, options) {
        options = options || {};
        tree._locale = locale;
        applyText(document, tree);
        updateMeta(tree);
        buildLangLinks(locale, tree);
        patchHeroSlides(tree);
        exposeApi(locale, tree);
        currentLocale = locale;
        if (options.reveal !== false) {
            reveal();
        }
    }

    function init() {
        var locale = getLocale();

        loadLocaleTree(locale)
            .then(function (tree) {
                applyLocale(locale, tree);
                prefetchLocales(locale);
            })
            .catch(function (err) {
                console.warn('i18n:', err);
                reveal();
                if (locale !== DEFAULT) {
                    loadLocaleTree(DEFAULT).then(function (tree) {
                        applyLocale(DEFAULT, tree);
                    });
                }
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
