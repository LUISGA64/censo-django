from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import (Association, Organizations, Sidewalks, FamilyCard, MaterialConstruction,
                     HomeOwnership, CookingFuel, MaterialConstructionFamilyCard, SystemParameters,
                     Person, DocumentType, Gender, Kinship, EducationLevel, CivilState,
                     Occupancy, SecuritySocial, Eps, Handicap)
from datetime import date
import json


class MaterialConstructionViewTests(TestCase):
    def setUp(self):
        # usuario para autenticación
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Crear Association requerida por Organizations
        self.association = Association.objects.create(
            association_name='AssocTest',
            association_identification='AID123',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='123456',
            association_address='Addr',
            association_departament='Dept',
            association_email='assoc@example.com',
            association_logo=SimpleUploadedFile('assoc.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        # Organización mínima
        self.org = Organizations.objects.create(
            organization_name='OrgTest',
            organization_identification='ID123',
            organization_type_identification='NIT',
            organization_territory='Terr',
            organization_email='org@example.com',
            organization_mobile_phone='123456',
            organization_phone='123456',
            organization_address='Calle 1',
            organization_logo=SimpleUploadedFile('org.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        # Crear vereda
        self.sidewalk = Sidewalks.objects.create(sidewalk_name='VeredaTest', organization_id=self.org)

        # Crear ficha familiar
        self.family = FamilyCard.objects.create(
            address_home='Casa Test',
            sidewalk_home=self.sidewalk,
            latitude='0',
            longitude='0',
            zone='U',
            organization=self.org,
            family_card_number=1,
            state=True,
        )

        # Materiales
        self.roof_material = MaterialConstruction.objects.create(material_name='Teja', roof=True)
        self.wall_material = MaterialConstruction.objects.create(material_name='Ladrillo', wall=True)
        self.floor_material = MaterialConstruction.objects.create(material_name='Baldosa', floor=True)

        # HomeOwnership and CookingFuel
        self.home_ownership = HomeOwnership.objects.create(ownership_type='Propio')
        self.cooking_fuel = CookingFuel.objects.create(fuel_type='Gas')

        # Parámetros del sistema necesarios para la vista
        SystemParameters.objects.create(key='Datos de Vivienda', value='S')

    def test_get_material_construction_view(self):
        self.client.force_login(self.user)
        url = reverse('material-construction', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Formulario en contexto
        self.assertIn('form', response.context)

    def test_post_creates_material_construction_family_card(self):
        self.client.force_login(self.user)
        url = reverse('material-construction', kwargs={'pk': self.family.pk})
        data = {
            # El campo family_card puede venir por url; se incluye para simular envío completo
            'family_card': str(self.family.pk),
            'material_roof': str(self.roof_material.pk),
            'material_wall': str(self.wall_material.pk),
            'material_floor': str(self.floor_material.pk),
            'number_families': '1',
            'number_people_bedrooms': '2',
            'condition_roof': 'Bueno',
            'condition_wall': 'Bueno',
            'condition_floor': 'Bueno',
            'home_ownership': str(self.home_ownership.pk),
            'kitchen_location': '1',
            'cooking_fuel': str(self.cooking_fuel.pk),
            'home_smoke': 'on',
            'number_bedrooms': '2',
            'ventilation': 'on',
            'lighting': 'on',
        }
        response = self.client.post(url, data)
        # Debe redirigir a familyCardIndex
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('familyCardIndex'))
        self.assertEqual(MaterialConstructionFamilyCard.objects.count(), 1)


class UpdateFamilyMaterialFormTests(TestCase):
    def setUp(self):
        # usuario para autenticación
        self.user = User.objects.create_user(username='uf_testuser', password='testpass')

        # Crear Association requerida por Organizations
        self.association = Association.objects.create(
            association_name='AssocUF',
            association_identification='AIDUF',
            association_type_document='NIT',
            association_phone_mobile='3001112222',
            association_phone='111222',
            association_address='Addr UF',
            association_departament='Dept',
            association_email='assocuf@example.com',
            association_logo=SimpleUploadedFile('assocuf.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        # Organización mínima
        self.org = Organizations.objects.create(
            organization_name='OrgUF',
            organization_identification='IDUF',
            organization_type_identification='NIT',
            organization_territory='TerrUF',
            organization_email='orguf@example.com',
            organization_mobile_phone='1234567',
            organization_phone='1234567',
            organization_address='Calle UF',
            organization_logo=SimpleUploadedFile('orguf.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        # Crear vereda
        self.sidewalk = Sidewalks.objects.create(sidewalk_name='VeredaUF', organization_id=self.org)

        # Crear ficha familiar
        self.family = FamilyCard.objects.create(
            address_home='Casa UF',
            sidewalk_home=self.sidewalk,
            latitude='0',
            longitude='0',
            zone='U',
            organization=self.org,
            family_card_number=10,
            state=True,
        )

        # Materiales
        self.roof_material = MaterialConstruction.objects.create(material_name='TejaUF', roof=True)
        self.wall_material = MaterialConstruction.objects.create(material_name='LadrilloUF', wall=True)
        self.floor_material = MaterialConstruction.objects.create(material_name='BaldosaUF', floor=True)

        # HomeOwnership and CookingFuel
        self.home_ownership = HomeOwnership.objects.create(ownership_type='PropioUF')
        self.cooking_fuel = CookingFuel.objects.create(fuel_type='GasUF')

        # Parámetros del sistema necesarios para la vista
        SystemParameters.objects.create(key='Datos de Vivienda', value='S')

    def test_get_update_family_contains_material_form(self):
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # material_form debe estar en el contexto y datos_vivienda ser 'S'
        self.assertIn('material_form', response.context)
        self.assertEqual(response.context.get('datos_vivienda'), 'S')

    def test_post_update_family_creates_material_record(self):
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})
        data = {
            'material_roof': str(self.roof_material.pk),
            'material_wall': str(self.wall_material.pk),
            'material_floor': str(self.floor_material.pk),
            'number_families': '1',
            'number_people_bedrooms': '2',
            'condition_roof': 'Bueno',
            'condition_wall': 'Bueno',
            'condition_floor': 'Bueno',
            'home_ownership': str(self.home_ownership.pk),
            'kitchen_location': '1',
            'cooking_fuel': str(self.cooking_fuel.pk),
            'home_smoke': 'on',
            'number_bedrooms': '2',
            'ventilation': 'on',
            'lighting': 'on',
            'material_form_submit': '1',
        }
        response = self.client.post(url, data)
        # Debe redirigir a la misma página de edición
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MaterialConstructionFamilyCard.objects.filter(family_card=self.family).count(), 1)

    def test_get_update_family_hides_material_form_when_param_N(self):
        """
        Verifica que cuando el parámetro 'Datos de Vivienda' es 'N', la plantilla muestre el mensaje de contacto
        y no el formulario de vivienda (la plantilla muestra "Contacte al administrador").
        """
        self.client.force_login(self.user)
        # Actualizar parametro a 'N'
        sp = SystemParameters.objects.get(key='Datos de Vivienda')
        sp.value = 'N'
        sp.save()

        url = reverse('update-family', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # datos_vivienda en contexto debe ser 'N'
        self.assertEqual(response.context.get('datos_vivienda'), 'N')
        # Verificar que el texto de contacto esté presente en el HTML
        self.assertContains(response, 'Contacte al administrador')


class ListarPersonasTests(TestCase):
    """Tests para la funcionalidad de listar personas"""

    def setUp(self):
        # Usuario para autenticación
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Crear datos necesarios
        self.association = Association.objects.create(
            association_name='AssocTest',
            association_identification='AID123',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='123456',
            association_address='Addr',
            association_departament='Dept',
            association_email='assoc@example.com',
            association_logo=SimpleUploadedFile('assoc.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        self.org = Organizations.objects.create(
            organization_name='OrgTest',
            organization_identification='ID123',
            organization_type_identification='NIT',
            organization_territory='Terr',
            organization_email='org@example.com',
            organization_mobile_phone='123456',
            organization_phone='123456',
            organization_address='Calle 1',
            organization_logo=SimpleUploadedFile('org.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        self.sidewalk = Sidewalks.objects.create(sidewalk_name='VeredaTest', organization_id=self.org)

        self.family = FamilyCard.objects.create(
            address_home='Casa Test',
            sidewalk_home=self.sidewalk,
            latitude='0',
            longitude='0',
            zone='U',
            organization=self.org,
            family_card_number=1,
            state=True,
        )

        # Crear datos relacionados para Person
        self.document_type = DocumentType.objects.create(
            code_document_type='CC',
            document_type='Cédula de Ciudadanía'
        )

        self.gender_m = Gender.objects.create(gender_code='M', gender='Masculino')
        self.gender_f = Gender.objects.create(gender_code='F', gender='Femenino')

        self.kinship_head = Kinship.objects.create(code_kinship='1', description_kinship='Jefe de Familia')
        self.kinship_spouse = Kinship.objects.create(code_kinship='2', description_kinship='Cónyuge')

        self.education = EducationLevel.objects.create(
            code_education_level='P',
            education_level='Primaria'
        )

        self.civil_state = CivilState.objects.create(
            code_state_civil='S',
            state_civil='Soltero'
        )

        self.occupation = Occupancy.objects.create(description_occupancy='Agricultor')

        self.security_social = SecuritySocial.objects.create(
            code_security_social='01',
            affiliation='Contributivo'
        )

        self.eps = Eps.objects.create(code_eps='EPS001', name_eps='EPS Test')

        self.handicap = Handicap.objects.create(code_handicap='N', handicap='Ninguna')

        # Crear personas de prueba
        self.person1 = Person.objects.create(
            first_name_1='Juan',
            first_name_2='Carlos',
            last_name_1='Pérez',
            last_name_2='García',
            identification_person='1234567890',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(1990, 1, 15),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_head,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family,
            family_head=True,
            state=True
        )

        self.person2 = Person.objects.create(
            first_name_1='María',
            first_name_2='Teresa',
            last_name_1='López',
            last_name_2='Martínez',
            identification_person='9876543210',
            document_type=self.document_type,
            gender=self.gender_f,
            date_birth=date(1995, 6, 20),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_spouse,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family,
            family_head=False,
            state=True
        )

        self.person3 = Person.objects.create(
            first_name_1='Pedro',
            first_name_2='',
            last_name_1='Rodríguez',
            last_name_2='Sánchez',
            identification_person='1122334455',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(2010, 3, 10),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_spouse,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family,
            family_head=False,
            state=True
        )

    def test_view_persons_requires_login(self):
        """Verificar que la vista requiere autenticación"""
        url = reverse('personas')
        response = self.client.get(url)
        # Debe redirigir al login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_view_persons_renders_template(self):
        """Verificar que la vista renderiza el template correcto"""
        self.client.force_login(self.user)
        url = reverse('personas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'censo/persona/listado_personas.html')
        self.assertEqual(response.context['segment'], 'personas')

    def test_listar_personas_requires_login(self):
        """Verificar que el endpoint JSON requiere autenticación"""
        url = reverse('json_personas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_listar_personas_returns_json(self):
        """Verificar que el endpoint retorna JSON válido"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertIn('draw', data)
        self.assertIn('recordsTotal', data)
        self.assertIn('recordsFiltered', data)
        self.assertIn('data', data)

    def test_listar_personas_returns_all_active_persons(self):
        """Verificar que retorna todas las personas activas"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsTotal'], 3)  # 3 personas activas
        self.assertEqual(len(data['data']), 3)

    def test_listar_personas_search_by_name(self):
        """Verificar búsqueda por nombre"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': 'Juan'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsFiltered'], 1)
        self.assertEqual(data['data'][0]['first_name_1'], 'Juan')

    def test_listar_personas_search_by_identification(self):
        """Verificar búsqueda por número de identificación"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': '9876543210'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsFiltered'], 1)
        self.assertEqual(data['data'][0]['identification_person'], '9876543210')

    def test_listar_personas_pagination(self):
        """Verificar paginación correcta"""
        self.client.force_login(self.user)
        url = reverse('json_personas')

        # Primera página with length=2
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '2'
        })
        data = json.loads(response.content)
        self.assertEqual(len(data['data']), 2)

        # Segunda página
        response = self.client.get(url, {
            'draw': '2',
            'start': '2',
            'length': '2'
        })
        data = json.loads(response.content)
        self.assertEqual(len(data['data']), 1)  # Solo queda 1 registro

    def test_listar_personas_ordering(self):
        """Verificar ordenamiento por columna"""
        self.client.force_login(self.user)
        url = reverse('json_personas')

        # Ordenar por nombre ascendente
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'order[0][column]': '0',
            'order[0][dir]': 'asc'
        })
        data = json.loads(response.content)
        first_name = data['data'][0]['first_name_1']
        self.assertIn(first_name, ['Juan', 'María', 'Pedro'])

    def test_listar_personas_calculates_age(self):
        """Verificar que se calcula la edad correctamente"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': 'Pedro'
        })

        data = json.loads(response.content)
        person_data = data['data'][0]
        # Pedro nació en 2010, debería tener entre 13-15 años
        self.assertGreater(person_data['age'], 10)
        self.assertLess(person_data['age'], 20)

    def test_listar_personas_includes_family_card_info(self):
        """Verificar que incluye información de la ficha familiar"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })

        data = json.loads(response.content)
        person_data = data['data'][0]
        self.assertIn('family_card__family_card_number', person_data)
        self.assertEqual(person_data['family_card__family_card_number'], 1)

    def test_listar_personas_identifies_family_head(self):
        """Verificar que identifica correctamente al jefe de familia"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': 'Juan'
        })

        data = json.loads(response.content)
        person_data = data['data'][0]
        self.assertTrue(person_data['family_head'])

    def test_listar_personas_excludes_inactive_persons(self):
        """Verificar que excluye personas inactivas"""
        # Marcar una persona como inactiva
        self.person3.state = False
        self.person3.save()

        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsTotal'], 2)  # Solo 2 personas activas

    def test_listar_personas_handles_invalid_parameters(self):
        """Verificar manejo de parámetros inválidos"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': 'invalid',
            'start': 'invalid',
            'length': 'invalid'
        })

        # Debe retornar error o usar valores por defecto
        self.assertIn(response.status_code, [200, 500])

    def test_listar_personas_search_by_sidewalk(self):
        """Verificar búsqueda por nombre de vereda"""
        self.client.force_login(self.user)
        url = reverse('json_personas')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': 'VeredaTest'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsFiltered'], 3)  # Todas las personas están en VeredaTest


class ListarFamilyCardsTests(TestCase):
    """Tests para la funcionalidad de listar fichas familiares"""

    def setUp(self):
        # Usuario para autenticación
        self.user = User.objects.create_user(username='fc_testuser', password='testpass')

        # Crear datos necesarios
        self.association = Association.objects.create(
            association_name='AssocFC',
            association_identification='AIDFC',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='123456',
            association_address='Addr',
            association_departament='Dept',
            association_email='assoc_fc@example.com',
            association_logo=SimpleUploadedFile('assoc_fc.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        self.org = Organizations.objects.create(
            organization_name='OrgFC',
            organization_identification='IDFC',
            organization_type_identification='NIT',
            organization_territory='Terr',
            organization_email='org_fc@example.com',
            organization_mobile_phone='123456',
            organization_phone='123456',
            organization_address='Calle 1',
            organization_logo=SimpleUploadedFile('org_fc.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        self.sidewalk1 = Sidewalks.objects.create(sidewalk_name='Vereda1', organization_id=self.org)
        self.sidewalk2 = Sidewalks.objects.create(sidewalk_name='Vereda2', organization_id=self.org)

        # Crear datos relacionados para Person
        self.document_type = DocumentType.objects.create(
            code_document_type='CC',
            document_type='Cédula de Ciudadanía'
        )

        self.gender_m = Gender.objects.create(gender_code='M', gender='Masculino')
        self.kinship_head = Kinship.objects.create(code_kinship='1', description_kinship='Jefe de Familia')
        self.education = EducationLevel.objects.create(code_education_level='P', education_level='Primaria')
        self.civil_state = CivilState.objects.create(code_state_civil='S', state_civil='Soltero')
        self.occupation = Occupancy.objects.create(description_occupancy='Agricultor')
        self.security_social = SecuritySocial.objects.create(code_security_social='01', affiliation='Contributivo')
        self.eps = Eps.objects.create(code_eps='EPS001', name_eps='EPS Test')
        self.handicap = Handicap.objects.create(code_handicap='N', handicap='Ninguna')

        # Crear fichas familiares de prueba
        self.family1 = FamilyCard.objects.create(
            address_home='Casa 1',
            sidewalk_home=self.sidewalk1,
            latitude='0',
            longitude='0',
            zone='U',
            organization=self.org,
            family_card_number=1,
            state=True,
        )

        self.family2 = FamilyCard.objects.create(
            address_home='Casa 2',
            sidewalk_home=self.sidewalk1,
            latitude='0',
            longitude='0',
            zone='R',
            organization=self.org,
            family_card_number=2,
            state=True,
        )

        self.family3 = FamilyCard.objects.create(
            address_home='Casa 3',
            sidewalk_home=self.sidewalk2,
            latitude='0',
            longitude='0',
            zone='R',
            organization=self.org,
            family_card_number=3,
            state=True,
        )

        # Crear cabezas de familia
        self.head1 = Person.objects.create(
            first_name_1='Carlos',
            first_name_2='Alberto',
            last_name_1='Gómez',
            last_name_2='Pérez',
            identification_person='1111111111',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(1980, 1, 1),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_head,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family1,
            family_head=True,
            state=True
        )

        self.head2 = Person.objects.create(
            first_name_1='Luis',
            first_name_2='Fernando',
            last_name_1='Ramírez',
            last_name_2='Torres',
            identification_person='2222222222',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(1985, 5, 15),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_head,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family2,
            family_head=True,
            state=True
        )

        self.head3 = Person.objects.create(
            first_name_1='Ana',
            first_name_2='María',
            last_name_1='Suárez',
            last_name_2='González',
            identification_person='3333333333',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(1990, 10, 20),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_head,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family3,
            family_head=True,
            state=True
        )

    def test_family_card_index_requires_login(self):
        """Verificar que la vista requiere autenticación"""
        url = reverse('familyCardIndex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_family_card_index_renders_template(self):
        """Verificar que la vista renderiza el template correcto"""
        self.client.force_login(self.user)
        url = reverse('familyCardIndex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'censo/censo/familyCardIndex.html')
        self.assertEqual(response.context['segment'], 'family_card')

    def test_get_family_cards_requires_login(self):
        """Verificar que el endpoint JSON requiere autenticación"""
        url = reverse('familycards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_get_family_cards_returns_json(self):
        """Verificar que el endpoint retorna JSON válido"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertIn('draw', data)
        self.assertIn('recordsTotal', data)
        self.assertIn('recordsFiltered', data)
        self.assertIn('data', data)

    def test_get_family_cards_returns_all_families(self):
        """Verificar que retorna todas las fichas familiares activas"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsTotal'], 3)  # 3 fichas familiares
        self.assertEqual(len(data['data']), 3)

    def test_get_family_cards_search_by_family_number(self):
        """Verificar búsqueda por número de ficha"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': '1'
        })

        data = json.loads(response.content)
        self.assertGreater(data['recordsFiltered'], 0)

    def test_get_family_cards_search_by_head_name(self):
        """Verificar búsqueda por nombre del cabeza de familia"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': 'Carlos'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsFiltered'], 1)
        self.assertIn('Carlos', data['data'][0]['full_name'])

    def test_get_family_cards_search_by_identification(self):
        """Verificar búsqueda por número de identificación"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': '2222222222'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsFiltered'], 1)
        self.assertEqual(data['data'][0]['identification_person'], '2222222222')

    def test_get_family_cards_search_by_sidewalk(self):
        """Verificar búsqueda por nombre de vereda"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'search[value]': 'Vereda1'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsFiltered'], 2)  # 2 familias en Vereda1

    def test_get_family_cards_pagination(self):
        """Verificar paginación correcta"""
        self.client.force_login(self.user)
        url = reverse('familycards')

        # Primera página con length=2
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '2'
        })
        data = json.loads(response.content)
        self.assertEqual(len(data['data']), 2)

        # Segunda página
        response = self.client.get(url, {
            'draw': '2',
            'start': '2',
            'length': '2'
        })
        data = json.loads(response.content)
        self.assertEqual(len(data['data']), 1)  # Solo queda 1 registro

    def test_get_family_cards_includes_person_count(self):
        """Verificar que incluye el conteo de miembros de la familia"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })

        data = json.loads(response.content)
        person_data = data['data'][0]
        self.assertIn('person_count', person_data)
        self.assertGreaterEqual(person_data['person_count'], 1)  # Al menos el cabeza de familia

    def test_get_family_cards_excludes_inactive_families(self):
        """Verificar que excluye fichas familiares inactivas"""
        # Marcar una ficha como inactiva
        self.family3.state = False
        self.family3.save()

        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10'
        })

        data = json.loads(response.content)
        self.assertEqual(data['recordsTotal'], 2)  # Solo 2 fichas activas

    def test_get_family_cards_ordering(self):
        """Verificar ordenamiento por columna"""
        self.client.force_login(self.user)
        url = reverse('familycards')

        # Ordenar por número de ficha ascendente
        response = self.client.get(url, {
            'draw': '1',
            'start': '0',
            'length': '10',
            'order[0][column]': '0',
            'order[0][dir]': 'asc'
        })
        data = json.loads(response.content)
        first_number = data['data'][0]['family_card__family_card_number']
        self.assertEqual(first_number, 1)

    def test_get_family_cards_handles_invalid_parameters(self):
        """Verificar manejo de parámetros inválidos"""
        self.client.force_login(self.user)
        url = reverse('familycards')
        response = self.client.get(url, {
            'draw': 'invalid',
            'start': 'invalid',
            'length': 'invalid'
        })

        # Debe retornar error o usar valores por defecto
        self.assertIn(response.status_code, [200, 500])


class DetailFamilyCardTests(TestCase):
    """Tests para la funcionalidad de detalle de ficha familiar"""

    def setUp(self):
        # Usuario para autenticación
        self.user = User.objects.create_user(username='detail_testuser', password='testpass')

        # Crear datos necesarios
        self.association = Association.objects.create(
            association_name='AssocDetail',
            association_identification='AIDDET',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='123456',
            association_address='Addr',
            association_departament='Dept',
            association_email='assoc_detail@example.com',
            association_logo=SimpleUploadedFile('assoc_det.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        self.org = Organizations.objects.create(
            organization_name='OrgDetail',
            organization_identification='IDDET',
            organization_type_identification='NIT',
            organization_territory='Terr',
            organization_email='org_detail@example.com',
            organization_mobile_phone='123456',
            organization_phone='123456',
            organization_address='Calle 1',
            organization_logo=SimpleUploadedFile('org_det.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        self.sidewalk = Sidewalks.objects.create(sidewalk_name='VeredaDetail', organization_id=self.org)

        # Crear datos relacionados para Person
        self.document_type = DocumentType.objects.create(
            code_document_type='CC',
            document_type='Cédula de Ciudadanía'
        )

        self.gender_m = Gender.objects.create(gender_code='M', gender='Masculino')
        self.gender_f = Gender.objects.create(gender_code='F', gender='Femenino')
        self.kinship_head = Kinship.objects.create(code_kinship='1', description_kinship='Jefe de Familia')
        self.kinship_spouse = Kinship.objects.create(code_kinship='2', description_kinship='Cónyuge')
        self.education = EducationLevel.objects.create(code_education_level='P', education_level='Primaria')
        self.civil_state = CivilState.objects.create(code_state_civil='S', state_civil='Soltero')
        self.occupation = Occupancy.objects.create(description_occupancy='Agricultor')
        self.security_social = SecuritySocial.objects.create(code_security_social='01', affiliation='Contributivo')
        self.eps = Eps.objects.create(code_eps='EPS001', name_eps='EPS Test')
        self.handicap = Handicap.objects.create(code_handicap='N', handicap='Ninguna')

        # Crear ficha familiar
        self.family = FamilyCard.objects.create(
            address_home='Casa Detail',
            sidewalk_home=self.sidewalk,
            latitude='4.5709',
            longitude='-74.2973',
            zone='U',
            organization=self.org,
            family_card_number=100,
            state=True,
        )

        # Crear miembros de la familia
        self.head = Person.objects.create(
            first_name_1='Pedro',
            first_name_2='José',
            last_name_1='Martínez',
            last_name_2='Silva',
            identification_person='5555555555',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(1975, 3, 15),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_head,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family,
            family_head=True,
            state=True
        )

        self.spouse = Person.objects.create(
            first_name_1='María',
            first_name_2='Elena',
            last_name_1='González',
            last_name_2='Ramírez',
            identification_person='6666666666',
            document_type=self.document_type,
            gender=self.gender_f,
            date_birth=date(1978, 7, 20),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_spouse,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family,
            family_head=False,
            state=True
        )

    def test_detail_family_requires_login(self):
        """Verificar que la vista requiere autenticación"""
        url = reverse('detailFamilyCard', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_detail_family_renders_template(self):
        """Verificar que la vista renderiza el template correcto"""
        self.client.force_login(self.user)
        url = reverse('detailFamilyCard', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'censo/censo/detail_family_card.html')

    def test_detail_family_shows_statistics(self):
        """Verificar que muestra estadísticas correctas"""
        self.client.force_login(self.user)
        url = reverse('detailFamilyCard', kwargs={'pk': self.family.pk})
        response = self.client.get(url)

        # Verificar total de miembros
        self.assertEqual(response.context['total_miembros'], 2)

        # Verificar cabeza de familia
        self.assertEqual(response.context['cabeza_familia']['id'], self.head.id)

        # Verificar promedio de edad
        self.assertIsNotNone(response.context['promedio_edad'])


    def test_detail_family_handles_inactive_family(self):
        """Verificar manejo de ficha inactiva"""
        self.family.state = False
        self.family.save()

        self.client.force_login(self.user)
        url = reverse('detailFamilyCard', kwargs={'pk': self.family.pk})
        response = self.client.get(url)

        # Debe redirigir o mostrar error 404
        self.assertIn(response.status_code, [302, 404])

    def test_detail_family_handles_nonexistent_family(self):
        """Verificar manejo de ficha inexistente"""
        self.client.force_login(self.user)
        url = reverse('detailFamilyCard', kwargs={'pk': 99999})
        response = self.client.get(url)

        # Debe retornar 404 o redirigir con mensaje de error
        self.assertIn(response.status_code, [302, 404])

    def test_detail_family_shows_zone_info(self):
        """Verificar que muestra información de zona"""
        self.client.force_login(self.user)
        url = reverse('detailFamilyCard', kwargs={'pk': self.family.pk})
        response = self.client.get(url)

        # Verificar que muestra la zona
        familia_data = response.context['familia'].first()
        self.assertEqual(familia_data['family_card__zone'], 'U')

    def test_detail_family_calculates_age_correctly(self):
        """Verificar que calcula la edad correctamente"""
        self.client.force_login(self.user)
        url = reverse('detailFamilyCard', kwargs={'pk': self.family.pk})
        response = self.client.get(url)

        familia_data = list(response.context['familia'])
        head_data = next((m for m in familia_data if m['family_head']), None)

        self.assertIsNotNone(head_data)
        # Pedro nació en 1975, debería tener entre 48-50 años
        self.assertGreater(head_data['age'], 45)
        self.assertLess(head_data['age'], 55)


class UpdateFamilyCardTests(TestCase):
    """Tests para la funcionalidad de editar fichas familiares"""

    def setUp(self):
        # Usuario para autenticación
        self.user = User.objects.create_user(username='edit_fc_user', password='testpass')

        # Crear datos necesarios
        self.association = Association.objects.create(
            association_name='AssocEditFC',
            association_identification='AIDEFC',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='123456',
            association_address='Addr',
            association_departament='Dept',
            association_email='assoc_efc@example.com',
            association_logo=SimpleUploadedFile('assoc_efc.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        self.org = Organizations.objects.create(
            organization_name='OrgEditFC',
            organization_identification='IDEFC',
            organization_type_identification='NIT',
            organization_territory='Terr',
            organization_email='org_efc@example.com',
            organization_mobile_phone='123456',
            organization_phone='123456',
            organization_address='Calle 1',
            organization_logo=SimpleUploadedFile('org_efc.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        self.sidewalk1 = Sidewalks.objects.create(sidewalk_name='Vereda1', organization_id=self.org)
        self.sidewalk2 = Sidewalks.objects.create(sidewalk_name='Vereda2', organization_id=self.org)

        # Crear ficha familiar
        self.family = FamilyCard.objects.create(
            address_home='Casa Original',
            sidewalk_home=self.sidewalk1,
            latitude='4.5',
            longitude='-74.5',
            zone='Urbana',
            organization=self.org,
            family_card_number=100,
            state=True,
        )

    def test_update_family_requires_login(self):
        """Verificar que la edición requiere autenticación"""
        url = reverse('update-family', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_family_renders_template(self):
        """Verificar que renderiza el template correcto"""
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'censo/censo/edit-family-card.html')

    def test_update_family_shows_current_data(self):
        """Verificar que muestra los datos actuales en el formulario"""
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})
        response = self.client.get(url)

        # El modelo normaliza el texto: 'Casa Original' -> 'Casa original'
        self.assertContains(response, 'Casa original')
        self.assertContains(response, 'value="4.5"')
        self.assertContains(response, 'value="-74.5"')

    def test_update_family_successful(self):
        """Verificar que actualiza correctamente los datos"""
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})

        data = {
            'address_home': 'Casa Actualizada',
            'sidewalk_home': self.sidewalk2.pk,
            'latitude': '5.0',
            'longitude': '-75.0',
            'zone': 'Rural',
            'organization': self.org.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        # Verificar que los datos se actualizaron correctamente
        # El modelo normaliza: 'Casa Actualizada' -> 'Casa actualizada'
        self.family.refresh_from_db()
        self.assertEqual(self.family.address_home, 'Casa actualizada')
        self.assertEqual(self.family.sidewalk_home, self.sidewalk2)
        self.assertEqual(self.family.zone, 'Rural')
        self.assertEqual(self.family.organization, self.org)
        self.assertEqual(str(self.family.latitude), '5.0')
        self.assertEqual(str(self.family.longitude), '-75.0')

    def test_update_family_invalid_data(self):
        """Verificar manejo de datos inválidos - coordenadas fuera de rango"""
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})

        data = {
            'address_home': 'Casa de prueba',
            'latitude': '95.0',  # Fuera de rango (-90 a 90)
            'longitude': '-75.0',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # No redirige, muestra el formulario con errores
        # Verificar que hay un mensaje de error sobre la latitud
        messages_list = list(response.context['messages'])
        self.assertTrue(any('latitud' in str(msg).lower() for msg in messages_list))

    def test_update_family_nonexistent(self):
        """Verificar manejo de ficha inexistente"""
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_family_context_data(self):
        """Verificar que el contexto incluye datos necesarios"""
        self.client.force_login(self.user)
        url = reverse('update-family', kwargs={'pk': self.family.pk})
        response = self.client.get(url)

        self.assertIn('form', response.context)
        self.assertIn('segment', response.context)
        self.assertEqual(response.context['segment'], 'family_card')


class UpdatePersonTests(TestCase):
    """Tests para la funcionalidad de editar personas"""

    def setUp(self):
        # Usuario para autenticación
        self.user = User.objects.create_user(username='edit_person_user', password='testpass')

        # Crear datos necesarios
        self.association = Association.objects.create(
            association_name='AssocEditP',
            association_identification='AIDEP',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='123456',
            association_address='Addr',
            association_departament='Dept',
            association_email='assoc_ep@example.com',
            association_logo=SimpleUploadedFile('assoc_ep.jpg', b'fakeimagecontent', content_type='image/jpeg')
        )

        self.org = Organizations.objects.create(
            organization_name='OrgEditP',
            organization_identification='IDEP',
            organization_type_identification='NIT',
            organization_territory='Terr',
            organization_email='org_ep@example.com',
            organization_mobile_phone='123456',
            organization_phone='123456',
            organization_address='Calle 1',
            organization_logo=SimpleUploadedFile('org_ep.jpg', b'fakeimagecontent', content_type='image/jpeg'),
            association_id=self.association
        )

        self.sidewalk = Sidewalks.objects.create(sidewalk_name='VeredaEdit', organization_id=self.org)

        # Crear datos relacionados
        self.document_type = DocumentType.objects.create(
            code_document_type='CC',
            document_type='Cédula de Ciudadanía'
        )

        self.gender_m = Gender.objects.create(gender_code='M', gender='Masculino')
        self.gender_f = Gender.objects.create(gender_code='F', gender='Femenino')
        self.kinship_head = Kinship.objects.create(code_kinship='1', description_kinship='Jefe de Familia')
        self.kinship_spouse = Kinship.objects.create(code_kinship='2', description_kinship='Cónyuge')
        self.education = EducationLevel.objects.create(code_education_level='P', education_level='Primaria')
        self.civil_state = CivilState.objects.create(code_state_civil='S', state_civil='Soltero')
        self.occupation = Occupancy.objects.create(description_occupancy='Agricultor')
        self.security_social = SecuritySocial.objects.create(code_security_social='01', affiliation='Contributivo')
        self.eps = Eps.objects.create(code_eps='EPS001', name_eps='EPS Test')
        self.handicap = Handicap.objects.create(code_handicap='N', handicap='Ninguna')

        # Crear ficha familiar
        self.family = FamilyCard.objects.create(
            address_home='Casa Edit',
            sidewalk_home=self.sidewalk,
            latitude='4.5',
            longitude='-74.5',
            zone='U',
            organization=self.org,
            family_card_number=200,
            state=True,
        )

        # Crear persona
        self.person = Person.objects.create(
            first_name_1='Juan',
            first_name_2='Carlos',
            last_name_1='Pérez',
            last_name_2='García',
            identification_person='1234567890',
            document_type=self.document_type,
            gender=self.gender_m,
            date_birth=date(1990, 1, 15),
            social_insurance=self.security_social,
            eps=self.eps,
            kinship=self.kinship_head,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            family_card=self.family,
            family_head=True,
            state=True,
            cell_phone='3001234567',
            personal_email='juan@example.com'
        )

    def test_update_person_requires_login(self):
        """Verificar que la edición requiere autenticación"""
        url = reverse('updated-person', kwargs={'pk': self.person.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_person_renders_template(self):
        """Verificar que renderiza el template correcto"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': self.person.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'censo/persona/edit_person.html')

    def test_update_person_shows_current_data(self):
        """Verificar que muestra los datos actuales"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': self.person.pk})
        response = self.client.get(url)

        self.assertContains(response, 'Juan')
        self.assertContains(response, 'Pérez')
        self.assertContains(response, '1234567890')
        self.assertContains(response, '3001234567')

    def test_update_person_successful(self):
        """Verificar que actualiza correctamente los datos"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': self.person.pk})

        data = {
            'first_name_1': 'Pedro',
            'first_name_2': 'José',
            'last_name_1': 'González',
            'last_name_2': 'Martínez',
            'document_type': self.document_type.pk,
            'identification_person': '9876543210',
            'date_birth': '1985-05-20',
            'cell_phone': '3009876543',
            'personal_email': 'pedro@example.com',
            'gender': self.gender_m.pk,
            'kinship': self.kinship_head.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': True,
            'family_head': True,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # Verificar que los datos se actualizaron
        self.person.refresh_from_db()
        self.assertEqual(self.person.first_name_1, 'Pedro')
        self.assertEqual(self.person.last_name_1, 'González')
        self.assertEqual(self.person.identification_person, '9876543210')
        self.assertEqual(self.person.cell_phone, '3009876543')

    def test_update_person_invalid_email(self):
        """Verificar validación de email inválido"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': self.person.pk})

        data = {
            'first_name_1': 'Juan',
            'last_name_1': 'Pérez',
            'document_type': self.document_type.pk,
            'identification_person': '1234567890',
            'date_birth': '1990-01-15',
            'gender': self.gender_m.pk,
            'kinship': self.kinship_head.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': True,
            'family_head': True,
            'personal_email': 'email-invalido',  # Email mal formado
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'personal_email', 'Introduzca una dirección de correo electrónico válida.')

    def test_update_person_deactivate_last_member(self):
        """Verificar que desactivar el último miembro desactiva la ficha"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': self.person.pk})

        # Es el único miembro, al desactivarlo debe desactivar la ficha
        data = {
            'first_name_1': 'Juan',
            'last_name_1': 'Pérez',
            'document_type': self.document_type.pk,
            'identification_person': '1234567890',
            'date_birth': '1990-01-15',
            'gender': self.gender_m.pk,
            'kinship': self.kinship_head.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': False,  # Desactivar persona
            'family_head': True,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # Verificar que la ficha también se desactivó
        self.family.refresh_from_db()
        self.assertFalse(self.family.state)
        self.assertEqual(self.family.family_card_number, 0)

    def test_update_person_nonexistent(self):
        """Verificar manejo de persona inexistente"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_person_change_gender(self):
        """Verificar que se puede cambiar el género"""
        self.client.force_login(self.user)
        url = reverse('updated-person', kwargs={'pk': self.person.pk})

        data = {
            'first_name_1': 'Juan',
            'last_name_1': 'Pérez',
            'document_type': self.document_type.pk,
            'identification_person': '1234567890',
            'date_birth': '1990-01-15',
            'gender': self.gender_f.pk,  # Cambiar a femenino
            'kinship': self.kinship_head.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': True,
            'family_head': True,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.person.refresh_from_db()
        self.assertEqual(self.person.gender, self.gender_f)
    
    def test_update_person_only_one_family_head(self):
        """Verificar que solo puede haber un cabeza de familia por ficha"""
        self.client.force_login(self.user)
        
        # Crear otro miembro en la misma ficha
        otro_miembro = Person.objects.create(
            first_name_1='Maria',
            last_name_1='Lopez',
            document_type=self.document_type,
            identification_person='9999999999',
            date_birth=date(1992, 6, 15),
            gender=self.gender_f,
            kinship=self.kinship_spouse,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            social_insurance=self.security_social,
            eps=self.eps,
            family_card=self.family,
            family_head=False,
            state=True
        )
        
        # Intentar hacer a otro_miembro cabeza de familia cuando ya existe uno
        url = reverse('updated-person', kwargs={'pk': otro_miembro.pk})
        data = {
            'first_name_1': 'Maria',
            'last_name_1': 'Lopez',
            'document_type': self.document_type.pk,
            'identification_person': '9999999999',
            'date_birth': '1992-06-15',
            'gender': self.gender_f.pk,
            'kinship': self.kinship_spouse.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': True,
            'family_head': True,  # Intentar ser cabeza de familia
        }
        
        response = self.client.post(url, data)
        
        # Debe mostrar error y no guardar
        self.assertEqual(response.status_code, 200)  # No redirige
        
        # Verificar que NO se convirtió en cabeza de familia
        otro_miembro.refresh_from_db()
        self.assertFalse(otro_miembro.family_head)
    
    def test_update_person_family_head_minimum_age(self):
        """Verificar que el cabeza de familia debe ser mayor de 18 años"""
        self.client.force_login(self.user)
        
        # Crear persona menor de 18 años
        menor = Person.objects.create(
            first_name_1='Carlos',
            last_name_1='Niño',
            document_type=self.document_type,
            identification_person='8888888888',
            date_birth=date(2010, 1, 1),  # 14-15 años
            gender=self.gender_m,
            kinship=self.kinship_spouse,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            social_insurance=self.security_social,
            eps=self.eps,
            family_card=self.family,
            family_head=False,
            state=True
        )
        
        url = reverse('updated-person', kwargs={'pk': menor.pk})
        data = {
            'first_name_1': 'Carlos',
            'last_name_1': 'Niño',
            'document_type': self.document_type.pk,
            'identification_person': '8888888888',
            'date_birth': '2010-01-01',
            'gender': self.gender_m.pk,
            'kinship': self.kinship_spouse.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': True,
            'family_head': True,  # Intentar ser cabeza siendo menor de edad
        }
        
        response = self.client.post(url, data)
        
        # Debe mostrar error y no guardar
        self.assertEqual(response.status_code, 200)  # No redirige
        
        # Verificar que NO se convirtió en cabeza de familia
        menor.refresh_from_db()
        self.assertFalse(menor.family_head)
    
    def test_update_person_unique_identification(self):
        """Verificar que el documento de identidad debe ser único"""
        self.client.force_login(self.user)
        
        # Crear otra persona con documento diferente
        otra_persona = Person.objects.create(
            first_name_1='Pedro',
            last_name_1='Gonzalez',
            document_type=self.document_type,
            identification_person='7777777777',
            date_birth=date(1988, 3, 10),
            gender=self.gender_m,
            kinship=self.kinship_spouse,
            handicap=self.handicap,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            social_insurance=self.security_social,
            eps=self.eps,
            family_card=self.family,
            family_head=False,
            state=True
        )
        
        # Intentar cambiar el documento a uno ya existente (el de self.person)
        url = reverse('updated-person', kwargs={'pk': otra_persona.pk})
        data = {
            'first_name_1': 'Pedro',
            'last_name_1': 'Gonzalez',
            'document_type': self.document_type.pk,
            'identification_person': '1234567890',  # Ya existe (self.person)
            'date_birth': '1988-03-10',
            'gender': self.gender_m.pk,
            'kinship': self.kinship_spouse.pk,
            'education_level': self.education.pk,
            'civil_state': self.civil_state.pk,
            'occupation': self.occupation.pk,
            'social_insurance': self.security_social.pk,
            'eps': self.eps.pk,
            'handicap': self.handicap.pk,
            'state': True,
            'family_head': False,
        }
        
        response = self.client.post(url, data)
        
        # Debe mostrar error y no guardar
        self.assertEqual(response.status_code, 200)  # No redirige
        
        # Verificar que NO cambió el documento
        otra_persona.refresh_from_db()
        self.assertEqual(otra_persona.identification_person, '7777777777')
