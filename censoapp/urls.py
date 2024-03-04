from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (home, dashboard, profile, association, CreateAssociation, family_card_index,
                    FamilyCardCreate, crear_persona, detalle_ficha, UpdateFamily)

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', login_required(CreateAssociation.as_view()), name='createAssociation'),
    path('familyCard/create', login_required(FamilyCardCreate.as_view()), name='createFamilyCard'),
    path('familyCard/index', login_required(family_card_index), name='familyCardIndex'),
    path('familyCard/create/<int:pk>', login_required(crear_persona), name='createPerson'),
    path('familyCard/detail/<int:pk>/', login_required(detalle_ficha), name='detailFamilyCard'),
    path('update-family/<int:pk>', login_required(UpdateFamily.as_view()), name='update-family')
    # path('familyCard/edit/<int:pk>', login_required(editar_ficha), name='editFamilyCard'),
]
