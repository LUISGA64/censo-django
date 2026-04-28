$(document).ready(function () {
    // Mostrar spinner al inicio
    $('#loadingSpinner').addClass('active');

    const table = $('#person').DataTable({
        ajax: {
            url: PERSONAS_JSON_URL,
            type: "GET",
            dataSrc: "data",
            error: function(xhr, error, code) {
                console.error('Error al cargar datos:', error);
                $('#loadingSpinner').removeClass('active');
                showNotification('Error al cargar los datos. Por favor, intente nuevamente.', 'error');
            }
        },
        serverSide: true,
        processing: true,
        deferRender: true,
        columns: [
            {
                data: null,
                name: "first_name_1",
                render: function (data, type, row) {
                    // Construir nombre completo limpiando espacios
                    const firstName1 = row.first_name_1 || '';
                    const firstName2 = row.first_name_2 || '';
                    const lastName1 = row.last_name_1 || '';
                    const lastName2 = row.last_name_2 || '';

                    const fullName = `${firstName1} ${firstName2} ${lastName1} ${lastName2}`
                        .replace(/\s+/g, ' ')
                        .trim();

                    const badge = row.family_head
                        ? `<span class="badge badge-family-head ms-2" 
                                  title="Jefe de Familia" 
                                  aria-label="Jefe de Familia">
                                <i class="fas fa-crown" style="font-size: 0.65rem;"></i> Jefe
                           </span>`
                        : '';

                    return `
                        <div class="d-flex flex-column">
                            <span class="text-dark fw-bold" style="font-size: 0.95rem;">${fullName} ${badge}</span>
                            <div class="text-xs text-muted mt-1">
                                <i class="fas fa-id-card me-1"></i>
                                <span class="text-uppercase">${row.document_type__code_document_type}</span> 
                                ${row.identification_person}
                            </div>
                        </div>`;
                }
            },
            {
                data: "date_birth",
                name: "date_birth",
                className: "text-center",
                render: function (data, type, row) {
                    if (!data) {
                        return '<span class="text-muted">-</span>';
                    }

                    if (type === 'sort' || type === 'type') {
                        return data;
                    }

                    const date = new Date(data);
                    const day = String(date.getDate()).padStart(2, '0');
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    const year = date.getFullYear();

                    return `
                        <span class="text-secondary" style="font-size: 0.9rem;">
                            ${day}/${month}/${year}
                        </span>`;
                }
            },
            {
                data: "age",
                name: "age",
                className: "text-center",
                render: function (data, type, row) {
                    if (!data && data !== 0) {
                        return '<span class="text-muted">-</span>';
                    }

                    return `
                        <span class="badge badge-age">
                            ${data} años
                        </span>`;
                }
            },
            {
                data: "gender",
                name: "gender",
                className: "text-center",
                render: function (data, type, row) {
                    if (!data) {
                        return '<span class="text-muted">-</span>';
                    }

                    const icon = data === 'Femenino' ?
                        '<i class="fas fa-venus me-1"></i>' :
                        '<i class="fas fa-mars me-1"></i>';

                    return `
                        <span class="text-secondary" style="font-size: 0.9rem;">
                            ${icon} ${data}
                        </span>`;
                }
            },
            {
                data: "family_card__family_card_number",
                name: "family_card__family_card_number",
                className: "text-center",
                render: function (data, type, row) {
                    if (!data || !row.family_card) {
                        return '<span class="text-muted">Sin asignar</span>';
                    }

                    return `
                        <a href="/familyCard/detail/${row.family_card}/" 
                           class="badge badge-ficha-link"
                           title="Ver detalles de la ficha familiar"
                           aria-label="Ver ficha familiar ${data}">
                            <i class="fas fa-home me-1"></i>
                            #${data}
                        </a>`;
                }
            },
            {
                data: null,
                name: "options",
                orderable: false,
                searchable: false,
                className: "text-center",
                render: function (data, type, row) {
                    const editUrl = UPDATED_PERSON_URL.replace('0', row.id);
                    const detailUrl = DETAIL_PERSON_URL.replace('0', row.id);
                    const personName = `${row.first_name_1} ${row.last_name_1}`.trim();

                    // Verificar si el usuario es VIEWER (solo lectura)
                    const isViewer = typeof USER_ROLE !== 'undefined' && USER_ROLE === 'VIEWER';
                    const isSuperUser = typeof IS_SUPERUSER !== 'undefined' && IS_SUPERUSER;
                    const canEdit = isSuperUser || !isViewer;

                    return `
                        <div class="dropdown dropdown-actions">
                            <button class="btn btn-actions dropdown-toggle" 
                                    type="button" 
                                    id="dropdownActions${row.id}" 
                                    data-bs-toggle="dropdown" 
                                    aria-expanded="false"
                                    aria-label="Acciones para ${personName}">
                                <i class="fas fa-cog"></i>
                                <span class="btn-text">Acciones</span>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" 
                                aria-labelledby="dropdownActions${row.id}">
                                <li>
                                    <a class="dropdown-item" href="${detailUrl}">
                                        <i class="fas fa-eye text-primary"></i>
                                        <span>Ver Detalle</span>
                                    </a>
                                </li>
                                ${canEdit ? `
                                <li>
                                    <a class="dropdown-item" href="${editUrl}">
                                        <i class="fas fa-edit text-warning"></i>
                                        <span>Editar Persona</span>
                                    </a>
                                </li>
                                ` : ''}
                            </ul>
                        </div>`;
                }
            }
        ],
        language: {
            url: DATATABLE_LANG_URL,
            processing: '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>'
        },
        responsive: true,
        pagingType: "full_numbers",
        lengthMenu: [[7, 10, 25, 50, 100], [7, 10, 25, 50, 100]],
        pageLength: 10,
        order: [[0, 'asc']],
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rt<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
        createdRow: function (row, data, dataIndex) {
            $(row).addClass('text-sm align-middle');
            $('td', row).addClass('py-3');
        },
        initComplete: function() {
            $('#loadingSpinner').removeClass('active');
        },
        drawCallback: function() {
            // Destruir tooltips existentes antes de recrear
            $('[data-bs-toggle="tooltip"]').each(function() {
                if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
                    const tooltip = bootstrap.Tooltip.getInstance(this);
                    if (tooltip) {
                        tooltip.dispose();
                    }
                }
            });

            // Inicializar nuevos tooltips
            if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
                const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
                tooltipTriggerList.forEach(function(tooltipTriggerEl) {
                    new bootstrap.Tooltip(tooltipTriggerEl);
                });
            }

            // Inicializar dropdowns de Bootstrap manualmente
            const dropdownElementList = document.querySelectorAll('.dropdown-actions [data-bs-toggle="dropdown"]');

            // Verificar si Bootstrap está disponible
            if (typeof bootstrap !== 'undefined' && bootstrap.Dropdown) {
                dropdownElementList.forEach(function(dropdownToggleEl) {
                    // Destruir instancia previa si existe
                    const existingDropdown = bootstrap.Dropdown.getInstance(dropdownToggleEl);
                    if (existingDropdown) {
                        existingDropdown.dispose();
                    }

                    // Crear nueva instancia con opciones explícitas
                    new bootstrap.Dropdown(dropdownToggleEl, {
                        boundary: 'viewport',
                        reference: 'toggle',
                        autoClose: true
                    });

                    // BACKUP: Event listener manual por si Bootstrap no funciona
                    dropdownToggleEl.addEventListener('click', function(e) {
                        const menu = this.nextElementSibling;
                        if (menu) {
                            // Forzar toggle manual si Bootstrap no responde
                            setTimeout(() => {
                                if (!menu.classList.contains('show')) {
                                    menu.classList.add('show');
                                    menu.style.position = 'absolute';
                                    menu.style.inset = '0px 0px auto auto';
                                    menu.style.margin = '0px';
                                    menu.style.transform = 'translate(0px, 34px)';
                                }
                            }, 50);
                        }
                    });
                });
            } else {
                // Fallback: event listeners manuales
                dropdownElementList.forEach(function(dropdownToggleEl) {
                    const newElement = dropdownToggleEl.cloneNode(true);
                    dropdownToggleEl.parentNode.replaceChild(newElement, dropdownToggleEl);

                    newElement.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();

                        // Cerrar otros dropdowns
                        document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
                            menu.classList.remove('show');
                        });

                        // Toggle del menú actual
                        const menu = this.nextElementSibling;
                        if (menu && menu.classList.contains('dropdown-menu')) {
                            menu.classList.toggle('show');
                        }
                    });
                });
            }
        }
    });

    // Función auxiliar para notificaciones (definida en el template)
    function showNotification(message, type = 'info') {
        const alertClass = type === 'success' ? 'alert-success' :
                         type === 'error' ? 'alert-danger' : 'alert-info';

        const alert = `
            <div class="alert ${alertClass} alert-dismissible fade show position-fixed top-0 end-0 m-3" 
                 role="alert" style="z-index: 10000;">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        $('body').append(alert);
        setTimeout(() => {
            $('.alert').alert('close');
        }, 4000);
    }

    // Hacer la función global para uso en otros scripts
    window.showNotification = showNotification;

    // ========================================
    // GESTIÓN DE DROPDOWNS (FALLBACK)
    // ========================================

    // Cerrar dropdowns cuando se hace clic fuera
    $(document).on('click', function(e) {
        // Si el click no es en un dropdown-toggle o dropdown-menu
        if (!$(e.target).closest('.dropdown-actions').length) {
            $('.dropdown-menu.show').removeClass('show');
        }
    });

    // Prevenir que el dropdown se cierre al hacer clic dentro del menú
    $(document).on('click', '.dropdown-menu', function(e) {
        e.stopPropagation();
    });

    // Cerrar dropdown al hacer clic en un item del menú
    $(document).on('click', '.dropdown-item', function() {
        $(this).closest('.dropdown-menu').removeClass('show');
    });

    // ========================================
    // FILTROS DE PERSONAS
    // ========================================

    let currentFilter = 'all';

    // Filtro personalizado para DataTables
    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            // Solo aplicar al datatable de personas
            if (settings.nTable.id !== 'person') {
                return true;
            }

            // Si el filtro es 'all', mostrar todos
            if (currentFilter === 'all') {
                return true;
            }

            // Si el filtro es 'heads', solo mostrar jefes de familia
            if (currentFilter === 'heads') {
                const rowData = table.row(dataIndex).data();
                return rowData && rowData.family_head === true;
            }

            return true;
        }
    );

    // Botón "Todos"
    $('#filterAll').on('click', function() {
        currentFilter = 'all';
        updateFilterButtons(this);
        table.draw();

        const totalRows = table.rows().count();
        showNotification(`Mostrando todas las personas (${totalRows} registros)`, 'info');
    });

    // Botón "Solo Jefes"
    $('#filterHeads').on('click', function() {
        currentFilter = 'heads';
        updateFilterButtons(this);
        table.draw();

        // Contar cuántos jefes hay después del filtro
        setTimeout(() => {
            const filteredRows = table.rows({search: 'applied'}).count();
            showNotification(`Mostrando solo jefes de familia (${filteredRows} registros)`, 'success');
        }, 100);
    });

    // Función para actualizar estado de botones
    function updateFilterButtons(activeBtn) {
        $('.btn-group button').removeClass('active');
        $(activeBtn).addClass('active');
    }
});