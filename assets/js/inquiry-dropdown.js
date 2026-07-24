/**
 * Site-styled custom dropdown for native <select> elements.
 */
(function () {
    'use strict';

    var openDropdown = null;

    function closeOpenDropdown() {
        if (!openDropdown) return;
        openDropdown.classList.remove('is-open');
        openDropdown.querySelector('.inquiry-dropdown__trigger').setAttribute('aria-expanded', 'false');
        openDropdown = null;
    }

    function updateTrigger(select, trigger) {
        var label = trigger.querySelector('.inquiry-dropdown__label');
        var opt = select.options[select.selectedIndex];
        label.textContent = opt ? opt.textContent : '';
        label.classList.toggle('is-placeholder', !select.value);
    }

    function rebuildMenu(select, menu) {
        menu.innerHTML = '';
        Array.prototype.forEach.call(select.options, function (opt) {
            if (opt.disabled && !opt.value) return;

            var li = document.createElement('li');
            li.className = 'inquiry-dropdown__option';
            li.setAttribute('role', 'option');
            li.dataset.value = opt.value;
            li.textContent = opt.textContent;

            if (opt.value === select.value) {
                li.classList.add('is-selected');
                li.setAttribute('aria-selected', 'true');
            }

            li.addEventListener('click', function () {
                select.value = opt.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                closeOpenDropdown();
                rebuildMenu(select, menu);
                updateTrigger(select, menu.previousElementSibling);
            });

            menu.appendChild(li);
        });
    }

    function init(select) {
        if (!select || select.dataset.dropdownReady === '1') {
            return select ? select.closest('.inquiry-dropdown') : null;
        }

        select.dataset.dropdownReady = '1';
        select.classList.add('sr-only');
        select.tabIndex = -1;

        var wrap = document.createElement('div');
        wrap.className = 'inquiry-dropdown';

        var parent = select.parentNode;
        if (parent.classList && parent.classList.contains('relative')) {
            parent.classList.remove('relative');
            parent.insertBefore(wrap, select);
            wrap.appendChild(select);
        } else {
            parent.insertBefore(wrap, select);
            wrap.appendChild(select);
        }

        var listId = select.id ? select.id + '-listbox' : 'inquiry-dropdown-listbox-' + Math.random().toString(36).slice(2);

        var trigger = document.createElement('button');
        trigger.type = 'button';
        trigger.className = 'inquiry-dropdown__trigger glass glass--chip';
        trigger.setAttribute('aria-haspopup', 'listbox');
        trigger.setAttribute('aria-expanded', 'false');
        trigger.setAttribute('aria-controls', listId);

        var label = document.createElement('span');
        label.className = 'inquiry-dropdown__label';
        trigger.appendChild(label);

        var chevron = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        chevron.setAttribute('class', 'inquiry-dropdown__chevron');
        chevron.setAttribute('fill', 'none');
        chevron.setAttribute('viewBox', '0 0 24 24');
        chevron.setAttribute('stroke', 'currentColor');
        chevron.setAttribute('stroke-width', '2');
        chevron.setAttribute('aria-hidden', 'true');
        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('stroke-linecap', 'round');
        path.setAttribute('stroke-linejoin', 'round');
        path.setAttribute('d', 'M19 9l-7 7-7-7');
        chevron.appendChild(path);
        trigger.appendChild(chevron);

        var menu = document.createElement('ul');
        menu.className = 'inquiry-dropdown__menu glass glass--menu';
        menu.id = listId;
        menu.setAttribute('role', 'listbox');

        wrap.appendChild(trigger);
        wrap.appendChild(menu);

        rebuildMenu(select, menu);
        updateTrigger(select, trigger);

        trigger.addEventListener('click', function () {
            var isOpen = wrap.classList.contains('is-open');
            closeOpenDropdown();
            if (!isOpen) {
                wrap.classList.add('is-open');
                trigger.setAttribute('aria-expanded', 'true');
                openDropdown = wrap;
                rebuildMenu(select, menu);
                // Keep open list in view and scrollable on short screens
                window.requestAnimationFrame(function () {
                    var rect = menu.getBoundingClientRect();
                    var pad = 16;
                    if (rect.bottom > window.innerHeight - pad) {
                        menu.scrollTop = 0;
                        wrap.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                    }
                });
            }
        });

        // Keep wheel/trackpad scrolling on the menu (Safari often scrolls the page instead)
        menu.addEventListener('wheel', function (e) {
            var canScroll = menu.scrollHeight > menu.clientHeight + 1;
            if (!canScroll) return;
            var top = menu.scrollTop;
            var max = menu.scrollHeight - menu.clientHeight;
            var delta = e.deltaY;
            var atTop = top <= 0 && delta < 0;
            var atBottom = top >= max - 1 && delta > 0;
            if (atTop || atBottom) return;
            e.preventDefault();
            e.stopPropagation();
            menu.scrollTop = Math.min(max, Math.max(0, top + delta));
        }, { passive: false });
        menu.addEventListener('touchmove', function (e) {
            e.stopPropagation();
        }, { passive: true });

        select.addEventListener('change', function () {
            rebuildMenu(select, menu);
            updateTrigger(select, trigger);
        });

        select._inquiryDropdownRefresh = function () {
            rebuildMenu(select, menu);
            updateTrigger(select, trigger);
        };

        return wrap;
    }

    function refresh(select) {
        if (!select) return;
        if (select._inquiryDropdownRefresh) {
            select._inquiryDropdownRefresh();
            return;
        }
        init(select);
    }

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.inquiry-dropdown')) {
            closeOpenDropdown();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeOpenDropdown();
    });

    window.InquiryDropdown = {
        init: init,
        refresh: refresh,
        closeAll: closeOpenDropdown,
    };
})();
