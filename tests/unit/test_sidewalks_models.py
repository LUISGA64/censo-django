"""
Tests unitarios para el modelo Sidewalks.
"""
import pytest
from censoapp.models import Sidewalks


@pytest.mark.django_db
class TestSidewalksModel:
    """Tests para el modelo Sidewalks (Veredas)."""

    def test_create_sidewalk(self, create_organization):
        """Test crear vereda básica."""
        organization = create_organization()

        sidewalk = Sidewalks.objects.create(
            sidewalk_name="Vereda Principal", organization_id=organization
        )

        assert sidewalk.pk is not None
        assert sidewalk.sidewalk_name == "Vereda Principal"
        assert sidewalk.organization_id == organization

    def test_sidewalk_string_representation(self, create_organization):
        """Test representación en string de vereda."""
        organization = create_organization()

        sidewalk = Sidewalks.objects.create(
            sidewalk_name="Vereda Test", organization_id=organization
        )

        assert str(sidewalk) == "Vereda Test"

    def test_sidewalk_with_description(self, create_organization):
        """Test vereda con descripción."""
        organization = create_organization()

        sidewalk = Sidewalks.objects.create(
            sidewalk_name="Vereda Norte",
            organization_id=organization,
            description="Vereda ubicada al norte del municipio",
        )

        assert sidewalk.description == "Vereda ubicada al norte del municipio"

    def test_sidewalk_with_coordinates(self, create_organization):
        """Test vereda con coordenadas GPS."""
        organization = create_organization()

        sidewalk = Sidewalks.objects.create(
            sidewalk_name="Vereda Centro",
            organization_id=organization,
            latitude=4.5709,
            longitude=-74.2973,
        )

        assert sidewalk.latitude == 4.5709
        assert sidewalk.longitude == -74.2973

    def test_sidewalk_without_coordinates(self, create_organization):
        """Test que vereda puede no tener coordenadas."""
        organization = create_organization()

        sidewalk = Sidewalks.objects.create(
            sidewalk_name="Vereda Sin GPS", organization_id=organization
        )

        # Las coordenadas pueden ser None o null
        assert sidewalk.latitude is None or sidewalk.latitude == 0
        assert sidewalk.longitude is None or sidewalk.longitude == 0

    def test_multiple_sidewalks_same_organization(self, create_organization):
        """Test que una organización puede tener múltiples veredas."""
        organization = create_organization()

        sidewalk1 = Sidewalks.objects.create(
            sidewalk_name="Vereda 1", organization_id=organization
        )

        sidewalk2 = Sidewalks.objects.create(
            sidewalk_name="Vereda 2", organization_id=organization
        )

        assert sidewalk1.organization_id == sidewalk2.organization_id
        assert Sidewalks.objects.filter(organization_id=organization).count() == 2

    def test_sidewalk_belongs_to_organization(self, create_organization):
        """Test que vereda pertenece a una organización específica."""
        org1 = create_organization(name="Org 1")
        org2 = create_organization(name="Org 2")

        sidewalk1 = Sidewalks.objects.create(
            sidewalk_name="Vereda Org 1", organization_id=org1
        )

        sidewalk2 = Sidewalks.objects.create(
            sidewalk_name="Vereda Org 2", organization_id=org2
        )

        assert sidewalk1.organization_id != sidewalk2.organization_id
        assert sidewalk1.organization_id.organization_name == "Org 1"
        assert sidewalk2.organization_id.organization_name == "Org 2"

    def test_sidewalk_can_have_families(self, create_sidewalk, create_family_card):
        """Test que una vereda puede tener familias asociadas."""
        sidewalk = create_sidewalk(name="Vereda Con Familias")

        # Crear familia asociada a esta vereda
        family = create_family_card(sidewalk=sidewalk)

        assert family.sidewalk_home == sidewalk

    def test_sidewalk_verbose_name(self, create_organization):
        """Test que el modelo tiene verbose_name correcto."""
        organization = create_organization()
        sidewalk = Sidewalks.objects.create(
            sidewalk_name="Test Verbose", organization_id=organization
        )

        # Verificar que el modelo tiene Meta con verbose_name
        meta = Sidewalks._meta
        assert meta.verbose_name == "Vereda"
        assert meta.verbose_name_plural == "Veredas"

    def test_sidewalk_name_required(self, create_organization):
        """Test que el nombre de vereda es requerido."""
        organization = create_organization()

        # Intentar crear sin nombre debería fallar
        with pytest.raises(Exception):  # IntegrityError o ValidationError
            Sidewalks.objects.create(
                sidewalk_name=None,  # Nombre requerido
                organization_id=organization,
            )

    def test_sidewalk_organization_required(self):
        """Test que la organización es requerida."""
        # Intentar crear sin organización debería fallar
        with pytest.raises(Exception):  # IntegrityError
            Sidewalks.objects.create(
                sidewalk_name="Vereda Sin Org",
                organization_id=None,  # Organización requerida
            )

