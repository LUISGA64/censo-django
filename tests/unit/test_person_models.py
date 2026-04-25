"""
Tests unitarios para el modelo Person.
"""
import pytest
from datetime import date
from censoapp.models import Person


@pytest.mark.django_db
class TestPersonModel:
    """Tests para el modelo Person."""

    def test_create_person_basic(
        self,
        create_family_card,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test crear persona básica."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap
        
        # Crear datos necesarios
        family = create_family_card()
        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()
        
        # Crear catalogos requeridos
        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social='01',
            defaults={'affiliation': 'Contributivo'}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps='001',
            defaults={'name_eps': 'EPS Test'}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship='01',
            defaults={'description_kinship': 'Hijo'}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy='Estudiante'
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap='N',
            defaults={'handicap': 'Ninguna'}
        )

        person = Person.objects.create(
            first_name_1="Juan",
            last_name_1="Pérez",
            identification_person="1234567890",
            date_birth=date(1990, 1, 1),
            family_card=family,
            gender=gender,
            document_type=doc_type,
            civil_state=civil_state,
            education_level=education,
            social_insurance=security_social,
            eps=eps,
            kinship=kinship,
            occupation=occupancy,
            handicap=handicap,
        )

        assert person.pk is not None
        assert person.first_name_1 == "Juan"
        assert person.last_name_1 == "Pérez"
        assert person.state is True  # Por defecto debe estar activo

    def test_person_full_name_in_str(
        self,
        create_family_card,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que __str__ muestra el nombre completo."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap
        
        family = create_family_card()
        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()
        
        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social='02',
            defaults={'affiliation': 'Subsidiado'}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps='002',
            defaults={'name_eps': 'EPS Test 2'}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship='02',
            defaults={'description_kinship': 'Padre'}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy='Empleado'
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap='N2',
            defaults={'handicap': 'Ninguna'}
        )

        person = Person.objects.create(
            first_name_1="María",
            first_name_2="Isabel",
            last_name_1="García",
            last_name_2="López",
            identification_person="9876543210",
            date_birth=date(1995, 5, 15),
            family_card=family,
            gender=gender,
            document_type=doc_type,
            civil_state=civil_state,
            education_level=education,
            social_insurance=security_social,
            eps=eps,
            kinship=kinship,
            occupation=occupancy,
            handicap=handicap,
        )

        # Verificar que __str__ contiene los nombres
        person_str = str(person)
        assert "María" in person_str
        assert "García" in person_str

    def test_person_family_head(
        self,
        create_family_card,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que una persona puede ser cabeza de familia."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap
        
        family = create_family_card()
        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()
        
        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social='03',
            defaults={'affiliation': 'Contributivo'}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps='003',
            defaults={'name_eps': 'EPS Test 3'}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship='03',
            defaults={'description_kinship': 'Jefe'}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy='Independiente'
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap='N3',
            defaults={'handicap': 'Ninguna'}
        )

        person = Person.objects.create(
            first_name_1="Pedro",
            last_name_1="Martínez",
            identification_person="1111111111",
            date_birth=date(1980, 3, 20),
            family_card=family,
            gender=gender,
            document_type=doc_type,
            civil_state=civil_state,
            education_level=education,
            social_insurance=security_social,
            eps=eps,
            kinship=kinship,
            occupation=occupancy,
            handicap=handicap,
            family_head=True,
        )

        assert person.family_head is True

    def test_person_belongs_to_family(
        self,
        create_family_card,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que persona pertenece a una familia."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap
        
        family = create_family_card()
        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()
        
        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social='04',
            defaults={'affiliation': 'Subsidiado'}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps='004',
            defaults={'name_eps': 'EPS Test 4'}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship='04',
            defaults={'description_kinship': 'Hermano'}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy='Desempleado'
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap='N4',
            defaults={'handicap': 'Ninguna'}
        )

        person = Person.objects.create(
            first_name_1="Ana",
            last_name_1="Rodríguez",
            identification_person="2222222222",
            date_birth=date(2000, 7, 10),
            family_card=family,
            gender=gender,
            document_type=doc_type,
            civil_state=civil_state,
            education_level=education,
            social_insurance=security_social,
            eps=eps,
            kinship=kinship,
            occupation=occupancy,
            handicap=handicap,
        )

        assert person.family_card == family
        assert person.family_card.organization is not None

    def test_person_state_default_active(
        self,
        create_family_card,
        create_gender,
        create_document_type,
        create_civil_state,
        create_education_level,
    ):
        """Test que por defecto las personas están activas."""
        from censoapp.models import SecuritySocial, Eps, Kinship, Occupancy, Handicap
        
        family = create_family_card()
        gender = create_gender()
        doc_type = create_document_type()
        civil_state = create_civil_state()
        education = create_education_level()
        
        security_social, _ = SecuritySocial.objects.get_or_create(
            code_security_social='05',
            defaults={'affiliation': 'Contributivo'}
        )
        eps, _ = Eps.objects.get_or_create(
            code_eps='005',
            defaults={'name_eps': 'EPS Test 5'}
        )
        kinship, _ = Kinship.objects.get_or_create(
            code_kinship='05',
            defaults={'description_kinship': 'Esposo'}
        )
        occupancy, _ = Occupancy.objects.get_or_create(
            description_occupancy='Pensionado'
        )
        handicap, _ = Handicap.objects.get_or_create(
            code_handicap='N5',
            defaults={'handicap': 'Ninguna'}
        )

        person = Person.objects.create(
            first_name_1="Carlos",
            last_name_1="González",
            identification_person="3333333333",
            date_birth=date(1985, 12, 25),
            family_card=family,
            gender=gender,
            document_type=doc_type,
            civil_state=civil_state,
            education_level=education,
            social_insurance=security_social,
            eps=eps,
            kinship=kinship,
            occupation=occupancy,
            handicap=handicap,
        )

        assert person.state is True


