"""
Tests para el formulario FormPerson.
"""
import pytest
from datetime import date, timedelta
from censoapp.forms import FormPerson


@pytest.mark.django_db
class TestFormPerson:
    """Tests para FormPerson."""

    def test_form_valid_with_all_required_fields(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que el formulario es válido con todos los campos requeridos."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="01", defaults={"affiliation": "Contributivo"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="001", defaults={"name_eps": "EPS Test"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="01", defaults={"description_kinship": "Hijo"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Estudiante"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "Juan",
            "last_name_1": "Pérez",
            "document_type": doc_type.id,
            "identification_person": "1234567890",
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
        }

        form = FormPerson(data=form_data)
        assert form.is_valid(), form.errors

    def test_form_valid_with_optional_fields(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que el formulario acepta campos opcionales."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="02", defaults={"affiliation": "Subsidiado"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="002", defaults={"name_eps": "EPS Test 2"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="02", defaults={"description_kinship": "Padre"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Empleado"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N2", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "María",
            "first_name_2": "Isabel",  # Opcional
            "last_name_1": "García",
            "last_name_2": "López",  # Opcional
            "document_type": doc_type.id,
            "identification_person": "9876543210",
            "gender": gender.id,
            "date_birth": "1995-05-15",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
            "cell_phone": "3001234567",  # Opcional
            "personal_email": "maria@example.com",  # Opcional
        }

        form = FormPerson(data=form_data)
        assert form.is_valid(), form.errors
        assert form.cleaned_data["first_name_2"] == "Isabel"
        assert form.cleaned_data["cell_phone"] == "3001234567"

    def test_form_invalid_missing_first_name(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que el formulario es inválido sin primer nombre."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="03", defaults={"affiliation": "Contributivo"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="003", defaults={"name_eps": "EPS Test 3"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="03", defaults={"description_kinship": "Hermano"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Independiente"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N3", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            # Falta first_name_1
            "last_name_1": "Pérez",
            "document_type": doc_type.id,
            "identification_person": "1111111111",
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
        }

        form = FormPerson(data=form_data)
        assert not form.is_valid()
        assert "first_name_1" in form.errors

    def test_form_invalid_missing_last_name(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que el formulario es inválido sin primer apellido."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="04", defaults={"affiliation": "Subsidiado"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="004", defaults={"name_eps": "EPS Test 4"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="04", defaults={"description_kinship": "Esposo"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Desempleado"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N4", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "Juan",
            # Falta last_name_1
            "document_type": doc_type.id,
            "identification_person": "2222222222",
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
        }

        form = FormPerson(data=form_data)
        assert not form.is_valid()
        assert "last_name_1" in form.errors

    def test_form_invalid_email_format(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que rechaza email con formato inválido."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="05", defaults={"affiliation": "Contributivo"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="005", defaults={"name_eps": "EPS Test 5"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="05", defaults={"description_kinship": "Madre"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Pensionado"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N5", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "Ana",
            "last_name_1": "Rodríguez",
            "document_type": doc_type.id,
            "identification_person": "3333333333",
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
            "personal_email": "email-invalido",  # Email inválido
        }

        form = FormPerson(data=form_data)
        assert not form.is_valid()
        assert "personal_email" in form.errors

    def test_form_name_max_length(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que rechaza nombres muy largos."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="06", defaults={"affiliation": "Contributivo"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="006", defaults={"name_eps": "EPS Test 6"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="06", defaults={"description_kinship": "Abuelo"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Agricultor"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N6", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "A" * 31,  # Más de 30 caracteres
            "last_name_1": "Pérez",
            "document_type": doc_type.id,
            "identification_person": "4444444444",
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
        }

        form = FormPerson(data=form_data)
        assert not form.is_valid()
        assert "first_name_1" in form.errors

    def test_form_identification_max_length(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que rechaza identificación muy larga."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="07", defaults={"affiliation": "Subsidiado"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="007", defaults={"name_eps": "EPS Test 7"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="07", defaults={"description_kinship": "Nieto"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Comerciante"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N7", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "Carlos",
            "last_name_1": "González",
            "document_type": doc_type.id,
            "identification_person": "1" * 16,  # Más de 15 caracteres
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
        }

        form = FormPerson(data=form_data)
        assert not form.is_valid()
        assert "identification_person" in form.errors

    def test_form_has_crispy_helper(self):
        """Test que el formulario tiene crispy helper configurado."""
        form = FormPerson()
        assert hasattr(form, "helper")
        assert form.helper.form_id == "id-Person"

    def test_form_fields_present(self):
        """Test que todos los campos esperados están presentes."""
        form = FormPerson()
        expected_fields = [
            "first_name_1",
            "first_name_2",
            "last_name_1",
            "last_name_2",
            "document_type",
            "identification_person",
            "gender",
            "date_birth",
            "kinship",
            "social_insurance",
            "eps",
            "handicap",
            "education_level",
            "civil_state",
            "occupation",
            "cell_phone",
            "personal_email",
        ]

        for field_name in expected_fields:
            assert field_name in form.fields

    def test_form_optional_fields_can_be_empty(
        self,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que los campos opcionales pueden estar vacíos."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap

        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()

        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social="08", defaults={"affiliation": "Contributivo"}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps="008", defaults={"name_eps": "EPS Test 8"}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship="08", defaults={"description_kinship": "Sobrino"}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy="Hogar"
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap="N8", defaults={"handicap": "Ninguna"}
        )

        form_data = {
            "first_name_1": "Pedro",
            "first_name_2": "",  # Opcional vacío
            "last_name_1": "Martínez",
            "last_name_2": "",  # Opcional vacío
            "document_type": doc_type.id,
            "identification_person": "5555555555",
            "gender": gender.id,
            "date_birth": "1990-01-01",
            "kinship": kinship.id,
            "social_insurance": security_social.id,
            "eps": eps.id,
            "handicap": handicap.id,
            "education_level": education.id,
            "civil_state": civil_state.id,
            "occupation": occupancy.id,
            "cell_phone": "",  # Opcional vacío
            "personal_email": "",  # Opcional vacío
        }

        form = FormPerson(data=form_data)
        assert form.is_valid(), form.errors

