"""
Script para generar hashes de verificación para documentos existentes
que no tienen hash asignado.

Ejecutar con:
python manage.py shell < generar_hashes_documentos.py
"""

import hashlib
from censoapp.models import GeneratedDocument

print("\n" + "="*60)
print("GENERANDO HASHES DE VERIFICACIÓN PARA DOCUMENTOS EXISTENTES")
print("="*60 + "\n")

# Buscar documentos sin hash
documentos_sin_hash = GeneratedDocument.objects.filter(
    verification_hash__isnull=True
) | GeneratedDocument.objects.filter(
    verification_hash=''
)

total = documentos_sin_hash.count()
print(f"📊 Documentos sin hash encontrados: {total}\n")

if total == 0:
    print("✅ Todos los documentos ya tienen hash de verificación.")
    print("\n" + "="*60 + "\n")
    exit()

# Generar y guardar hashes
actualizados = 0
errores = 0

for doc in documentos_sin_hash:
    try:
        # Crear hash único
        verification_data = f"{doc.id}|{doc.document_number}|{doc.issue_date.isoformat()}"
        doc_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]

        # Guardar
        doc.verification_hash = doc_hash
        doc.save(update_fields=['verification_hash'])

        actualizados += 1
        print(f"✅ Documento {doc.document_number:15} | Hash: {doc_hash} | Persona: {doc.person.full_name}")

    except Exception as e:
        errores += 1
        print(f"❌ Error en documento {doc.id}: {str(e)}")

# Resumen
print("\n" + "-"*60)
print(f"📊 RESUMEN:")
print(f"   Total procesados: {total}")
print(f"   ✅ Actualizados:  {actualizados}")
print(f"   ❌ Errores:       {errores}")
print("-"*60 + "\n")

# Verificar
sin_hash_restantes = GeneratedDocument.objects.filter(
    verification_hash__isnull=True
).count() + GeneratedDocument.objects.filter(
    verification_hash=''
).count()

if sin_hash_restantes == 0:
    print("🎉 ¡ÉXITO! Todos los documentos tienen hash de verificación.\n")
else:
    print(f"⚠️ Aún quedan {sin_hash_restantes} documentos sin hash.\n")

print("="*60 + "\n")

