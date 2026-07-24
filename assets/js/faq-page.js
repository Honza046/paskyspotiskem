/**
 * FAQ page – category filter, live search, show-more, contact form.
 */
(function () {
    'use strict';

    if (document.body.getAttribute('data-page') !== 'faq') return;

    var list = document.querySelector('[data-faq-list]');
    var searchInput = document.querySelector('[data-faq-search]');
    var countEl = document.querySelector('[data-faq-count]');
    var emptyEl = document.querySelector('[data-faq-empty]');
    var moreBtn = document.querySelector('[data-faq-more-toggle]');
    var chips = Array.prototype.slice.call(document.querySelectorAll('[data-faq-filter]'));
    if (!list) return;

    var PREVIEW_LIMIT = 5;
    var BATCH_SIZE = 5;
    var STAGGER_MS = 45;
    var items = Array.prototype.slice.call(list.querySelectorAll('[data-faq-item]'));
    var activeCategory = 'all';
    var query = '';
    var visibleLimit = PREVIEW_LIMIT;
    var animToken = 0;

    function t(key, fallback) {
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            return window.paskyI18n.t(key, fallback);
        }
        return fallback;
    }

    function fmt(template, vars) {
        return String(template || '').replace(/\{(\w+)\}/g, function (_, key) {
            return vars[key] != null ? String(vars[key]) : '';
        });
    }

    function normalize(text) {
        return String(text || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function syncSearchHaystacks() {
        items.forEach(function (item) {
            var id = item.getAttribute('data-id') || '';
            var qEl = item.querySelector('.faq-item__q');
            var aEl = item.querySelector('.faq-item__a');
            var q = qEl ? qEl.textContent : '';
            var a = aEl ? aEl.textContent : '';
            var extra = t('faq.items.' + id + '.search', '');
            item.setAttribute('data-search', [q, a, extra].join(' '));
        });
    }

    function isFiltering() {
        return !!query || activeCategory !== 'all';
    }

    function matches(item) {
        var cat = item.getAttribute('data-category') || '';
        if (activeCategory !== 'all' && cat !== activeCategory) {
            return false;
        }
        if (!query) {
            return true;
        }
        var hay = normalize(item.getAttribute('data-search') || item.textContent);
        return hay.indexOf(query) !== -1;
    }

    function matchedItems() {
        return items.filter(matches);
    }

    function prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function closeItem(item) {
        if (!item.classList.contains('is-open')) return;
        item.classList.remove('is-open');
        var trigger = item.querySelector('.faq-item__trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }

    function setItemVisible(item, show, instant) {
        if (show) {
            item.hidden = false;
            item.removeAttribute('aria-hidden');
            if (instant || prefersReducedMotion()) {
                item.classList.remove('is-hidden', 'is-revealing');
                return;
            }
            if (item.classList.contains('is-hidden')) {
                item.classList.add('is-revealing');
                // force reflow so transition runs from collapsed state
                void item.offsetHeight;
                item.classList.remove('is-hidden');
                window.setTimeout(function () {
                    item.classList.remove('is-revealing');
                }, 420);
            } else {
                item.classList.remove('is-hidden', 'is-revealing');
            }
            return;
        }

        closeItem(item);
        if (instant || prefersReducedMotion()) {
            item.classList.add('is-hidden');
            item.classList.remove('is-revealing');
            item.hidden = true;
            item.setAttribute('aria-hidden', 'true');
            return;
        }
        item.classList.add('is-hidden');
        item.classList.remove('is-revealing');
        item.setAttribute('aria-hidden', 'true');
        window.setTimeout(function () {
            if (item.classList.contains('is-hidden')) {
                item.hidden = true;
            }
        }, 380);
    }

    function updateMoreButton(shown, totalMatched) {
        if (!moreBtn) return;
        var remaining = Math.max(0, totalMatched - shown);
        var canCollapse = !isFiltering() && visibleLimit > PREVIEW_LIMIT;
        var showBtn = !isFiltering() && (remaining > 0 || canCollapse);
        moreBtn.classList.toggle('hidden', !showBtn);
        moreBtn.disabled = false;
        if (!showBtn) return;

        if (remaining > 0) {
            var next = Math.min(BATCH_SIZE, remaining);
            moreBtn.dataset.action = 'more';
            moreBtn.setAttribute('aria-expanded', 'false');
            moreBtn.innerHTML =
                fmt(t('faq.more', 'Zobrazit dalších {n} tipů'), { n: next }) +
                '<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.25" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>';
            return;
        }

        moreBtn.dataset.action = 'less';
        moreBtn.setAttribute('aria-expanded', 'true');
        moreBtn.innerHTML =
            t('faq.less', 'Zobrazit méně') +
            '<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.25" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/></svg>';
    }

    function updateCount(visible) {
        if (!countEl) return;
        var total = items.length;
        if (!isFiltering() && visibleLimit <= PREVIEW_LIMIT) {
            countEl.textContent = fmt(t('faq.count_preview', 'Zobrazeno {shown} z {total}'), {
                shown: Math.min(PREVIEW_LIMIT, total),
                total: total,
            });
            return;
        }
        if (visible === total && !isFiltering()) {
            countEl.textContent = fmt(t('faq.count_all', '{n} tipů'), { n: total });
            return;
        }
        countEl.textContent = fmt(t('faq.count_filtered', 'Zobrazeno {visible} z {total}'), {
            visible: visible,
            total: total,
        });
    }

    function apply(options) {
        options = options || {};
        var animate = options.animate !== false;
        var staggerHide = !!options.staggerHide;
        var staggerShow = !!options.staggerShow;
        var token = ++animToken;
        var matched = matchedItems();
        var limit = isFiltering() ? matched.length : Math.min(visibleLimit, matched.length);
        var visible = 0;
        var toReveal = [];
        var toHide = [];

        items.forEach(function (item) {
            var matchIndex = matched.indexOf(item);
            var shouldShow = matchIndex !== -1 && matchIndex < limit;
            var currentlyHidden = item.classList.contains('is-hidden') || item.hidden;

            if (shouldShow) {
                visible += 1;
                if (currentlyHidden) {
                    toReveal.push(item);
                } else {
                    setItemVisible(item, true, true);
                }
            } else if (!currentlyHidden) {
                toHide.push(item);
            } else {
                setItemVisible(item, false, true);
            }
        });

        function runHide(done) {
            if (!toHide.length) {
                done();
                return;
            }
            if (!animate || prefersReducedMotion() || !staggerHide) {
                toHide.forEach(function (item) {
                    setItemVisible(item, false, !animate);
                });
                done();
                return;
            }
            // hide from bottom up for a smoother collapse
            var ordered = toHide.slice().reverse();
            ordered.forEach(function (item, i) {
                window.setTimeout(function () {
                    if (token !== animToken) return;
                    setItemVisible(item, false, false);
                    if (i === ordered.length - 1) {
                        window.setTimeout(done, 320);
                    }
                }, i * STAGGER_MS);
            });
        }

        function runReveal() {
            if (!toReveal.length || token !== animToken) return;
            if (!animate || prefersReducedMotion() || !staggerShow) {
                toReveal.forEach(function (item) {
                    setItemVisible(item, true, !animate);
                });
                return;
            }
            toReveal.forEach(function (item, i) {
                window.setTimeout(function () {
                    if (token !== animToken) return;
                    setItemVisible(item, true, false);
                }, i * STAGGER_MS);
            });
        }

        runHide(function () {
            if (token !== animToken) return;
            runReveal();
        });

        if (emptyEl) {
            emptyEl.classList.toggle('hidden', visible !== 0);
        }
        updateMoreButton(limit, matched.length);
        updateCount(visible);
    }

    chips.forEach(function (chip) {
        chip.addEventListener('click', function () {
            activeCategory = chip.getAttribute('data-faq-filter') || 'all';
            chips.forEach(function (other) {
                var on = other === chip;
                other.classList.toggle('is-active', on);
                other.setAttribute('aria-pressed', on ? 'true' : 'false');
            });
            visibleLimit = PREVIEW_LIMIT;
            apply({ animate: false });
        });
    });

    if (searchInput) {
        var timer = null;
        searchInput.addEventListener('input', function () {
            window.clearTimeout(timer);
            timer = window.setTimeout(function () {
                query = normalize(searchInput.value);
                visibleLimit = PREVIEW_LIMIT;
                apply({ animate: false });
            }, 120);
        });
    }

    if (moreBtn) {
        moreBtn.addEventListener('click', function () {
            var matched = matchedItems();
            var action = moreBtn.dataset.action || 'more';

            if (action === 'less') {
                visibleLimit = PREVIEW_LIMIT;
                apply({ animate: true, staggerHide: true, staggerShow: false });
                window.setTimeout(function () {
                    if (list && typeof list.scrollIntoView === 'function') {
                        list.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 80);
                return;
            }

            visibleLimit = Math.min(visibleLimit + BATCH_SIZE, matched.length);
            apply({ animate: true, staggerShow: true, staggerHide: false });
        });
    }

    function openFromHash() {
        var id = (window.location.hash || '').replace(/^#/, '');
        if (!id) return;
        var target = list.querySelector('[data-faq-item][data-id="' + id + '"]');
        if (!target) return;
        var matched = matchedItems();
        var idx = matched.indexOf(target);
        if (idx >= PREVIEW_LIMIT) {
            visibleLimit = Math.max(visibleLimit, idx + 1);
        }
        apply({ animate: false });
        var trigger = target.querySelector('.faq-item__trigger');
        if (trigger && !target.classList.contains('is-open')) {
            trigger.click();
        }
        window.setTimeout(function () {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 50);
    }

    /* --- FAQ contact form ----------------------------------------------- */
    var form = document.getElementById('faq-contact-form');
    var submitBtn = form ? form.querySelector('[type="submit"]') : null;
    var defaultLabel = submitBtn ? submitBtn.textContent : 'Odeslat zprávu';
    var msgBox = document.getElementById('faq-contact-message');

    function refreshI18nUi() {
        syncSearchHaystacks();
        if (searchInput) {
            query = normalize(searchInput.value);
        }
        apply({ animate: false });
        if (submitBtn && !submitBtn.disabled) {
            defaultLabel = t('faq.cta_button', defaultLabel);
            submitBtn.textContent = defaultLabel;
        }
    }

    document.addEventListener('pasky:i18n-ready', refreshI18nUi);

    syncSearchHaystacks();
    apply({ animate: false });
    openFromHash();
    window.addEventListener('hashchange', openFromHash);

    if (!form) return;

    function showFormMessage(type, text) {
        if (!msgBox) return;
        msgBox.hidden = false;
        msgBox.setAttribute('role', type === 'error' ? 'alert' : 'status');
        msgBox.className =
            'mt-5 mb-0 rounded-xl border px-4 py-3 text-sm ' +
            (type === 'success'
                ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
                : 'border-red-200 bg-red-50 text-red-800');
        msgBox.textContent = text;
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        if (!submitBtn) return;

        var payload = {
            source: 'faq-contact',
            contactName: (form.querySelector('#faq-name') || {}).value || '',
            email: (form.querySelector('#faq-email') || {}).value || '',
            phone: (form.querySelector('#faq-phone') || {}).value || '',
            note: (form.querySelector('#faq-message') || {}).value || '',
            gdprConsent: !!form.querySelector('#faq-gdpr:checked'),
            website: (form.querySelector('[name="website"]') || {}).value || '',
        };

        submitBtn.disabled = true;
        submitBtn.textContent = t('faq.form.sending', 'Odesílám…');

        fetch('/api/inquiry', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })
            .then(function (res) {
                return res.json().then(function (data) {
                    return { ok: res.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok) {
                    throw new Error((result.data && result.data.error) || t('faq.form.error', 'Odeslání se nezdařilo.'));
                }
                form.reset();
                showFormMessage('success', t('faq.form.success', 'Děkujeme, zpráva byla odeslána. Ozveme se co nejdřív.'));
            })
            .catch(function (err) {
                showFormMessage(
                    'error',
                    err.message || t('faq.form.error', 'Odeslání se nezdařilo. Napište nám prosím na karel.petrak@alfain.eu.')
                );
            })
            .finally(function () {
                submitBtn.disabled = false;
                submitBtn.textContent = t('faq.cta_button', defaultLabel);
            });
    });
})();
