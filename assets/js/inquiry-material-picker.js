/**
 * Inquiry form – material category + product picker (sortiment catalog).
 */
(function () {
    'use strict';

    var materialSelect = document.getElementById('input_material');
    var productWrap = document.getElementById('inquiry-product-wrap');
    var productSelect = document.getElementById('input_product');
    var productHint = document.getElementById('inquiry-product-hint');
    var form = document.getElementById('gform_1');

    if (!materialSelect || !productSelect || !form) {
        return;
    }

    var catalog = null;
    var i18nReady = false;
    var dropdownsReady = false;
    var BOPP_SLUG = 'bopp-pasky';

    function formText(key, fallback) {
        if (window.paskyI18n && typeof window.paskyI18n.t === 'function') {
            return window.paskyI18n.t('home.form.' + key, fallback);
        }
        return fallback;
    }

    function categoryTitle(slug, fallback) {
        if (window.paskyI18n && typeof window.paskyI18n.get === 'function') {
            var val = window.paskyI18n.get('sortiment.categories.' + slug + '.title');
            if (typeof val === 'string' && val.length) return val;
        }
        return fallback;
    }

    function productData(slug) {
        if (window.paskyI18n && typeof window.paskyI18n.get === 'function') {
            return window.paskyI18n.get('sortiment.products.' + slug);
        }
        return null;
    }

    function ensureDropdowns() {
        if (!dropdownsReady && window.InquiryDropdown) {
            window.InquiryDropdown.init(materialSelect);
            window.InquiryDropdown.init(productSelect);
            dropdownsReady = true;
        }
    }

    function refreshDropdowns() {
        ensureDropdowns();
        if (window.InquiryDropdown) {
            window.InquiryDropdown.refresh(materialSelect);
            window.InquiryDropdown.refresh(productSelect);
        }
    }

    function populateMaterials() {
        if (!catalog) return;

        var selected = materialSelect.value;
        materialSelect.innerHTML = '';
        var placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = formText('material_placeholder', 'Vyberte materiál…');
        placeholder.disabled = true;
        placeholder.selected = !selected;
        materialSelect.appendChild(placeholder);

        catalog.categories.forEach(function (cat) {
            var opt = document.createElement('option');
            opt.value = cat.slug;
            opt.textContent = categoryTitle(cat.slug, cat.title);
            if (cat.slug === selected) opt.selected = true;
            materialSelect.appendChild(opt);
        });
        refreshDropdowns();
    }

    function resetProductSelect() {
        productSelect.innerHTML = '';
        var placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = formText('product_placeholder', 'Vyberte pásku (volitelné)…');
        placeholder.selected = true;
        productSelect.appendChild(placeholder);
        if (productHint) {
            productHint.textContent = '';
            productHint.classList.add('hidden');
        }
        refreshDropdowns();
    }

    function populateProducts(categorySlug) {
        resetProductSelect();
        var products = catalog.products[categorySlug] || [];
        var selectedSlug = productSelect.dataset.selectedSlug || '';
        var firstOpt = productSelect.options[0];

        products.forEach(function (product) {
            var opt = document.createElement('option');
            var translated = productData(product.slug);
            opt.value = translated && translated.name ? translated.name : product.name;
            opt.textContent = opt.value;
            opt.dataset.tagline = translated && translated.tagline ? translated.tagline : (product.tagline || '');
            opt.dataset.slug = product.slug || '';
            if (product.slug === selectedSlug) {
                opt.selected = true;
                if (firstOpt) firstOpt.selected = false;
            }
            productSelect.appendChild(opt);
        });

        delete productSelect.dataset.selectedSlug;
        refreshDropdowns();
        updateProductHint();
    }

    function syncAdhesiveFromProduct() {
        if (materialSelect.value !== BOPP_SLUG) return;
        var selected = productSelect.options[productSelect.selectedIndex];
        var slug = selected && selected.dataset ? selected.dataset.slug : '';
        if (!slug) return;

        var name = (selected.value || '').toLowerCase();
        var target = null;
        if (name.indexOf('acrylic') !== -1 || name.indexOf('acryl') !== -1) {
            target = 'Akryl';
        } else if (name.indexOf('hot melt') !== -1) {
            target = 'HOT MELT';
        }
        if (!target) return;
        form.querySelectorAll('input[name="input_8"]').forEach(function (radio) {
            radio.checked = radio.value === target;
        });
        if (typeof window.__toggleAcrylNoiseOption === 'function') {
            window.__toggleAcrylNoiseOption();
        }
        if (typeof window.__syncQtyMinForAdhesive === 'function') {
            window.__syncQtyMinForAdhesive();
        }
    }

    function updateProductHint() {
        if (!productHint) return;
        var selected = productSelect.options[productSelect.selectedIndex];
        var tagline = selected && selected.dataset ? selected.dataset.tagline : '';
        if (tagline) {
            productHint.textContent = tagline;
            productHint.classList.remove('hidden');
        } else {
            productHint.textContent = '';
            productHint.classList.add('hidden');
        }
    }

    function onMaterialChange() {
        var slug = materialSelect.value;
        if (!slug) {
            productWrap.classList.add('hidden');
            resetProductSelect();
            return;
        }
        populateProducts(slug);
        productWrap.classList.remove('hidden');
    }

    function applyUrlPrefill() {
        var params = new URLSearchParams(window.location.search);
        var material = params.get('material');
        var product = params.get('product');
        if (!material) return;

        if (materialSelect.querySelector('option[value="' + material + '"]')) {
            materialSelect.value = material;
            if (product) productSelect.dataset.selectedSlug = product;
            onMaterialChange();
        }

        if (product) {
            var match = Array.prototype.find.call(productSelect.options, function (opt) {
                return opt.dataset.slug === product || opt.value === product;
            });
            if (match) {
                productSelect.value = match.value;
                refreshDropdowns();
                updateProductHint();
                syncAdhesiveFromProduct();
            }
        }
    }

    function refreshCatalogLabels() {
        if (!catalog) return;

        var material = materialSelect.value;
        var productSlug = '';
        var selected = productSelect.options[productSelect.selectedIndex];
        if (selected && selected.dataset && selected.dataset.slug) {
            productSlug = selected.dataset.slug;
        }

        populateMaterials();

        if (material) {
            productSelect.dataset.selectedSlug = productSlug;
            materialSelect.value = material;
            onMaterialChange();
            if (productSlug) {
                Array.prototype.forEach.call(productSelect.options, function (opt) {
                    if (opt.dataset.slug === productSlug) {
                        productSelect.value = opt.value;
                    }
                });
                refreshDropdowns();
                updateProductHint();
            }
        }
    }

    function bootPicker() {
        if (!catalog || !i18nReady) return;
        ensureDropdowns();
        populateMaterials();
        applyUrlPrefill();
    }

    materialSelect.addEventListener('change', onMaterialChange);
    productSelect.addEventListener('change', function () {
        updateProductHint();
        syncAdhesiveFromProduct();
    });

    document.addEventListener('pasky:i18n-ready', function () {
        i18nReady = true;
        bootPicker();
        refreshCatalogLabels();
    });

    document.addEventListener('pasky:i18n-pages-applied', refreshCatalogLabels);

    if (window.paskyI18n) {
        i18nReady = true;
    }

    fetch('/data/inquiry-catalog.json')
        .then(function (res) {
            if (!res.ok) throw new Error('catalog fetch failed');
            return res.json();
        })
        .then(function (data) {
            catalog = data;
            bootPicker();
        })
        .catch(function () {
            materialSelect.innerHTML = '<option value="" disabled selected>' +
                formText('catalog_error', 'Katalog se nepodařilo načíst') + '</option>';
            refreshDropdowns();
        });

    window.InquiryMaterialPicker = { refresh: refreshCatalogLabels };
})();
