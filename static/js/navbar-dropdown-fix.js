/**
 * NAVBAR DROPDOWN FIX V3 - Solución mejorada para dropdown
 * Fix crítico: Forzar display:none cuando se cierra
 */
(function() {
    'use strict';
    // Esperar a que el DOM esté completamente cargado
    function initDropdown() {
        var dropdownToggle = document.querySelector('#navbarDropdownUser');
        var dropdownMenu = dropdownToggle ? dropdownToggle.nextElementSibling : null;
        var navItem = dropdownToggle ? dropdownToggle.closest('.nav-item.dropdown') : null;
        if (!dropdownToggle || !dropdownMenu) {
            return;
        }
        // Forzar estilos críticos via JavaScript
        dropdownToggle.style.cursor = 'pointer';
        dropdownToggle.style.pointerEvents = 'auto';
        dropdownMenu.style.pointerEvents = 'auto';
        // Variable para controlar el estado
        var isOpen = false;
        var isToggling = false;
        // Función para abrir el dropdown
        function openDropdown() {
            if (isOpen) return;
            dropdownMenu.classList.add('show');
            dropdownToggle.setAttribute('aria-expanded', 'true');
            navItem.classList.add('show');
            isOpen = true;
            // Forzar estilos cuando está abierto
            dropdownMenu.style.display = 'block';
            dropdownMenu.style.position = 'absolute';
            dropdownMenu.style.zIndex = '9999';
            dropdownMenu.style.opacity = '1';
            dropdownMenu.style.pointerEvents = 'auto';
            dropdownMenu.style.visibility = 'visible';
        }
        // Función para cerrar el dropdown
        function closeDropdown() {
            if (!isOpen) return;
            dropdownMenu.classList.remove('show');
            dropdownToggle.setAttribute('aria-expanded', 'false');
            navItem.classList.remove('show');
            isOpen = false;
            // CRÍTICO: Forzar ocultación inmediata
            dropdownMenu.style.display = 'none';
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.opacity = '0';
        }
        // Toggle del dropdown
        function toggleDropdown(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            if (isToggling) {
                return;
            }
            isToggling = true;
            if (isOpen) {
                closeDropdown();
            } else {
                openDropdown();
            }
            setTimeout(function() {
                isToggling = false;
            }, 100);
        }
        dropdownToggle.addEventListener('click', function(e) {
            toggleDropdown(e);
        });
        var dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
        dropdownItems.forEach(function(item) {
            item.style.cursor = 'pointer';
            item.style.pointerEvents = 'auto';
            item.addEventListener('click', function(e) {
                if (item.tagName === 'A' && item.href && item.href !== '#') {
                    closeDropdown();
                } else {
                    closeDropdown();
                }
            });
        });
        document.addEventListener('click', function(e) {
            if (!isOpen) return;
            var clickedInside = navItem.contains(e.target);
            if (!clickedInside) {
                closeDropdown();
            }
        });
        dropdownMenu.addEventListener('click', function(e) {
            if (e.target === dropdownMenu) {
                closeDropdown();
            }
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isOpen) {
                closeDropdown();
            }
        });
        dropdownToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleDropdown(e);
            }
        });
        window.addEventListener('blur', function() {
            if (isOpen) {
                closeDropdown();
            }
        });
        dropdownToggle.setAttribute('data-dropdown-initialized', 'true');
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDropdown);
    } else {
        initDropdown();
    }
    window.addEventListener('load', function() {
        var dropdownToggle = document.querySelector('#navbarDropdownUser');
        if (dropdownToggle && !dropdownToggle.hasAttribute('data-dropdown-initialized')) {
            initDropdown();
        }
    });
})();
