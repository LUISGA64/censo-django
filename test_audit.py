# Script de Demostración - Auditoría con Django-Simple-History
# Ejecutar con: python manage.py shell < test_audit.py

from censoapp.models import FamilyCard, Person, MaterialConstructionFamilyCard
from django.contrib.auth.models import User

print("\n" + "="*60)
print("🔍 DEMOSTRACIÓN DE AUDITORÍA CON DJANGO-SIMPLE-HISTORY")
print("="*60 + "\n")

# 1. Verificar que las tablas históricas existen
print("1️⃣  Verificando tablas históricas...")
print(f"   ✓ FamilyCard.history existe: {hasattr(FamilyCard, 'history')}")
print(f"   ✓ Person.history existe: {hasattr(Person, 'history')}")
print(f"   ✓ MaterialConstructionFamilyCard.history existe: {hasattr(MaterialConstructionFamilyCard, 'history')}")

# 2. Contar registros históricos
print("\n2️⃣  Conteo de registros históricos:")
try:
    family_history_count = FamilyCard.history.count()
    person_history_count = Person.history.count()
    material_history_count = MaterialConstructionFamilyCard.history.count()

    print(f"   📊 FamilyCard: {family_history_count} registros históricos")
    print(f"   📊 Person: {person_history_count} registros históricos")
    print(f"   📊 MaterialConstructionFamilyCard: {material_history_count} registros históricos")
except Exception as e:
    print(f"   ⚠️  Error al contar registros: {e}")

# 3. Mostrar ejemplo de historial de una ficha
print("\n3️⃣  Ejemplo de historial de Ficha Familiar:")
try:
    ficha = FamilyCard.objects.first()
    if ficha:
        print(f"   📋 Ficha N° {ficha.family_card_number}")
        print(f"   📅 Cambios registrados: {ficha.history.count()}")

        # Mostrar último cambio
        ultimo_cambio = ficha.history.first()
        if ultimo_cambio:
            print(f"\n   Último cambio:")
            print(f"   - Tipo: {ultimo_cambio.get_history_type_display()}")
            print(f"   - Fecha: {ultimo_cambio.history_date}")
            print(f"   - Usuario: {ultimo_cambio.history_user or 'Sistema'}")
            print(f"   - Estado: {'Activa' if ultimo_cambio.state else 'Inactiva'}")
    else:
        print("   ℹ️  No hay fichas familiares en la base de datos")
except Exception as e:
    print(f"   ⚠️  Error: {e}")

# 4. Mostrar ejemplo de historial de persona
print("\n4️⃣  Ejemplo de historial de Persona:")
try:
    persona = Person.objects.first()
    if persona:
        print(f"   👤 {persona.first_name_1} {persona.last_name_1}")
        print(f"   📅 Cambios registrados: {persona.history.count()}")

        # Mostrar último cambio
        ultimo_cambio = persona.history.first()
        if ultimo_cambio:
            print(f"\n   Último cambio:")
            print(f"   - Tipo: {ultimo_cambio.get_history_type_display()}")
            print(f"   - Fecha: {ultimo_cambio.history_date}")
            print(f"   - Usuario: {ultimo_cambio.history_user or 'Sistema'}")
            print(f"   - Cabeza de Familia: {'Sí' if ultimo_cambio.family_head else 'No'}")
    else:
        print("   ℹ️  No hay personas en la base de datos")
except Exception as e:
    print(f"   ⚠️  Error: {e}")

# 5. Estadísticas generales
print("\n5️⃣  Estadísticas de Auditoría:")
try:
    total_cambios = family_history_count + person_history_count + material_history_count
    print(f"   📊 Total de cambios registrados: {total_cambios}")
    print(f"   📈 Distribución:")
    print(f"      - Fichas Familiares: {family_history_count} ({family_history_count/total_cambios*100:.1f}%)" if total_cambios > 0 else "      - Fichas Familiares: 0 (0%)")
    print(f"      - Personas: {person_history_count} ({person_history_count/total_cambios*100:.1f}%)" if total_cambios > 0 else "      - Personas: 0 (0%)")
    print(f"      - Datos de Vivienda: {material_history_count} ({material_history_count/total_cambios*100:.1f}%)" if total_cambios > 0 else "      - Datos de Vivienda: 0 (0%)")
except Exception as e:
    print(f"   ⚠️  Error: {e}")

print("\n" + "="*60)
print("✅ DEMOSTRACIÓN COMPLETADA")
print("="*60 + "\n")

print("💡 TIPS:")
print("   - Para ver el historial en admin: accede a cualquier registro")
print("   - Para ver el historial en frontend: ve al detalle de una ficha")
print("   - Los cambios se registran automáticamente en cada save()")
print("\n")

