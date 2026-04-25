"""
Tests unitarios para el modelo UserProfile.
"""
import pytest
from censoapp.models import UserProfile


@pytest.mark.django_db
class TestUserProfileModel:
    """Tests para el modelo UserProfile."""

    def test_create_user_profile(self, create_user, create_organization):
        """Test crear perfil de usuario básico."""
        user = create_user(username="testprofile")
        organization = create_organization()

        profile = UserProfile.objects.create(
            user=user, organization=organization, role="OPERATOR"
        )

        assert profile.pk is not None
        assert profile.user == user
        assert profile.organization == organization
        assert profile.role == "OPERATOR"

    def test_user_profile_default_values(self, create_user, create_organization):
        """Test valores por defecto del perfil."""
        user = create_user(username="defaultuser")
        organization = create_organization()

        profile = UserProfile.objects.create(user=user, organization=organization)

        assert profile.role == "OPERATOR"  # Valor por defecto
        assert profile.is_active is True  # Valor por defecto
        assert profile.can_view_all_organizations is False  # Valor por defecto

    def test_user_profile_admin_role(self, create_user, create_organization):
        """Test perfil con rol de administrador."""
        user = create_user(username="adminuser")
        organization = create_organization()

        profile = UserProfile.objects.create(
            user=user, organization=organization, role="ADMIN"
        )

        assert profile.role == "ADMIN"

    def test_user_profile_viewer_role(self, create_user, create_organization):
        """Test perfil con rol de solo consulta."""
        user = create_user(username="vieweruser")
        organization = create_organization()

        profile = UserProfile.objects.create(
            user=user, organization=organization, role="VIEWER"
        )

        assert profile.role == "VIEWER"

    def test_user_profile_can_view_all_organizations(
        self, create_user, create_organization
    ):
        """Test perfil con acceso a todas las organizaciones."""
        user = create_user(username="superoperator")
        organization = create_organization()

        profile = UserProfile.objects.create(
            user=user,
            organization=organization,
            role="ADMIN",
            can_view_all_organizations=True,
        )

        assert profile.can_view_all_organizations is True

    def test_user_profile_string_representation(
        self, create_user, create_organization
    ):
        """Test representación en string del perfil."""
        user = create_user(username="stringtest")
        organization = create_organization(name="Test Org")

        profile = UserProfile.objects.create(user=user, organization=organization)

        profile_str = str(profile)
        assert "stringtest" in profile_str
        assert "Test Org" in profile_str

    def test_user_profile_one_to_one_user(self, create_user, create_organization):
        """Test que el perfil es uno a uno con el usuario."""
        user = create_user(username="onetoone")
        organization = create_organization()

        profile1 = UserProfile.objects.create(user=user, organization=organization)

        # Intentar crear otro perfil para el mismo usuario debería fallar
        with pytest.raises(Exception):  # IntegrityError
            UserProfile.objects.create(user=user, organization=organization)

    def test_user_profile_has_permission_to_view_organization(
        self, create_user, create_organization
    ):
        """Test método has_permission_to_view_organization."""
        user = create_user(username="permissiontest")
        org1 = create_organization(name="Org 1")
        org2 = create_organization(name="Org 2")

        profile = UserProfile.objects.create(user=user, organization=org1)

        # Debe tener permiso para ver su propia organización
        if hasattr(profile, "has_permission_to_view_organization"):
            assert profile.has_permission_to_view_organization(org1) is True
            # No debe tener permiso para ver otra organización
            assert profile.has_permission_to_view_organization(org2) is False

    def test_user_profile_superuser_permissions(
        self, create_user, create_organization
    ):
        """Test que superusuarios tienen permisos especiales."""
        superuser = create_user(username="superuser", is_superuser=True, is_staff=True)
        organization = create_organization()

        # Superusuario puede tener perfil (aunque no es requerido)
        profile = UserProfile.objects.create(
            user=superuser,
            organization=organization,
            role="ADMIN",
            can_view_all_organizations=True,
        )

        assert profile.user.is_superuser is True
        assert profile.can_view_all_organizations is True

    def test_user_profile_inactive(self, create_user, create_organization):
        """Test que un perfil puede ser desactivado."""
        user = create_user(username="inactiveuser")
        organization = create_organization()

        profile = UserProfile.objects.create(user=user, organization=organization)

        profile.is_active = False
        profile.save()

        assert profile.is_active is False

    def test_multiple_users_same_organization(
        self, create_user, create_organization
    ):
        """Test que múltiples usuarios pueden pertenecer a la misma organización."""
        organization = create_organization()

        user1 = create_user(username="user1")
        user2 = create_user(username="user2")

        profile1 = UserProfile.objects.create(user=user1, organization=organization)
        profile2 = UserProfile.objects.create(user=user2, organization=organization)

        assert profile1.organization == profile2.organization
        assert (
            UserProfile.objects.filter(organization=organization).count() == 2
        )

    def test_user_profile_timestamps(self, create_user, create_organization):
        """Test que se crean timestamps automáticamente."""
        user = create_user(username="timestampuser")
        organization = create_organization()

        profile = UserProfile.objects.create(user=user, organization=organization)

        assert profile.created_at is not None
        assert profile.updated_at is not None
        assert profile.updated_at >= profile.created_at

