from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Association, Organizations, Sidewalks, FamilyCard, MaterialConstruction, HomeOwnership, CookingFuel, MaterialConstructionFamilyCard, SystemParameters


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
