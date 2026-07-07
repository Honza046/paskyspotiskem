(function () {
    const slides = [
        {
            title: 'LEPICÍ PÁSKY SE SPODNÍM TISKEM',
            subtitle: 'Vysoce spolehlivé BOPP pásky s tiskem chráněným pod folií i ekologické varianty pro udržitelné balení.',
            ctaPrimary: { text: 'Prohlédnout nabídku', href: '#nabidka' },
            ctaSecondary: { text: 'Nezávazná kalkulace', href: '#gf_1' },
        },
        {
            title: 'PROČ SI VYBRAT NÁS?',
            subtitle: 'Více než 30 let zkušeností a spolupráce s předními e-shopy i průmyslovými podniky. Spolehlivost, rychlé dodání a individuální přístup ke každé zakázce.',
            ctaPrimary: { text: 'Prohlédnout nabídku', href: '#nabidka' },
            ctaSecondary: { text: 'Nezávazná kalkulace', href: '#gf_1' },
        },
        {
            title: 'OTESTUJTE NAŠI KVALITU VE SVÉM PROVOZU',
            subtitle: 'Nechte si zaslat bezplatný vzorek nebo nezávaznou kalkulaci na míru. Přesvědčte se o odolnosti a pevnosti lepidla ještě před objednávkou.',
            ctaPrimary: { text: 'Vyžádat vzorky', href: '#gf_1' },
            ctaSecondary: { text: 'Nezávazná kalkulace', href: '#gf_1' },
        },
    ];
    const els = document.querySelectorAll('.hero-slide');
    const title = document.getElementById('hero-title');
    const subtitle = document.getElementById('hero-subtitle');
    const ctaPrimary = document.getElementById('hero-cta-primary');
    const ctaSecondary = document.getElementById('hero-cta-secondary');
    const dotsWrap = document.getElementById('hero-dots');
    let current = 0, timer;

    slides.forEach(function (_, i) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'h-2.5 w-2.5 rounded-full border-2 border-white/60 transition-all' + (i === 0 ? ' bg-orange-500 border-orange-500 w-8' : '');
        btn.addEventListener('click', function () { go(i); start(); });
        dotsWrap.appendChild(btn);
    });

    window.__heroSlides = slides;
    window.__heroRefresh = function () { go(current); };

    function go(i) {
        current = (i + slides.length) % slides.length;
        const slide = slides[current];
        els.forEach(function (el, idx) { el.classList.toggle('is-active', idx === current); });
        title.textContent = slide.title;
        subtitle.textContent = slide.subtitle;
        if (ctaPrimary && slide.ctaPrimary) {
            ctaPrimary.textContent = slide.ctaPrimary.text;
            ctaPrimary.href = slide.ctaPrimary.href;
        }
        if (ctaSecondary && slide.ctaSecondary) {
            ctaSecondary.textContent = slide.ctaSecondary.text;
            ctaSecondary.href = slide.ctaSecondary.href;
        }
        dotsWrap.querySelectorAll('button').forEach(function (dot, idx) {
            dot.className = 'h-2.5 rounded-full border-2 border-white/60 transition-all ' + (idx === current ? 'w-8 bg-orange-500 border-orange-500' : 'w-2.5 bg-transparent');
        });
    }

    function start() { clearInterval(timer); timer = setInterval(function () { go(current + 1); }, 6000); }
    go(0); start();

    document.getElementById('menu-toggle').addEventListener('click', function () {
        const nav = document.getElementById('mobile-nav');
        const open = nav.classList.toggle('hidden') === false;
        this.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    /* Multi-step form */
    (function () {
        const form = document.getElementById('gform_1');
        if (!form) return;

        const pages = form.querySelectorAll('.gform_page');
        const progressBar = document.getElementById('form-progress-bar');
        const stepLabel = document.getElementById('form-step-label');
        const stepName = document.getElementById('form-step-name');
        const dots = document.querySelectorAll('#form-progress-dots [data-dot]');
        const stepNames = ['Specifikace produktu', 'Rozměry a množství', 'Kontaktní údaje'];
        let current = 0;

        function updateDesignRecap() {
            var recapEl = document.getElementById('design-recap-text');
            if (!recapEl) return;
            var material = form.querySelector('input[name="input_8"]:checked');
            var baseColor = form.querySelector('input[name="input_9"]:checked');
            var textForm = document.getElementById('tape-print-text-form');
            var parts = [];
            if (material) parts.push(material.value);
            if (baseColor) parts.push(baseColor.value);
            parts.push(textForm && textForm.value.trim() ? '"' + textForm.value.trim() + '"' : 'bez textu');
            recapEl.textContent = parts.join(' · ');
        }

        function syncModalFromForm() {
            var modal = document.getElementById('tape-3d-modal');
            if (!modal) return;
            var material = form.querySelector('input[name="input_8"]:checked');
            var baseColor = form.querySelector('input[name="input_9"]:checked');
            if (material) {
                var m = modal.querySelector('input[name="modal_input_8"][value="' + material.value + '"]');
                if (m) m.checked = true;
            }
            if (baseColor) {
                var c = modal.querySelector('input[name="modal_input_9"][value="' + baseColor.value + '"]');
                if (c) c.checked = true;
            }
            var textForm = document.getElementById('tape-print-text-form');
            var textModal = document.getElementById('tape-print-text');
            if (textForm && textModal) textModal.value = textForm.value;
            var colorHidden = document.getElementById('tape-text-color-value');
            if (colorHidden) {
                var colorRadio = modal.querySelector('input[name="tape_text_color"][value="' + colorHidden.value + '"]');
                if (colorRadio) colorRadio.checked = true;
                var colorCustom = document.getElementById('tape-text-color-custom');
                if (colorCustom) colorCustom.value = colorHidden.value;
            }
            var sizeForm = document.getElementById('tape-text-size-form');
            var sizeModal = document.getElementById('tape-text-size');
            var sizeLabel = document.getElementById('tape-text-size-value');
            if (sizeForm && sizeModal) {
                sizeModal.value = sizeForm.value;
                if (sizeLabel) sizeLabel.textContent = sizeForm.value;
            }
            var offsetForm = document.getElementById('tape-text-offset-form');
            var offsetModal = document.getElementById('tape-text-offset');
            var offsetLabel = document.getElementById('tape-text-offset-value');
            if (offsetForm && offsetModal) {
                offsetModal.value = offsetForm.value;
                if (offsetLabel) offsetLabel.textContent = offsetForm.value;
            }
            var fontForm = document.getElementById('tape-font-form');
            if (fontForm && modal) {
                var fontRadio = modal.querySelector('input[name="tape_font_family"][value="' + fontForm.value + '"]');
                if (fontRadio) fontRadio.checked = true;
            }
            var spacingForm = document.getElementById('tape-motif-spacing-form');
            var spacingModal = document.getElementById('tape-motif-spacing');
            var spacingLabel = document.getElementById('tape-motif-spacing-value');
            if (spacingForm && spacingModal) {
                spacingModal.value = spacingForm.value;
                if (spacingLabel) spacingLabel.textContent = spacingForm.value;
            }
            var widthForm = form.querySelector('input[name="input_12"]:checked');
            var modalWidths = ['25', '50', '75'];
            if (widthForm && modalWidths.indexOf(widthForm.value) !== -1) {
                var mw = modal.querySelector('input[name="modal_input_12"][value="' + widthForm.value + '"]');
                if (mw) mw.checked = true;
            }
            var lengthForm = form.querySelector('input[name="input_11"]:checked');
            var modalLengths = ['66', '132', '330'];
            if (lengthForm && modalLengths.indexOf(lengthForm.value) !== -1) {
                var ml = modal.querySelector('input[name="modal_input_11"][value="' + lengthForm.value + '"]');
                if (ml) ml.checked = true;
            }
        }

        function syncFormFromModal() {
            var modal = document.getElementById('tape-3d-modal');
            if (!modal) return;
            var modalMaterial = modal.querySelector('input[name="modal_input_8"]:checked');
            var modalColor = modal.querySelector('input[name="modal_input_9"]:checked');
            if (modalMaterial) {
                var f = form.querySelector('input[name="input_8"][value="' + modalMaterial.value + '"]');
                if (f) f.checked = true;
            }
            if (modalColor) {
                var fc = form.querySelector('input[name="input_9"][value="' + modalColor.value + '"]');
                if (fc) fc.checked = true;
            }
            var textModal = document.getElementById('tape-print-text');
            var textForm = document.getElementById('tape-print-text-form');
            if (textModal && textForm) textForm.value = textModal.value;
            var colorHidden = document.getElementById('tape-text-color-value');
            var colorRadio = modal.querySelector('input[name="tape_text_color"]:checked');
            var colorCustom = document.getElementById('tape-text-color-custom');
            if (colorHidden) {
                if (colorRadio) colorHidden.value = colorRadio.value;
                else if (colorCustom) colorHidden.value = colorCustom.value;
            }
            var sizeModal = document.getElementById('tape-text-size');
            var sizeForm = document.getElementById('tape-text-size-form');
            if (sizeModal && sizeForm) sizeForm.value = sizeModal.value;
            var offsetModal = document.getElementById('tape-text-offset');
            var offsetForm = document.getElementById('tape-text-offset-form');
            if (offsetModal && offsetForm) offsetForm.value = offsetModal.value;
            var fontRadio = modal.querySelector('input[name="tape_font_family"]:checked');
            var fontForm = document.getElementById('tape-font-form');
            if (fontRadio && fontForm) fontForm.value = fontRadio.value;
            var spacingModal = document.getElementById('tape-motif-spacing');
            var spacingForm = document.getElementById('tape-motif-spacing-form');
            if (spacingModal && spacingForm) spacingForm.value = spacingModal.value;
            var modalWidth = modal.querySelector('input[name="modal_input_12"]:checked');
            if (modalWidth) {
                var fw = form.querySelector('input[name="input_12"][value="' + modalWidth.value + '"]');
                if (fw) fw.checked = true;
            }
            var modalLength = modal.querySelector('input[name="modal_input_11"]:checked');
            if (modalLength) {
                var fl = form.querySelector('input[name="input_11"][value="' + modalLength.value + '"]');
                if (fl) fl.checked = true;
            }
            updateDesignRecap();
        }

        function open3dModal() {
            var modal = document.getElementById('tape-3d-modal');
            if (!modal) return;
            syncModalFromForm();
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            document.body.classList.add('modal-open');
            if (window.TapeConfigurator3D) {
                window.TapeConfigurator3D.syncFromForm();
                requestAnimationFrame(function () {
                    window.TapeConfigurator3D.resize();
                    setTimeout(function () { window.TapeConfigurator3D.resize(); }, 150);
                });
            }
        }

        function close3dModal() {
            var modal = document.getElementById('tape-3d-modal');
            if (!modal) return;
            syncFormFromModal();
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            document.body.classList.remove('modal-open');
        }

        var modalOpenBtn = document.getElementById('tape-3d-modal-open');
        var modalCloseBtn = document.getElementById('tape-3d-modal-close');
        var modalEl = document.getElementById('tape-3d-modal');
        if (modalOpenBtn) modalOpenBtn.addEventListener('click', open3dModal);
        if (modalCloseBtn) modalCloseBtn.addEventListener('click', close3dModal);
        if (modalEl) {
            modalEl.addEventListener('click', function (e) {
                if (e.target === modalEl) close3dModal();
            });
        }
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modalEl && !modalEl.classList.contains('hidden')) close3dModal();
        });

        function validatePage(index) {
            const page = pages[index];
            const fields = page.querySelectorAll('input[required], textarea[required], select[required]');
            for (const field of fields) {
                if (!field.checkValidity()) {
                    field.reportValidity();
                    field.focus();
                    return false;
                }
            }
            return true;
        }

        function goTo(index) {
            if (index < 0 || index >= pages.length) return;
            pages.forEach(function (page, i) {
                page.classList.toggle('hidden', i !== index);
            });
            current = index;
            const pct = ((index + 1) / pages.length) * 100;
            progressBar.style.width = pct + '%';
            stepLabel.textContent = 'Krok ' + (index + 1) + ' ze ' + pages.length;
            stepName.textContent = stepNames[index];
            dots.forEach(function (dot, i) {
                dot.className = 'rounded-full transition-all ' + (i === index ? 'h-2 w-8 bg-orange-500' : i < index ? 'h-2 w-2 bg-orange-300' : 'h-2 w-2 bg-slate-200');
            });

            if (index === 1) updateDesignRecap();
            form.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        form.querySelectorAll('.btn-next').forEach(function (btn) {
            btn.addEventListener('click', function () {
                if (validatePage(current)) goTo(current + 1);
            });
        });

        form.querySelectorAll('.btn-prev').forEach(function (btn) {
            btn.addEventListener('click', function () { goTo(current - 1); });
        });

        form.addEventListener('submit', function (e) {
            if (!validatePage(current)) {
                e.preventDefault();
            }
        });

        /* Množstevní sleva – dynamický badge */
        var qtyInput = document.getElementById('qty');
        var qtyBadge = document.getElementById('qty-discount-badge');
        var qtyBadgeText = document.getElementById('qty-discount-text');
        var QTY_THRESHOLD = 360;
        var tipText = 'Tip: Od 360 ks získáváte dopravu zdarma a velkoobchodní ceny.';
        var successText = '🔥 Skvělá volba! Aktivovali jste velkoobchodní slevu 15 % a dopravu zdarma.';
        var badgeGray = 'mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-100 max-h-16 border-slate-200 bg-slate-50 font-medium text-slate-500';
        var badgeGreen = 'mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-100 max-h-16 border-emerald-200 bg-emerald-50 font-semibold text-emerald-700 shadow-sm shadow-emerald-100';
        var badgeHidden = 'mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-0 max-h-0 py-0 border-transparent pointer-events-none';

        function updateQtyDiscountBadge() {
            if (!qtyInput || !qtyBadge || !qtyBadgeText) return;

            var raw = qtyInput.value.trim();
            var qty = raw === '' ? NaN : parseInt(raw, 10);

            if (raw === '' || isNaN(qty)) {
                qtyBadge.className = badgeHidden;
                qtyBadgeText.textContent = tipText;
                return;
            }

            if (qty >= QTY_THRESHOLD) {
                qtyBadge.className = badgeGreen;
                qtyBadgeText.textContent = successText;
            } else {
                qtyBadge.className = badgeGray;
                qtyBadgeText.textContent = tipText;
            }
        }

        if (qtyInput) {
            qtyInput.addEventListener('input', updateQtyDiscountBadge);
            qtyInput.addEventListener('change', updateQtyDiscountBadge);
            updateQtyDiscountBadge();
        }
    })();
})();
