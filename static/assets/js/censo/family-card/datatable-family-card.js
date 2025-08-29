$(document).ready(function () {
    $('#familycard').DataTable({
        ajax: {
            url: FAMILYCARD_JSON_URL,
            type: "GET",
            dataSrc: "data"
        },
        serverSide: true,
        processing: true,
        order: [[0, "asc"]],
        columns: [
            {
                data: "family_card__family_card_number",
                name: "family_card_number",
                orderable: false,
                searchable: false,
                render: function (data, type, row) {
                    return `<span class="text-muted text-center d-block">${data}</span>`;
                }
            },

            {
                data: "null",
                name: "full_name",
                orderable: false,
                render: function (data, type, row) {
                    return `<div>
                                <span class="text-muted text-start d-block">${row.full_name}</span>
                                <span class="text-muted text-xs">${row.document_type__code_document_type} ${row.identification_person}</span>
                            </div>`;
                }
            },
            {
                data: "family_card__sidewalk_home__sidewalk_name",
                name: "sidewalk_home",
                orderable: false,
                searchable: false,
                render: function (data, type, row) {
                    return `<div class="text-left"><span class="badge bg-gradient-success text-xs">${data}</span></div>`
                }
            },
            {
                data: "person_count",
                name: "person_count",
                render: function (data, type, row) {
                    return `<div class="text-center"><span class="badge bg-info text-sm">${data}</span></div>`
                }
            },
            {
                data: null,
                name: "options",
                orderable: false,
                searchable: false,
                render: function (data, type, row) {
                    const editUrl = EDIT_FAMILY_CARD_URL.replace('0', row.family_card_id);
                    const viewCard = VIEW_FAMILY_CARD_URL.replace('0', row.family_card_id);
                    const newPerson = NEW_PERSON_FAMILY.replace('0', row.family_card_id);
                    const materialConst = MATERIAL_CONSTRUCTION.replace('0', row.family_card_id);
                    return `
                        <div class="btn-container text-center justify-content-center" role="group">
                            <a href="${editUrl}" class="text-muted text-bolder" title="Editar"><span class="btn-inner--icon"><i class="fa-solid fa-pen-to-square"></i></span></a>
                            <a href="${viewCard}" class="text-muted ms-3" title="Detalles"><span class="btn-inner--icon"><i class="fa-solid fa-binoculars"></i></span></a>
                            <a href="${newPerson}" class="text-muted ms-3"><span class="btn-inner--icon"><i class="fa-solid fa-user-plus"></i></span></a>
                            <a href="${materialConst}" class="text-muted ms-3" title="Material de construcción"><span class="btn-inner--icon"><i class="fa-solid fa-house"></i></span></a>
                        </div>`;
                }
            }
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4],
                width: "20%",
                target: "_all",
            }
        ],
        language: {
            url: DATATABLE_LANG_URL
        },
        responsive: true,
        pagingType: "full_numbers",
        lengthMenu: [5, 10, 25, 50],
        pageLength: 10,
        createdRow: function (row, data, dataIndex) {
            $(row).addClass('text-sm');
            $('td', row).addClass('text-start'); // Add this line to align text to the right
        }
    });
    detailCard = (id) => {
        window.location.href = "{% url 'detailFamilyCard' 0 %}".replace('0', id);
    }

    editRecord = (id) => {
        window.location.href = "{% url 'update-family' 0 %}".replace('0', id);
    }
    agregarPersona = (id) => {
        window.location.href = "{% url 'createPerson' 0 %}".replace('0', id);
    }

    materialConstruction = (id) => {
        window.location.href = "{% url 'materialConstruction' 0 %}".replace('0', id);
    }
});