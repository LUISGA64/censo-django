from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (home, dashboard, profile, association, CreateAssociation, FamilyCardIndex,
                    FamilyCardCreate)

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', login_required(CreateAssociation.as_view()), name='createAssociation'),
    path('familyCard/create', login_required(FamilyCardCreate.as_view()), name='createFamilyCard'),
    path('familyCard/index', login_required(FamilyCardIndex.as_view()), name='familyCardIndex'),
]
