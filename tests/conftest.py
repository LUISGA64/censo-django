"""
Configuración global para pytest.

Este archivo contiene fixtures compartidos y configuración
que se usará en todos los tests del proyecto.
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from censoapp.models import (
    Association,
    Organizations,
    Sidewalks,
    FamilyCard,
    UserProfile,
    Gender,
    CivilState,
    EducationLevel,
    DocumentType,
)


@pytest.fixture
def client():
    """Cliente de Django para hacer requests HTTP en tests."""
    return Client()


@pytest.fixture
def create_user(db):
    """
    Factory fixture para crear usuarios de prueba.

    Uso:
        def test_something(create_user):
            user = create_user(username="testuser")
    """

    def make_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        **kwargs
    ):
        return User.objects.create_user(
            username=username, email=email, password=password, **kwargs
        )

    return make_user


@pytest.fixture
def create_association(db):
    """Factory para crear asociaciones."""

    def make_association(name="Test Association", **kwargs):
        return Association.objects.create(
            association_name=name,
            association_identification=kwargs.get("identification", "123456789"),
            association_type_document="NIT",
            association_phone_mobile="3001234567",
            association_phone="1234567",
            association_address="Test Address",
            association_departament="Test Dept",
            association_email=kwargs.get("email", "test@test.com"),
            **{k: v for k, v in kwargs.items() if k not in ["identification", "email"]}
        )

    return make_association


@pytest.fixture
def create_organization(db, create_association):
    """Factory para crear organizaciones."""
    counter = 0

    def make_organization(name="Test Organization", association=None, **kwargs):
        nonlocal counter
        counter += 1
        
        if association is None:
            association = create_association()

        # Generar ID único si no se proporciona
        unique_id = kwargs.get("identification", f"{987654321 + counter}")

        return Organizations.objects.create(
            organization_name=name,
            organization_identification=unique_id,
            organization_territory="Test Territory",
            organization_email=kwargs.get("email", f"org{counter}@test.com"),
            organization_mobile_phone="3001234567",
            organization_phone="1234567",
            organization_address="Test Address",
            association_id=association,
            **{k: v for k, v in kwargs.items() if k not in ["identification", "email"]}
        )

    return make_organization


@pytest.fixture
def create_sidewalk(db, create_organization):
    """Factory para crear veredas."""

    def make_sidewalk(name="Test Sidewalk", organization=None, **kwargs):
        if organization is None:
            organization = create_organization()

        return Sidewalks.objects.create(
            sidewalk_name=name, organization_id=organization, **kwargs
        )

    return make_sidewalk


@pytest.fixture
def create_family_card(db, create_sidewalk, create_organization):
    """Factory para crear fichas familiares."""

    def make_family_card(sidewalk=None, organization=None, **kwargs):
        if organization is None:
            organization = create_organization()
        if sidewalk is None:
            sidewalk = create_sidewalk(organization=organization)

        return FamilyCard.objects.create(
            sidewalk_home=sidewalk,
            zone=kwargs.get("zone", "U"),
            organization=organization,
            address_home=kwargs.get("address", "Test Address"),
            latitude=kwargs.get("latitude", "0"),
            longitude=kwargs.get("longitude", "0"),
            **{
                k: v
                for k, v in kwargs.items()
                if k not in ["zone", "address", "latitude", "longitude"]
            }
        )

    return make_family_card


@pytest.fixture
def authenticated_user(db, client, create_user, create_organization):
    """
    Usuario autenticado con organización asignada.

    Retorna un diccionario con 'user', 'organization' y 'client' autenticado.
    """
    user = create_user()
    organization = create_organization()

    UserProfile.objects.create(user=user, organization=organization, role="ADMIN")

    client.force_login(user)

    return {"user": user, "organization": organization, "client": client}


@pytest.fixture
def create_gender(db):
    """Factory para crear géneros."""

    def make_gender(code="M", name="Masculino"):
        return Gender.objects.get_or_create(gender_code=code, defaults={"gender": name})[
            0
        ]

    return make_gender


@pytest.fixture
def create_civil_state(db):
    """Factory para crear estados civiles."""

    def make_civil_state(code="S", name="Soltero"):
        return CivilState.objects.get_or_create(
            code_state_civil=code, defaults={"state_civil": name}
        )[0]

    return make_civil_state


@pytest.fixture
def create_education_level(db):
    """Factory para crear niveles educativos."""

    def make_education_level(code="P", name="Primaria"):
        return EducationLevel.objects.get_or_create(
            code_education_level=code, defaults={"education_level": name}
        )[0]

    return make_education_level


@pytest.fixture
def create_document_type(db):
    """Factory para crear tipos de documento."""

    def make_document_type(code="CC", name="Cédula de Ciudadanía"):
        # El modelo correcto es IdentificationDocumentType
        from censoapp.models import IdentificationDocumentType
        return IdentificationDocumentType.objects.get_or_create(
            code_document_type=code, defaults={"document_type": name}
        )[0]

    return make_document_type



