from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib.auth.decorators import login_required

from .models import MaterialConstruction
from .viewsets import SidewalksViewSet, AssociationViewSet, OrganizationViewSet
from .views import (home, profile, association, CreateAssociation, family_card_index,
                    crear_persona, detalle_ficha, UpdateFamily, get_family_cards, create_family_card,
                    listar_personas, view_persons, UpdatePerson, person_by_gender, DetailPersona, update_family_head,
                    delete_person_familyCard, get_system_parameters, MaterialConstructionView, export_persons_excel)


urlpatterns = [
    path('', login_required(home), name='home'),
    # path('dashboard/', login_required(dashboard), name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', login_required(CreateAssociation.as_view()), name='createAssociation'),

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


    # Document Aval
    # path('aval/')

]
