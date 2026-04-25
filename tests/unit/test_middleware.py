"""
Tests para Middleware personalizado.
"""
import pytest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from censoapp.middleware import OrganizationAccessMiddleware


@pytest.mark.django_db
class TestOrganizationAccessMiddleware:
    """Tests para OrganizationAccessMiddleware."""

    def test_middleware_adds_organization_to_request(
        self, create_user, create_organization
    ):
        """Test que el middleware añade la organización al request."""
        from censoapp.models import UserProfile
        
        user = create_user(username="testuser")
        org = create_organization(name="Test Org")
        UserProfile.objects.create(user=user, organization=org, role="OPERATOR")
        
        # Crear request
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        
        # Mock de get_response
        def get_response(request):
            return HttpResponse("OK")
        
        # Crear middleware
        middleware = OrganizationAccessMiddleware(get_response)
        
        # Procesar request
        response = middleware(request)
        
        # Verificar que se añadió la organización
        assert hasattr(request, 'organization')
        assert request.organization == org

    def test_middleware_handles_anonymous_user(self):
        """Test que el middleware maneja usuarios anónimos."""
        factory = RequestFactory()
        request = factory.get('/')
        request.user = AnonymousUser()
        
        def get_response(request):
            return HttpResponse("OK")
        
        middleware = OrganizationAccessMiddleware(get_response)
        response = middleware(request)
        
        # No debe añadir organización para usuarios anónimos
        assert not hasattr(request, 'organization') or request.organization is None

    def test_middleware_handles_user_without_profile(
        self, create_user
    ):
        """Test que el middleware maneja usuarios sin perfil."""
        user = create_user(username="noprofile")
        
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        
        def get_response(request):
            return HttpResponse("OK")
        
        middleware = OrganizationAccessMiddleware(get_response)
        response = middleware(request)
        
        # Debe manejar gracefully
        assert response.status_code in [200, 302]  # OK o redirect

    def test_middleware_allows_superuser_access(
        self, create_user, create_organization
    ):
        """Test que superusuarios tienen acceso completo."""
        from censoapp.models import UserProfile
        
        superuser = create_user(username="superuser", is_superuser=True, is_staff=True)
        org = create_organization()
        
        UserProfile.objects.create(
            user=superuser,
            organization=org,
            role="ADMIN",
            can_view_all_organizations=True
        )
        
        factory = RequestFactory()
        request = factory.get('/')
        request.user = superuser
        
        def get_response(request):
            return HttpResponse("OK")
        
        middleware = OrganizationAccessMiddleware(get_response)
        response = middleware(request)
        
        assert response.status_code == 200

