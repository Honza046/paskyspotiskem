/**
 * Sortiment – interactive tag filter (compact bar with dropdowns).
 *
 * Reads product data from a <script id="sortiment-products" type="application/json">
 * blob, toggles filter tags via dropdown menus, renders active badges and matching
 * product cards. When no filter is active, the standard category grid is shown.
 */
(function () {
    'use strict';

    var dataEl = document.getElementById('sortiment-products');
    var panel = document.getElementById('sortiment-filter');
    var categoryGrid = document.getElementById('sortiment-categories');
    var featuredSection = document.getElementById('sortiment-featured');
    var results = document.getElementById('sortiment-results');
    var resultsGrid = document.getElementById('sortiment-results-grid');
    var resultsCount = document.getElementById('sortiment-results-count');
    var emptyState = document.getElementById('sortiment-empty');
    var clearBtn = document.getElementById('sortiment-clear');
    var activeZone = document.getElementById('sortiment-active');

    if (!dataEl || !panel || !categoryGrid || !results || !resultsGrid) {
        return;
    }

    var products = [];
    try {
        products = JSON.parse(dataEl.textContent || '[]');
    } catch (e) {
        products = [];
    }

    var inquiryUrl = resultsGrid.getAttribute('data-inquiry') || '/index.html#gf_1';
    var pills = Array.prototype.slice.call(panel.querySelectorAll('[data-tag]'));
    var dropdowns = Array.prototype.slice.call(panel.querySelectorAll('[data-dropdown]'));

    function t(key, fallback) {
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            return window.paskyI18n.t(key, fallback);
        }
        return fallback;
    }

    function productSlugFromDetail(detail) {
        var parts = String(detail || '').split('/').filter(Boolean);
        return parts[parts.length - 1] || '';
    }

    function localizedProduct(p) {
        var slug = productSlugFromDetail(p.detail);
        var loc = window.paskyI18n && window.paskyI18n.get
            ? window.paskyI18n.get('sortiment.products.' + slug)
            : null;
        if (!loc) return p;
        return {
            name: loc.name || p.name,
            tagline: loc.tagline || p.tagline,
            category: loc.category_title || p.category,
            detail: p.detail,
            image: p.image,
            tags: p.tags,
            portrait: p.portrait,
        };
    }

    function countLabel(n) {
        if (n === 1) return t('js.sortiment.product_one', '1 produkt');
        var few = t('js.sortiment.product_few', '{n} produkty').replace('{n}', String(n));
        var many = t('js.sortiment.product_many', '{n} produktů').replace('{n}', String(n));
        return n >= 2 && n <= 4 ? few : many;
    }

    var TAG_BADGE_ORDER = ['ekologicke', 'mrazuvzdorne', 'vysoke-teploty', 'chemicka-odolnost', 'stroje', 'rucni'];
    var TAG_BADGE_KEYS = {
        ekologicke: 'js.sortiment.tag_eco',
        mrazuvzdorne: 'js.sortiment.tag_cold',
        'vysoke-teploty': 'js.sortiment.tag_hot',
        'chemicka-odolnost': 'js.sortiment.tag_chem',
        stroje: 'js.sortiment.tag_machines',
        rucni: 'js.sortiment.tag_hand',
    };
    var TAG_BADGE_FALLBACK = {
        ekologicke: 'ECO',
        mrazuvzdorne: '-70 °C',
        'vysoke-teploty': 'Vysoké teploty',
        'chemicka-odolnost': 'Chemická odolnost',
        stroje: 'Stroje',
        rucni: 'Ruční',
    };

    function tagBadgeLabel(tag) {
        var key = TAG_BADGE_KEYS[tag];
        return key ? t(key, TAG_BADGE_FALLBACK[tag] || tag) : tag;
    }

    function tagPillsHTML(tags, maxShow) {
        maxShow = maxShow || 2;
        var pt = tags || [];
        var shown = TAG_BADGE_ORDER.filter(function (tag) { return pt.indexOf(tag) !== -1; }).slice(0, maxShow);
        if (!shown.length) return '';
        return '<div class="product-tags">' + shown.map(function (tag) {
            return '<span class="product-tag product-tag--' + esc(tag) + '">' + esc(tagBadgeLabel(tag)) + '</span>';
        }).join('') + '</div>';
    }

    function updateCategoryCounts() {
        document.querySelectorAll('[data-category-count]').forEach(function (el) {
            var n = parseInt(el.getAttribute('data-category-count'), 10);
            if (!isNaN(n)) el.textContent = countLabel(n);
        });
    }

    function labelOf(tag) {
        for (var i = 0; i < pills.length; i++) {
            if (pills[i].getAttribute('data-tag') === tag) {
                return pills[i].getAttribute('data-label') || tag;
            }
        }
        return tag;
    }

    function activeTags() {
        return pills
            .filter(function (p) { return p.getAttribute('aria-pressed') === 'true'; })
            .map(function (p) { return p.getAttribute('data-tag'); });
    }

    function setPill(pill, on) {
        pill.setAttribute('aria-pressed', on ? 'true' : 'false');
        pill.classList.toggle('bg-orange-50', on);
        pill.classList.toggle('text-orange-600', on);
        pill.classList.toggle('text-slate-700', !on);
        var check = pill.querySelector('[data-check]');
        if (check) { check.classList.toggle('hidden', !on); }
    }

    function esc(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    function cardHTML(p) {
        p = localizedProduct(p);
        var portrait = !!p.portrait;
        var imageBoxClass = portrait
            ? 'product-image-frame block w-full h-56 flex items-center justify-center overflow-hidden'
            : 'product-image-frame block w-full h-56 flex items-center justify-center overflow-hidden p-6';
        var imageClass = portrait
            ? 'h-52 w-auto max-w-none scale-[1.75] object-contain mix-blend-multiply contrast-[1.1] brightness-[1.05] transform transition-transform duration-300 group-hover:scale-[1.85]'
            : 'w-full h-full object-contain max-h-48 mix-blend-multiply contrast-[1.1] brightness-[1.05] transform transition-transform duration-300 group-hover:scale-105';

        return '' +
        '<article class="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-100 hover:shadow-lg">' +
            '<a href="' + esc(p.detail) + '" class="' + imageBoxClass + ' relative">' +
                tagPillsHTML(p.tags) +
                '<img src="' + esc(p.image) + '" alt="' + esc(p.name) + '" loading="lazy" class="' + imageClass + '">' +
            '</a>' +
            '<div class="flex flex-1 flex-col p-6">' +
                '<span class="text-xs font-semibold uppercase tracking-wide text-orange-600">' + esc(p.category) + '</span>' +
                '<a href="' + esc(p.detail) + '"><h3 class="mt-1 text-lg font-bold text-slate-900 hover:text-orange-600">' + esc(p.name) + '</h3></a>' +
                '<p class="mt-2 flex-1 text-sm leading-relaxed text-slate-600">' + esc(p.tagline || '') + '</p>' +
                '<div class="mt-5 flex gap-2">' +
                    '<a href="' + esc(p.detail) + '" class="flex-1 inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50">' + esc(t('js.sortiment.detail', 'Detail')) + '</a>' +
                    '<a href="' + esc(inquiryUrl) + '" class="flex-1 inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-orange-600 to-amber-500 px-4 py-2.5 text-sm font-bold text-white shadow-sm transition-all hover:scale-[1.02] hover:shadow-md">' + esc(t('js.sortiment.inquire', 'Poptat')) + '</a>' +
                '</div>' +
            '</div>' +
        '</article>';
    }

    function badgeHTML(tag) {
        return '' +
        '<span class="bg-orange-50 text-orange-600 border border-orange-100 text-xs font-semibold rounded-full px-3 py-1 flex items-center gap-1.5">' +
            esc(labelOf(tag)) +
            '<button type="button" data-remove="' + esc(tag) + '" aria-label="' + esc(t('js.sortiment.remove_filter', 'Odebrat filtr')) + '" class="flex h-4 w-4 items-center justify-center rounded-full text-orange-500 transition-colors hover:bg-orange-100 hover:text-orange-700">' +
                '<svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18"/></svg>' +
            '</button>' +
        '</span>';
    }

    function updateCounts() {
        dropdowns.forEach(function (dd) {
            var count = dd.querySelectorAll('[data-tag][aria-pressed="true"]').length;
            var badge = dd.querySelector('[data-count]');
            if (!badge) { return; }
            if (count > 0) {
                badge.textContent = count;
                badge.classList.remove('hidden');
                badge.classList.add('inline-flex');
            } else {
                badge.classList.add('hidden');
                badge.classList.remove('inline-flex');
            }
        });
    }

    function render() {
        var tags = activeTags();

        updateCounts();

        if (activeZone) {
            activeZone.innerHTML = tags.map(badgeHTML).join('');
        }
        if (clearBtn) {
            clearBtn.classList.toggle('hidden', tags.length === 0);
        }

        if (tags.length === 0) {
            categoryGrid.classList.remove('hidden');
            if (featuredSection) featuredSection.classList.remove('hidden');
            results.classList.add('hidden');
            return;
        }

        // AND logic: product must contain every selected tag.
        var matches = products.filter(function (p) {
            var pt = p.tags || [];
            return tags.every(function (t) { return pt.indexOf(t) !== -1; });
        });

        categoryGrid.classList.add('hidden');
        if (featuredSection) featuredSection.classList.add('hidden');
        results.classList.remove('hidden');

        if (resultsCount) {
            resultsCount.textContent = countLabel(matches.length);
        }

        if (matches.length === 0) {
            resultsGrid.innerHTML = '';
            if (emptyState) { emptyState.classList.remove('hidden'); }
            return;
        }

        if (emptyState) { emptyState.classList.add('hidden'); }
        resultsGrid.innerHTML = matches.map(cardHTML).join('');
    }

    // --- Dropdown open / close ---------------------------------------------
    function closeAllDropdowns(except) {
        dropdowns.forEach(function (dd) {
            if (dd === except) { return; }
            var menu = dd.querySelector('[data-dropdown-menu]');
            var chev = dd.querySelector('[data-chevron]');
            if (menu) { menu.classList.add('hidden'); }
            if (chev) { chev.classList.remove('rotate-180'); }
        });
    }

    dropdowns.forEach(function (dd) {
        var toggle = dd.querySelector('[data-dropdown-toggle]');
        var menu = dd.querySelector('[data-dropdown-menu]');
        var chev = dd.querySelector('[data-chevron]');
        if (!toggle || !menu) { return; }

        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            var willOpen = menu.classList.contains('hidden');
            closeAllDropdowns(dd);
            menu.classList.toggle('hidden', !willOpen);
            if (chev) { chev.classList.toggle('rotate-180', willOpen); }
        });

        menu.addEventListener('click', function (e) { e.stopPropagation(); });
    });

    document.addEventListener('click', function () { closeAllDropdowns(null); });

    // --- Pills -------------------------------------------------------------
    pills.forEach(function (pill) {
        setPill(pill, false);
        pill.addEventListener('click', function () {
            setPill(pill, pill.getAttribute('aria-pressed') !== 'true');
            render();
        });
    });

    // --- Active badge removal (event delegation) ---------------------------
    if (activeZone) {
        activeZone.addEventListener('click', function (e) {
            var btn = e.target.closest('[data-remove]');
            if (!btn) { return; }
            var tag = btn.getAttribute('data-remove');
            pills.forEach(function (p) {
                if (p.getAttribute('data-tag') === tag) { setPill(p, false); }
            });
            render();
        });
    }

    // --- Clear all ---------------------------------------------------------
    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            pills.forEach(function (p) { setPill(p, false); });
            render();
        });
    }

    render();
    updateCategoryCounts();

    document.addEventListener('pasky:i18n-ready', function () {
        render();
        updateCategoryCounts();
    });
    document.addEventListener('pasky:i18n-pages-applied', function () {
        render();
        updateCategoryCounts();
    });
})();
