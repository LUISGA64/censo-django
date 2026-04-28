$(document).ready(function () {
    // Mostrar spinner al inicio
    $('#loadingSpinner').addClass('active');

    const table = $('#familycard').DataTable({
        ajax: {
            url: FAMILYCARD_JSON_URL,
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
        order: [[0, "asc"]],
        columns: [
            {
                data: "family_card__family_card_number",
                name: "family_card_number",
                className: "text-center",
                render: function (data, type, row) {
                    if (!data) {
                        return '<span class="text-muted">-</span>';
                    }

                    if (type === 'sort' || type === 'type') {
                        return data;
                    }

                    return `
                        <span class="badge badge-ficha" 
                              title="Número de ficha familiar"
                              aria-label="Ficha número ${data}">
                            <i class="fas fa-home me-1"></i>
                            #${data}
                        </span>`;
                }
            },
            {
                data: null,
                name: "full_name",
                render: function (data, type, row) {
                    const fullName = row.full_name || 'Sin nombre';
                    const docType = row.document_type__code_document_type || '';
                    const docNumber = row.identification_person || '';

                    return `
                        <div class="d-flex flex-column">
                            <span class="text-dark fw-bold" style="font-size: 0.95rem;">
                                ${fullName}
                            </span>
                            <div class="text-xs text-muted mt-1">
                                <i class="fas fa-id-card me-1"></i>
                                <span class="text-uppercase">${docType}</span> ${docNumber}
                            </div>
                        </div>`;
                }
            },
            {
                data: "family_card__sidewalk_home__sidewalk_name",
                name: "sidewalk_home",
                className: "text-start",
                render: function (data, type, row) {
                    if (!data) {
                        return '<span class="text-muted">Sin asignar</span>';
                    }

                    const zone = row.family_card__zone || '';
                    const zoneText = zone === 'U' ? 'Urbano' : 'Rural';

                    return `
                        <div class="d-flex flex-column">
                            <span class="text-dark fw-medium" style="font-size: 0.9rem;">
                                ${data}
                            </span>
                            <span class="text-xs vereda-info mt-1">
                                <i class="fas fa-${zone === 'U' ? 'city' : 'tree'} me-1"></i>
                                ${zoneText}
                            </span>
                        </div>`;
                }
            },
            {
                data: "person_count",
                name: "person_count",
                className: "text-center",
                render: function (data, type, row) {
                    if (!data && data !== 0) {
                        return '<span class="text-muted">0</span>';
                    }

                    return `
                        <span class="badge badge-members"
                              title="${data} miembro(s) en la familia">
                            <i class="fas fa-users me-1"></i>
                            ${data}
                        </span>`;
                }
            },
            {
                data: null,
                name: "options",
                orderable: false,
                searchable: false,
                className: "text-center",
                render: function (data, type, row) {
                    const editUrl = EDIT_FAMILY_CARD_URL.replace('0', row.family_card_id);
                    const viewCard = VIEW_FAMILY_CARD_URL.replace('0', row.family_card_id);
                    const newPerson = NEW_PERSON_FAMILY.replace('0', row.family_card_id);
                    const materialConst = MATERIAL_CONSTRUCTION.replace('0', row.family_card_id);
                    const fichaNum = row.family_card__family_card_number;

                    // Verificar si el usuario es VIEWER (solo lectura)
                    const isViewer = typeof USER_ROLE !== 'undefined' && USER_ROLE === 'VIEWER';
                    const isSuperUser = typeof IS_SUPERUSER !== 'undefined' && IS_SUPERUSER;
                    const canEdit = isSuperUser || !isViewer;

                    return `
                        <div class="dropdown dropdown-actions">
                            <button class="btn btn-actions dropdown-toggle" 
                                    type="button" 
                                    id="dropdownActions${row.family_card_id}" 
                                    data-bs-toggle="dropdown" 
                                    aria-expanded="false"
                                    aria-label="Acciones para ficha ${fichaNum}">
                                <i class="fas fa-cog"></i>
                                <span class="btn-text">Acciones</span>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" 
                                aria-labelledby="dropdownActions${row.family_card_id}">
                                <li>
                                    <a class="dropdown-item" href="${viewCard}">
                                        <i class="fas fa-eye text-primary"></i>
                                        <span>Ver Detalle</span>
                                    </a>
                                </li>
                                ${canEdit ? `
                                <li>
                                    <a class="dropdown-item" href="${editUrl}">
                                        <i class="fas fa-edit text-warning"></i>
                                        <span>Editar Ficha</span>
                                    </a>
                                </li>
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <a class="dropdown-item" href="${newPerson}">
                                        <i class="fas fa-user-plus text-success"></i>
                                        <span>Agregar Miembro</span>
                                    </a>
                                </li>
                                <li>
                                    <a class="dropdown-item" href="${materialConst}">
                                        <i class="fas fa-home text-info"></i>
                                        <span>Datos de Vivienda</span>
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
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        pageLength: 10,
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
});

