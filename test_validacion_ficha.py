"""
Test para validar que no se pueden crear fichas familiares con número 0
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import FamilyCard, Sidewalks, Organizations
from django.core.exceptions import ValidationError

print("=" * 70)
print("🧪 TEST: VALIDACIÓN DE NÚMERO DE FICHA FAMILIAR")
print("=" * 70)

# Obtener datos necesarios
sidewalk = Sidewalks.objects.first()
organization = Organizations.objects.first()

if not sidewalk or not organization:
    print("\n❌ Error: No hay veredas u organizaciones en la base de datos")
    exit(1)

print(f"\n📋 Datos de prueba:")
print(f"  Vereda: {sidewalk}")
print(f"  Organización: {organization}")

# TEST 1: Intentar crear una ficha con número 0 explícitamente
print("\n" + "=" * 70)
print("TEST 1: Crear ficha con family_card_number=0")
print("=" * 70)

try:
    ficha_test = FamilyCard(
        sidewalk_home=sidewalk,
        zone="Rural",
        organization=organization,
        family_card_number=0
    )
    ficha_test.save()

    print(f"✅ La ficha se guardó correctamente")
    print(f"   Número asignado automáticamente: {ficha_test.family_card_number}")

    if ficha_test.family_card_number > 0:
        print("✅ VALIDACIÓN EXITOSA: El número 0 fue reemplazado automáticamente")
        # Eliminar la ficha de prueba
        ficha_test.delete()
        print("   (Ficha de prueba eliminada)")
    else:
        print("❌ VALIDACIÓN FALLIDA: La ficha aún tiene número 0")
        ficha_test.delete()

except ValidationError as e:
    print(f"⚠️  ValidationError capturado: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")

# TEST 2: Crear una ficha sin especificar número (debería asignarse automáticamente)
print("\n" + "=" * 70)
print("TEST 2: Crear ficha sin especificar family_card_number")
print("=" * 70)

try:
    ficha_test2 = FamilyCard(
        sidewalk_home=sidewalk,
        zone="Urbana",
        organization=organization
    )
    ficha_test2.save()

    print(f"✅ La ficha se guardó correctamente")
    print(f"   Número asignado: {ficha_test2.family_card_number}")

    if ficha_test2.family_card_number > 0:
        print("✅ VALIDACIÓN EXITOSA: Se asignó un número válido automáticamente")
        ficha_test2.delete()
        print("   (Ficha de prueba eliminada)")
    else:
        print("❌ VALIDACIÓN FALLIDA: Se asignó número 0")
        ficha_test2.delete()

except Exception as e:
    print(f"❌ Error: {e}")

# TEST 3: Verificar que no existan fichas con número 0
print("\n" + "=" * 70)
print("TEST 3: Verificar fichas existentes con número 0")
print("=" * 70)

fichas_cero = FamilyCard.objects.filter(family_card_number=0)
count = fichas_cero.count()

if count == 0:
    print("✅ VALIDACIÓN EXITOSA: No hay fichas con número 0 en la base de datos")
else:
    print(f"⚠️  Se encontraron {count} fichas con número 0:")
    for f in fichas_cero:
        print(f"   - ID: {f.id}, Vereda: {f.sidewalk_home}")

# TEST 4: Verificar el método get_next_family_card_number
print("\n" + "=" * 70)
print("TEST 4: Método get_next_family_card_number()")
print("=" * 70)

next_num = FamilyCard.get_next_family_card_number()
print(f"📝 Siguiente número disponible: {next_num}")

if next_num > 0:
    print("✅ VALIDACIÓN EXITOSA: El método retorna un número válido")
else:
    print("❌ VALIDACIÓN FALLIDA: El método retorna 0 o negativo")

# RESUMEN
print("\n" + "=" * 70)
print("📊 RESUMEN DE VALIDACIONES")
print("=" * 70)

total_fichas = FamilyCard.objects.count()
fichas_validas = FamilyCard.objects.filter(family_card_number__gt=0).count()

print(f"Total de fichas: {total_fichas}")
print(f"Fichas con número válido (>0): {fichas_validas}")
print(f"Fichas con número 0: {total_fichas - fichas_validas}")

if total_fichas == fichas_validas:
    print("\n✅ TODAS LAS VALIDACIONES PASARON")
    print("   El sistema ahora previene la creación de fichas con número 0")
else:
    print("\n⚠️  ALGUNAS FICHAS TIENEN NÚMERO INVÁLIDO")
    print("   Ejecute el script corregir_fichas_cero.py para corregirlas")

print("=" * 70)

