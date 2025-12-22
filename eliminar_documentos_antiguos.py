"""
Script para eliminar todos los documentos generados anteriormente.
Los documentos antiguos pueden no ser compatibles con la nueva funcionalidad de QR.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument

print("=" * 80)
print("Eliminación de Documentos Antiguos")
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

    # Mostrar un resumen antes de eliminar
    print("Resumen de documentos a eliminar:")
    print("-" * 80)

    tipos = GeneratedDocument.objects.values('document_type__document_type_name').distinct()
    for tipo in tipos:
        tipo_nombre = tipo['document_type__document_type_name']
        count = GeneratedDocument.objects.filter(document_type__document_type_name=tipo_nombre).count()
        print(f"  - {tipo_nombre}: {count} documento(s)")

    print("-" * 80)
    print()

    # Eliminar automáticamente
    print("⚠️  ATENCIÓN: Eliminando documentos antiguos...")
    print("   (Confirmación automática - usuario ha autorizado)")
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
    print("   Ahora puede generar documentos con la nueva funcionalidad de QR")
    print("=" * 80)

print()

