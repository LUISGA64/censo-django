/**
 * CENSO DJANGO - SELECTOR DE TEMAS
 * Permite cambiar entre diferentes paletas de colores
 */

(function() {
    'use strict';

    const THEMES = {
        empresarial: {
            name: 'Azul Corporativo (Actual)',
            css: '/static/assets/css/censo-theme.css',
            description: 'Tema empresarial con azul oscuro corporativo'
        },
        primefaces: {
            name: 'PrimeFaces Saga Blue',
            css: '/static/assets/css/censo-theme-primefaces.css',
            description: 'Tema Material Design inspirado en PrimeFaces'
        }
    };

    // Obtener tema actual
    function getCurrentTheme() {
        return localStorage.getItem('censo-theme') || 'empresarial';
    }

    // Guardar tema seleccionado
    function saveTheme(themeName) {
        localStorage.setItem('censo-theme', themeName);
    }

    // Aplicar tema
    function applyTheme(themeName) {
        const theme = THEMES[themeName];
        if (!theme) return;

        // Buscar el link del tema actual
        let themeLink = document.getElementById('censo-theme-link');

        if (!themeLink) {
            // Crear el link si no existe
            themeLink = document.createElement('link');
            themeLink.id = 'censo-theme-link';
            themeLink.rel = 'stylesheet';

            // Insertar después del soft-ui-dashboard.css
            const mainCss = document.getElementById('pagestyle');
            if (mainCss && mainCss.parentNode) {
                mainCss.parentNode.insertBefore(themeLink, mainCss.nextSibling);
            } else {
                document.head.appendChild(themeLink);
            }
        }

        // Cambiar el href
        themeLink.href = theme.css;

        // Guardar preferencia
        saveTheme(themeName);

        // Actualizar selector si existe
        updateThemeSelector(themeName);
    }

    // Actualizar selector visual
    function updateThemeSelector(themeName) {
        const selector = document.getElementById('theme-selector');
        if (selector) {
            selector.value = themeName;
        }
    }

    // Crear botón flotante de selección de tema
    function createThemeButton() {
        // Crear contenedor
        const container = document.createElement('div');
        container.id = 'theme-switcher-container';
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            padding: 16px;
            min-width: 300px;
        `;

        // Crear contenido
        container.innerHTML = `
            <div style="margin-bottom: 12px;">
                <h6 style="margin: 0 0 8px 0; font-weight: 600; color: #111827;">
                    <i class="fas fa-palette" style="margin-right: 8px;"></i>
                    Selector de Tema
                </h6>
                <p style="margin: 0; font-size: 0.875rem; color: #6B7280;">
                    Elige el tema que más te guste
                </p>
            </div>
            
            <select id="theme-selector" class="form-select form-select-sm" style="margin-bottom: 12px;">
                <option value="empresarial">Azul Corporativo (Actual)</option>
                <option value="primefaces">PrimeFaces Saga Blue</option>
            </select>
            
            <div style="display: flex; gap: 8px;">
                <button id="apply-theme-btn" class="btn btn-primary btn-sm" style="flex: 1;">
                    <i class="fas fa-check"></i> Aplicar
                </button>
                <button id="close-theme-btn" class="btn btn-secondary btn-sm">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div id="theme-description" style="margin-top: 12px; padding: 8px; background: #F3F4F6; border-radius: 4px; font-size: 0.8125rem; color: #374151;">
            </div>
        `;

        document.body.appendChild(container);

        // Event listeners
        const selector = document.getElementById('theme-selector');
        const applyBtn = document.getElementById('apply-theme-btn');
        const closeBtn = document.getElementById('close-theme-btn');
        const description = document.getElementById('theme-description');

        // Establecer tema actual
        selector.value = getCurrentTheme();
        updateDescription(getCurrentTheme());

        // Actualizar descripción al cambiar
        selector.addEventListener('change', function() {
            updateDescription(this.value);
        });

        // Aplicar tema
        applyBtn.addEventListener('click', function() {
            const selectedTheme = selector.value;
            applyTheme(selectedTheme);

            // Mostrar confirmación
            showNotification('Tema aplicado correctamente', 'success');
        });

        // Cerrar panel
        closeBtn.addEventListener('click', function() {
            container.style.display = 'none';
        });

        function updateDescription(themeName) {
            const theme = THEMES[themeName];
            if (theme && description) {
                description.textContent = theme.description;
            }
        }
    }

    // Crear botón para abrir el selector
    function createToggleButton() {
        const button = document.createElement('button');
        button.id = 'theme-toggle-btn';
        button.innerHTML = '<i class="fas fa-palette"></i>';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9998;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            border: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            font-size: 1.25rem;
            transition: all 0.3s ease;
        `;

        button.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 6px 16px rgba(0,0,0,0.4)';
        });

        button.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        });

        button.addEventListener('click', function() {
            const container = document.getElementById('theme-switcher-container');
            if (container) {
                container.style.display = container.style.display === 'none' ? 'block' : 'none';
            }
        });

        document.body.appendChild(button);
    }

    // Mostrar notificación
    function showNotification(message, type = 'info') {
        // Si SweetAlert2 está disponible
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                title: type === 'success' ? '¡Éxito!' : 'Información',
                text: message,
                icon: type,
                timer: 2000,
                showConfirmButton: false,
                toast: true,
                position: 'top-end'
            });
        } else {
            // Notificación simple
            const notification = document.createElement('div');
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? '#4CAF50' : '#2196F3'};
                color: white;
                padding: 16px 24px;
                border-radius: 4px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                z-index: 10000;
                animation: slideIn 0.3s ease;
            `;

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 2000);
        }
    }

    // Inicializar al cargar la página
    function init() {
        // Aplicar tema guardado
        const currentTheme = getCurrentTheme();
        applyTheme(currentTheme);

        // Crear controles después de que la página cargue
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                createThemeButton();
                createToggleButton();
            });
        } else {
            createThemeButton();
            createToggleButton();
        }
    }

    // Ejecutar
    init();

    // Exponer funciones globalmente
    window.CensoTheme = {
        apply: applyTheme,
        current: getCurrentTheme,
        themes: THEMES
    };

})();

