"""
Verificar el estado de la persona con identificación 58262324
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import Person, FamilyCard

print("=" * 70)
print("🔍 VERIFICACIÓN DE PERSONA CON IDENTIFICACIÓN 58262324")
print("=" * 70)

try:
    persona = Person.objects.get(identification_person='58262324')

    print(f"\n👤 Información de la Persona:")
    print(f"   ID: {persona.id}")
    print(f"   Nombre completo: {persona.full_name}")
    print(f"   Identificación: {persona.identification_person}")
    print(f"   Cabeza de familia: {'Sí' if persona.family_head else 'No'}")
    print(f"   Estado: {'Activo' if persona.state else 'Inactivo'}")

    print(f"\n🏠 Información de la Ficha Familiar:")
    print(f"   ID de Ficha: {persona.family_card_id}")

    if persona.family_card:
        ficha = persona.family_card
        print(f"   Número de Ficha: {ficha.family_card_number}")
        print(f"   Vereda: {ficha.sidewalk_home}")
        print(f"   Zona: {ficha.zone}")
        print(f"   Organización: {ficha.organization}")
        print(f"   Estado: {'Activa' if ficha.state else 'Inactiva'}")

        # Verificar que el número de ficha sea válido
        if ficha.family_card_number > 0:
            print(f"\n✅ CORRECTO: La ficha tiene un número válido ({ficha.family_card_number})")
        else:
            print(f"\n❌ ERROR: La ficha tiene número inválido ({ficha.family_card_number})")

        # Contar miembros de la familia
        from censoapp.models import Person as P
        miembros = P.objects.filter(family_card=ficha, state=True)
        print(f"\n👨‍👩‍👧‍👦 Miembros de la Familia: {miembros.count()}")
        for m in miembros:
            tipo = "👑 Cabeza" if m.family_head else "👥 Miembro"
            print(f"   {tipo}: {m.full_name} - {m.identification_person}")
    else:
        print(f"   ❌ ERROR: No tiene ficha familiar asignada")

except Person.DoesNotExist:
    print("\n❌ ERROR: No se encontró una persona con identificación 58262324")
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 70)

