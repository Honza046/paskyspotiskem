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
    var items = Array.prototype.slice.call(list.querySelectorAll('[data-faq-item]'));
    var activeCategory = 'all';
    var query = '';
    var expanded = false;

    items.forEach(function (item, index) {
        if (index >= PREVIEW_LIMIT) {
            item.setAttribute('data-faq-more', 'true');
        }
    });

    function normalize(text) {
        return String(text || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/\s+/g, ' ')
            .trim();
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

    function updateMoreButton(remaining) {
        if (!moreBtn) return;
        var showBtn = !isFiltering() && !expanded && remaining > 0;
        moreBtn.classList.toggle('hidden', !showBtn);
        if (!showBtn) return;
        moreBtn.setAttribute('aria-expanded', 'false');
        moreBtn.innerHTML =
            'Zobrazit dalších ' + remaining + ' otázek' +
            '<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.25" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>';
    }

    function updateCount(visible) {
        if (!countEl) return;
        var total = items.length;
        if (!isFiltering() && !expanded) {
            countEl.textContent = 'Zobrazeno ' + Math.min(PREVIEW_LIMIT, total) + ' z ' + total;
            return;
        }
        if (visible === total && !isFiltering()) {
            countEl.textContent = total + ' otázek';
            return;
        }
        countEl.textContent = 'Zobrazeno ' + visible + ' z ' + total;
    }

    function apply() {
        var visible = 0;
        var remainingMore = 0;
        var previewShown = 0;

        items.forEach(function (item) {
            var match = matches(item);
            var isMore = item.getAttribute('data-faq-more') === 'true';
            var show = false;

            if (match) {
                if (isFiltering() || expanded) {
                    show = true;
                } else if (!isMore) {
                    show = true;
                    previewShown += 1;
                } else {
                    remainingMore += 1;
                }
            }

            item.classList.toggle('is-hidden', !show);
            item.hidden = !show;

            if (show) {
                visible += 1;
            } else if (item.classList.contains('is-open')) {
                item.classList.remove('is-open');
                var trigger = item.querySelector('.faq-item__trigger');
                if (trigger) trigger.setAttribute('aria-expanded', 'false');
            }
        });

        if (emptyEl) {
            emptyEl.classList.toggle('hidden', visible !== 0);
        }
        updateMoreButton(remainingMore);
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
            apply();
        });
    });

    if (searchInput) {
        var timer = null;
        searchInput.addEventListener('input', function () {
            window.clearTimeout(timer);
            timer = window.setTimeout(function () {
                query = normalize(searchInput.value);
                apply();
            }, 120);
        });
    }

    if (moreBtn) {
        moreBtn.addEventListener('click', function () {
            expanded = true;
            apply();
        });
    }

    function openFromHash() {
        var id = (window.location.hash || '').replace(/^#/, '');
        if (!id) return;
        var target = list.querySelector('[data-faq-item][data-id="' + id + '"]');
        if (!target) return;
        if (target.getAttribute('data-faq-more') === 'true') {
            expanded = true;
        }
        apply();
        var trigger = target.querySelector('.faq-item__trigger');
        if (trigger && !target.classList.contains('is-open')) {
            trigger.click();
        }
        window.setTimeout(function () {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 50);
    }

    apply();
    openFromHash();
    window.addEventListener('hashchange', openFromHash);

    /* --- FAQ contact form ----------------------------------------------- */
    var form = document.getElementById('faq-contact-form');
    if (!form) return;

    var submitBtn = form.querySelector('[type="submit"]');
    var defaultLabel = submitBtn ? submitBtn.textContent : 'Odeslat zprávu';
    var msgBox = document.getElementById('faq-contact-message');

    function showFormMessage(type, text) {
        if (!msgBox) return;
        msgBox.hidden = false;
        msgBox.setAttribute('role', type === 'error' ? 'alert' : 'status');
        msgBox.className =
            'mb-4 rounded-xl border px-4 py-3 text-sm ' +
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
        submitBtn.textContent = 'Odesílám…';

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
                    throw new Error((result.data && result.data.error) || 'Odeslání se nezdařilo.');
                }
                form.reset();
                showFormMessage('success', 'Děkujeme, zpráva byla odeslána. Ozveme se co nejdřív.');
            })
            .catch(function (err) {
                showFormMessage(
                    'error',
                    err.message || 'Odeslání se nezdařilo. Napište nám prosím na karel.petrak@alfain.eu.'
                );
            })
            .finally(function () {
                submitBtn.disabled = false;
                submitBtn.textContent = defaultLabel;
            });
    });
})();
