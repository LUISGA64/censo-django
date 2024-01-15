from django.urls import path
from .views import home, dashboard, profile, association, createAssociation
from django.urls import reverse_lazy

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association.as_view(), name='association'),
    path('createAssociation', createAssociation.as_view(), name='createAssociation'),
]
