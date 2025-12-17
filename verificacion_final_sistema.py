"""
Verificación Final del Sistema - Fichas Familiares
Verifica que no existan problemas con números de ficha
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import FamilyCard, Person

print("=" * 70)
print("🔍 VERIFICACIÓN FINAL DEL SISTEMA")
print("=" * 70)

# 1. Verificar fichas con número 0
print("\n1️⃣  Verificando fichas con número 0...")
fichas_cero = FamilyCard.objects.filter(family_card_number=0)
if fichas_cero.count() == 0:
    print("   ✅ No hay fichas con número 0")
else:
    print(f"   ❌ Se encontraron {fichas_cero.count()} fichas con número 0")

# 2. Verificar números duplicados
print("\n2️⃣  Verificando números duplicados...")
from django.db.models import Count
duplicados = FamilyCard.objects.values('family_card_number').annotate(
    count=Count('id')
).filter(count__gt=1)

if duplicados.count() == 0:
    print("   ✅ No hay números duplicados")
else:
    print(f"   ❌ Se encontraron {duplicados.count()} números duplicados:")
    for dup in duplicados:
        print(f"      - Número {dup['family_card_number']}: {dup['count']} fichas")

# 3. Verificar personas sin ficha
print("\n3️⃣  Verificando personas sin ficha familiar...")
personas_sin_ficha = Person.objects.filter(family_card__isnull=True, state=True)
if personas_sin_ficha.count() == 0:
    print("   ✅ Todas las personas tienen ficha familiar")
else:
    print(f"   ❌ {personas_sin_ficha.count()} personas sin ficha:")
    for p in personas_sin_ficha:
        print(f"      - {p.full_name} - {p.identification_person}")

# 4. Verificar persona específica (58262324)
print("\n4️⃣  Verificando persona con identificación 58262324...")
try:
    persona = Person.objects.get(identification_person='58262324')
    if persona.family_card and persona.family_card.family_card_number > 0:
        print(f"   ✅ Persona encontrada con ficha #{persona.family_card.family_card_number}")
    else:
        print(f"   ❌ Persona tiene ficha con número inválido")
except Person.DoesNotExist:
    print("   ⚠️  Persona no encontrada")

# 5. Estadísticas generales
print("\n5️⃣  Estadísticas generales...")
total_fichas = FamilyCard.objects.count()
total_personas = Person.objects.filter(state=True).count()
cabezas = Person.objects.filter(family_head=True, state=True).count()

print(f"   📊 Total de fichas: {total_fichas}")
print(f"   📊 Total de personas activas: {total_personas}")
print(f"   📊 Cabezas de familia: {cabezas}")
print(f"   📊 Promedio miembros/familia: {total_personas/total_fichas:.2f}")

# 6. Verificar integridad de números
print("\n6️⃣  Verificando integridad de números de ficha...")
fichas = FamilyCard.objects.all().order_by('family_card_number')
numeros = [f.family_card_number for f in fichas]
numeros_validos = [n for n in numeros if n > 0]

if len(numeros_validos) == len(numeros):
    print(f"   ✅ Todos los números son válidos (> 0)")
    print(f"   📝 Rango: {min(numeros_validos)} - {max(numeros_validos)}")
else:
    print(f"   ❌ Hay números inválidos en el sistema")

# RESUMEN FINAL
print("\n" + "=" * 70)
print("📊 RESUMEN DE VERIFICACIÓN")
print("=" * 70)

errores = 0
if fichas_cero.count() > 0:
    errores += 1
if duplicados.count() > 0:
    errores += 1
if personas_sin_ficha.count() > 0:
    errores += 1

if errores == 0:
    print("\n✅ ¡SISTEMA VERIFICADO CORRECTAMENTE!")
    print("   No se encontraron problemas de integridad")
    print("   Todas las validaciones pasaron exitosamente")
else:
    print(f"\n⚠️  SE ENCONTRARON {errores} PROBLEMAS")
    print("   Ejecute 'python corregir_fichas_cero.py' para corregir")

print("\n" + "=" * 70)
print("Verificación completada")
print("=" * 70)

