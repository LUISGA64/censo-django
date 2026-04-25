"""
Tests unitarios para modelos de Organization.
"""
import pytest
from censoapp.models import Organizations, Association


@pytest.mark.django_db
class TestOrganizationModel:
    """Tests para el modelo Organizations."""

    def test_create_organization(self, create_organization):
        """Test crear organización básica."""
        org = create_organization(name="Test Org")

        assert org.organization_name == "Test Org"
        assert org.pk is not None
        assert str(org) == "Test Org"

    def test_organization_with_association(self, create_organization, create_association):
        """Test que organización tiene asociación correcta."""
        association = create_association(name="My Association")
        org = create_organization(association=association)

        assert org.association_id == association
        assert org.association_id.association_name == "My Association"

    def test_organization_unique_identification(
        self, create_organization, create_association
    ):
        """Test que el número de identificación es único."""
        association = create_association()

        # Primera organización
        create_organization(identification="111111", association=association)

        # Intentar crear otra con mismo ID debe fallar
        with pytest.raises(Exception):  # IntegrityError
            create_organization(identification="111111", association=association)


@pytest.mark.django_db
class TestAssociationModel:
    """Tests para el modelo Association."""

    def test_create_association(self, create_association):
        """Test crear asociación."""
        assoc = create_association(name="Test Association")

        assert assoc.association_name == "Test Association"
        assert assoc.pk is not None

    def test_association_string_representation(self, create_association):
        """Test representación en string."""
        assoc = create_association(
            name="My Assoc", identification="123456789"
        )

        assert str(assoc) == "My Assoc 123456789"

