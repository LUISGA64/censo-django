"""
Script para verificar el hash de verificación de los documentos generados.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument

print("=" * 80)
print("Verificación de Hash de Documentos")
print("=" * 80)
print()

# Obtener el último documento generado
ultimo_doc = GeneratedDocument.objects.last()

if not ultimo_doc:
    print("❌ No hay documentos en la base de datos.")
else:
    print(f"📄 Documento: #{ultimo_doc.document_number}")
    print(f"   Tipo: {ultimo_doc.document_type.document_type_name}")
    print(f"   Persona: {ultimo_doc.person.full_name}")
    print(f"   Fecha emisión: {ultimo_doc.issue_date}")
    print()
    print(f"🔐 Hash de verificación:")
    print(f"   Valor: {ultimo_doc.verification_hash}")
    print(f"   Longitud: {len(ultimo_doc.verification_hash) if ultimo_doc.verification_hash else 0} caracteres")
    print(f"   Tipo: {type(ultimo_doc.verification_hash).__name__}")
    print()

    if ultimo_doc.verification_hash:
        # Verificar si es un hash SHA-256 válido (64 caracteres hexadecimales)
        import re
        if re.match(r'^[a-fA-F0-9]{64}$', ultimo_doc.verification_hash):
            print("✅ Hash SHA-256 válido (64 caracteres hexadecimales)")
        else:
            print(f"⚠️  Hash NO es SHA-256 válido")
            print(f"   Se esperaban 64 caracteres hexadecimales")
            print(f"   Se encontraron {len(ultimo_doc.verification_hash)} caracteres")

        # Mostrar URL de verificación
        print()
        print(f"🔗 URL de verificación:")
        print(f"   http://127.0.0.1:8000/documento/verificar/{ultimo_doc.verification_hash}/")
    else:
        print("❌ El documento NO tiene hash de verificación")

print()
print("=" * 80)

