/**
 * Multi-step inquiry form – submit to /api/inquiry.
 */
(function () {
    'use strict';

    var form = document.getElementById('gform_1');
    if (!form) return;

    var wrapper = document.getElementById('gform_wrapper_1');
    var submitBtn = document.getElementById('gform_submit_button_1');
    var defaultSubmitLabel = submitBtn ? submitBtn.textContent : 'Odeslat poptávku';

    function getRadioValue(name) {
        var checked = form.querySelector('input[name="' + name + '"]:checked');
        return checked ? checked.value : '';
    }

    function getSelectLabel(id) {
        var el = document.getElementById(id);
        if (!el || el.selectedIndex < 0) return '';
        var opt = el.options[el.selectedIndex];
        if (!opt || !opt.value) return '';
        return opt.textContent.trim();
    }

    function getSelectValue(id) {
        var el = document.getElementById(id);
        return el ? el.value.trim() : '';
    }

    function collectPayload() {
        return {
            materialSlug: getSelectValue('input_material'),
            materialLabel: getSelectLabel('input_material'),
            product: getSelectValue('input_product'),
            adhesive: getRadioValue('input_8'),
            acrylNoSilent: !!form.querySelector('#input_acryl_no_silent:checked'),
            baseColor: getRadioValue('input_9'),
            printColors: getRadioValue('input_10'),
            widthMm: getRadioValue('input_12'),
            lengthM: getRadioValue('input_11'),
            quantity: (document.getElementById('qty') || {}).value || '',
            orderPeriod: getRadioValue('input_18'),
            company: (document.getElementById('company') || {}).value || '',
            ico: (document.getElementById('ico') || {}).value || '',
            contactName: (document.getElementById('name') || {}).value || '',
            email: (document.getElementById('email') || {}).value || '',
            phone: (document.getElementById('phone') || {}).value || '',
            note: (document.getElementById('note') || {}).value || '',
            gdprConsent: !!form.querySelector('input[name="input_14.1"]:checked'),
            website: (form.querySelector('input[name="website"]') || {}).value || '',
        };
    }

    function setSubmitting(isSubmitting) {
        if (!submitBtn) return;
        submitBtn.disabled = isSubmitting;
        submitBtn.setAttribute('aria-busy', isSubmitting ? 'true' : 'false');
        submitBtn.textContent = isSubmitting ? 'Odesílám…' : defaultSubmitLabel;
        submitBtn.classList.toggle('opacity-70', isSubmitting);
        submitBtn.classList.toggle('pointer-events-none', isSubmitting);
    }

    function showMessage(type, text) {
        var existing = document.getElementById('inquiry-form-message');
        if (existing) existing.remove();

        var box = document.createElement('div');
        box.id = 'inquiry-form-message';
        box.setAttribute('role', type === 'error' ? 'alert' : 'status');
        box.className =
            'mx-auto mb-6 max-w-2xl rounded-2xl border px-5 py-4 text-sm leading-relaxed ' +
            (type === 'success'
                ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
                : 'border-red-200 bg-red-50 text-red-800');

        if (type === 'success') {
            box.innerHTML =
                '<p class="font-bold">Děkujeme, poptávka byla odeslána.</p>' +
                '<p class="mt-1">Ozveme se vám co nejdříve na uvedený e-mail. Kopie žádosti šla týmu prodeje.</p>';
        } else {
            box.textContent = text;
        }

        var head = document.getElementById('form-outer-head');
        if (head && head.parentNode) {
            head.parentNode.insertBefore(box, head.nextSibling);
        } else if (wrapper) {
            wrapper.parentNode.insertBefore(box, wrapper);
        }

        box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function showSuccess() {
        showMessage('success');
        if (wrapper) {
            wrapper.classList.add('hidden');
        }
        var head = document.getElementById('form-outer-head');
        if (head) head.classList.add('hidden');
    }

    window.__submitInquiryForm = function (validatePage, currentStep, goToStep, validateAll) {
        return async function handleSubmit(e) {
            e.preventDefault();

            var validation = { ok: true, firstInvalid: -1 };
            if (typeof validateAll === 'function') {
                validation = validateAll();
            } else if (typeof validatePage === 'function') {
                validation = { ok: validatePage(currentStep), firstInvalid: currentStep };
            }

            if (!validation.ok) {
                if (typeof goToStep === 'function' && validation.firstInvalid >= 0) {
                    goToStep(validation.firstInvalid);
                }
                return;
            }

            setSubmitting(true);

            try {
                var payload = collectPayload();
                var response = await fetch('/api/inquiry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                var data = await response.json().catch(function () { return {}; });

                if (!response.ok || !data.ok) {
                    throw new Error(data.error || 'Odeslání se nezdařilo.');
                }

                showSuccess();
            } catch (err) {
                showMessage('error', err.message || 'Odeslání se nezdařilo. Zkuste to prosím znovu.');
            } finally {
                setSubmitting(false);
            }
        };
    };
})();
