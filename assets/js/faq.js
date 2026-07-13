/**
 * FAQ accordion – animated panels, single-open mode.
 */
(function () {
    'use strict';

    var list = document.querySelector('[data-faq-list]');
    if (!list) return;

    var items = Array.prototype.slice.call(list.querySelectorAll('.faq-item'));

    function closeItem(item) {
        var trigger = item.querySelector('.faq-item__trigger');
        item.classList.remove('is-open');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }

    function openItem(item) {
        items.forEach(function (other) {
            if (other !== item) closeItem(other);
        });
        var trigger = item.querySelector('.faq-item__trigger');
        item.classList.add('is-open');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
    }

    items.forEach(function (item, index) {
        var trigger = item.querySelector('.faq-item__trigger');
        var panel = item.querySelector('.faq-item__panel');
        if (!trigger || !panel) return;

        var panelId = 'faq-panel-' + index;
        var triggerId = 'faq-trigger-' + index;
        trigger.id = triggerId;
        panel.id = panelId;
        trigger.setAttribute('aria-controls', panelId);
        panel.setAttribute('role', 'region');
        panel.setAttribute('aria-labelledby', triggerId);

        trigger.addEventListener('click', function () {
            if (item.classList.contains('is-open')) {
                closeItem(item);
            } else {
                openItem(item);
            }
        });
    });
})();
