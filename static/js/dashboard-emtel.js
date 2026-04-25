// ============================================
// CENSO WEB - DASHBOARD ESTILO EMTEL
// Inicialización de Componentes y Utilidades
// Versión: 3.0
// Fecha: 2026-02-27
// ============================================

document.addEventListener('DOMContentLoaded', function() {

    // ============================================
    // INICIALIZAR TOOLTIPS DE BOOTSTRAP
    // ============================================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            html: true,
            placement: 'top',
            trigger: 'hover',
            container: 'body',
            customClass: 'custom-tooltip'
        });
    });

    // ============================================
    // FORMATEAR NÚMEROS CON SEPARADOR DE MILES
    // ============================================
    document.querySelectorAll('.format-number').forEach(function(el) {
        const num = parseFloat(el.textContent.replace(/,/g, ''));
        if (!isNaN(num)) {
            el.textContent = num.toLocaleString('es-CO');
        }
    });

    // ============================================
    // ANIMACIÓN DE CONTADORES
    // ============================================
    const animateValue = (element, start, end, duration) => {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value.toLocaleString('es-CO');
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };

    // Aplicar animación a elementos con clase .counter
    document.querySelectorAll('.counter').forEach(function(counter) {
        const target = parseInt(counter.getAttribute('data-target'));
        if (!isNaN(target)) {
            animateValue(counter, 0, target, 1500);
        }
    });

    // ============================================
    // VALIDACIÓN DE FECHAS EN FILTROS
    // ============================================
    const fechaInicio = document.getElementById('fecha_inicio');
    const fechaFinal = document.getElementById('fecha_final');

    if (fechaInicio && fechaFinal) {
        fechaInicio.addEventListener('change', function() {
            if (fechaFinal.value && new Date(this.value) > new Date(fechaFinal.value)) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Fecha Inválida',
                    text: 'La fecha inicial no puede ser mayor a la fecha final',
                    confirmButtonColor: '#2196F3'
                });
                this.value = '';
            }
        });

        fechaFinal.addEventListener('change', function() {
            if (fechaInicio.value && new Date(fechaInicio.value) > new Date(this.value)) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Fecha Inválida',
                    text: 'La fecha final no puede ser menor a la fecha inicial',
                    confirmButtonColor: '#2196F3'
                });
                this.value = '';
            }
        });
    }

    // ============================================
    // LAZY LOADING DE IMÁGENES
    // ============================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
    }

    // ============================================
    // SMOOTH SCROLL PARA ANCLAS
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

    // ============================================
    // INDICADOR DE CARGA PARA FORMULARIOS
    // ============================================
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('no-loading')) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';

                // Restaurar después de 30 segundos (safety)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 30000);
            }
        });
    });

    // ============================================
    // COPIAR AL PORTAPAPELES
    // ============================================
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                Swal.fire({
                    icon: 'success',
                    title: 'Copiado',
                    text: 'Texto copiado al portapapeles',
                    timer: 2000,
                    showConfirmButton: false
                });
            });
        });
    });

    console.log('✅ Dashboard EMTEL Style inicializado correctamente');
});

// ============================================
// FUNCIÓN PARA ACTUALIZAR GRÁFICOS
// ============================================
function updateChart(chartInstance, newLabels, newData) {
    if (chartInstance) {
        chartInstance.data.labels = newLabels;
        chartInstance.data.datasets[0].data = newData;
        chartInstance.update('active');
    }
}

// ============================================
// FUNCIÓN PARA RECARGAR DATOS VÍA AJAX
// ============================================
function refreshDashboardData(url, callback) {
    fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (callback && typeof callback === 'function') {
            callback(data);
        }
    })
    .catch(error => {
        console.error('Error al actualizar datos:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudieron actualizar los datos del dashboard',
            confirmButtonColor: '#2196F3'
        });
    });
}

// ============================================
// UTILIDADES DE FORMATO
// ============================================
const FormatUtils = {
    // Formatear número con separador de miles
    formatNumber: (num) => {
        return num.toLocaleString('es-CO');
    },

    // Formatear moneda
    formatCurrency: (num) => {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0
        }).format(num);
    },

    // Formatear porcentaje
    formatPercent: (num) => {
        return `${num.toFixed(1)}%`;
    },

    // Formatear fecha
    formatDate: (date) => {
        return new Date(date).toLocaleDateString('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
};

// Exportar para uso global
window.DashboardUtils = {
    updateChart,
    refreshDashboardData,
    FormatUtils
};

console.log('📊 Dashboard EMTEL Utils cargados');

