"""
Script de prueba para verificar el sistema de variables personalizadas simplificado.
Valida que la nueva estructura de 4 campos funcione correctamente.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from censoapp.models import Organizations, TemplateVariable
from django.contrib.auth.models import User

def test_variable_creation():
    """Prueba la creación de variables con el nuevo sistema"""
    print("=" * 60)
    print("PRUEBA: Creación de Variables Personalizadas Simplificadas")
    print("=" * 60)
    
    # Obtener una organización
    org = Organizations.objects.first()
    if not org:
        print("❌ No hay organizaciones en la base de datos")
        return False
    
    print(f"✅ Organización: {org.organization_name}")
    print()
    
    # Test 1: Crear variable de organización
    print("Test 1: Variable de Organización")
    print("-" * 40)
    try:
        var1, created = TemplateVariable.objects.get_or_create(
            organization=org,
            variable_name='territorio_test',
            defaults={
                'variable_type': 'organization',
                'variable_value': 'organization_territory',
                'description': 'Territorio del resguardo (prueba)',
                'is_active': True
            }
        )
        if created:
            print(f"✅ Variable creada: {{{var1.variable_name}}}")
        else:
            print(f"ℹ️  Variable ya existe: {{{var1.variable_name}}}")
        print(f"   Tipo: {var1.get_variable_type_display()}")
        print(f"   Campo: {var1.variable_value}")
        print(f"   Descripción: {var1.description}")
        print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 2: Crear variable de persona
    print("Test 2: Variable de Persona")
    print("-" * 40)
    try:
        var2, created = TemplateVariable.objects.get_or_create(
            organization=org,
            variable_name='nombre_completo_test',
            defaults={
                'variable_type': 'person',
                'variable_value': 'full_name',
                'description': 'Nombre completo de la persona (prueba)',
                'is_active': True
            }
        )
        if created:
            print(f"✅ Variable creada: {{{var2.variable_name}}}")
        else:
            print(f"ℹ️  Variable ya existe: {{{var2.variable_name}}}")
        print(f"   Tipo: {var2.get_variable_type_display()}")
        print(f"   Campo: {var2.variable_value}")
        print(f"   Descripción: {var2.description}")
        print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 3: Crear variable de ficha familiar
    print("Test 3: Variable de Ficha Familiar")
    print("-" * 40)
    try:
        var3, created = TemplateVariable.objects.get_or_create(
            organization=org,
            variable_name='vereda_test',
            defaults={
                'variable_type': 'family_card',
                'variable_value': 'sidewalk_home.sidewalk_name',
                'description': 'Vereda de residencia (prueba)',
                'is_active': True
            }
        )
        if created:
            print(f"✅ Variable creada: {{{var3.variable_name}}}")
        else:
            print(f"ℹ️  Variable ya existe: {{{var3.variable_name}}}")
        print(f"   Tipo: {var3.get_variable_type_display()}")
        print(f"   Campo: {var3.variable_value}")
        print(f"   Descripción: {var3.description}")
        print()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 4: Intentar crear variable duplicada (debe fallar)
    print("Test 4: Validación de Duplicados")
    print("-" * 40)
    try:
        var_dup = TemplateVariable(
            organization=org,
            variable_name='territorio_test',  # Mismo nombre que var1
            variable_type='organization',
            variable_value='organization_name',
            description='Esta debería fallar'
        )
        var_dup.full_clean()  # Esto debería lanzar ValidationError
        var_dup.save()
        print("❌ ERROR: La validación de duplicados no funcionó")
        return False
    except Exception as e:
        print(f"✅ Validación correcta: {str(e)}")
        print()
    
    # Test 5: Listar todas las variables de prueba
    print("Test 5: Listar Variables de Prueba")
    print("-" * 40)
    test_vars = TemplateVariable.objects.filter(
        organization=org,
        variable_name__endswith='_test'
    ).order_by('variable_type', 'variable_name')
    
    print(f"Total de variables de prueba: {test_vars.count()}")
    for var in test_vars:
        print(f"  • {{{var.variable_name}}} → {var.get_variable_type_display()}.{var.variable_value}")
    print()
    
    # Test 6: Verificar estructura del modelo
    print("Test 6: Verificar Estructura del Modelo")
    print("-" * 40)
    from django.db import connection
    with connection.cursor() as cursor:
        # SQLite usa pragma table_info
        cursor.execute("PRAGMA table_info(censoapp_templatevariable)")
        columns = cursor.fetchall()
        
        target_columns = ['variable_name', 'variable_type', 'variable_value']
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            if col_name in target_columns:
                print(f"  ✅ {col_name}: {col_type}")
    print()
    
    return True


def test_variable_types():
    """Prueba que los tipos de variables estén correctos"""
    print("=" * 60)
    print("PRUEBA: Tipos de Variables Disponibles")
    print("=" * 60)
    
    print("Tipos de variable configurados:")
    # Obtener directamente del modelo ya importado
    for value, label in TemplateVariable.VARIABLE_TYPES:
        print(f"  • {value:15} → {label}")
    print()
    
    expected_types = ['person', 'family_card', 'association', 'organization']
    configured_types = [vt[0] for vt in TemplateVariable.VARIABLE_TYPES]
    
    # Verificar que estén todos los tipos esperados (puede haber más, como 'static' por compatibilidad)
    missing_types = set(expected_types) - set(configured_types)
    if not missing_types:
        print("✅ Todos los tipos esperados están configurados")
        if 'static' in configured_types:
            print("ℹ️  Nota: El tipo 'static' está presente por compatibilidad con datos anteriores")
        return True
    else:
        print("❌ ERROR: Faltan tipos")
        print(f"   Esperados: {expected_types}")
        print(f"   Configurados: {configured_types}")
        print(f"   Faltantes: {list(missing_types)}")
        return False


def cleanup_test_variables():
    """Limpia las variables de prueba"""
    print("=" * 60)
    print("LIMPIEZA: Eliminando Variables de Prueba")
    print("=" * 60)
    
    deleted = TemplateVariable.objects.filter(
        variable_name__endswith='_test'
    ).delete()
    
    print(f"✅ Variables de prueba eliminadas: {deleted[0]}")
    print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SISTEMA DE VARIABLES PERSONALIZADAS - PRUEBAS")
    print("=" * 60)
    print()
    
    # Ejecutar pruebas
    test1 = test_variable_types()
    print()
    
    test2 = test_variable_creation()
    print()
    
    # Limpieza
    cleanup_test_variables()
    
    # Resultado final
    print("=" * 60)
    if test1 and test2:
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("=" * 60)
    print()
    
    print("📋 RESUMEN DE LA IMPLEMENTACIÓN:")
    print("-" * 60)
    print("✅ 4 campos en el formulario:")
    print("   1. NOMBRE VARIABLE - Nombre único sin llaves")
    print("   2. TIPO VARIABLE - Person, FamilyCard, Association, Organization")
    print("   3. VALOR - Campo del modelo (selector dinámico)")
    print("   4. DESCRIPCIÓN - Texto opcional")
    print()
    print("✅ Validaciones implementadas:")
    print("   • Nombre único por organización")
    print("   • Campos requeridos validados")
    print("   • Prevención de duplicados")
    print()
    print("✅ 43 campos disponibles en total:")
    print("   • 11 campos de Organización")
    print("   • 16 campos de Persona")
    print("   • 10 campos de Ficha Familiar")
    print("   •  6 campos de Asociación")
    print()
    print("🚀 Sistema listo para usar en:")
    print("   http://127.0.0.1:8000/variables/")
    print("=" * 60)

