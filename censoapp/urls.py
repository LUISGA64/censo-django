from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib.auth.decorators import login_required
from .viewsets import SidewalksViewSet, AssociationViewSet, OrganizationViewSet
from .views import (home, profile, association, CreateAssociation, family_card_index,
                    crear_persona, detalle_ficha, UpdateFamily, get_family_cards, create_family_card,
                    listar_personas, view_persons, UpdatePerson, person_by_gender)

# router = routers.DefaultRouter()
# router.register(r'sidewalks', SidewalksViewSet, 'sidewalks')
# router.register(r'associations', AssociationViewSet, 'associations')
# router.register(r'organizations', OrganizationViewSet, 'organizations')
# router.register(r'documenttypes', OrganizationViewSet, 'documenttypes')
# router.register(r'civilstates', OrganizationViewSet, 'civilstates')
# router.register(r'educationlevels', OrganizationViewSet, 'educationlevels')
# router.register(r'eps', OrganizationViewSet, 'eps')
# router.register(r'kinships', OrganizationViewSet, 'kinships')
# router.register(r'occupancies', OrganizationViewSet, 'occupancies')
# router.register(r'securitysocials', OrganizationViewSet, 'security-socials')
# router.register(r'handicaps', OrganizationViewSet, 'handicaps')


# urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls)),
#     path('docs/', include_docs_urls(title='Sidewalks API')),
# ]

urlpatterns = [
    path('', login_required(home), name='home'),
    # path('dashboard/', login_required(dashboard), name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('association', association, name='association'),
    path('createAssociation', login_required(CreateAssociation.as_view()), name='createAssociation'),
    path('familyCard/create', login_required(create_family_card), name='createFamilyCard'),
    path('familyCard/index', login_required(family_card_index), name='familyCardIndex'),
    path('familyCard/create/<int:pk>', login_required(crear_persona), name='createPerson'),
    path('familyCard/detail/<int:pk>/', login_required(detalle_ficha), name='detailFamilyCard'),
    path('update-family/<int:pk>', login_required(UpdateFamily.as_view()), name='update-family'),
    path('personas', login_required(view_persons), name='personas'),
    path('edit-person/<int:pk>', login_required(UpdatePerson.as_view()), name='updated-person'),

    # ----- JSON API  ----
    path('json_familycards', login_required(get_family_cards), name='familycards'),
    path('json_personas/', login_required(listar_personas), name='json_personas'),
    path('json_person_gender/', login_required(person_by_gender), name='persons-gender'),

]
