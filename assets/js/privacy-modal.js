/**
 * GDPR / privacy info modal for inquiry form consent link.
 */
(function () {
    'use strict';

    var modal = document.getElementById('privacy-modal');
    if (!modal) {
        return;
    }

    var closeBtn = document.getElementById('privacy-modal-close');
    var backdrop = modal.querySelector('[data-privacy-modal-close]');
    var lastFocus = null;

    function openModal(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        lastFocus = document.activeElement;
        modal.hidden = false;
        modal.classList.add('is-open');
        document.body.style.overflow = 'hidden';
        if (closeBtn) {
            closeBtn.focus();
        }
    }

    function closeModal() {
        modal.hidden = true;
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
        if (lastFocus && typeof lastFocus.focus === 'function') {
            lastFocus.focus();
        }
    }

    document.querySelectorAll('[data-privacy-modal-open]').forEach(function (trigger) {
        trigger.addEventListener('click', openModal);
        trigger.addEventListener('mousedown', function (e) {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    if (backdrop) {
        backdrop.addEventListener('click', closeModal);
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
})();
