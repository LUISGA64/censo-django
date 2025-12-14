"""
Script de Prueba Completa de Auditoría
Ejecutar con: python manage.py shell
Luego: exec(open('test_auditoria_completo.py').read())
"""

from django.contrib.auth.models import User
from censoapp.models import (
    FamilyCard, Person, Sidewalks, Organizations, Association,
    DocumentType, Gender, Kinship, EducationLevel, CivilState,
    Occupancy, SecuritySocial, Eps, Handicap, MaterialConstructionFamilyCard,
    MaterialConstruction, HomeOwnership, CookingFuel
)
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
import os

print("\n" + "="*70)
print("🧪 PRUEBA COMPLETA DE AUDITORÍA CON DJANGO-SIMPLE-HISTORY")
print("="*70 + "\n")

# Verificar que el historial está habilitado
print("1️⃣  Verificando que el historial está habilitado...")
print(f"   ✅ FamilyCard.history: {hasattr(FamilyCard, 'history')}")
print(f"   ✅ Person.history: {hasattr(Person, 'history')}")
print(f"   ✅ MaterialConstructionFamilyCard.history: {hasattr(MaterialConstructionFamilyCard, 'history')}")

# Obtener o crear usuario de prueba
print("\n2️⃣  Configurando usuario de prueba...")
user, created = User.objects.get_or_create(
    username='test_audit_user',
    defaults={'email': 'test@audit.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"   ✅ Usuario creado: {user.username}")
else:
    print(f"   ℹ️  Usuario existente: {user.username}")

# Configurar datos base necesarios
print("\n3️⃣  Configurando datos base...")

# Obtener o crear Association
try:
    association = Association.objects.first()
    if not association:
        # Crear imagen fake
        fake_image = SimpleUploadedFile(
            "test.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        association = Association.objects.create(
            association_name='Test Association',
            association_identification='123456789',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='6012345678',
            association_address='Calle Test',
            association_departament='Test Dept',
            association_email='test@association.com',
            association_logo=fake_image
        )
        print(f"   ✅ Association creada: {association.association_name}")
    else:
        print(f"   ℹ️  Association existente: {association.association_name}")
except Exception as e:
    print(f"   ⚠️  Error con Association: {e}")

# Obtener o crear Organization
try:
    organization = Organizations.objects.first()
    if not organization:
        fake_image = SimpleUploadedFile(
            "test_org.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        organization = Organizations.objects.create(
            organization_name='Test Organization',
            organization_identification='987654321',
            organization_type_identification='NIT',
            organization_territory='Test Territory',
            organization_email='test@org.com',
            organization_mobile_phone='3009876543',
            organization_phone='6019876543',
            organization_address='Carrera Test',
            organization_logo=fake_image,
            association_id=association
        )
        print(f"   ✅ Organization creada: {organization.organization_name}")
    else:
        print(f"   ℹ️  Organization existente: {organization.organization_name}")
except Exception as e:
    print(f"   ⚠️  Error con Organization: {e}")

# Obtener o crear Sidewalk
sidewalk, created = Sidewalks.objects.get_or_create(
    sidewalk_name='Vereda Test Auditoría',
    defaults={'organization_id': organization}
)
print(f"   {'✅ Vereda creada' if created else 'ℹ️  Vereda existente'}: {sidewalk.sidewalk_name}")

# Obtener datos para Person
document_type = DocumentType.objects.first() or DocumentType.objects.create(
    code_document_type='CC', document_type='Cédula'
)
gender = Gender.objects.first() or Gender.objects.create(
    gender_code='M', gender='Masculino'
)
kinship = Kinship.objects.first() or Kinship.objects.create(
    code_kinship='1', description_kinship='Cabeza'
)
education = EducationLevel.objects.first() or EducationLevel.objects.create(
    code_education_level='1', education_level='Primaria'
)
civil_state = CivilState.objects.first() or CivilState.objects.create(
    code_state_civil='S', state_civil='Soltero'
)
occupation = Occupancy.objects.first() or Occupancy.objects.create(
    description_occupancy='Agricultor'
)
social_security = SecuritySocial.objects.first() or SecuritySocial.objects.create(
    code_security_social='01', affiliation='Contributivo'
)
eps = Eps.objects.first() or Eps.objects.create(
    code_eps='EPS001', name_eps='Test EPS'
)
handicap = Handicap.objects.first() or Handicap.objects.create(
    code_handicap='0', handicap='Ninguna'
)

print("   ✅ Datos base configurados")

# PRUEBA 1: Crear Ficha Familiar
print("\n" + "="*70)
print("4️⃣  PRUEBA 1: Crear Ficha Familiar")
print("="*70)

try:
    # Obtener siguiente número de ficha
    next_number = FamilyCard.get_next_family_card_number()
    
    family_card = FamilyCard.objects.create(
        address_home='Casa de Prueba Auditoría',
        sidewalk_home=sidewalk,
        latitude='4.123456',
        longitude='-74.123456',
        zone='R',
        organization=organization,
        family_card_number=next_number,
        state=True
    )
    
    print(f"   ✅ Ficha Familiar creada: N° {family_card.family_card_number}")
    print(f"   📊 Registros en historial: {family_card.history.count()}")
    
    # Verificar historial
    if family_card.history.count() > 0:
        ultimo = family_card.history.first()
        print(f"   📝 Último cambio:")
        print(f"      - Tipo: {ultimo.get_history_type_display()}")
        print(f"      - Fecha: {ultimo.history_date}")
        print(f"      - Usuario: {ultimo.history_user or 'Sistema'}")
        print(f"      - Estado: {'Activa' if ultimo.state else 'Inactiva'}")
    
except Exception as e:
    print(f"   ❌ Error al crear ficha: {e}")
    family_card = None

# PRUEBA 2: Actualizar Ficha Familiar
if family_card:
    print("\n" + "="*70)
    print("5️⃣  PRUEBA 2: Actualizar Ficha Familiar")
    print("="*70)
    
    try:
        # Actualizar la dirección
        family_card.address_home = 'Casa Actualizada - Prueba Auditoría'
        family_card.zone = 'U'  # Cambiar de Rural a Urbana
        family_card.save()
        
        print(f"   ✅ Ficha actualizada")
        print(f"   📊 Registros en historial: {family_card.history.count()}")
        
        # Mostrar los últimos 2 cambios
        print(f"\n   📜 Historial de cambios:")
        for i, record in enumerate(family_card.history.all()[:2], 1):
            print(f"\n   Cambio {i}:")
            print(f"      - Tipo: {record.get_history_type_display()}")
            print(f"      - Fecha: {record.history_date}")
            print(f"      - Zona: {record.get_zone_display()}")
            print(f"      - Dirección: {record.address_home}")
        
    except Exception as e:
        print(f"   ❌ Error al actualizar: {e}")

# PRUEBA 3: Crear Persona (Cabeza de Familia)
if family_card:
    print("\n" + "="*70)
    print("6️⃣  PRUEBA 3: Crear Persona (Cabeza de Familia)")
    print("="*70)
    
    try:
        birth_date = date.today() - timedelta(days=365*30)  # 30 años
        
        person = Person.objects.create(
            first_name_1='Juan',
            first_name_2='Carlos',
            last_name_1='Pérez',
            last_name_2='García',
            identification_person=f'TEST{next_number}001',
            document_type=document_type,
            date_birth=birth_date,
            cell_phone='3001234567',
            personal_email='juan@test.com',
            gender=gender,
            kinship=kinship,
            education_level=education,
            civil_state=civil_state,
            occupation=occupation,
            social_insurance=social_security,
            eps=eps,
            handicap=handicap,
            family_card=family_card,
            family_head=True,
            state=True
        )
        
        print(f"   ✅ Persona creada: {person.full_name}")
        print(f"   📊 Registros en historial: {person.history.count()}")
        
        if person.history.count() > 0:
            ultimo = person.history.first()
            print(f"   📝 Último cambio:")
            print(f"      - Tipo: {ultimo.get_history_type_display()}")
            print(f"      - Fecha: {ultimo.history_date}")
            print(f"      - Cabeza: {'Sí' if ultimo.family_head else 'No'}")
        
    except Exception as e:
        print(f"   ❌ Error al crear persona: {e}")
        person = None

# PRUEBA 4: Actualizar Persona
if person:
    print("\n" + "="*70)
    print("7️⃣  PRUEBA 4: Actualizar Persona")
    print("="*70)
    
    try:
        # Actualizar teléfono y email
        person.cell_phone = '3009876543'
        person.personal_email = 'juan.actualizado@test.com'
        person.save()
        
        print(f"   ✅ Persona actualizada")
        print(f"   📊 Registros en historial: {person.history.count()}")
        
        # Mostrar cambios
        print(f"\n   📜 Últimos cambios:")
        for i, record in enumerate(person.history.all()[:2], 1):
            print(f"\n   Cambio {i}:")
            print(f"      - Tipo: {record.get_history_type_display()}")
            print(f"      - Teléfono: {record.cell_phone}")
            print(f"      - Email: {record.personal_email}")
        
    except Exception as e:
        print(f"   ❌ Error al actualizar persona: {e}")

# PRUEBA 5: Crear MaterialConstructionFamilyCard
if family_card:
    print("\n" + "="*70)
    print("8️⃣  PRUEBA 5: Crear Datos de Vivienda")
    print("="*70)
    
    try:
        # Obtener o crear materiales
        roof_mat = MaterialConstruction.objects.filter(roof=True).first()
        wall_mat = MaterialConstruction.objects.filter(wall=True).first()
        floor_mat = MaterialConstruction.objects.filter(floor=True).first()
        
        if not roof_mat:
            roof_mat = MaterialConstruction.objects.create(
                material_name='Teja Test', roof=True
            )
        if not wall_mat:
            wall_mat = MaterialConstruction.objects.create(
                material_name='Ladrillo Test', wall=True
            )
        if not floor_mat:
            floor_mat = MaterialConstruction.objects.create(
                material_name='Baldosa Test', floor=True
            )
        
        # Obtener HomeOwnership y CookingFuel
        home_ownership = HomeOwnership.objects.first()
        if not home_ownership:
            home_ownership = HomeOwnership.objects.create(
                ownership_type='Propio'
            )
        
        cooking_fuel = CookingFuel.objects.first()
        if not cooking_fuel:
            cooking_fuel = CookingFuel.objects.create(
                fuel_type='Gas'
            )
        
        # Verificar si ya existe
        material, created = MaterialConstructionFamilyCard.objects.get_or_create(
            family_card=family_card,
            defaults={
                'material_roof': roof_mat,
                'material_wall': wall_mat,
                'material_floor': floor_mat,
                'number_families': 1,
                'number_people_bedrooms': 2,
                'condition_roof': 'Bueno',
                'condition_wall': 'Bueno',
                'condition_floor': 'Bueno',
                'home_ownership': home_ownership,
                'kitchen_location': 1,
                'cooking_fuel': cooking_fuel,
                'home_smoke': False,
                'number_bedrooms': 2,
                'ventilation': True,
                'lighting': True,
            }
        )
        
        print(f"   ✅ Datos de vivienda {'creados' if created else 'ya existían'}")
        print(f"   📊 Registros en historial: {material.history.count()}")
        
        if material.history.count() > 0:
            ultimo = material.history.first()
            print(f"   📝 Último cambio:")
            print(f"      - Tipo: {ultimo.get_history_type_display()}")
            print(f"      - Habitaciones: {ultimo.number_bedrooms}")
            print(f"      - Ventilación: {'Sí' if ultimo.ventilation else 'No'}")
        
    except Exception as e:
        print(f"   ❌ Error con datos de vivienda: {e}")

# RESUMEN FINAL
print("\n" + "="*70)
print("📊 RESUMEN FINAL DE LA AUDITORÍA")
print("="*70 + "\n")

try:
    total_family = FamilyCard.history.count()
    total_person = Person.history.count()
    total_material = MaterialConstructionFamilyCard.history.count()
    total_general = total_family + total_person + total_material
    
    print(f"   📈 Total de registros históricos en el sistema:")
    print(f"      - FamilyCard: {total_family} registros")
    print(f"      - Person: {total_person} registros")
    print(f"      - MaterialConstructionFamilyCard: {total_material} registros")
    print(f"      - TOTAL: {total_general} registros\n")
    
    if family_card:
        print(f"   🏠 Ficha de prueba N° {family_card.family_card_number}:")
        print(f"      - URL Admin: http://localhost:8000/admin/censoapp/familycard/{family_card.id}/change/")
        print(f"      - URL Detalle: http://localhost:8000/familyCard/detail/{family_card.id}/")
        print(f"      - Cambios registrados: {family_card.history.count()}")
    
    if person:
        print(f"\n   👤 Persona de prueba: {person.full_name}")
        print(f"      - URL Admin: http://localhost:8000/admin/censoapp/person/{person.id}/change/")
        print(f"      - Cambios registrados: {person.history.count()}")
    
except Exception as e:
    print(f"   ⚠️  Error al generar resumen: {e}")

print("\n" + "="*70)
print("✅ PRUEBAS DE AUDITORÍA COMPLETADAS")
print("="*70)
print("\n💡 PRÓXIMOS PASOS:")
print("   1. Accede al admin: http://localhost:8000/admin")
print("   2. Haz clic en el botón 'History' de cualquier registro")
print("   3. Ve al detalle de la ficha y haz clic en 'Historial de Cambios'")
print("   4. Verifica que todos los cambios están registrados\n")

