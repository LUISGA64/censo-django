$(document).ready(function () {
    $('#person').DataTable({
        ajax: {
            url: PERSONAS_JSON_URL,
            type: "GET",
            dataSrc: "data"
        },
        serverSide: true,
        processing: true,
        columns: [
            {
                data: null,
                name: "first_name_1",
                render: function (data, type, row) {
                    const fullName = `${row.first_name_1} ${row.first_name_2} ${row.last_name_1} ${row.last_name_2}`.replace(/\s+/g, ' ').trim();
                    const badge = row.family_head
                        ? `<span class="badge bg-gradient-success ms-2" title="Family Head" aria-label="Family Head">Jefe de Familia</span>`
                        : '';
                    return `
                        <div>
                            <span class="text-muted text-secondary-emphasis">${fullName}</span>
                            <div class="text-xs text-secondary mb-0 mt-1">
                                ${row.document_type__code_document_type} - ${row.identification_person}
                                ${badge}
                            </div>
                        </div>`;
                }
            },
            {
                data: "date_birth",
                name: "date_birth",
                orderable: false,
                searchable: false,
                render: function (data, type, row) {
                    if (data) {
                        const date = new Date(data);
                        const day = String(date.getDate()).padStart(2, '0');
                        const month = String(date.getMonth() + 1).padStart(2, '0');
                        const year = date.getFullYear();
                        return `<span class="text-secondary text-center d-block">
                            <i class="fa-solid fa-calendar-days"></i>
                            ${day}/${month}/${year}
                        </span>`;
                    }
                    return '<span class="text-secondary text-center d-block"></span>';
                }
            },
            {
                data: "age",
                name: "age",
                searchable: false,
                orderable: false,
                render: function (data, type, row) {
                    if (data) {
                        return `<span class="text-secondary text-center d-block">${data} años</span>`;
                    }
                    return '<span class="text-secondary text-center d-block"></span>';
                }
            },
            {
                data: "gender",
                name: "gender",
                searchable: false,
                orderable: false,
                render: function (data, type, row) {
                    if (data) {
                        return `<span class="text-secondary text-center d-block">${data}</span>`;
                    }
                    return '<span class="text-secondary text-center d-block"></span>';
                }
            },
            {
                data: "family_card__family_card_number",
                name: "family_card__family_card_number",
                searchable: false,
                orderable: false,
                render: function (data, type, row) {
                    if (data && row.family_card) {
                        return `<div class="d-flex justify-content-center">
                                    <a href="/familyCard/detail/${row.family_card}/" class="badge bg-info text-white text-center" style="color: #0d6efd">
                                    <span class="letter-spacing-1"> Ficha # </span> ${data}</a>
                                </div>`;
                    }
                    return '<span class="text-secondary text-center d-block"></span>';
                }
            },
            {
                data: null,
                name: "options",
                orderable: false,
                searchable: false,
                render: function (data, type, row) {
                    const editUrl = UPDATED_PERSON_URL.replace('0', row.id);
                    const detailPerson = DETAIL_PERSON_URL.replace('0', row.id);
                    return `
                        <div class="action-icons d-flex justify-content-center align-items-center">
                            <a href="${editUrl}" title="Editar" class="text-secondary"><i class="fa-solid fa-pen-to-square"></i></a>
                            <a href="${detailPerson}" title="Detalles" class="text-secondary ms-3"><i class="fa-solid fa-binoculars"></i></a>
                        </div>`;
                }
            }
        ],
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4],
                width: "30%",
                target: "_all",
            }
        ],
        language: {
            url: DATATABLE_LANG_URL // Define esta variable en tu HTML
        },
        responsive: true,
        pagingType: "full_numbers",
        lengthMenu: [5, 7, 25, 50],
        pageLength: 7,
        createdRow: function (row, data, dataIndex) {
            $(row).addClass('text-sm');
            $('td', row).addClass('text-sm-start');
        }
    });
});