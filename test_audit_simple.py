"""Test Auditoria - Simple version"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from django.contrib.auth.models import User
from censoapp.models import FamilyCard, Person
from datetime import datetime

print("\n" + "="*70)
print("PRUEBA DE AUDITORIA - DJANGO SIMPLE HISTORY")
print("="*70 + "\n")

# Test 1: Verificar historial habilitado
print("1. Verificando historial...")
print(f"   FamilyCard.history: {hasattr(FamilyCard, 'history')}")
print(f"   Person.history: {hasattr(Person, 'history')}")

# Test 2: Contar registros historicos
print("\n2. Contando registros historicos...")
try:
    family_count = FamilyCard.history.count()
    person_count = Person.history.count()
    print(f"   FamilyCard: {family_count} registros")
    print(f"   Person: {person_count} registros")
    print(f"   TOTAL: {family_count + person_count} registros")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Mostrar ultimo cambio en ficha
print("\n3. Ultimo cambio en fichas familiares...")
try:
    ultima_ficha = FamilyCard.objects.order_by('-id').first()
    if ultima_ficha:
        print(f"   Ficha No {ultima_ficha.family_card_number}")
        print(f"   Cambios registrados: {ultima_ficha.history.count()}")

        if ultima_ficha.history.count() > 0:
            ultimo = ultima_ficha.history.first()
            print(f"   Ultimo cambio:")
            print(f"     - Tipo: {ultimo.get_history_type_display()}")
            print(f"     - Fecha: {ultimo.history_date}")
            print(f"     - Usuario: {ultimo.history_user or 'Sistema'}")
            print(f"     - Estado: {'Activa' if ultimo.state else 'Inactiva'}")
            print(f"     - Zona: {ultimo.get_zone_display()}")
    else:
        print("   No hay fichas en la BD")
except Exception as e:
    print(f"   Error: {e}")

# Test 4: Mostrar ultimo cambio en persona
print("\n4. Ultimo cambio en personas...")
try:
    ultima_persona = Person.objects.order_by('-id').first()
    if ultima_persona:
        print(f"   Persona: {ultima_persona.first_name_1} {ultima_persona.last_name_1}")
        print(f"   Cambios registrados: {ultima_persona.history.count()}")

        if ultima_persona.history.count() > 0:
            ultimo = ultima_persona.history.first()
            print(f"   Ultimo cambio:")
            print(f"     - Tipo: {ultimo.get_history_type_display()}")
            print(f"     - Fecha: {ultimo.history_date}")
            print(f"     - Usuario: {ultimo.history_user or 'Sistema'}")
            print(f"     - Cabeza: {'Si' if ultimo.family_head else 'No'}")
    else:
        print("   No hay personas en la BD")
except Exception as e:
    print(f"   Error: {e}")

# Test 5: Crear una ficha de prueba
print("\n5. Creando ficha de prueba...")
try:
    from censoapp.models import Sidewalks, Organizations

    sidewalk = Sidewalks.objects.first()
    organization = Organizations.objects.first()

    if sidewalk and organization:
        next_num = FamilyCard.get_next_family_card_number()

        nueva_ficha = FamilyCard.objects.create(
            address_home='Test Auditoria',
            sidewalk_home=sidewalk,
            latitude='0',
            longitude='0',
            zone='R',
            organization=organization,
            family_card_number=next_num,
            state=True
        )

        print(f"   Ficha creada: No {nueva_ficha.family_card_number}")
        print(f"   Historial: {nueva_ficha.history.count()} registros")

        # Actualizar la ficha
        nueva_ficha.zone = 'U'
        nueva_ficha.address_home = 'Test Auditoria Actualizada'
        nueva_ficha.save()

        print(f"   Ficha actualizada")
        print(f"   Historial: {nueva_ficha.history.count()} registros")

        # Mostrar historial
        print(f"\n   Historial completo:")
        for i, record in enumerate(nueva_ficha.history.all(), 1):
            print(f"     {i}. {record.get_history_type_display()} - {record.history_date} - Zona: {record.get_zone_display()}")

        print(f"\n   URL Admin: http://localhost:8000/admin/censoapp/familycard/{nueva_ficha.id}/change/")
        print(f"   URL Detalle: http://localhost:8000/familyCard/detail/{nueva_ficha.id}/")
    else:
        print("   Faltan datos base (sidewalk/organization)")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*70)
print("PRUEBA COMPLETADA")
print("="*70)
print("\nAcciones sugeridas:")
print("1. Abrir http://localhost:8000/admin")
print("2. Ver cualquier Ficha Familiar o Persona")
print("3. Hacer clic en el boton 'History'")
print("4. Ver el detalle de una ficha y abrir tab 'Historial de Cambios'\n")

