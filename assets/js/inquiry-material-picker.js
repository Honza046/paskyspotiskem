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
    var BOPP_SLUG = 'bopp-pasky';

    function refreshDropdowns() {
        if (window.InquiryDropdown) {
            window.InquiryDropdown.refresh(materialSelect);
            window.InquiryDropdown.refresh(productSelect);
        }
    }

    function populateMaterials() {
        materialSelect.innerHTML = '';
        var placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = 'Vyberte materiál…';
        placeholder.disabled = true;
        placeholder.selected = true;
        materialSelect.appendChild(placeholder);

        catalog.categories.forEach(function (cat) {
            var opt = document.createElement('option');
            opt.value = cat.slug;
            opt.textContent = cat.title;
            materialSelect.appendChild(opt);
        });
        refreshDropdowns();
    }

    function resetProductSelect() {
        productSelect.innerHTML = '';
        var placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = 'Vyberte pásku (volitelné)…';
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
        products.forEach(function (product) {
            var opt = document.createElement('option');
            opt.value = product.name;
            opt.textContent = product.name;
            opt.dataset.tagline = product.tagline || '';
            opt.dataset.slug = product.slug || '';
            productSelect.appendChild(opt);
        });
        refreshDropdowns();
    }

    function syncAdhesiveFromProduct() {
        if (materialSelect.value !== BOPP_SLUG) return;
        var name = productSelect.value;
        if (!name) return;
        var lower = name.toLowerCase();
        var target = null;
        if (lower.indexOf('acrylic') !== -1 || lower.indexOf('acryl') !== -1) {
            target = 'ACRYL';
        } else if (lower.indexOf('hot melt') !== -1) {
            target = 'HOT MELT';
        }
        if (!target) return;
        form.querySelectorAll('input[name="input_8"]').forEach(function (radio) {
            radio.checked = radio.value === target;
        });
        if (typeof window.__toggleAcrylNoiseOption === 'function') {
            window.__toggleAcrylNoiseOption();
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

    if (window.InquiryDropdown) {
        window.InquiryDropdown.init(materialSelect);
        window.InquiryDropdown.init(productSelect);
    }

    fetch('/data/inquiry-catalog.json')
        .then(function (res) {
            if (!res.ok) throw new Error('catalog fetch failed');
            return res.json();
        })
        .then(function (data) {
            catalog = data;
            populateMaterials();
            materialSelect.addEventListener('change', onMaterialChange);
            productSelect.addEventListener('change', function () {
                updateProductHint();
                syncAdhesiveFromProduct();
            });
            applyUrlPrefill();
        })
        .catch(function () {
            materialSelect.innerHTML = '<option value="" disabled selected>Katalog se nepodařilo načíst</option>';
            refreshDropdowns();
        });
})();
