/**
 * Page-specific i18n: sortiment categories/products, gallery items, inquiry form.
 */
(function () {
    'use strict';

    function t(key, fallback) {
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            return window.paskyI18n.t(key, fallback);
        }
        return fallback || key;
    }

    function getTree() {
        return window.paskyI18n && window.paskyI18n.get ? window.paskyI18n : null;
    }

    function parseSortimentPath() {
        var parts = window.location.pathname.split('/').filter(Boolean);
        if (parts[0] !== 'sortiment') return null;
        return { cat: parts[1] || '', product: parts[2] || '' };
    }

    function setText(el, text) {
        if (el && typeof text === 'string') el.textContent = text;
    }

    function setHtml(el, html) {
        if (el && typeof html === 'string') el.innerHTML = html;
    }

    function escHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function renderAboutBody1(p, about) {
        if (!p || !about) return;
        if (about.body1_highlight && about.body1_tooltip) {
            p.innerHTML =
                escHtml(about.body1_prefix || '') +
                '<span tabindex="0" class="group relative inline cursor-help font-semibold italic text-orange-600 outline-none">' +
                escHtml(about.body1_highlight) +
                '<span class="pointer-events-none absolute bottom-full left-0 z-30 mb-2 w-72 rounded-xl bg-slate-900 px-4 py-3 text-sm font-normal not-italic leading-snug text-white opacity-0 shadow-xl transition-opacity duration-200 group-hover:opacity-100 group-focus:opacity-100 sm:w-80">' +
                escHtml(about.body1_tooltip) +
                '<span class="absolute left-8 top-full -translate-x-1/2 border-8 border-transparent border-t-slate-900"></span></span></span>' +
                escHtml(about.body1_suffix || '');
            return;
        }
        if (about.body1) setText(p, about.body1);
    }

    function setCtaLabel(el, label) {
        if (!el || !label) return;
        var svg = el.querySelector('svg');
        el.textContent = '';
        el.appendChild(document.createTextNode(label + (svg ? ' ' : '')));
        if (svg) el.appendChild(svg);
    }

    function applySortimentFilters(tree) {
        var ui = tree.get('sortiment.ui') || {};
        var filters = tree.get('sortiment.filters') || {};
        var filterBar = document.getElementById('sortiment-filter');
        if (!filterBar) return;

        var filterHeading = filterBar.querySelector('.flex.items-center.gap-2.font-medium');
        if (filterHeading && ui.filter) {
            var filterText = filterHeading.querySelector('[data-i18n-filter-label]');
            if (filterText) {
                setText(filterText, ui.filter);
            } else {
                filterHeading.childNodes.forEach(function (node) {
                    if (node.nodeType === 3 && node.textContent.trim()) node.textContent = ' ' + ui.filter;
                });
            }
        }

        var groups = [
            { key: 'properties', index: 0 },
            { key: 'resistance', index: 1 },
            { key: 'usage', index: 2 }
        ];
        var dropdowns = filterBar.querySelectorAll('[data-dropdown]');
        groups.forEach(function (group) {
            var data = filters[group.key];
            var dropdown = dropdowns[group.index];
            if (!data || !dropdown) return;
            var toggle = dropdown.querySelector('[data-dropdown-toggle] > span:first-child');
            if (toggle && data.label) setText(toggle, data.label);
            dropdown.querySelectorAll('[data-tag]').forEach(function (btn) {
                var tag = btn.getAttribute('data-tag');
                if (!tag || !data[tag]) return;
                btn.setAttribute('data-label', data[tag]);
                var span = btn.querySelector('span:first-child');
                if (span) setText(span, data[tag]);
            });
        });

        var empty = document.querySelector('#sortiment-empty p');
        if (empty && ui.empty) setText(empty, ui.empty);
    }

    function applySortimentIndex(tree) {
        if (document.body.getAttribute('data-page') !== 'sortiment') return;
        if (parseSortimentPath() && parseSortimentPath().cat) return;

        var ui = tree.get('sortiment.ui') || {};
        var heroSubtitle = document.querySelector('main > section:first-child p.mx-auto');
        if (heroSubtitle && ui.subtitle) setText(heroSubtitle, ui.subtitle);

        applySortimentFilters(tree);

        var categories = tree.get('sortiment.categories') || {};
        var showProducts = ui.show_products;
        document.querySelectorAll('#sortiment-categories a[href*="/sortiment/"]').forEach(function (link) {
            var parts = (link.getAttribute('href') || '').split('/').filter(Boolean);
            var slug = parts[parts.indexOf('sortiment') + 1];
            var cat = categories[slug];
            if (!cat) return;
            var card = link.closest('article') || link;
            setText(card.querySelector('h3'), cat.title);
            setText(card.querySelector('p'), cat.description);
            var btn = card.querySelector('span.inline-flex');
            if (btn && showProducts) setCtaLabel(btn, showProducts);
        });

        var logoTagline = document.querySelector('.site-header span.hidden.text-sm');
        if (logoTagline) {
            var siteName = tree.get('meta.site_name');
            if (siteName) setText(logoTagline, siteName);
        }
    }

    function applySortimentPage(tree) {
        var path = parseSortimentPath();
        if (!path || !path.cat) return;

        var page = tree.get('sortiment.page') || {};
        var cat = tree.get('sortiment.categories.' + path.cat);
        if (!cat) return;

        document.querySelectorAll('nav[aria-label="Drobečková navigace"] a').forEach(function (a, i, all) {
            if (i === 0) setText(a, page.breadcrumb_home || a.textContent);
            if (a.getAttribute('href') && a.getAttribute('href').indexOf('sortiment') > -1 && i < all.length - 1) {
                setText(a, page.breadcrumb_sortiment || a.textContent);
            }
        });
        if (page.breadcrumb_aria) {
            document.querySelectorAll('nav[aria-label="Drobečková navigace"]').forEach(function (nav) {
                nav.setAttribute('aria-label', page.breadcrumb_aria);
            });
        }

        if (path.product) {
            applySortimentProduct(tree, path.cat, path.product, cat, page);
            return;
        }

        applySortimentCategory(tree, path.cat, cat, page);
    }

    function applySortimentCategory(tree, catSlug, cat, page) {
        var crumbs = document.querySelector('main nav[aria-label="Drobečková navigace"], main nav[aria-label]');
        if (crumbs) {
            var last = crumbs.querySelector('span.text-slate-600, span:last-child');
            if (last) setText(last, cat.title);
        }

        var heroH1 = document.querySelector('main section h1');
        var heroP = heroH1 ? heroH1.parentElement.querySelector('p') : null;
        setText(heroH1, cat.title);
        setText(heroP, cat.intro);

        var heroCta = document.querySelector('main section a[href*="gf_1"]');
        var categoryCtas = tree.get('sortiment.category_ctas.' + catSlug) || {};
        if (heroCta && categoryCtas.hero) {
            setText(heroCta, categoryCtas.hero);
        }

        var bottomCatCta = document.querySelector('main section.border-t a.bg-gradient-to-r, main .mt-12 a.bg-gradient-to-r');
        if (bottomCatCta && categoryCtas.bottom) {
            setText(bottomCatCta, categoryCtas.bottom);
        }

        document.querySelectorAll('main h2').forEach(function (h2) {
            var txt = h2.textContent.trim();
            if (/klíčové|key|eigenschaft|caratteristic/i.test(txt)) setText(h2, page.section_key_properties);
            if (/produkty v|products in|produkte in|prodotti in/i.test(txt)) setText(h2, page.section_products);
            if (/typické|typical|typische|tipici/i.test(txt)) setText(h2, page.section_typical_use);
        });

        var propCards = document.querySelectorAll('main section .grid article');
        var props = cat.properties || {};
        var propKeys = Object.keys(props);
        propCards.forEach(function (card, i) {
            if (i >= propKeys.length) return;
            var title = propKeys[i];
            var h3 = card.querySelector('h3');
            var p = card.querySelector('p');
            setText(h3, title);
            setText(p, props[title]);
        });

        var apps = cat.applications || [];
        document.querySelectorAll('main section .grid .text-sm.font-medium.text-slate-700').forEach(function (span, i) {
            if (apps[i]) setText(span, apps[i]);
        });

        document.querySelectorAll('main a[href*="/sortiment/"]').forEach(function (link) {
            var card = link.closest('a.group');
            if (!card) return;
            var href = link.getAttribute('href') || '';
            var slug = href.split('/').filter(Boolean).pop();
            var prod = tree.get('sortiment.products.' + slug);
            if (!prod) return;
            var h3 = card.querySelector('h3');
            var p = card.querySelector('p');
            var btn = card.querySelector('span.inline-flex');
            setText(h3, prod.name);
            setText(p, prod.tagline);
            if (btn && page.view_detail) {
                var svg = btn.querySelector('svg');
                btn.textContent = '';
                btn.appendChild(document.createTextNode(page.view_detail + ' '));
                if (svg) btn.appendChild(svg.cloneNode(true));
            }
        });

        document.querySelectorAll('main .mt-12 a, main .mt-8 a').forEach(function (a) {
            if (a.textContent.indexOf('Sortiment') > -1 || a.textContent.indexOf('sortiment') > -1) {
                if (page.back_to_sortiment) {
                    var svg = a.querySelector('svg');
                    a.textContent = '';
                    if (svg) a.appendChild(svg.cloneNode(true));
                    a.appendChild(document.createTextNode(' ' + page.back_to_sortiment));
                }
            }
        });

        document.title = cat.title + ' | ' + t('meta.site_name', 'Pásky s potiskem');
    }

    function setBackLink(link, label) {
        if (!link || !label) return;
        var svg = link.querySelector('svg');
        link.textContent = '';
        if (svg) link.appendChild(svg.cloneNode(true));
        link.appendChild(document.createTextNode(' ' + label));
    }

    function applySortimentProduct(tree, catSlug, productSlug, cat, page) {
        var prod = tree.get('sortiment.products.' + productSlug);
        if (!prod) return;

        var ctas = prod.ctas || {};

        var crumbs = document.querySelector('main nav[aria-label], main nav');
        if (crumbs) {
            var links = crumbs.querySelectorAll('a');
            links.forEach(function (a, i) {
                var href = a.getAttribute('href') || '';
                if (i === 0 && page.breadcrumb_home) setText(a, page.breadcrumb_home);
                else if ((href.indexOf('/sortiment') > -1 || href.indexOf('sortiment.html') > -1) &&
                    href.indexOf('/sortiment/' + catSlug) === -1 && page.breadcrumb_sortiment) {
                    setText(a, page.breadcrumb_sortiment);
                } else if (href.indexOf('/sortiment/' + catSlug) > -1 && !href.endsWith(productSlug)) {
                    setText(a, cat.title);
                }
            });
            if (page.breadcrumb_aria) crumbs.setAttribute('aria-label', page.breadcrumb_aria);
            var last = crumbs.querySelector('span.text-slate-600');
            if (last) setText(last, prod.name);
        }

        var catLabel = document.querySelector('main span.text-orange-600.uppercase');
        if (catLabel) setText(catLabel, cat.title);
        var h1 = document.querySelector('main h1');
        if (h1) setText(h1, prod.name);
        var tagline = document.querySelector('main h1 + p');
        if (tagline) setText(tagline, prod.tagline);

        var heroImg = document.querySelector('main section img');
        if (heroImg && prod.name) heroImg.alt = prod.name;

        var specPills = prod.spec_pills || [];
        document.querySelectorAll('main h1 + p + div.flex-wrap span.rounded-full').forEach(function (span, i) {
            if (specPills[i]) setText(span, specPills[i]);
        });

        document.querySelectorAll('main a[href*="gf_1"]').forEach(function (a) {
            if (a.classList.contains('bg-gradient-to-r') || a.classList.contains('from-orange-600')) {
                if (ctas.hero) setCtaLabel(a, ctas.hero);
            }
            if (a.classList.contains('text-orange-600') && a.closest('.product-tailor-box')) {
                if (ctas.tailor_link) setCtaLabel(a, ctas.tailor_link);
            }
        });

        document.querySelectorAll('main a[href*="/sortiment/' + catSlug + '"]').forEach(function (a) {
            if (a.closest('nav')) return;
            if (a.classList.contains('border') && a.closest('main > section:first-of-type')) {
                if (page.back_to_category) setBackLink(a, page.back_to_category);
            } else if (ctas.back_category) {
                setBackLink(a, ctas.back_category);
            }
        });

        document.querySelectorAll('main h2, main h3').forEach(function (h) {
            var txt = h.textContent.trim();
            if (/technické|technical|technische|tecnici/i.test(txt)) setText(h, page.section_technical_params);
            if (/hlavní výhody|main benefits|hauptvorteile|vantaggi/i.test(txt)) setText(h, page.section_benefits);
            if (/typické použití|typical use|typische|utilizzi/i.test(txt) && h.tagName === 'H3') setText(h, page.section_uses_label);
            if (/na míru|tailor|maß|su misura/i.test(txt)) setText(h, page.tailor_title);
        });

        var labels = prod.params_labels || {};
        var paramKeys = ['carrier', 'thickness', 'adhesive', 'adhesion', 'temperature', 'strength'];
        document.querySelectorAll('main table th').forEach(function (th, i) {
            if (labels[paramKeys[i]]) setText(th, labels[paramKeys[i]]);
        });

        var paramsValues = prod.params_values || {};
        document.querySelectorAll('main table tbody tr td:last-child').forEach(function (td, i) {
            if (paramsValues[paramKeys[i]]) setText(td, paramsValues[paramKeys[i]]);
        });

        var note = document.querySelector('main .overflow-hidden.rounded-2xl + p.text-xs, main table + p.text-xs');
        if (note && page.params_note) setText(note, page.params_note);

        var minQty = document.querySelector('main .product-min-qty');
        if (minQty) {
            if (prod.min_qty_note) setText(minQty, prod.min_qty_note);
            else minQty.hidden = true;
        }

        var benefits = prod.benefits || [];
        document.querySelectorAll('main .grid.grid-cols-1.gap-4 > div.flex.gap-4').forEach(function (card, i) {
            if (!benefits[i]) return;
            setText(card.querySelector('h3'), benefits[i].title);
            setText(card.querySelector('p'), benefits[i].text);
        });

        var uses = prod.uses || [];
        document.querySelectorAll('main ul.grid li span.text-sm.font-medium').forEach(function (span, i) {
            if (uses[i]) setText(span, uses[i]);
        });

        var bullets = (ctas.tailor_bullets || prod.tailor_bullets || []);
        document.querySelectorAll('.product-tailor-list li').forEach(function (li, i) {
            if (!bullets[i]) return;
            var dot = li.querySelector('span[aria-hidden="true"]');
            li.textContent = '';
            if (dot) li.appendChild(dot.cloneNode(true));
            li.appendChild(document.createTextNode(bullets[i]));
        });

        var bottomCta = document.querySelector('main section.border-t a.bg-gradient-to-r, main section:last-of-type a.bg-gradient-to-r');
        if (bottomCta && ctas.bottom) setText(bottomCta, ctas.bottom);

        var noPrint = document.querySelector('.product-neutral-note p, .max-w-3xl.rounded-2xl p');
        if (noPrint && page.no_print_note) {
            var bold = noPrint.querySelector('.font-bold');
            var link = noPrint.querySelector('a');
            noPrint.textContent = '';
            if (bold) {
                var boldEl = document.createElement('span');
                boldEl.className = bold.className;
                boldEl.textContent = page.no_print_note;
                noPrint.appendChild(boldEl);
                noPrint.appendChild(document.createTextNode(' '));
            }
            if (page.no_print_body) {
                noPrint.appendChild(document.createTextNode(page.no_print_body + ' '));
            }
            if (link && page.no_print_link) {
                var newLink = link.cloneNode(false);
                newLink.textContent = page.no_print_link;
                newLink.href = link.getAttribute('href') || link.href;
                noPrint.appendChild(newLink);
            }
        }

        var logoTagline = document.querySelector('.site-header span.hidden.text-sm');
        if (logoTagline) {
            var siteName = tree.get('meta.site_name');
            if (siteName) setText(logoTagline, siteName);
        }

        document.title = prod.name + ' | ' + t('meta.site_name', 'Pásky s potiskem');
    }

    function colorsLabel(num, tree) {
        var js = (tree.get && tree.get('js.gallery')) || {};
        var n = parseInt(num, 10);
        if (n === 1) {
            return js.color_one || '1 barva';
        }
        if (n >= 2 && n <= 4) {
            return (js.color_few || '{n} barvy').replace('{n}', String(n));
        }
        return (js.color_many || '{n} barev').replace('{n}', String(n));
    }

    function applyGalleryFilters(tree) {
        var filters = tree.get('gallery.filters') || {};
        var groups = filters.groups || {};
        var filterBar = document.getElementById('gallery-filter');
        if (!filterBar) return;

        var filterHeading = filterBar.querySelector('.flex.items-center.gap-2.font-medium');
        if (filterHeading && filters.filter) {
            filterHeading.childNodes.forEach(function (node) {
                if (node.nodeType === 3 && node.textContent.trim()) {
                    node.textContent = ' ' + filters.filter;
                }
            });
        }

        if (filters.clear_all) {
            var clearBtn = document.getElementById('gallery-clear');
            if (clearBtn) setText(clearBtn, filters.clear_all);
        }

        var groupKeys = ['category', 'adhesive', 'industry', 'type'];
        var dropdowns = filterBar.querySelectorAll('[data-dropdown]');
        groupKeys.forEach(function (key, index) {
            var data = groups[key];
            var dropdown = dropdowns[index];
            if (!data || !dropdown) return;
            var toggle = dropdown.querySelector('[data-dropdown-toggle] > span:first-child');
            if (toggle && data.label) setText(toggle, data.label);
            dropdown.querySelectorAll('[data-tag]').forEach(function (btn) {
                var tag = btn.getAttribute('data-tag');
                if (!tag || !data.options || !data.options[tag]) return;
                btn.setAttribute('data-label', data.options[tag]);
                var span = btn.querySelector('span:first-child');
                if (span) setText(span, data.options[tag]);
            });
        });

        var empty = document.querySelector('#gallery-empty p');
        var emptyText = tree.get('gallery.sections.empty');
        if (empty && emptyText) setText(empty, emptyText);
    }

    function applyGalleryCardTags(item, tree, data) {
        var cardBody = item.querySelector('.p-4, .p-5');
        if (!cardBody) return;
        var pills = cardBody.querySelector('[class*="flex-wrap"]');
        if (!pills) return;
        var spans = pills.querySelectorAll('span');
        if (spans.length < 3) return;
        if (data.industry_label) setText(spans[0], data.industry_label);
        var colors = item.getAttribute('data-colors');
        if (colors) setText(spans[2], colorsLabel(colors, tree));
    }

    function applyGalleryPage(tree) {
        if (document.body.getAttribute('data-page') !== 'gallery') return;
        var items = tree.get('gallery.items') || {};
        var cards = tree.get('gallery.cards') || {};
        var sections = tree.get('gallery.sections') || {};
        var ui = tree.get('gallery.ui') || {};
        var lightbox = tree.get('gallery.lightbox') || {};

        var hero = document.querySelector('main > section.border-b.border-slate-100.bg-white');
        if (hero) {
            setText(hero.querySelector('p.mb-2'), ui.label);
            setText(hero.querySelector('h1'), ui.title);
            setText(hero.querySelector('.max-w-2xl p'), ui.subtitle);
            var heroCta = hero.querySelector('a[href*="#gf"]');
            if (heroCta && ui.cta_custom) setText(heroCta, ui.cta_custom);
        }

        applyGalleryFilters(tree);

        document.querySelectorAll('[data-gallery-item]').forEach(function (item) {
            var id = item.getAttribute('data-id');
            var data = items[id];
            if (!data) return;
            item.setAttribute('data-title', data.title);
            item.setAttribute('data-description', data.description);
            if (data.industry_label) item.setAttribute('data-industry-label', data.industry_label);

            var titleEl = item.querySelector('h2, h3');
            setText(titleEl, data.title);

            var img = item.querySelector('img');
            if (img && data.title) {
                img.setAttribute('alt', data.title);
            }

            var desc = item.querySelector('[data-lightbox-trigger]');
            if (desc && cards.view_detail_aria) {
                desc.setAttribute('aria-label', cards.view_detail_aria.replace('{title}', data.title));
            }

            var overlayWrap = item.querySelector('[data-lightbox-trigger] [class*="group-hover:opacity-100"]');
            if (overlayWrap && cards.view_detail) {
                var svg = overlayWrap.querySelector('svg');
                overlayWrap.textContent = '';
                if (svg) overlayWrap.appendChild(svg);
                overlayWrap.appendChild(document.createTextNode(' ' + cards.view_detail));
            }

            var featuredBadge = item.querySelector('[data-lightbox-trigger] > span.absolute.left-3.top-3');
            if (featuredBadge && item.getAttribute('data-featured') === 'true' && cards.featured_badge) {
                setText(featuredBadge, cards.featured_badge);
            }

            var techBadge = item.querySelector('[data-lightbox-trigger] > span.absolute.right-3.top-3');
            if (techBadge && cards.technology_badge) {
                setText(techBadge, cards.technology_badge);
            }

            applyGalleryCardTags(item, tree, data);
        });

        document.querySelectorAll('#gallery-featured-section h2, #gallery-references-section h2, #gallery-demos-section h2').forEach(function (h2) {
            if (h2.closest('#gallery-featured-section') && sections.featured) setText(h2, sections.featured);
            if (h2.closest('#gallery-references-section') && sections.references_title) setText(h2, sections.references_title);
            if (h2.closest('#gallery-demos-section') && sections.demos_title) setText(h2, sections.demos_title);
        });

        document.querySelectorAll('#gallery-references-section p, #gallery-demos-section p').forEach(function (p) {
            if (p.closest('#gallery-references-section') && sections.references_subtitle) setText(p, sections.references_subtitle);
            if (p.closest('#gallery-demos-section') && sections.demos_subtitle) setText(p, sections.demos_subtitle);
        });

        var cta = tree.get('gallery.cta') || {};
        var ctaSection = document.querySelector('main > section.border-t.border-slate-100.bg-white');
        if (ctaSection) {
            if (cta.title) setText(ctaSection.querySelector('h2'), cta.title);
            if (cta.text) setText(ctaSection.querySelector('p'), cta.text);
            if (cta.button) {
                var ctaLink = ctaSection.querySelector('a[href*="#gf"]');
                if (ctaLink) setCtaLabel(ctaLink, cta.button);
            }
        }

        if (lightbox.close) {
            var closeBtn = document.getElementById('lightbox-close');
            if (closeBtn) closeBtn.setAttribute('aria-label', lightbox.close);
        }
        if (lightbox.prev) {
            var prevBtn = document.getElementById('lightbox-prev');
            if (prevBtn) prevBtn.setAttribute('aria-label', lightbox.prev);
        }
        if (lightbox.next) {
            var nextBtn = document.getElementById('lightbox-next');
            if (nextBtn) nextBtn.setAttribute('aria-label', lightbox.next);
        }
        if (lightbox.cta) {
            var modalCta = document.getElementById('lightbox-cta');
            if (modalCta) setCtaLabel(modalCta, lightbox.cta);
        }
        if (cards.technology_demo) {
            var techLabel = document.querySelector('#lightbox-graphic span.text-xs');
            if (techLabel) setText(techLabel, cards.technology_demo);
        }

        var logoTagline = document.querySelector('.site-header span.hidden.text-sm');
        if (logoTagline) {
            var siteName = tree.get('meta.site_name');
            if (siteName) setText(logoTagline, siteName);
        }
    }

    function setLabel(forId, text, required) {
        var lbl = document.querySelector('label[for="' + forId + '"]');
        if (!lbl || !text) return;
        if (required) {
            lbl.innerHTML = text + ' <span class="text-orange-600">*</span>';
        } else {
            lbl.textContent = text;
        }
    }

    function setLegendRequired(legendEl, text) {
        if (!legendEl || !text) return;
        legendEl.innerHTML = text + ' <span class="text-orange-600">*</span>';
    }

    function applyFormPage(tree) {
        var formData = tree.get('home.form');
        if (!formData || !document.getElementById('gform_1')) return;

        setText(document.querySelector('#form-outer-head p'), formData.label);
        setText(document.querySelector('#form-outer-head h2'), formData.title);

        var steps = formData.steps || [];
        window.__formStepNames = steps.length ? steps : undefined;
        window.__formStepLabelTpl = formData.step_label || undefined;

        document.querySelectorAll('#gform_page_1_1 h3').forEach(function (h) { setText(h, formData.step1_title); });
        document.querySelectorAll('#gform_page_1_1 > p.mb-6').forEach(function (p) { setText(p, formData.step1_hint); });
        document.querySelectorAll('#gform_page_1_2 h3').forEach(function (h) { setText(h, formData.step2_title); });
        document.querySelectorAll('#gform_page_1_2 > p.mb-6').forEach(function (p) { setText(p, formData.step2_hint); });
        document.querySelectorAll('#gform_page_1_3 h3').forEach(function (h) { setText(h, formData.step3_title); });
        document.querySelectorAll('#gform_page_1_3 > p.mb-6').forEach(function (p) { setText(p, formData.step3_hint); });

        setLabel('input_material', formData.material_label, true);
        setLabel('input_product', formData.product_label, false);

        var adhesiveLegend = document.querySelector('#inquiry-adhesive-wrap legend');
        if (adhesiveLegend && formData.tape_type) setLegendRequired(adhesiveLegend, formData.tape_type);

        document.querySelectorAll('input[name="input_8"]').forEach(function (radio) {
            var hint = radio.parentElement && radio.parentElement.querySelector('span.mt-1');
            if (!hint) return;
            if (radio.value === 'HOT MELT') setText(hint, formData.hot_melt_hint);
            if (radio.value === 'ACRYL') setText(hint, formData.acryl_hint);
        });

        var acrylBox = document.querySelector('#acryl-noise-option');
        if (acrylBox) {
            setText(acrylBox.querySelector('.font-semibold.text-slate-900'), formData.acryl_no_silent_title);
            setText(acrylBox.querySelector('.text-xs.text-slate-500'), formData.acryl_no_silent_text);
        }

        var step1Fieldsets = document.querySelectorAll('#gform_page_1_1 fieldset');
        if (step1Fieldsets[1] && formData.base_color) {
            setLegendRequired(step1Fieldsets[1].querySelector('legend'), formData.base_color);
        }
        if (step1Fieldsets[2] && formData.print_colors) {
            setText(step1Fieldsets[2].querySelector('legend'), formData.print_colors);
        }

        var colorKeys = ['bila', 'hneda', 'transparentni', 'jina'];
        document.querySelectorAll('input[name="input_9"]').forEach(function (radio, i) {
            var key = colorKeys[i];
            if (!formData.colors || !formData.colors[key]) return;
            var span = radio.parentElement && radio.parentElement.querySelector('span');
            if (span) span.textContent = formData.colors[key];
        });

        var widthLegend = document.querySelector('#gform_page_1_2 fieldset:nth-of-type(1) legend');
        if (widthLegend && formData.width_label) widthLegend.textContent = formData.width_label;
        var lengthLegend = document.querySelector('#gform_page_1_2 fieldset:nth-of-type(2) legend');
        if (lengthLegend && formData.length_label) lengthLegend.textContent = formData.length_label;
        var periodLegend = document.querySelector('#gform_page_1_2 fieldset:nth-of-type(3) legend, #gform_page_1_2 > fieldset:last-of-type legend');
        if (periodLegend && formData.order_period_label) periodLegend.textContent = formData.order_period_label;

        setLabel('qty', formData.quantity_label, true);
        var qtyMinHint = document.querySelector('#qty + p.text-xs');
        if (qtyMinHint) {
            setText(qtyMinHint, formData.quantity_min || formData.quantity_hint || qtyMinHint.textContent);
        }

        var periodKeys = ['monthly', 'quarterly', 'biannual', 'annual'];
        document.querySelectorAll('input[name="input_18"]').forEach(function (radio, i) {
            var label = formData.order_periods && formData.order_periods[periodKeys[i]];
            if (!label) return;
            var span = radio.parentElement && radio.parentElement.querySelector('span');
            if (span) span.textContent = label;
        });

        setLabel('company', formData.company_label, true);
        setLabel('ico', formData.ico_label, true);
        setLabel('name', formData.name_label, true);
        setLabel('email', formData.email_label, true);
        setLabel('phone', formData.phone_label, true);
        setLabel('note', formData.note_label, false);

        var sampleBtn = document.getElementById('note-sample-btn');
        if (sampleBtn && formData.sample_note_btn) setText(sampleBtn, formData.sample_note_btn);

        document.querySelectorAll('.btn-next').forEach(function (b) { setText(b, formData.continue || b.textContent); });
        document.querySelectorAll('.btn-prev').forEach(function (b) { setText(b, formData.back || b.textContent); });
        var submit = document.getElementById('gform_submit_button_1');
        if (submit && formData.submit) submit.textContent = formData.submit;

        window.__formQtyTexts = {
            tip: formData.quantity_tip || formData.quantity_min,
            success: formData.quantity_success,
            invalid: formData.quantity_min || formData.quantity_tip
        };
        window.__formValidationTexts = formData.validation || {};
        window.__sampleNoteText = formData.sample_note_text || window.__sampleNoteText;

        if (typeof window.__updateQtyDiscountBadge === 'function') {
            window.__updateQtyDiscountBadge();
        }

        if (window.InquiryMaterialPicker && typeof window.InquiryMaterialPicker.refresh === 'function') {
            window.InquiryMaterialPicker.refresh();
        }

        if (typeof window.__goToInquiryStep === 'function') {
            var gform = document.getElementById('gform_1');
            var activePage = gform ? gform.querySelector('.gform_page:not(.hidden)') : null;
            var idx = activePage ? parseInt(activePage.getAttribute('data-step') || '0', 10) : 0;
            window.__goToInquiryStep(idx, { scroll: false });
        }
    }

    function applyHomePage(tree) {
        var page = document.body.getAttribute('data-page');
        if (page && page !== 'home') return;

        var about = tree.get('home.about');
        if (about) {
            var aboutSection = document.querySelector('#o-nas');
            if (aboutSection) {
                var textCol = aboutSection.querySelector(':scope > div:first-child');
                if (textCol) {
                    var paras = textCol.querySelectorAll('p');
                    if (paras[0] && about.lead) setText(paras[0], about.lead);
                    if (paras[1]) renderAboutBody1(paras[1] || textCol.querySelector('[data-about-body1]'), about);
                    if (paras[2] && about.body2) setText(paras[2], about.body2);
                }
                var teamOverlay = aboutSection.querySelector('.absolute.bottom-4');
                if (teamOverlay) {
                    var teamPs = teamOverlay.querySelectorAll('p');
                    if (teamPs[0] && about.team_title) setText(teamPs[0], about.team_title);
                    if (teamPs[1] && about.team_subtitle) setText(teamPs[1], about.team_subtitle);
                }
                var aboutImg = aboutSection.querySelector('img');
                if (aboutImg && about.image_alt) aboutImg.alt = about.image_alt;
            }
        }

        var refs = tree.get('home.references');
        if (refs) {
            var refSection = document.querySelector('#reference');
            if (refSection) {
                setText(refSection.querySelector('.text-center p.mx-auto'), refs.subtitle);
                var statLabels = refSection.querySelectorAll('.ref-stat-card__label');
                var statKeys = ['stat_customers', 'stat_experience', 'stat_iso'];
                statLabels.forEach(function (el, i) {
                    if (refs[statKeys[i]]) setText(el, refs[statKeys[i]]);
                });
            }
        }

        var lep = tree.get('home.lepidla');
        if (lep) {
            var lepSection = document.querySelector('#lepidla');
            if (lepSection) {
                setText(lepSection.querySelector('.mb-12 > p'), lep.label);
                setText(lepSection.querySelector('.mb-12 > h2'), lep.title);
                var articles = lepSection.querySelectorAll('article');
                if (articles[0]) {
                    setText(articles[0].querySelector('span.inline-flex'), lep.hot_melt_badge);
                    setText(articles[0].querySelector('h3'), lep.hot_melt_title);
                    setText(articles[0].querySelector('p.text-sm.font-medium'), lep.hot_melt_subtitle);
                    setText(articles[0].querySelector('p.leading-relaxed'), lep.hot_melt_text);
                }
                if (articles[1]) {
                    setText(articles[1].querySelector('span.inline-flex'), lep.acryl_badge);
                    setText(articles[1].querySelector('h3'), lep.acryl_title);
                    setText(articles[1].querySelector('p.text-sm.font-medium'), lep.acryl_subtitle);
                    setText(articles[1].querySelector('p.leading-relaxed'), lep.acryl_text);
                }
            }
        }

        var sus = tree.get('home.sustainability');
        if (sus) {
            var susSection = document.querySelector('#udrzitelnost');
            if (susSection) {
                setText(susSection.querySelector('.mb-12 > p'), sus.label);
                setText(susSection.querySelector('.mb-12 > h2'), sus.title);
                setText(susSection.querySelector('.mb-12 > p.mx-auto'), sus.subtitle);
                var cards = susSection.querySelectorAll('article');
                var cardKeys = [
                    ['card1_title', 'card1_text'],
                    ['card2_title', 'card2_text'],
                    ['card3_title', 'card3_text']
                ];
                cards.forEach(function (card, i) {
                    if (!cardKeys[i]) return;
                    setText(card.querySelector('h3'), sus[cardKeys[i][0]]);
                    setText(card.querySelector('p'), sus[cardKeys[i][1]]);
                });
            }
        }

        var benefits = tree.get('home.benefits');
        if (benefits) {
            var vyhody = document.querySelector('#vyhody');
            if (vyhody) {
                var benefitCards = vyhody.querySelectorAll('article');
                if (benefitCards[0]) {
                    setText(benefitCards[0].querySelector('span.inline-flex'), benefits.security_badge);
                    setText(benefitCards[0].querySelector('h3'), benefits.security_title);
                    setText(benefitCards[0].querySelector('p.leading-relaxed'), benefits.security_text);
                }
                if (benefitCards[1]) {
                    setText(benefitCards[1].querySelector('span.inline-flex'), benefits.glue_badge);
                    setText(benefitCards[1].querySelector('h3'), benefits.glue_title);
                    setText(benefitCards[1].querySelector('p.leading-relaxed'), benefits.glue_text);
                    var glueTag = benefitCards[1].querySelector('.mt-6 span:last-child');
                    if (glueTag && benefits.glue_extra_tag) setText(glueTag, benefits.glue_extra_tag);
                }
            }
        }

        var contacts = tree.get('home.contacts');
        if (contacts) {
            var contactSection = document.querySelector('#kontakt1');
            if (contactSection) {
                setText(contactSection.querySelector('.mb-12 > p'), contacts.label);
                var people = contactSection.querySelectorAll('article');
                if (people[0]) {
                    setText(people[0].querySelector('h3'), contacts.karel_name);
                    setText(people[0].querySelector('p.text-slate-500'), contacts.karel_role);
                }
                if (people[1]) {
                    setText(people[1].querySelector('h3'), contacts.vojtech_name);
                    setText(people[1].querySelector('p.text-slate-500'), contacts.vojtech_role);
                }
            }
        }

        var sample = tree.get('home.sample');
        if (sample) {
            setText(document.querySelector('#vzorek-zdarma h2'), sample.title);
        }
    }

    function applyFooter(tree) {
        var footer = tree.get('footer');
        if (!footer) return;
        var addr = document.querySelector('footer address');
        if (addr) {
            addr.innerHTML = '<strong class="text-slate-200">' + footer.company + '</strong><br>' +
                footer.street + '<br>' +
                footer.city + '<br>' +
                footer.country;
        }
        var phoneBlock = document.querySelector('footer h4[data-i18n="footer.phone_heading"]');
        if (phoneBlock) {
            var hours = phoneBlock.parentElement.querySelector('p.mt-2');
            if (hours && footer.phone_hours) setText(hours, footer.phone_hours);
        }
        var copySpan = document.querySelector('footer .border-t .flex-wrap > span');
        if (copySpan && footer.copyright) {
            var link = copySpan.querySelector('a');
            copySpan.textContent = '';
            copySpan.appendChild(document.createTextNode('2026 © '));
            if (link) copySpan.appendChild(link.cloneNode(true));
            copySpan.appendChild(document.createTextNode(' | ' + footer.copyright));
        }
        var madeBy = document.querySelector('.footer-made-by');
        if (madeBy && footer.made_by) {
            var credit = madeBy.querySelector('.footer-credit__text');
            madeBy.childNodes[0].textContent = footer.made_by + ' ';
            if (credit && footer.made_by_link) credit.textContent = footer.made_by_link;
        }
    }

    function applyHomeExtras(tree) {
        applyHomePage(tree);
    }

    function applyPageTranslations(tree) {
        var page = document.body.getAttribute('data-page') || 'home';
        if (page === 'sortiment' || parseSortimentPath()) {
            applySortimentIndex(tree);
            applySortimentPage(tree);
        }
        if (page === 'gallery') {
            applyGalleryPage(tree);
        }
        applyFormPage(tree);
        applyHomeExtras(tree);
        applyFooter(tree);

        document.dispatchEvent(new CustomEvent('pasky:i18n-pages-applied'));
    }

    document.addEventListener('pasky:i18n-ready', function (e) {
        var api = getTree();
        if (!api) return;
        applyPageTranslations({
            get: function (key) { return api.get(key); }
        });
    });

    if (window.paskyI18n) {
        applyPageTranslations({
            get: function (key) { return window.paskyI18n.get(key); }
        });
    }
})();
