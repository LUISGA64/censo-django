"""
Script para corregir fichas familiares con número 0
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import FamilyCard, Person

print("=" * 70)
print("🔍 BUSCANDO FICHAS CON NÚMERO 0")
print("=" * 70)

# Buscar fichas con número 0
fichas_cero = FamilyCard.objects.filter(family_card_number=0)
print(f"\n📊 Fichas encontradas con número 0: {fichas_cero.count()}")

if fichas_cero.exists():
    print("\nDetalles de las fichas:")
    for ficha in fichas_cero:
        personas = Person.objects.filter(family_card=ficha)
        print(f"\n  - ID Ficha: {ficha.id}")
        print(f"    Número actual: {ficha.family_card_number}")
        print(f"    Vereda: {ficha.sidewalk_home}")
        print(f"    Organización: {ficha.organization}")
        print(f"    Creada: {ficha.created_at}")
        print(f"    Personas: {personas.count()}")
        for p in personas:
            print(f"      * {p.full_name} - {p.identification_person}")

    print("\n" + "=" * 70)
    print("🔧 CORRIGIENDO NÚMEROS DE FICHA")
    print("=" * 70)

    # Obtener el siguiente número disponible
    next_number = FamilyCard.get_next_family_card_number()
    print(f"\n📝 Siguiente número disponible: {next_number}")

    # Corregir cada ficha
    for ficha in fichas_cero:
        old_number = ficha.family_card_number
        ficha.family_card_number = next_number
        ficha.save()

        print(f"\n✅ Ficha ID {ficha.id} corregida:")
        print(f"   Número anterior: {old_number}")
        print(f"   Número nuevo: {next_number}")
        print(f"   Vereda: {ficha.sidewalk_home}")

        next_number += 1

    print("\n" + "=" * 70)
    print("✅ CORRECCIÓN COMPLETADA")
    print("=" * 70)

    # Verificar que no queden fichas con número 0
    fichas_cero_restantes = FamilyCard.objects.filter(family_card_number=0)
    print(f"\n📊 Fichas con número 0 después de corrección: {fichas_cero_restantes.count()}")

else:
    print("\n✅ No se encontraron fichas con número 0")
    print("=" * 70)

# Mostrar resumen de todas las fichas
print("\n📊 RESUMEN GENERAL")
print("=" * 70)
total_fichas = FamilyCard.objects.count()
print(f"Total de fichas: {total_fichas}")

# Verificar duplicados
from django.db.models import Count
duplicados = FamilyCard.objects.values('family_card_number').annotate(
    count=Count('id')
).filter(count__gt=1)

if duplicados.exists():
    print("\n⚠️  ADVERTENCIA: Se encontraron números duplicados:")
    for dup in duplicados:
        print(f"  - Número {dup['family_card_number']}: {dup['count']} fichas")
else:
    print("\n✅ No hay números de ficha duplicados")

print("=" * 70)

