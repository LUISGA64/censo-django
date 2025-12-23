from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib.auth.decorators import login_required

from .models import MaterialConstruction
from .viewsets import SidewalksViewSet, AssociationViewSet, OrganizationViewSet
from .views import (home, profile, association, CreateAssociation, family_card_index,
                    crear_persona, detalle_ficha, UpdateFamily, get_family_cards, create_family_card,
                    listar_personas, view_persons, UpdatePerson, person_by_gender, DetailPersona, update_family_head,
                    delete_person_familyCard, get_system_parameters, MaterialConstructionView, export_persons_excel,
                    organization_detail, global_search, global_search_api,
                    importacion_masiva_inicio, descargar_template_importacion, validar_archivo_importacion,
                    confirmar_importacion, ver_log_importacion, descargar_log_importacion)
from .document_views import (view_document, list_person_documents, download_document_pdf,
                            organization_documents_stats, preview_document_pdf, verify_document)
from .simple_document_views import (select_document_type, generate_aval_general, generate_aval_estudio,
                                   generate_constancia_pertenencia)


urlpatterns = [
    path('', login_required(home), name='home'),
    # path('dashboard/', login_required(dashboard), name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', login_required(CreateAssociation.as_view()), name='createAssociation'),

    # Organizaciones
    path('organizacion/<int:pk>/', login_required(organization_detail), name='organization-detail'),

    # ----- FICHAS FAMILIARES -----
    path('familyCard/create', login_required(create_family_card), name='createFamilyCard'),
    path('familyCard/index', login_required(family_card_index), name='familyCardIndex'),
    path('familyCard/detail/<int:pk>/', login_required(detalle_ficha), name='detailFamilyCard'),
    path('update-family/<int:pk>', login_required(UpdateFamily.as_view()), name='update-family'),

    # Materiales de construcción
    path('material-construction/<int:pk>', login_required(MaterialConstructionView.as_view()), name='material-construction'),

    # ----- PERSONAS -----
    path('personas', login_required(view_persons), name='personas'),
    path('person/create/<int:pk>', login_required(crear_persona), name='createPerson'),
    path('edit-person/<int:pk>', login_required(UpdatePerson.as_view()), name='updated-person'),
    path('personas/detail/<int:pk>', login_required(DetailPersona.as_view()), name='detail-person'),


    # Editar el cabeza de familia
    path('personas/edit-head/<int:family>/<int:person>', login_required(update_family_head), name='edit-head-person'),
    path('update-family-head/<int:family>/<int:person>/', login_required(update_family_head), name='update-family-head'),

    # Desvincular persona de la familia
    path('persona/delete/<int:person>/', login_required(delete_person_familyCard), name='unlink-person-family'),
    path('delete-person-family/<int:person>/', login_required(delete_person_familyCard), name='delete-person-family'),

    # ----- JSON API  ----
    path('json_familycards', login_required(get_family_cards), name='familycards'),
    path('json_personas/', login_required(listar_personas), name='json_personas'),
    path('json_person_gender/', login_required(person_by_gender), name='persons-gender'),

    # Parámetros del aplicativo
    path('api-params/', login_required(get_system_parameters), name='system-parameters'),

    # ----- EXPORTACIONES -----
    path('export/personas/excel/', login_required(export_persons_excel), name='export-persons-excel'),

    # ----- DOCUMENTOS (Sistema Simple con jsPDF) -----
    path('documento/seleccionar/<int:person_id>/', login_required(select_document_type), name='select-document-type'),
    path('documento/aval-general/<int:person_id>/', login_required(generate_aval_general), name='generate-aval-general'),
    path('documento/aval-estudio/<int:person_id>/', login_required(generate_aval_estudio), name='generate-aval-estudio'),
    path('documento/constancia/<int:person_id>/', login_required(generate_constancia_pertenencia), name='generate-constancia'),

    # Visualización y gestión de documentos generados
    path('documento/ver/<int:document_id>/', login_required(view_document), name='view-document'),
    path('documento/preview/<int:document_id>/', login_required(preview_document_pdf), name='preview-document-pdf'),
    path('documento/persona/<int:person_id>/', login_required(list_person_documents), name='list-person-documents'),
    path('documento/descargar/<int:document_id>/', login_required(download_document_pdf), name='download-document-pdf'),

    # Verificación de documentos (acceso público para terceros)
    path('documento/verificar/<str:hash>/', verify_document, name='verify-document'),

    # Estadísticas de documentos
    path('documentos/estadisticas/', login_required(organization_documents_stats), name='documents-stats'),
    path('documentos/estadisticas/<int:organization_id>/', login_required(organization_documents_stats), name='documents-stats-org'),

    # ----- BÚSQUEDA GLOBAL -----
    path('busqueda/', login_required(global_search), name='global-search'),
    path('api/busqueda/', login_required(global_search_api), name='global-search-api'),

    # ----- IMPORTACIÓN MASIVA -----
    path('importacion/', login_required(importacion_masiva_inicio), name='importacion-masiva'),
    path('importacion/template/', login_required(descargar_template_importacion), name='descargar-template'),
    path('importacion/validar/', login_required(validar_archivo_importacion), name='validar-importacion'),
    path('importacion/confirmar/', login_required(confirmar_importacion), name='confirmar-importacion'),
    path('importacion/log/', login_required(ver_log_importacion), name='ver-log-importacion'),
    path('importacion/log/descargar/', login_required(descargar_log_importacion), name='descargar-log-importacion'),
]
