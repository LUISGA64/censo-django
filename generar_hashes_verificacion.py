"""
Script para generar hashes de verificación para todos los documentos
"""
import os
import django
import hashlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument

print("=" * 70)
print("🔐 GENERACIÓN DE HASHES DE VERIFICACIÓN PARA DOCUMENTOS")
print("=" * 70)

docs = GeneratedDocument.objects.all()
total = docs.count()
updated = 0

print(f"\n📊 Total de documentos: {total}\n")

for doc in docs:
    print(f"Documento {doc.id}: {doc.document_number}")
    print(f"  Tipo: {doc.document_type.document_type_name}")
    print(f"  Persona: {doc.person.full_name}")
    print(f"  Organización: {doc.organization.organization_name}")

    has_content = bool(doc.document_content)
    has_hash = bool(doc.verification_hash)
    has_number = bool(doc.document_number)
    signers_count = doc.signers.count()

    print(f"  ✓ Contenido: {'Sí' if has_content else 'NO'} ({len(doc.document_content) if has_content else 0} caracteres)")
    print(f"  ✓ Número: {'Sí' if has_number else 'NO'}")
    print(f"  ✓ Firmantes: {signers_count}")
    print(f"  ✓ Hash: {'Sí' if has_hash else 'NO'}")

    if not has_hash:
        # Generar hash
        verification_data = f"{doc.id}|{doc.document_number}|{doc.issue_date.isoformat()}"
        doc.verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]
        doc.save(update_fields=['verification_hash'])
        print(f"  ✅ Hash generado: {doc.verification_hash}")
        updated += 1
    else:
        print(f"  ℹ️  Hash existente: {doc.verification_hash}")

    print()

print("=" * 70)
print(f"✅ PROCESO COMPLETADO")
print(f"   Documentos procesados: {total}")
print(f"   Hashes generados: {updated}")
print(f"   Hashes ya existentes: {total - updated}")
print("=" * 70)

print("\n💡 Próximos pasos:")
print("   1. Limpiar cache del navegador (Ctrl+Shift+Delete)")
print("   2. Acceder a la vista de estadísticas de documentos")
print("   3. Intentar previsualizar el documento")
print("   4. Si persiste el error, usar descarga directa")
print("\n" + "=" * 70)

