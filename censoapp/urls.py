from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib.auth.decorators import login_required

from .models import MaterialConstruction
from .viewsets import (
    SidewalksViewSet, AssociationViewSet, OrganizationViewSet,
    PersonViewSet, FamilyCardViewSet, GeneratedDocumentViewSet
)
from .views import (home, profile, association, CreateAssociation, family_card_index,
                    crear_persona, detalle_ficha, UpdateFamily, get_family_cards, create_family_card,
                    listar_personas, view_persons, UpdatePerson, person_by_gender, DetailPersona, update_family_head,
                    delete_person_familyCard, get_system_parameters, MaterialConstructionView, export_persons_excel,
                    organization_detail,
                    importacion_masiva_inicio, descargar_template_importacion, validar_archivo_importacion,
                    confirmar_importacion, ver_log_importacion, descargar_log_importacion)
# Búsqueda Global - Nueva implementación mejorada
from .search_views import global_search, test_search_view, search_page_view
from .document_views import (view_document, list_person_documents, download_document_pdf,
                            organization_documents_stats, preview_document_pdf, verify_document)
from .simple_document_views import (select_document_type, generate_aval_general, generate_aval_estudio,
                                   generate_constancia_pertenencia)
# Dashboard Analytics
from .dashboard_views import (dashboard_analytics, api_gender_distribution, api_age_pyramid,
                              api_education_distribution, api_civil_state, api_sidewalks,
                              api_population_growth)
# Geolocalización
from .geolocation_views import (map_view, map_sidewalks_data, map_heatmap, map_clusters,
                                sidewalk_detail_map, update_sidewalk_location)
# Notificaciones
from .notification_views import (notifications_list, notification_detail, mark_as_read,
                                 mark_all_as_read, notifications_unread, notification_preferences,
                                 delete_notification)

# ==============================================================================
# API REST ROUTER
# ==============================================================================

router = routers.DefaultRouter()
router.register(r'sidewalks', SidewalksViewSet, basename='sidewalk')
router.register(r'associations', AssociationViewSet, basename='association')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'persons', PersonViewSet, basename='person')
router.register(r'family-cards', FamilyCardViewSet, basename='family-card')
router.register(r'documents', GeneratedDocumentViewSet, basename='document')


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
    path('search/', login_required(search_page_view), name='search-page'),  # Página HTML
    path('api/search/', login_required(global_search), name='global-search'),  # API JSON
    path('test-search/', login_required(test_search_view), name='test-search'),  # Vista de prueba

    # ----- IMPORTACIÓN MASIVA -----
    path('importacion/', login_required(importacion_masiva_inicio), name='importacion-masiva'),
    path('importacion/template/', login_required(descargar_template_importacion), name='descargar-template'),
    path('importacion/validar/', login_required(validar_archivo_importacion), name='validar-importacion'),
    path('importacion/confirmar/', login_required(confirmar_importacion), name='confirmar-importacion'),
    path('importacion/log/', login_required(ver_log_importacion), name='ver-log-importacion'),
    path('importacion/log/descargar/', login_required(descargar_log_importacion), name='descargar-log-importacion'),

    # ----- DASHBOARD ANALÍTICO -----
    path('dashboard/analytics/', login_required(dashboard_analytics), name='dashboard-analytics'),
    # APIs del dashboard
    path('api/dashboard/gender/', login_required(api_gender_distribution), name='api-gender'),
    path('api/dashboard/age-pyramid/', login_required(api_age_pyramid), name='api-age-pyramid'),
    path('api/dashboard/education/', login_required(api_education_distribution), name='api-education'),
    path('api/dashboard/civil-state/', login_required(api_civil_state), name='api-civil-state'),
    path('api/dashboard/sidewalks/', login_required(api_sidewalks), name='api-sidewalks'),
    path('api/dashboard/population-growth/', login_required(api_population_growth), name='api-population-growth'),

    # ----- GEOLOCALIZACIÓN Y MAPAS -----
    path('mapa/', login_required(map_view), name='map-view'),
    path('api/map/sidewalks/', login_required(map_sidewalks_data), name='map-sidewalks-data'),
    path('mapa/calor/', login_required(map_heatmap), name='map-heatmap'),
    path('mapa/clusters/', login_required(map_clusters), name='map-clusters'),
    path('mapa/vereda/<int:sidewalk_id>/', login_required(sidewalk_detail_map), name='sidewalk-detail-map'),
    path('api/sidewalk/<int:sidewalk_id>/location/', login_required(update_sidewalk_location), name='update-sidewalk-location'),

    # ----- NOTIFICACIONES -----
    path('notifications/', login_required(notifications_list), name='notifications-list'),
    path('notifications/<int:notification_id>/', login_required(notification_detail), name='notification-detail'),
    path('notifications/<int:notification_id>/mark-read/', login_required(mark_as_read), name='mark-as-read'),
    path('notifications/mark-all-read/', login_required(mark_all_as_read), name='mark-all-as-read'),
    path('api/notifications/unread/', login_required(notifications_unread), name='notifications-unread'),
    path('notifications/<int:notification_id>/delete/', login_required(delete_notification), name='delete-notification'),
    path('notifications/preferences/', login_required(notification_preferences), name='notification-preferences'),

    # ----- API REST CON JWT -----
    path('api/v1/', include(router.urls)),
]
