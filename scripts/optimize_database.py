"""
Script de optimización y análisis de base de datos
Reemplaza comandos obsoletos como sqlindexes
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from django.db import connection
from django.apps import apps
from django.db.models import Count, Q
from django.core.management import call_command
from censoapp.models import (
    Person, FamilyCard, Sidewalks, Association,
    Organizations, UserProfile
)


def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_database_indexes():
    """Verifica los índices actuales en la base de datos"""
    print_section("ÍNDICES DE BASE DE DATOS")

    with connection.cursor() as cursor:
        # Para MySQL
        if 'mysql' in connection.settings_dict['ENGINE']:
            cursor.execute("""
                SELECT 
                    TABLE_NAME,
                    INDEX_NAME,
                    GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as COLUMNS
                FROM information_schema.STATISTICS
                WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME LIKE 'censoapp_%%'
                GROUP BY TABLE_NAME, INDEX_NAME
                ORDER BY TABLE_NAME, INDEX_NAME
            """, [connection.settings_dict['NAME']])

            current_table = None
            for row in cursor.fetchall():
                table, index, columns = row
                if table != current_table:
                    print(f"\n📋 {table}")
                    current_table = table
                print(f"   └─ {index}: {columns}")

        # Para SQLite
        elif 'sqlite' in connection.settings_dict['ENGINE']:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'censoapp_%'")
            tables = [row[0] for row in cursor.fetchall()]

            for table in tables:
                print(f"\n📋 {table}")
                cursor.execute(f"PRAGMA index_list({table})")
                indexes = cursor.fetchall()
                for idx in indexes:
                    print(f"   └─ {idx[1]}")


def analyze_query_performance():
    """Analiza el rendimiento de consultas comunes"""
    print_section("ANÁLISIS DE RENDIMIENTO DE CONSULTAS")

    # Test 1: Contar personas
    from django.db import reset_queries
    from django.conf import settings

    if settings.DEBUG:
        print("\n🔍 Test 1: Contar todas las personas")
        reset_queries()
        count = Person.objects.count()
        print(f"   Resultado: {count} personas")
        print(f"   Queries ejecutadas: {len(connection.queries)}")

        print("\n🔍 Test 2: Personas con relaciones (select_related)")
        reset_queries()
        persons = list(Person.objects.select_related(
            'document_type', 'gender', 'family_card'
        )[:10])
        print(f"   Resultado: {len(persons)} personas cargadas")
        print(f"   Queries ejecutadas: {len(connection.queries)}")

        print("\n🔍 Test 3: Fichas familiares con personas (prefetch_related)")
        reset_queries()
        families = list(FamilyCard.objects.prefetch_related('person_set')[:10])
        print(f"   Resultado: {len(families)} fichas cargadas")
        print(f"   Queries ejecutadas: {len(connection.queries)}")
    else:
        print("⚠️  DEBUG=False. Active DEBUG=True para ver queries detalladas")


def check_missing_indexes():
    """Sugiere índices faltantes basados en campos comunes"""
    print_section("SUGERENCIAS DE ÍNDICES")

    suggestions = []

    # Verificar campos de búsqueda frecuente en Person
    print("\n📊 Modelo Person:")
    print("   ✓ id (PRIMARY KEY - ya indexado)")
    print("   ✓ family_card_id (FOREIGN KEY - ya indexado)")

    # Sugerir índices adicionales
    suggestions.append({
        'model': 'Person',
        'fields': ['identification_person'],
        'reason': 'Búsqueda frecuente por identificación'
    })

    suggestions.append({
        'model': 'Person',
        'fields': ['first_name_1', 'last_name_1'],
        'reason': 'Búsqueda frecuente por nombre'
    })

    suggestions.append({
        'model': 'FamilyCard',
        'fields': ['organization_id'],
        'reason': 'Filtrado frecuente por organización'
    })

    suggestions.append({
        'model': 'Sidewalks',
        'fields': ['organization_id'],
        'reason': 'Filtrado por organización'
    })

    print("\n💡 Índices sugeridos para agregar en models.py:")
    for sug in suggestions:
        index_name = f"{sug['model'].lower()}_{'_'.join(sug['fields'][:2])}_idx"
        print(f"\n   {sug['model']}:")
        print(f"   └─ class Meta:")
        print(f"      indexes = [")
        print(f"          models.Index(fields={sug['fields']}, name='{index_name}'),")
        print(f"      ]")
        print(f"   Razón: {sug['reason']}")


def database_statistics():
    """Muestra estadísticas de la base de datos"""
    print_section("ESTADÍSTICAS DE BASE DE DATOS")

    try:
        person_count = Person.objects.count()
        family_count = FamilyCard.objects.count()
        sidewalks_count = Sidewalks.objects.count()
        org_count = Organizations.objects.count()
        user_count = UserProfile.objects.count()

        print(f"\n📊 Registros totales:")
        print(f"   • Personas: {person_count:,}")
        print(f"   • Fichas Familiares: {family_count:,}")
        print(f"   • Veredas: {sidewalks_count:,}")
        print(f"   • Organizaciones: {org_count:,}")
        print(f"   • Usuarios: {user_count:,}")

        # Promedio de personas por familia
        if family_count > 0:
            avg_persons = person_count / family_count
            print(f"\n📈 Promedios:")
            print(f"   • Personas por familia: {avg_persons:.2f}")

        # Organizaciones con más familias
        print(f"\n🏆 Top organizaciones por familias:")
        top_orgs = Organizations.objects.annotate(
            family_count=Count('familycard')
        ).order_by('-family_count')[:5]

        for org in top_orgs:
            print(f"   • {org.organization_name}: {org.family_count} familias")

    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")


def check_database_size():
    """Verifica el tamaño de la base de datos"""
    print_section("TAMAÑO DE BASE DE DATOS")

    with connection.cursor() as cursor:
        if 'mysql' in connection.settings_dict['ENGINE']:
            cursor.execute("""
                SELECT 
                    TABLE_NAME,
                    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'Size (MB)',
                    TABLE_ROWS
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME LIKE 'censoapp_%%'
                ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC
            """, [connection.settings_dict['NAME']])

            print("\n📦 Tamaño por tabla:")
            total_size = 0
            for row in cursor.fetchall():
                table, size, rows = row
                print(f"   • {table}: {size} MB ({rows:,} filas)")
                total_size += float(size or 0)

            print(f"\n💾 Total: {total_size:.2f} MB")
        else:
            print("⚠️  Estadísticas de tamaño solo disponibles para MySQL")


def run_optimizations():
    """Ejecuta optimizaciones recomendadas"""
    print_section("OPTIMIZACIONES RECOMENDADAS")

    print("\n🔧 Optimizaciones que puedes ejecutar:")

    print("\n1. Limpiar sesiones expiradas:")
    print("   python manage.py clearsessions")

    print("\n2. Optimizar tablas MySQL:")
    print("   python manage.py dbshell")
    print("   OPTIMIZE TABLE censoapp_person, censoapp_familycard;")

    print("\n3. Actualizar estadísticas de consulta:")
    print("   python manage.py dbshell")
    print("   ANALYZE TABLE censoapp_person, censoapp_familycard;")

    print("\n4. Verificar integridad de datos:")
    print("   python manage.py check --deploy")

    print("\n5. Crear backup antes de optimizar:")
    print("   python manage.py dumpdata > backup.json")


def main():
    """Ejecuta todos los análisis"""
    print("\n🚀 ANÁLISIS Y OPTIMIZACIÓN DE BASE DE DATOS")
    print("=" * 60)

    try:
        database_statistics()
        check_database_size()
        check_database_indexes()
        check_missing_indexes()
        analyze_query_performance()
        run_optimizations()

        print("\n" + "=" * 60)
        print("✅ Análisis completado")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
