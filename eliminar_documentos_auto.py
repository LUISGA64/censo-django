"""
Script para eliminar TODOS los documentos generados.
Ejecución automática sin confirmación.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument

print("=" * 80)
print("Eliminación Automática de Documentos")
print("=" * 80)
print()

# Contar documentos existentes
total_docs = GeneratedDocument.objects.count()

if total_docs == 0:
    print("✅ No hay documentos en la base de datos.")
    print("   El sistema está limpio.")
else:
    print(f"📋 Documentos encontrados: {total_docs}")
    print()

    # Mostrar resumen
    print("Resumen de documentos a eliminar:")
    print("-" * 80)

    from django.db.models import Count
    tipos = GeneratedDocument.objects.values('document_type__document_type_name').annotate(count=Count('id'))
    for tipo in tipos:
        tipo_nombre = tipo['document_type__document_type_name'] or 'Sin tipo'
        count = tipo['count']
        print(f"  - {tipo_nombre}: {count} documento(s)")

    print("-" * 80)
    print()

    # Eliminar AUTOMÁTICAMENTE (sin confirmación)
    print("⚠️  Eliminando documentos automáticamente...")
    print("   (Usuario ha autorizado eliminación automática)")
    print()
    print("🗑️  Eliminando documentos...")

    # Eliminar todos los documentos
    deleted_count, deleted_details = GeneratedDocument.objects.all().delete()

    print(f"✅ {deleted_count} registros eliminados exitosamente")
    print()
    print("Detalles de la eliminación:")
    for model, count in deleted_details.items():
        if count > 0:
            print(f"  - {model}: {count}")

    print()
    print("=" * 80)
    print("✅ Base de datos limpiada correctamente")
    print("   Sistema listo para generar documentos con la nueva funcionalidad")
    print("=" * 80)

print()

