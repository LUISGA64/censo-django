"""
Tests unitarios para el modelo FamilyCard.
"""
import pytest
from censoapp.models import FamilyCard


@pytest.mark.django_db
class TestFamilyCardModel:
    """Tests para el modelo FamilyCard."""

    def test_create_family_card(self, create_family_card):
        """Test crear ficha familiar básica."""
        family = create_family_card()

        assert family.pk is not None
        assert family.zone in ["U", "R"]
        assert family.state is True

    def test_family_card_auto_number(self, create_family_card):
        """Test que el número de ficha se asigna automáticamente."""
        family1 = create_family_card()
        family2 = create_family_card()

        assert family1.family_card_number > 0
        assert family2.family_card_number > family1.family_card_number

    def test_family_card_with_address(self, create_family_card):
        """Test ficha con dirección."""
        family = create_family_card(address="Casa 123, Vereda X")

        # El modelo capitaliza automáticamente (primera letra mayúscula)
        assert family.address_home.lower() == "casa 123, vereda x"

    def test_family_card_with_coordinates(self, create_family_card):
        """Test ficha con coordenadas GPS."""
        family = create_family_card(latitude="4.5709", longitude="-74.2973")

        assert family.latitude == "4.5709"
        assert family.longitude == "-74.2973"

    def test_get_next_family_card_number(self, create_family_card):
        """Test obtener siguiente número de ficha."""
        # Crear algunas fichas
        create_family_card()
        create_family_card()
        last_family = create_family_card()

        next_number = FamilyCard.get_next_family_card_number()

        assert next_number > last_family.family_card_number

    def test_family_card_belongs_to_organization(
        self, create_family_card, create_organization
    ):
        """Test que la ficha pertenece a una organización."""
        org = create_organization(name="My Org")
        family = create_family_card(organization=org)

        assert family.organization == org
        assert family.organization.organization_name == "My Org"

    def test_family_card_zones(self, create_family_card):
        """Test diferentes zonas (Urbana/Rural)."""
        urban_family = create_family_card(zone="U")
        rural_family = create_family_card(zone="R")

        assert urban_family.zone == "U"
        assert rural_family.zone == "R"

