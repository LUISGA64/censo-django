/**
 * OPTIMIZACIONES MÓVILES - CENSO WEB
 * Mejoras de UX para dispositivos móviles y tablets
 */

(function() {
    'use strict';

    // ========================================
    // DETECCIÓN DE DISPOSITIVO
    // ========================================

    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isTablet = /(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(navigator.userAgent);
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;

    // Agregar clases al body
    document.addEventListener('DOMContentLoaded', function() {
        if (isMobile) document.body.classList.add('is-mobile');
        if (isTablet) document.body.classList.add('is-tablet');
        if (isTouchDevice) document.body.classList.add('is-touch');
        if (isIOS) document.body.classList.add('is-ios');
    });

    // ========================================
    // SIDEBAR MÓVIL
    // ========================================

    class MobileSidebar {
        constructor() {
            this.sidebar = document.querySelector('.sidenav');
            this.toggleBtn = document.querySelector('.sidenav-toggler');
            this.body = document.body;
            this.overlay = null;

            if (this.sidebar && window.innerWidth < 1200) {
                this.init();
            }
        }

        init() {
            // Crear overlay
            this.createOverlay();

            // Event listeners
            if (this.toggleBtn) {
                this.toggleBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.toggle();
                });
            }

            // Cerrar al hacer click en overlay
            if (this.overlay) {
                this.overlay.addEventListener('click', () => {
                    this.close();
                });
            }

            // Cerrar al hacer click en un link (opcional)
            const sidebarLinks = this.sidebar.querySelectorAll('.nav-link:not(.dropdown-toggle)');
            sidebarLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth < 1200) {
                        setTimeout(() => this.close(), 200);
                    }
                });
            });

            // Cerrar con ESC
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isOpen()) {
                    this.close();
                }
            });

            // Cerrar al cambiar orientación
            window.addEventListener('orientationchange', () => {
                if (this.isOpen()) {
                    this.close();
                }
            });
        }

        createOverlay() {
            this.overlay = document.createElement('div');
            this.overlay.className = 'sidebar-overlay';
            this.overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                z-index: 1040;
                display: none;
                opacity: 0;
                transition: opacity 0.3s ease-in-out;
            `;
            document.body.appendChild(this.overlay);
        }

        toggle() {
            this.isOpen() ? this.close() : this.open();
        }

        open() {
            this.body.classList.add('g-sidenav-show');
            this.sidebar.style.transform = 'translateX(0)';

            if (this.overlay) {
                this.overlay.style.display = 'block';
                setTimeout(() => {
                    this.overlay.style.opacity = '1';
                }, 10);
            }

            // Prevenir scroll en body
            this.body.style.overflow = 'hidden';
        }

        close() {
            this.body.classList.remove('g-sidenav-show');
            this.sidebar.style.transform = '';

            if (this.overlay) {
                this.overlay.style.opacity = '0';
                setTimeout(() => {
                    this.overlay.style.display = 'none';
                }, 300);
            }

            // Restaurar scroll
            this.body.style.overflow = '';
        }

        isOpen() {
            return this.body.classList.contains('g-sidenav-show');
        }
    }

    // ========================================
    // TABLAS RESPONSIVAS
    // ========================================

    class ResponsiveTables {
        constructor() {
            this.tables = document.querySelectorAll('table:not(.no-responsive)');
            if (this.tables.length > 0 && window.innerWidth < 768) {
                this.init();
            }
        }

        init() {
            this.tables.forEach(table => {
                // Agregar data-label a cada celda
                const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
                const rows = table.querySelectorAll('tbody tr');

                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    cells.forEach((cell, index) => {
                        if (headers[index]) {
                            cell.setAttribute('data-label', headers[index]);
                        }
                    });
                });

                // Agregar clase wrapper si no existe
                if (!table.parentElement.classList.contains('table-responsive')) {
                    const wrapper = document.createElement('div');
                    wrapper.className = 'table-responsive';
                    table.parentNode.insertBefore(wrapper, table);
                    wrapper.appendChild(table);
                }
            });
        }

        // Convertir tabla a cards en móvil
        static toCards(tableSelector) {
            if (window.innerWidth >= 768) return;

            const table = document.querySelector(tableSelector);
            if (!table) return;

            table.classList.add('table-mobile-cards');
        }
    }

    // ========================================
    // FORMULARIOS MEJORADOS
    // ========================================

    class MobileForms {
        constructor() {
            this.forms = document.querySelectorAll('form');
            if (this.forms.length > 0 && isMobile) {
                this.init();
            }
        }

        init() {
            this.forms.forEach(form => {
                // Auto-scroll al campo con error
                const errorFields = form.querySelectorAll('.is-invalid, .error');
                if (errorFields.length > 0) {
                    errorFields[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                    errorFields[0].focus();
                }

                // Mejorar select2 para móvil
                this.optimizeSelect2();
            });

            // Agregar botón de limpiar en inputs de búsqueda
            this.addClearButtons();
        }

        optimizeSelect2() {
            if (typeof $.fn.select2 !== 'undefined') {
                $('.select2').each(function() {
                    if (!$(this).data('select2')) {
                        $(this).select2({
                            width: '100%',
                            dropdownAutoWidth: true,
                            minimumResultsForSearch: isMobile ? 0 : 10,
                            language: {
                                noResults: function() {
                                    return "No se encontraron resultados";
                                },
                                searching: function() {
                                    return "Buscando...";
                                }
                            }
                        });
                    }
                });
            }
        }

        addClearButtons() {
            const searchInputs = document.querySelectorAll('input[type="search"], input.search-input');
            searchInputs.forEach(input => {
                if (input.parentElement.querySelector('.clear-input')) return;

                const clearBtn = document.createElement('button');
                clearBtn.type = 'button';
                clearBtn.className = 'clear-input';
                clearBtn.innerHTML = '<i class="fas fa-times-circle"></i>';
                clearBtn.style.cssText = `
                    position: absolute;
                    right: 10px;
                    top: 50%;
                    transform: translateY(-50%);
                    background: none;
                    border: none;
                    color: #999;
                    cursor: pointer;
                    display: none;
                    padding: 5px;
                    z-index: 10;
                `;

                // Posicionar el input container
                input.parentElement.style.position = 'relative';
                input.parentElement.appendChild(clearBtn);

                // Mostrar/ocultar botón
                input.addEventListener('input', () => {
                    clearBtn.style.display = input.value ? 'block' : 'none';
                });

                // Limpiar input
                clearBtn.addEventListener('click', () => {
                    input.value = '';
                    input.dispatchEvent(new Event('input'));
                    input.focus();
                    clearBtn.style.display = 'none';
                });
            });
        }
    }

    // ========================================
    // MEJORAS DE TOUCH
    // ========================================

    class TouchEnhancements {
        constructor() {
            if (isTouchDevice) {
                this.init();
            }
        }

        init() {
            // Agregar clase active al tocar elementos clickeables
            const clickableElements = document.querySelectorAll('a, button, .btn, .clickable');

            clickableElements.forEach(el => {
                el.addEventListener('touchstart', function() {
                    this.classList.add('touch-active');
                }, { passive: true });

                el.addEventListener('touchend', function() {
                    setTimeout(() => {
                        this.classList.remove('touch-active');
                    }, 150);
                }, { passive: true });

                el.addEventListener('touchcancel', function() {
                    this.classList.remove('touch-active');
                }, { passive: true });
            });

            // Prevenir zoom en doble tap en iOS
            if (isIOS) {
                let lastTouchEnd = 0;
                document.addEventListener('touchend', function(event) {
                    const now = Date.now();
                    if (now - lastTouchEnd <= 300) {
                        event.preventDefault();
                    }
                    lastTouchEnd = now;
                }, false);
            }

            // Scroll suave
            this.enableSmoothScroll();
        }

        enableSmoothScroll() {
            // Solo en enlaces internos
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        }
    }

    // ========================================
    // OPTIMIZACIÓN DE IMÁGENES
    // ========================================

    class LazyLoadImages {
        constructor() {
            this.images = document.querySelectorAll('img[data-src]');
            if (this.images.length > 0) {
                this.init();
            }
        }

        init() {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                            imageObserver.unobserve(img);
                        }
                    });
                });

                this.images.forEach(img => imageObserver.observe(img));
            } else {
                // Fallback: cargar todas las imágenes
                this.images.forEach(img => {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                });
            }
        }
    }

    // ========================================
    // DETECCIÓN DE ORIENTACIÓN
    // ========================================

    class OrientationHandler {
        constructor() {
            if (isMobile) {
                this.init();
            }
        }

        init() {
            window.addEventListener('orientationchange', () => {
                // Recargar ciertos componentes si es necesario
                this.handleOrientationChange();
            });
        }

        handleOrientationChange() {
            // Ajustar altura de mapas
            const maps = document.querySelectorAll('.leaflet-container');
            maps.forEach(map => {
                if (window.orientation === 90 || window.orientation === -90) {
                    // Landscape
                    map.style.height = '300px';
                } else {
                    // Portrait
                    map.style.height = '400px';
                }
            });

            // Refresh DataTables si existen
            if (typeof $.fn.DataTable !== 'undefined') {
                setTimeout(() => {
                    $.fn.DataTable.tables({ visible: true, api: true }).columns.adjust();
                }, 300);
            }
        }
    }

    // ========================================
    // OFFLINE DETECTION
    // ========================================

    class OfflineHandler {
        constructor() {
            this.init();
        }

        init() {
            window.addEventListener('online', () => {
                this.showNotification('Conexión restaurada', 'success');
            });

            window.addEventListener('offline', () => {
                this.showNotification('Sin conexión a Internet', 'warning');
            });
        }

        showNotification(message, type) {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    icon: type,
                    title: message,
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true
                });
            }
        }
    }

    // ========================================
    // PERFORMANCE MONITOR
    // ========================================

    class PerformanceMonitor {
        constructor() {
            if (isMobile && 'performance' in window) {
                this.init();
            }
        }

        init() {
            // Monitorear tiempo de carga
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = window.performance.timing;
                    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;

                    // Log solo si es muy lento (> 3 segundos)
                    if (pageLoadTime > 3000) {
                        console.warn(`⚠️ Página cargó lentamente: ${(pageLoadTime / 1000).toFixed(2)}s`);
                    }
                }, 0);
            });

            // Advertir si hay memoria baja
            if ('deviceMemory' in navigator && navigator.deviceMemory < 2) {
                console.info('ℹ️ Dispositivo con memoria limitada detectado');
            }
        }
    }

    // ========================================
    // UTILIDADES
    // ========================================

    const MobileUtils = {
        // Vibrar dispositivo (si está disponible)
        vibrate: (pattern = [100]) => {
            if ('vibrate' in navigator) {
                navigator.vibrate(pattern);
            }
        },

        // Copiar al portapapeles
        copyToClipboard: async (text) => {
            try {
                await navigator.clipboard.writeText(text);
                MobileUtils.showToast('Copiado al portapapeles', 'success');
                MobileUtils.vibrate([50]);
            } catch (err) {
                console.error('Error al copiar:', err);
            }
        },

        // Toast notification simple
        showToast: (message, type = 'info') => {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    icon: type,
                    title: message,
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2000,
                    timerProgressBar: true
                });
            }
        },

        // Detectar si está en pantalla completa
        isFullscreen: () => {
            return window.innerHeight === screen.height;
        },

        // Solicitar pantalla completa
        requestFullscreen: () => {
            const elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) {
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) {
                elem.msRequestFullscreen();
            }
        }
    };

    // ========================================
    // INICIALIZACIÓN
    // ========================================

    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar componentes
        new MobileSidebar();
        new ResponsiveTables();
        new MobileForms();
        new TouchEnhancements();
        new LazyLoadImages();
        new OrientationHandler();
        new OfflineHandler();
        new PerformanceMonitor();

        // Exponer utilidades globalmente
        window.MobileUtils = MobileUtils;
    });

    // ========================================
    // RESIZE HANDLER CON DEBOUNCE
    // ========================================

    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            // Refresh DataTables
            if (typeof $.fn.DataTable !== 'undefined') {
                $.fn.DataTable.tables({ visible: true, api: true }).columns.adjust();
            }

            // Ajustar mapas
            if (typeof L !== 'undefined') {
                document.querySelectorAll('.leaflet-container').forEach(container => {
                    if (container._leaflet_id) {
                        const map = L.map(container);
                        if (map) {
                            map.invalidateSize();
                        }
                    }
                });
            }
        }, 250);
    });

})();
