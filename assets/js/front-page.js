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
            ctaPrimary: { text: 'Vyžádat vzorky', href: '#gf_1', inquirySample: true },
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
            ctaPrimary.classList.toggle('js-inquiry-sample', !!slide.ctaPrimary.inquirySample);
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

        function toggleAcrylNoiseOption() {
            var material = form.querySelector('input[name="input_8"]:checked');
            var isAcryl = material && material.value === 'ACRYL';
            var opt = document.getElementById('acryl-noise-option');
            var cb = document.getElementById('input_acryl_no_silent');
            if (opt) opt.classList.toggle('hidden', !isAcryl);
            if (!isAcryl && cb) cb.checked = false;
        }

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

            form.scrollIntoView({ behavior: 'auto', block: 'nearest' });
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
        var QTY_MIN = 360;
        var tipText = 'Minimální množství je 360 ks.';
        var successText = '🔥 Skvělá volba! Máte dopravu zdarma. Doprava trvá přibližně 3–4 týdny.';
        var badgeGray = 'mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-100 max-h-24 border-slate-200 bg-slate-50 font-medium text-slate-500';
        var badgeGreen = 'mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-100 max-h-24 border-emerald-200 bg-emerald-50 font-semibold text-emerald-700 shadow-sm shadow-emerald-100';
        var badgeHidden = 'mt-2 overflow-hidden rounded-lg border px-3 py-1.5 text-xs leading-snug transition-all duration-300 ease-out opacity-0 max-h-0 py-0 border-transparent pointer-events-none';

        function updateQtyDiscountBadge() {
            if (!qtyInput || !qtyBadge || !qtyBadgeText) return;

            var raw = qtyInput.value.trim();
            var qty = raw === '' ? NaN : parseInt(raw, 10);

            if (raw === '' || isNaN(qty)) {
                qtyBadge.className = badgeGray;
                qtyBadgeText.textContent = tipText;
                return;
            }

            if (qty >= QTY_MIN) {
                qtyBadge.className = badgeGreen;
                qtyBadgeText.textContent = successText;
            } else {
                qtyBadge.className = badgeGray;
                qtyBadgeText.textContent = tipText;
            }
        }

        if (qtyInput) {
            qtyInput.addEventListener('invalid', function () {
                if (qtyInput.validity.rangeUnderflow) {
                    qtyInput.setCustomValidity('Minimální množství je 360 ks.');
                }
            });
            qtyInput.addEventListener('input', function () {
                qtyInput.setCustomValidity('');
                updateQtyDiscountBadge();
            });
            qtyInput.addEventListener('change', updateQtyDiscountBadge);
            updateQtyDiscountBadge();
        }

        form.querySelectorAll('input[name="input_8"]').forEach(function (radio) {
            radio.addEventListener('change', toggleAcrylNoiseOption);
        });
        toggleAcrylNoiseOption();

        var SAMPLE_NOTE_TEXT = 'Mám zájem o testovací vzorek.';
        var CONTACT_STEP = 2;

        function applySampleNote() {
            var note = document.getElementById('note');
            if (note) note.value = SAMPLE_NOTE_TEXT;
        }

        function openInquiryWithSample(e) {
            if (e) e.preventDefault();
            if (window.location.hash !== '#gf_1') {
                history.replaceState(null, '', '#gf_1');
            }
            goTo(CONTACT_STEP);
            applySampleNote();
            var note = document.getElementById('note');
            if (note) {
                setTimeout(function () { note.focus(); }, 300);
            }
        }

        window.__openInquiryWithSample = openInquiryWithSample;

        document.addEventListener('click', function (e) {
            if (e.target.closest('.js-inquiry-sample')) {
                openInquiryWithSample(e);
            }
        });

        var noteSampleBtn = document.getElementById('note-sample-btn');
        if (noteSampleBtn) {
            noteSampleBtn.addEventListener('click', function () {
                applySampleNote();
                var note = document.getElementById('note');
                if (note) note.focus();
            });
        }

        var inquiryParams = new URLSearchParams(window.location.search);
        if (inquiryParams.get('vzorek') === '1' && window.location.hash === '#gf_1') {
            setTimeout(openInquiryWithSample, 150);
        }
    })();
})();
