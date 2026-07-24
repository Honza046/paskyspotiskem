/**
 * Gallery page – filter bar, sections, lightbox with case-study panel.
 */
(function () {
    'use strict';

    var filterPanel = document.getElementById('gallery-filter');
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-gallery-item]'));
    var modal = document.getElementById('gallery-lightbox');
    if (modal) {
        document.querySelectorAll('#gallery-lightbox').forEach(function (node, index) {
            if (index > 0) {
                node.parentNode.removeChild(node);
            }
        });
        modal.hidden = true;
        modal.classList.remove('is-open');
    }
    var featuredSection = document.getElementById('gallery-featured-section');
    var referencesSection = document.getElementById('gallery-references-section');
    var productionSection = document.getElementById('gallery-production-section');
    var resultsSection = document.getElementById('gallery-results-section');
    var resultsGrid = document.getElementById('gallery-results');
    var emptyState = document.getElementById('gallery-empty');
    var countEl = document.getElementById('gallery-count');
    var activeZone = document.getElementById('gallery-active');
    var clearBtn = document.getElementById('gallery-clear');

    var pills = filterPanel
        ? Array.prototype.slice.call(filterPanel.querySelectorAll('[data-tag][data-filter-group]'))
        : [];
    var dropdowns = filterPanel
        ? Array.prototype.slice.call(filterPanel.querySelectorAll('[data-dropdown]'))
        : [];

    var inquiryBase = filterPanel ? (filterPanel.getAttribute('data-inquiry') || 'index.html#gf_1') : 'index.html#gf_1';
    var visibleItems = [];
    var currentIndex = -1;
    var itemPlaces = items.map(function (item) {
        return {
            item: item,
            parent: item.parentElement,
            next: item.nextElementSibling
        };
    });

    function uniqueById(list) {
        var seen = {};
        var out = [];
        list.forEach(function (item) {
            var id = item.getAttribute('data-id') || '';
            if (seen[id]) {
                return;
            }
            seen[id] = true;
            out.push(item);
        });
        return out;
    }

    var uniqueItemCount = uniqueById(items).length;

    function restoreItems() {
        itemPlaces.forEach(function (place) {
            if (!place.parent) {
                return;
            }
            if (place.next && place.next.parentElement === place.parent) {
                place.parent.insertBefore(place.item, place.next);
            } else {
                place.parent.appendChild(place.item);
            }
            if (place.item.getAttribute('data-featured') === 'true' && place.parent.id === 'gallery-featured') {
                place.item.classList.remove('lg:col-span-2');
            }
        });
    }

    function jsT(key, fallback) {
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            return window.paskyI18n.t(key, fallback);
        }
        return fallback;
    }

    var graphicIcons = {
        security: '<svg class="h-16 w-16 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/></svg>',
        glue: '<svg class="h-16 w-16 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg>',
        industrial: '<svg class="h-16 w-16 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z"/></svg>',
        warning: '<svg class="h-16 w-16 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>'
    };

    var graphicGradients = {
        security: 'from-rose-50 via-white to-orange-50',
        glue: 'from-amber-50 via-white to-orange-50',
        industrial: 'from-slate-50 via-white to-sky-50',
        warning: 'from-yellow-50 via-white to-orange-50'
    };

    function esc(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
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

    function activeFilters() {
        var map = {};
        pills.forEach(function (pill) {
            if (pill.getAttribute('aria-pressed') !== 'true') {
                return;
            }
            var group = pill.getAttribute('data-filter-group');
            if (!map[group]) {
                map[group] = [];
            }
            map[group].push(pill.getAttribute('data-tag'));
        });
        return map;
    }

    function hasActiveFilters() {
        var map = activeFilters();
        return Object.keys(map).some(function (key) {
            return map[key].length > 0;
        });
    }

    function itemMatches(item, filters) {
        var groups = Object.keys(filters);
        for (var i = 0; i < groups.length; i++) {
            var group = groups[i];
            var tags = filters[group];
            if (!tags.length) {
                continue;
            }
            var value = item.getAttribute('data-' + group);
            if (tags.indexOf(value) === -1) {
                return false;
            }
        }
        return true;
    }

    function setPill(pill, on) {
        pill.setAttribute('aria-pressed', on ? 'true' : 'false');
        pill.classList.toggle('bg-orange-50', on);
        pill.classList.toggle('text-orange-600', on);
        pill.classList.toggle('text-slate-700', !on);
        var check = pill.querySelector('[data-check]');
        if (check) {
            check.classList.toggle('hidden', !on);
        }
    }

    function badgeHTML(tag) {
        return '' +
            '<span class="flex items-center gap-1.5 rounded-full border border-orange-100 bg-orange-50 px-3 py-1 text-xs font-semibold text-orange-600">' +
                esc(labelOf(tag)) +
                '<button type="button" data-remove="' + esc(tag) + '" aria-label="' + esc(jsT('js.gallery.remove_filter', 'Odebrat filtr')) + '" class="flex h-4 w-4 items-center justify-center rounded-full text-orange-500 transition-colors hover:bg-orange-100 hover:text-orange-700">' +
                    '<svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18"/></svg>' +
                '</button>' +
            '</span>';
    }

    function updateCounts() {
        dropdowns.forEach(function (dd) {
            var count = dd.querySelectorAll('[data-tag][aria-pressed="true"]').length;
            var badge = dd.querySelector('[data-count]');
            if (!badge) {
                return;
            }
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

    function renderFilters() {
        var filters = activeFilters();
        var tags = [];
        Object.keys(filters).forEach(function (group) {
            tags = tags.concat(filters[group]);
        });
        var filtered = hasActiveFilters();

        if (activeZone) {
            activeZone.innerHTML = tags.map(badgeHTML).join('');
        }
        if (clearBtn) {
            clearBtn.classList.toggle('hidden', tags.length === 0);
        }
        updateCounts();

        visibleItems = [];
        var seenVisible = {};
        items.forEach(function (item) {
            var show = !filtered || itemMatches(item, filters);
            var id = item.getAttribute('data-id') || '';
            if (show) {
                if (!seenVisible[id]) {
                    seenVisible[id] = true;
                    visibleItems.push(item);
                } else if (filtered) {
                    item.classList.add('hidden');
                    return;
                }
            }
            item.classList.remove('hidden');
        });

        var count = visibleItems.length;
        if (countEl) {
            if (!filtered || count === uniqueItemCount) {
                countEl.textContent = jsT('js.gallery.count_all', '{count} ukázek').replace('{count}', String(uniqueItemCount));
            } else {
                countEl.textContent = jsT('js.gallery.count_filtered', 'Zobrazeno {visible} z {total}')
                    .replace('{visible}', String(count))
                    .replace('{total}', String(uniqueItemCount));
            }
        }

        if (filtered && resultsSection && resultsGrid) {
            restoreItems();

            if (featuredSection) {
                featuredSection.classList.add('hidden');
            }
            if (referencesSection) {
                referencesSection.classList.add('hidden');
            }
            if (productionSection) {
                productionSection.classList.add('hidden');
            }
            resultsSection.classList.remove('hidden');

            visibleItems.forEach(function (item) {
                item.classList.remove('lg:col-span-2');
                resultsGrid.appendChild(item);
            });

            resultsGrid.classList.toggle('hidden', count === 0);
            if (emptyState) {
                emptyState.classList.toggle('hidden', count > 0);
            }
            return;
        }

        restoreItems();

        if (resultsSection) {
            resultsSection.classList.add('hidden');
        }
        if (resultsGrid) {
            resultsGrid.classList.remove('hidden');
        }
        if (emptyState) {
            emptyState.classList.add('hidden');
        }

        if (featuredSection) {
            featuredSection.classList.remove('hidden');
        }
        if (referencesSection) {
            referencesSection.classList.remove('hidden');
        }
        if (productionSection) {
            productionSection.classList.remove('hidden');
        }
    }

    function toggleDropdown(dd, open) {
        var menu = dd.querySelector('[data-dropdown-menu]');
        var chevron = dd.querySelector('[data-chevron]');
        if (!menu) {
            return;
        }
        menu.classList.toggle('hidden', !open);
        menu.classList.toggle('flex', open);
        if (chevron) {
            chevron.classList.toggle('rotate-180', open);
        }
    }

    if (filterPanel && pills.length) {
        dropdowns.forEach(function (dd) {
            var toggle = dd.querySelector('[data-dropdown-toggle]');
            if (!toggle) {
                return;
            }
            toggle.addEventListener('click', function (e) {
                e.stopPropagation();
                var isOpen = !dd.querySelector('[data-dropdown-menu]').classList.contains('hidden');
                dropdowns.forEach(function (other) {
                    toggleDropdown(other, false);
                });
                toggleDropdown(dd, !isOpen);
            });
        });

        document.addEventListener('click', function () {
            dropdowns.forEach(function (dd) {
                toggleDropdown(dd, false);
            });
        });

        pills.forEach(function (pill) {
            pill.addEventListener('click', function (e) {
                e.stopPropagation();
                var on = pill.getAttribute('aria-pressed') !== 'true';
                setPill(pill, on);
                renderFilters();
            });
        });

        if (activeZone) {
            activeZone.addEventListener('click', function (e) {
                var btn = e.target.closest('[data-remove]');
                if (!btn) {
                    return;
                }
                var tag = btn.getAttribute('data-remove');
                pills.forEach(function (pill) {
                    if (pill.getAttribute('data-tag') === tag) {
                        setPill(pill, false);
                    }
                });
                renderFilters();
            });
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', function () {
                pills.forEach(function (pill) {
                    setPill(pill, false);
                });
                renderFilters();
                document.dispatchEvent(new CustomEvent('pasky:gallery-type-cleared'));
            });
        }

        window.paskyGallerySetTypeFilter = function (typeTag) {
            pills.forEach(function (pill) {
                if (pill.getAttribute('data-filter-group') === 'type') {
                    setPill(pill, !!typeTag && pill.getAttribute('data-tag') === typeTag);
                }
            });
            renderFilters();
        };

        renderFilters();
        document.addEventListener('pasky:i18n-ready', renderFilters);
        document.addEventListener('pasky:i18n-pages-applied', renderFilters);
    }

    if (items.length && modal) {
        var modalImg = document.getElementById('lightbox-image');
        var modalGraphic = document.getElementById('lightbox-graphic');
        var modalGraphicIcon = document.getElementById('lightbox-graphic-icon');
        var modalTitle = document.getElementById('lightbox-title');
        var modalClient = document.getElementById('lightbox-client');
        var modalMeta = document.getElementById('lightbox-meta');
        var modalDescription = document.getElementById('lightbox-description');
        var modalCta = document.getElementById('lightbox-cta');
        var closeBtn = document.getElementById('lightbox-close');
        var backdrop = document.getElementById('lightbox-backdrop');
        var prevBtn = document.getElementById('lightbox-prev');
        var nextBtn = document.getElementById('lightbox-next');

        function colorsLabel(n) {
        var num = parseInt(n, 10);
        if (num === 1) {
            return jsT('js.gallery.color_one', '1 barva');
        }
        if (num >= 2 && num <= 4) {
            return jsT('js.gallery.color_few', '{n} barvy').replace('{n}', String(num));
        }
        return jsT('js.gallery.color_many', '{n} barev').replace('{n}', String(num));
    }

        function metaRow(label, value) {
            if (!value) {
                return '';
            }
            return '' +
                '<div class="flex justify-between gap-4 border-b border-slate-100 py-2">' +
                    '<dt class="font-medium text-slate-500">' + esc(label) + '</dt>' +
                    '<dd class="text-right font-semibold text-slate-800">' + esc(value) + '</dd>' +
                '</div>';
        }

        function itemData(item) {
            return {
                image: item.getAttribute('data-image'),
                title: item.getAttribute('data-title'),
                client: item.getAttribute('data-client'),
                width: item.getAttribute('data-width'),
                colors: item.getAttribute('data-colors'),
                adhesive: item.getAttribute('data-adhesive-label'),
                industry: item.getAttribute('data-industry-label'),
                location: item.getAttribute('data-location'),
                description: item.getAttribute('data-description'),
                graphic: item.getAttribute('data-graphic') === 'true',
                graphicStyle: item.getAttribute('data-graphic-style') || 'security',
                type: item.getAttribute('data-type')
            };
        }

        function inquiryUrl(title) {
            var base = inquiryBase;
            var hash = '';
            if (base.indexOf('#') > -1) {
                var parts = base.split('#');
                base = parts[0];
                hash = '#' + parts.slice(1).join('#');
            }
            var sep = base.indexOf('?') > -1 ? '&' : '?';
            return base + sep + 'poptavka=' + encodeURIComponent(title) + hash;
        }

        function lightboxLabel(key, fallback) {
            return jsT('gallery.lightbox.' + key, fallback);
        }

        function openLightboxAt(index) {
            if (!visibleItems.length) {
                visibleItems = items.filter(function (item) {
                    return !item.classList.contains('hidden');
                });
            }
            if (index < 0 || index >= visibleItems.length) {
                return;
            }

            currentIndex = index;
            var data = itemData(visibleItems[index]);

            if (data.graphic) {
                modalImg.classList.add('hidden');
                var gradient = graphicGradients[data.graphicStyle] || graphicGradients.security;
                modalGraphic.className = 'flex h-full min-h-[220px] w-full flex-col items-center justify-center bg-gradient-to-br p-10 text-center lg:min-h-[320px] ' + gradient;
                modalGraphicIcon.innerHTML = graphicIcons[data.graphicStyle] || graphicIcons.security;
            } else {
                modalGraphic.classList.add('hidden');
                modalImg.classList.remove('hidden');
                modalImg.src = data.image;
                modalImg.alt = data.title;
            }

            modalTitle.textContent = data.title;

            if (data.client) {
                modalClient.textContent = data.client;
                modalClient.classList.remove('hidden');
            } else {
                modalClient.classList.add('hidden');
            }

            if (data.type === 'production') {
                modalMeta.innerHTML =
                    metaRow(lightboxLabel('meta_industry', 'Odvětví'), data.industry) +
                    metaRow(lightboxLabel('meta_location', 'Lokalita'), data.location);
            } else {
                modalMeta.innerHTML =
                    metaRow(lightboxLabel('meta_industry', 'Odvětví'), data.industry) +
                    metaRow(lightboxLabel('meta_width', 'Šířka'), data.width) +
                    metaRow(lightboxLabel('meta_colors', 'Barvy'), data.colors ? colorsLabel(data.colors) : '') +
                    metaRow(lightboxLabel('meta_adhesive', 'Lepidlo'), data.adhesive);
            }

            modalDescription.textContent = data.description || '';

            // Production photos are not print references – hide inquiry CTA
            if (modalCta) {
                if (data.type === 'production') {
                    modalCta.classList.add('hidden');
                    modalCta.setAttribute('aria-hidden', 'true');
                } else {
                    modalCta.classList.remove('hidden');
                    modalCta.removeAttribute('aria-hidden');
                    modalCta.href = inquiryUrl(data.title);
                    var ctaText = lightboxLabel('cta', 'Chci podobný potisk');
                    var ctaSvg = modalCta.querySelector('svg');
                    modalCta.textContent = '';
                    modalCta.appendChild(document.createTextNode(ctaText + (ctaSvg ? ' ' : '')));
                    if (ctaSvg) modalCta.appendChild(ctaSvg);
                }
            }

            modal.hidden = false;
            modal.classList.add('is-open');
            document.body.classList.add('overflow-hidden');
            closeBtn.focus();

            if (prevBtn) {
                prevBtn.classList.toggle('hidden', visibleItems.length <= 1);
            }
            if (nextBtn) {
                nextBtn.classList.toggle('hidden', visibleItems.length <= 1);
            }
        }

        function closeLightbox() {
            modal.hidden = true;
            modal.classList.remove('is-open');
            document.body.classList.remove('overflow-hidden');
            if (modalImg) {
                modalImg.src = '';
            }
            currentIndex = -1;
        }

        function stepLightbox(delta) {
            if (!visibleItems.length) {
                return;
            }
            var next = currentIndex + delta;
            if (next < 0) {
                next = visibleItems.length - 1;
            }
            if (next >= visibleItems.length) {
                next = 0;
            }
            openLightboxAt(next);
        }

        items.forEach(function (item) {
            var trigger = item.querySelector('[data-lightbox-trigger]');
            if (!trigger) {
                return;
            }
            trigger.addEventListener('click', function () {
                visibleItems = items.filter(function (el) {
                    return !el.classList.contains('hidden');
                });
                var index = visibleItems.indexOf(item);
                openLightboxAt(index);
            });
        });

        closeBtn.addEventListener('click', closeLightbox);
        backdrop.addEventListener('click', closeLightbox);
        if (prevBtn) {
            prevBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                stepLightbox(-1);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                stepLightbox(1);
            });
        }
        document.addEventListener('keydown', function (e) {
            if (modal.hidden) {
                return;
            }
            if (e.key === 'Escape') {
                closeLightbox();
            }
            if (e.key === 'ArrowLeft') {
                stepLightbox(-1);
            }
            if (e.key === 'ArrowRight') {
                stepLightbox(1);
            }
        });

        document.addEventListener('pasky:i18n-pages-applied', function () {
            if (currentIndex >= 0) {
                openLightboxAt(currentIndex);
            }
        });
    }
})();
