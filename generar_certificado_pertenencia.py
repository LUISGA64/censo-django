"""
Script para generar un documento de prueba: Certificado de Pertenencia a la Comunidad

Este script:
1. Verifica que existan los datos necesarios (organización, persona, tipo de documento, junta directiva)
2. Genera un certificado de pertenencia para una persona de la organización 1
3. Muestra la información del documento generado
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import (
    Person, Organizations, DocumentType, GeneratedDocument, BoardPosition
)

print("=" * 80)
print("📜 GENERACIÓN DE CERTIFICADO DE PERTENENCIA - DOCUMENTO DE PRUEBA")
print("=" * 80)

# 1. Verificar que exista la organización
print("\n1️⃣  Verificando organización...")
try:
    organization = Organizations.objects.get(id=1)
    print(f"   ✅ Organización encontrada: {organization.organization_name}")
except Organizations.DoesNotExist:
    print("   ❌ No se encontró la organización con ID 1")
    print("   💡 Ejecuta primero el script de creación de datos básicos")
    exit(1)

# 2. Verificar que exista el tipo de documento "Constancia de Pertenencia"
print("\n2️⃣  Verificando tipo de documento...")
try:
    doc_type = DocumentType.objects.get(
        document_type_name="Constancia de Pertenencia",
        is_active=True
    )
    print(f"   ✅ Tipo de documento encontrado: {doc_type.document_type_name}")
    print(f"      - Descripción: {doc_type.description}")
    print(f"      - Requiere vencimiento: {'Sí' if doc_type.requires_expiration else 'No'}")
except DocumentType.DoesNotExist:
    print("   ❌ No se encontró el tipo de documento 'Constancia de Pertenencia'")
    print("   💡 Ejecuta primero: python crear_datos_documentos.py")
    exit(1)

# 3. Verificar que exista una persona en la organización
print("\n3️⃣  Buscando persona en la organización...")
person = Person.objects.filter(
    family_card__organization=organization,
    state=True
).first()

if not person:
    print("   ❌ No hay personas registradas en esta organización")
    print("   💡 Ejecuta primero el script de creación de 50 fichas familiares")
    exit(1)

print(f"   ✅ Persona seleccionada: {person.full_name}")
print(f"      - Identificación: {person.document_type} {person.identification_person}")
print(f"      - Fecha de nacimiento: {person.date_birth.strftime('%d/%m/%Y')}")
print(f"      - Edad: {person.calcular_anios}")
if person.family_card and person.family_card.sidewalk_home:
    print(f"      - Vereda: {person.family_card.sidewalk_home.sidewalk_name}")
    print(f"      - Zona: {person.family_card.zone}")

# 4. Verificar que exista junta directiva vigente
print("\n4️⃣  Verificando junta directiva vigente...")
today = date.today()
board_positions = BoardPosition.get_valid_positions_on_date(organization, today)
signers = BoardPosition.get_signers_on_date(organization, today)

if not board_positions.exists():
    print("   ❌ No hay junta directiva vigente para esta organización")
    print("   💡 Ejecuta primero: python crear_datos_documentos.py")
    exit(1)

print(f"   ✅ Junta directiva vigente encontrada")
print(f"      - Total de cargos: {board_positions.count()}")
print(f"      - Firmantes autorizados: {signers.count()}")
print("\n      Firmantes:")
for signer in signers:
    print(f"         - {signer.get_position_name_display()}: {signer.holder_person.full_name}")

# 5. Generar el documento
print("\n5️⃣  Generando certificado de pertenencia...")

# Fechas del documento
issue_date = today
expiration_date = today + timedelta(days=90)  # 90 días de vigencia

# Generar contenido del documento usando la plantilla
template = doc_type.template_content

# Variables para la plantilla
from datetime import datetime
meses = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}

variables = {
    'organizacion': organization.organization_name,
    'nombre_completo': person.full_name,
    'tipo_documento': str(person.document_type),
    'identificacion': person.identification_person,
    'fecha_nacimiento': person.date_birth.strftime('%d de %B de %Y'),
    'edad': person.calcular_anios,
    'vereda': person.family_card.sidewalk_home.sidewalk_name if person.family_card and person.family_card.sidewalk_home else 'N/A',
    'zona': person.family_card.zone if person.family_card else 'N/A',
    'direccion': person.family_card.address_home if person.family_card and person.family_card.address_home else 'N/A',
    'dia': today.day,
    'mes': meses[today.month],
    'año': today.year,
    'fecha_vencimiento': expiration_date.strftime('%d de %B de %Y')
}

# Reemplazar variables en la plantilla
document_content = template
for key, value in variables.items():
    document_content = document_content.replace(f'{{{key}}}', str(value))

# Crear el documento
try:
    document = GeneratedDocument.objects.create(
        person=person,
        document_type=doc_type,
        organization=organization,
        document_content=document_content,
        issue_date=issue_date,
        expiration_date=expiration_date,
        status='ISSUED',
        created_by=None  # Usuario del sistema (puede ser None para scripts)
    )

    # Asignar firmantes
    document.signers.set(signers)
    document.save()

    print(f"   ✅ Certificado generado exitosamente")
    print(f"      - ID del documento: {document.id}")
    print(f"      - Número de documento: {document.document_number or 'Por asignar'}")
    print(f"      - Fecha de expedición: {document.issue_date.strftime('%d/%m/%Y')}")
    print(f"      - Fecha de vencimiento: {document.expiration_date.strftime('%d/%m/%Y')}")
    print(f"      - Estado: {document.get_status_display()}")
    if document.verification_hash:
        print(f"      - Hash de verificación: {document.verification_hash[:16]}...")

except Exception as e:
    print(f"   ❌ Error al generar el documento: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

# 6. Mostrar información del documento generado
print("\n6️⃣  Información completa del documento generado:")
print("\n" + "=" * 80)
print(f"CERTIFICADO DE PERTENENCIA No. {document.document_number or 'Por asignar'}")
print("=" * 80)
print(f"\nOrganización: {organization.organization_name}")
print(f"NIT: {organization.organization_identification}")
print(f"\nPersona: {person.full_name}")
print(f"Documento: {person.document_type} {person.identification_person}")
print(f"Fecha de nacimiento: {person.date_birth.strftime('%d de %B de %Y')}")
print(f"Edad: {person.calcular_anios}")

if person.family_card and person.family_card.sidewalk_home:
    print(f"Vereda: {person.family_card.sidewalk_home.sidewalk_name}")
    print(f"Zona: {person.family_card.zone}")

print(f"\nFecha de expedición: {document.issue_date.strftime('%d de %B de %Y')}")
print(f"Fecha de vencimiento: {document.expiration_date.strftime('%d de %B de %Y')}")
print(f"Días de vigencia: {(document.expiration_date - document.issue_date).days} días")

print("\nFirmantes:")
for signer in document.signers.all():
    print(f"  - {signer.get_position_name_display()}: {signer.holder_person.full_name}")

if document.verification_hash:
    print(f"\nCódigo de verificación (QR): {document.verification_hash}")
else:
    print(f"\nCódigo de verificación (QR): Por generar")

print("\n" + "-" * 80)
print("CONTENIDO DEL DOCUMENTO:")
print("-" * 80)
print(document.document_content)
print("=" * 80)

# 7. Estadísticas finales
print("\n7️⃣  Estadísticas de documentos:")
total_docs = GeneratedDocument.objects.filter(organization=organization).count()
docs_pertenencia = GeneratedDocument.objects.filter(
    organization=organization,
    document_type=doc_type
).count()

print(f"   - Total de documentos de la organización: {total_docs}")
print(f"   - Certificados de pertenencia: {docs_pertenencia}")
print(f"   - Documentos activos: {GeneratedDocument.objects.filter(organization=organization, status='GENERATED').count()}")
print(f"   - Documentos anulados: {GeneratedDocument.objects.filter(organization=organization, status='CANCELLED').count()}")

print("\n" + "=" * 80)
print("✅ CERTIFICADO DE PERTENENCIA GENERADO EXITOSAMENTE")
print("=" * 80)

print("\n💡 Próximos pasos:")
print("   1. Acceder al sistema web")
print("   2. Ir a: Estadísticas de Documentos")
print("   3. Ver el documento generado en la tabla")
print("   4. Descargar el PDF del certificado")
print("   5. Verificar el código QR del documento")

if document.verification_hash:
    print(f"\n🔗 URL de verificación: /documents/verify/{document.verification_hash}/")
print(f"🔗 URL de descarga: /documents/pdf/{document.id}/")
print(f"🔗 URL de vista previa: /documents/preview/{document.id}/")

print("\n" + "=" * 80)

