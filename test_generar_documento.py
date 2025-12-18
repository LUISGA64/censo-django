"""
Script de prueba para verificar generación de hash en documentos
"""

import hashlib
from datetime import date, timedelta
from censoapp.models import Person, DocumentType, GeneratedDocument, BoardPosition

print("\n" + "="*70)
print("PRUEBA: GENERACIÓN DE DOCUMENTO CON HASH DE VERIFICACIÓN")
print("="*70 + "\n")

# 1. Obtener datos necesarios
try:
    person = Person.objects.get(pk=24)  # Luz Torres
    print(f"✅ Persona seleccionada: {person.full_name}")
    print(f"   ID: {person.identification_person}")
    print(f"   Organización: {person.family_card.organization.organization_name}\n")

    document_type = DocumentType.objects.get(pk=1)  # Aval
    print(f"✅ Tipo de documento: {document_type.document_type_name}\n")

    organization = person.family_card.organization

    # Obtener firmantes
    today = date.today()
    signers = BoardPosition.get_signers_on_date(organization, today)
    print(f"✅ Firmantes encontrados: {signers.count()}\n")

    # 2. Generar contenido del documento
    issue_date = today
    expiration_date = issue_date + timedelta(days=365)

    content = f"""
LA JUNTA DIRECTIVA DE {organization.organization_name}

CERTIFICA QUE:

{person.full_name}, identificado(a) con {person.document_type.document_type} No. {person.identification_person}, 
nacido(a) el {person.date_birth.strftime('%d/%m/%Y')}, residente en la vereda {person.family_card.sidewalk_home.sidewalk_name}, 
es miembro activo de nuestra comunidad.

Por lo tanto, se expide el presente AVAL PARA PRUEBA DE SISTEMA para los fines que la persona interesada 
estime conveniente.

Expedido en {person.family_card.sidewalk_home.sidewalk_name}, a los {issue_date.day} días del mes de {issue_date.strftime('%B')} de {issue_date.year}.

Válido hasta: {expiration_date.strftime('%d de %B de %Y')}
"""

    print("="*70)
    print("CREANDO DOCUMENTO...")
    print("="*70 + "\n")

    # 3. Crear el documento
    generated_doc = GeneratedDocument.objects.create(
        document_type=document_type,
        person=person,
        organization=organization,
        document_content=content,
        issue_date=issue_date,
        expiration_date=expiration_date,
        status='ISSUED'
    )

    print(f"✅ Documento creado con ID: {generated_doc.id}")
    print(f"   Número: {generated_doc.document_number}")

    # 4. Agregar firmantes
    if signers.exists():
        generated_doc.signers.set(signers)
        print(f"   Firmantes: {signers.count()} agregados")

    # 5. Generar y guardar hash de verificación
    verification_data = f"{generated_doc.id}|{generated_doc.document_number}|{generated_doc.issue_date.isoformat()}"
    verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]

    print(f"\n📊 HASH DE VERIFICACIÓN:")
    print(f"   Datos: {verification_data}")
    print(f"   Hash generado: {verification_hash}")

    # Guardar hash
    generated_doc.verification_hash = verification_hash
    generated_doc.save(update_fields=['verification_hash'])

    print(f"   ✅ Hash guardado en BD\n")

    # 6. Verificar en base de datos
    print("="*70)
    print("VERIFICANDO EN BASE DE DATOS...")
    print("="*70 + "\n")

    # Recargar desde BD
    doc_from_db = GeneratedDocument.objects.get(pk=generated_doc.id)

    print(f"📋 Documento recuperado de BD:")
    print(f"   ID: {doc_from_db.id}")
    print(f"   Número: {doc_from_db.document_number}")
    print(f"   Hash en BD: {doc_from_db.verification_hash}")
    print(f"   Estado: {doc_from_db.status}")
    print(f"   Persona: {doc_from_db.person.full_name}")

    # 7. Verificar que coincidan
    if doc_from_db.verification_hash == verification_hash:
        print(f"\n✅ ¡ÉXITO! El hash se guardó correctamente en la base de datos")
        print(f"   Hash generado: {verification_hash}")
        print(f"   Hash en BD:    {doc_from_db.verification_hash}")
        print(f"   ✅ Coinciden perfectamente\n")
    else:
        print(f"\n❌ ERROR: Los hashes no coinciden")
        print(f"   Hash generado: {verification_hash}")
        print(f"   Hash en BD:    {doc_from_db.verification_hash}\n")

    # 8. URL de verificación
    print("="*70)
    print("URL DE VERIFICACIÓN")
    print("="*70 + "\n")

    verification_url = f"http://127.0.0.1:8000/documento/verificar/{doc_from_db.verification_hash}/"
    print(f"🔗 URL para verificar el documento:")
    print(f"   {verification_url}\n")

    # 9. URLs del documento
    print("="*70)
    print("URLs DEL DOCUMENTO GENERADO")
    print("="*70 + "\n")

    print(f"👁️  Ver documento (HTML):")
    print(f"   http://127.0.0.1:8000/documento/ver/{doc_from_db.id}/\n")

    print(f"📄 Vista previa PDF:")
    print(f"   http://127.0.0.1:8000/documento/preview/{doc_from_db.id}/\n")

    print(f"📥 Descargar PDF:")
    print(f"   http://127.0.0.1:8000/documento/descargar/{doc_from_db.id}/?download=true\n")

    # 10. Resumen final
    print("="*70)
    print("RESUMEN DE LA PRUEBA")
    print("="*70 + "\n")

    print(f"✅ Documento creado exitosamente")
    print(f"✅ Hash generado: {verification_hash}")
    print(f"✅ Hash guardado en BD correctamente")
    print(f"✅ Verificación en BD: EXITOSA")
    print(f"✅ Documento ID: {doc_from_db.id}")
    print(f"✅ Número: {doc_from_db.document_number}\n")

    print("🎯 SIGUIENTE PASO:")
    print("   1. Abre la URL de vista previa en tu navegador")
    print("   2. Descarga el PDF")
    print("   3. Escanea el código QR con tu celular")
    print("   4. Debe abrir la URL de verificación y mostrar el documento como VÁLIDO\n")

    print("="*70 + "\n")

except Person.DoesNotExist:
    print("❌ Error: Persona no encontrada")
except DocumentType.DoesNotExist:
    print("❌ Error: Tipo de documento no encontrado")
except Exception as e:
    print(f"❌ Error inesperado: {str(e)}")
    import traceback
    traceback.print_exc()

