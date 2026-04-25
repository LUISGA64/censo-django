/**
 * CensoWeb - Búsqueda Global
 * Sistema de búsqueda global con autocompletado
 */

(function() {
    'use strict';

    let searchTimeout;
    let currentRequest = null;

    // Elementos del DOM
    const searchInput = document.getElementById('globalSearchInput');
    const searchResults = document.getElementById('globalSearchResults');

    if (!searchInput || !searchResults) {
        console.warn('Elementos de búsqueda global no encontrados en el DOM');
        return;
    }

    /**
     * Inicializar búsqueda global
     */
    function initGlobalSearch() {
        // Event listener para input
        searchInput.addEventListener('input', handleSearchInput);

        // Event listener para teclas (Escape, Enter)
        searchInput.addEventListener('keydown', handleKeyDown);

        // Cerrar resultados al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.global-search-container')) {
                hideResults();
            }
        });

        // Focus en input con Ctrl+K o Cmd+K
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    /**
     * Manejar entrada de búsqueda
     */
    function handleSearchInput(e) {
        const query = e.target.value.trim();

        // Cancelar búsqueda anterior
        clearTimeout(searchTimeout);

        // Cancelar request anterior si existe
        if (currentRequest) {
            currentRequest.abort();
        }

        // Si query es muy corto, ocultar resultados
        if (query.length < 3) {
            hideResults();
            return;
        }

        // Mostrar loading
        showLoading();

        // Debounce - esperar 300ms antes de buscar
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    }

    /**
     * Obtener CSRF token de las cookies
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Realizar búsqueda
     */
    function performSearch(query) {
        console.log('Buscando:', query); // Debug

        const controller = new AbortController();
        currentRequest = controller;

        const csrftoken = getCookie('csrftoken');

        fetch(`/api/search/?q=${encodeURIComponent(query)}`, {
            method: 'GET',
            signal: controller.signal,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            credentials: 'same-origin'
        })
        .then(response => {
            console.log('Response status:', response.status); // Debug
            if (!response.ok) {
                throw new Error('Error en la búsqueda');
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data); // Debug
            renderResults(data);
            currentRequest = null;
        })
        .catch(error => {
            if (error.name === 'AbortError') {
                // Request cancelado, ignorar
                return;
            }
            showError('Error al realizar la búsqueda. Intente nuevamente.');
            currentRequest = null;
        });
    }

    /**
     * Renderizar resultados
     */
    function renderResults(data) {
        if (data.error) {
            showError(data.error);
            return;
        }

        if (data.total === 0) {
            showNoResults(data.query);
            return;
        }

        let html = '';

        // Resultados de Personas
        if (data.personas && data.personas.length > 0) {
            html += `
                <div class="search-category">
                    <div class="search-category-header">
                        <i class="fas fa-user"></i>
                        <span>Personas</span>
                        <span class="badge bg-primary">${data.personas.length}</span>
                    </div>
                </div>
            `;

            data.personas.forEach(persona => {
                html += `
                    <a href="${persona.url}" class="search-result-item" onclick="window.location.href='${persona.url}'; return true;">
                        <div class="search-item-icon">
                            <i class="fas fa-user-circle"></i>
                        </div>
                        <div class="search-item-content">
                            <div class="search-item-title">${highlightMatch(persona.name, data.query)}</div>
                            <div class="search-item-meta">
                                <span class="badge badge-sm bg-secondary">${persona.document_type}</span>
                                <span>${highlightMatch(persona.identification, data.query)}</span>
                                ${persona.family_card_number ? `<span>Ficha #${persona.family_card_number}</span>` : ''}
                            </div>
                        </div>
                    </a>
                `;
            });
        }

        // Resultados de Fichas Familiares
        if (data.fichas && data.fichas.length > 0) {
            html += `
                <div class="search-category">
                    <div class="search-category-header">
                        <i class="fas fa-home"></i>
                        <span>Fichas Familiares</span>
                        <span class="badge bg-success">${data.fichas.length}</span>
                    </div>
                </div>
            `;

            data.fichas.forEach(ficha => {
                html += `
                    <a href="${ficha.url}" class="search-result-item">
                        <div class="search-item-icon">
                            <i class="fas fa-house-user"></i>
                        </div>
                        <div class="search-item-content">
                            <div class="search-item-title">Ficha #${highlightMatch(String(ficha.number), data.query)}</div>
                            <div class="search-item-meta">
                                <span>${highlightMatch(ficha.address, data.query)}</span>
                                ${ficha.sidewalk ? `<span>• ${ficha.sidewalk}</span>` : ''}
                                <span>• ${ficha.members_count} integrante(s)</span>
                            </div>
                        </div>
                    </a>
                `;
            });
        }

        // Resultados de Documentos
        if (data.documentos && data.documentos.length > 0) {
            html += `
                <div class="search-category">
                    <div class="search-category-header">
                        <i class="fas fa-file-alt"></i>
                        <span>Documentos</span>
                        <span class="badge bg-info">${data.documentos.length}</span>
                    </div>
                </div>
            `;

            data.documentos.forEach(doc => {
                const statusClass = doc.is_expired ? 'bg-danger' : 'bg-success';
                const statusText = doc.is_expired ? 'Vencido' : 'Vigente';

                html += `
                    <a href="${doc.url}" class="search-result-item" onclick="window.location.href='${doc.url}'; return true;">
                        <div class="search-item-icon">
                            <i class="fas fa-file-pdf"></i>
                        </div>
                        <div class="search-item-content">
                            <div class="search-item-title">${highlightMatch(doc.number, data.query)}</div>
                            <div class="search-item-meta">
                                <span>${highlightMatch(doc.person_name, data.query)}</span>
                                <span class="badge badge-sm ${statusClass}">${statusText}</span>
                            </div>
                        </div>
                    </a>
                `;
            });
        }

        // Footer con total de resultados
        html += `
            <div class="search-footer">
                Se encontraron ${data.total} resultado(s) para "<strong>${escapeHtml(data.query)}</strong>"
            </div>
        `;

        searchResults.innerHTML = html;
        showResults();
    }

    /**
     * Resaltar coincidencias en el texto
     */
    function highlightMatch(text, query) {
        if (!text || !query) return text;

        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    /**
     * Escapar HTML
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Escapar regex
     */
    function escapeRegex(text) {
        return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * Mostrar loading
     */
    function showLoading() {
        searchResults.innerHTML = `
            <div class="search-loading">
                <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Buscando...</span>
                </div>
                <span>Buscando...</span>
            </div>
        `;
        showResults();
    }

    /**
     * Mostrar error
     */
    function showError(message) {
        searchResults.innerHTML = `
            <div class="search-error">
                <i class="fas fa-exclamation-circle"></i>
                <span>${escapeHtml(message)}</span>
            </div>
        `;
        showResults();
    }

    /**
     * Mostrar "sin resultados"
     */
    function showNoResults(query) {
        searchResults.innerHTML = `
            <div class="search-no-results">
                <i class="fas fa-search"></i>
                <p>No se encontraron resultados para "<strong>${escapeHtml(query)}</strong>"</p>
                <small>Intenta con otros términos de búsqueda</small>
            </div>
        `;
        showResults();
    }

    /**
     * Mostrar resultados
     */
    function showResults() {
        searchResults.style.display = 'block';
        searchResults.classList.add('show');
    }

    /**
     * Ocultar resultados
     */
    function hideResults() {
        searchResults.style.display = 'none';
        searchResults.classList.remove('show');
    }

    /**
     * Manejar teclas especiales
     */
    function handleKeyDown(e) {
        // Escape - cerrar resultados
        if (e.key === 'Escape') {
            hideResults();
            searchInput.blur();
        }

        // Enter - ir al primer resultado
        if (e.key === 'Enter') {
            const firstResult = searchResults.querySelector('.search-result-item');
            if (firstResult) {
                window.location.href = firstResult.getAttribute('href');
            }
        }
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initGlobalSearch);
    } else {
        initGlobalSearch();
    }

})();
