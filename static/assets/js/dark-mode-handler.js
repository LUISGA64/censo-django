const themeSwitch = document.getElementById("theme-switch");
const themeIndicator = document.getElementById("theme-indicator");
const themeButton = document.getElementById("theme-toggle-btn");
const page = document.body;

const themeStates = ["light", "dark"];
const indicators = ["fa-sun", "fa-moon"];
const pageClass = ["bg-gray-100", "dark-page"];

let currentTheme = localStorage.getItem("theme");

function setTheme(theme) {
    localStorage.setItem("theme", themeStates[theme]);
}

function setIndicator(theme) {
    themeIndicator.classList.remove(indicators[0]);
    themeIndicator.classList.remove(indicators[1]);
    themeIndicator.classList.add(indicators[theme]);
}

function setPage(theme) {
    page.classList.remove(pageClass[0]);
    page.classList.remove(pageClass[1]);
    page.classList.add(pageClass[theme]);

    // Agregar clase dark-mode al body para CSS
    if (theme === 1) {
        page.classList.add('dark-mode');
    } else {
        page.classList.remove('dark-mode');
    }
}

function applyTheme(theme) {
    setTheme(theme);
    setIndicator(theme);
    setPage(theme);

    // Actualizar el título del botón para accesibilidad
    if (themeButton) {
        const nextTheme = theme === 0 ? 'oscuro' : 'claro';
        themeButton.setAttribute('title', 'Cambiar a tema ' + nextTheme);
    }
}

// Inicialización
if (currentTheme === null || currentTheme === themeStates[0]) {
    applyTheme(0);
    if (themeSwitch) themeSwitch.checked = true;
}

if (currentTheme === themeStates[1]) {
    applyTheme(1);
    if (themeSwitch) themeSwitch.checked = false;
}

// Event listener para el checkbox oculto
if (themeSwitch) {
    themeSwitch.addEventListener('change', function () {
        if (this.checked) {
            applyTheme(0);
        } else {
            applyTheme(1);
        }
    });
}

// Event listener para el botón visible
if (themeButton) {
    themeButton.addEventListener('click', function(e) {
        e.preventDefault();

        // Toggle del checkbox
        if (themeSwitch) {
            themeSwitch.checked = !themeSwitch.checked;
            themeSwitch.dispatchEvent(new Event('change'));
        }

        // Efecto visual de click
        this.style.transform = 'scale(0.95)';
        setTimeout(function() {
            themeButton.style.transform = '';
        }, 100);
    });
}

// Detectar preferencia del sistema (opcional)
if (window.matchMedia && !localStorage.getItem("theme")) {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
        applyTheme(1);
        if (themeSwitch) themeSwitch.checked = false;
    }
}

