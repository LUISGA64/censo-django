from django.urls import path
from .views import home, dashboard, profile, association, CreateAssociation, FamilyCardIndex, create_family_card
from django.urls import reverse_lazy

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', CreateAssociation.as_view(), name='createAssociation'),
    path('familyCard/list', FamilyCardIndex.as_view(), name='familyCard_list'),
    path('familyCard/create', create_family_card, name='createFamilyCard'),
]
