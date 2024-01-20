from django.urls import path
from .views import home, dashboard, profile, association, CreateAssociation, censo_index, registrar_censo
from django.urls import reverse_lazy

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', CreateAssociation.as_view(), name='createAssociation'),
    path('censoIndex', censo_index, name='censoIndex'),
    path('registrarCenso', registrar_censo, name='registrarCenso'),
]
