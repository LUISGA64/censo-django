"""
Tests para el formulario FormFamilyCard.
"""
import pytest
from django.core.exceptions import ValidationError
from censoapp.forms import FormFamilyCard


@pytest.mark.django_db
class TestFormFamilyCard:
    """Tests para FormFamilyCard."""

    def test_form_valid_with_all_required_fields(
        self, create_sidewalk, create_organization
    ):
        """Test que el formulario es válido con todos los campos requeridos."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert form.is_valid(), form.errors

    def test_form_valid_with_optional_address(
        self, create_sidewalk, create_organization
    ):
        """Test que el formulario acepta dirección opcional."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "address_home": "Casa #5, Al lado del colegio",
            "sidewalk_home": sidewalk.id,
            "zone": "Rural",
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert form.is_valid(), form.errors
        assert form.cleaned_data["address_home"] == "Casa #5, Al lado del colegio"

    def test_form_valid_with_coordinates(
        self, create_sidewalk, create_organization
    ):
        """Test que el formulario acepta coordenadas válidas."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
            "latitude": "4.5709",
            "longitude": "-74.2973",
        }

        form = FormFamilyCard(data=form_data)
        assert form.is_valid(), form.errors
        assert form.cleaned_data["latitude"] == "4.5709"
        assert form.cleaned_data["longitude"] == "-74.2973"

    def test_form_invalid_missing_sidewalk(self, create_organization):
        """Test que el formulario es inválido sin vereda."""
        organization = create_organization()

        form_data = {
            "zone": "Urbana",
            "organization": organization.id,
            # Falta sidewalk_home
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "sidewalk_home" in form.errors

    def test_form_invalid_missing_zone(self, create_sidewalk, create_organization):
        """Test que el formulario es inválido sin zona."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "organization": organization.id,
            # Falta zone
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "zone" in form.errors

    def test_form_invalid_missing_organization(self, create_sidewalk):
        """Test que el formulario es inválido sin organización."""
        sidewalk = create_sidewalk()

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            # Falta organization
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "organization" in form.errors

    def test_form_invalid_latitude_out_of_range(
        self, create_sidewalk, create_organization
    ):
        """Test que rechaza latitud fuera de rango."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
            "latitude": "100",  # Fuera de rango (-90 a 90)
            "longitude": "-74.2973",
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "latitude" in form.errors

    def test_form_invalid_longitude_out_of_range(
        self, create_sidewalk, create_organization
    ):
        """Test que rechaza longitud fuera de rango."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
            "latitude": "4.5709",
            "longitude": "-200",  # Fuera de rango (-180 a 180)
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "longitude" in form.errors

    def test_form_invalid_latitude_format(
        self, create_sidewalk, create_organization
    ):
        """Test que rechaza latitud con formato inválido."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
            "latitude": "abc",  # Formato inválido
            "longitude": "-74.2973",
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "latitude" in form.errors

    def test_form_invalid_coordinates_incomplete(
        self, create_sidewalk, create_organization
    ):
        """Test que rechaza coordenadas incompletas."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        # Solo latitud sin longitud
        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
            "latitude": "4.5709",
            # Falta longitude
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "__all__" in form.errors or "longitude" in form.errors

    def test_form_invalid_zone_choice(self, create_sidewalk, create_organization):
        """Test que rechaza zona inválida."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Invalid",  # Zona inválida (solo U o R)
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "zone" in form.errors

    def test_form_address_max_length(self, create_sidewalk, create_organization):
        """Test que rechaza dirección muy larga."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "address_home": "A" * 51,  # Más de 50 caracteres
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "address_home" in form.errors

    def test_form_empty_optional_fields(self, create_sidewalk, create_organization):
        """Test que campos opcionales pueden estar vacíos."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "address_home": "",
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
            "latitude": "",
            "longitude": "",
        }

        form = FormFamilyCard(data=form_data)
        assert form.is_valid(), form.errors

    def test_form_zone_urban(self, create_sidewalk, create_organization):
        """Test que acepta zona urbana."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Urbana",
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data["zone"] == "Urbana"

    def test_form_zone_rural(self, create_sidewalk, create_organization):
        """Test que acepta zona rural."""
        organization = create_organization()
        sidewalk = create_sidewalk(organization=organization)

        form_data = {
            "sidewalk_home": sidewalk.id,
            "zone": "Rural",
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert form.is_valid()
        assert form.cleaned_data["zone"] == "Rural"

    def test_form_has_crispy_helper(self):
        """Test que el formulario tiene crispy helper configurado."""
        form = FormFamilyCard()
        assert hasattr(form, "helper")
        assert form.helper.form_id == "id-FamilyCard"

    def test_form_fields_present(self):
        """Test que todos los campos esperados están presentes."""
        form = FormFamilyCard()
        expected_fields = [
            "address_home",
            "sidewalk_home",
            "latitude",
            "longitude",
            "zone",
            "organization",
        ]

        for field_name in expected_fields:
            assert field_name in form.fields

    def test_form_invalid_sidewalk_doesnt_exist(self, create_organization):
        """Test que rechaza vereda que no existe."""
        organization = create_organization()

        form_data = {
            "sidewalk_home": 99999,  # ID que no existe
            "zone": "Urbana",
            "organization": organization.id,
        }

        form = FormFamilyCard(data=form_data)
        assert not form.is_valid()
        assert "sidewalk_home" in form.errors

