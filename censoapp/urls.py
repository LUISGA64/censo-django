from django.urls import path, include
from django.contrib.auth.decorators import login_required
# from .views import (home, dashboard, profile, association, CreateAssociation, family_card_index,
#                     FamilyCardCreate, crear_persona, detalle_ficha, UpdateFamily, get_family_cards)

from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from .viewsets import SidewalksViewSet, AssociationViewSet, OrganizationViewSet

router = routers.DefaultRouter()
router.register(r'sidewalks', SidewalksViewSet, 'sidewalks')
router.register(r'associations', AssociationViewSet, 'associations')
router.register(r'organizations', OrganizationViewSet, 'organizations')
router.register(r'documenttypes', OrganizationViewSet, 'documenttypes')
router.register(r'civilstates', OrganizationViewSet, 'civilstates')
router.register(r'educationlevels', OrganizationViewSet, 'educationlevels')
router.register(r'eps', OrganizationViewSet, 'eps')
router.register(r'kinships', OrganizationViewSet, 'kinships')
router.register(r'occupancies', OrganizationViewSet, 'occupancies')
router.register(r'securitysocials', OrganizationViewSet, 'security-socials')
router.register(r'handicaps', OrganizationViewSet, 'handicaps')


urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='Sidewalks API')),
]

# urlpatterns = [
#     path('', home, name='home'),
#     path('dashboard/', dashboard, name='dashboard'),
#     path('accounts/profile/', profile, name='profile'),
#     path('association', association, name='association'),
#     path('createAssociation', login_required(CreateAssociation.as_view()), name='createAssociation'),
#     path('familyCard/create', login_required(FamilyCardCreate.as_view()), name='createFamilyCard'),
#     path('familyCard/index', login_required(family_card_index), name='familyCardIndex'),
#     path('familyCard/create/<int:pk>', login_required(crear_persona), name='createPerson'),
#     path('familyCard/detail/<int:pk>/', login_required(detalle_ficha), name='detailFamilyCard'),
#     path('update-family/<int:pk>', login_required(UpdateFamily.as_view()), name='update-family'),
#     path('familycards', get_family_cards, name='familycards'),
# ]
