"""
Script para crear el documento ID 4 específicamente
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
print("📜 CREANDO DOCUMENTO ID 4 - CERTIFICADO DE PERTENENCIA")
print("=" * 80)

# Verificar si ya existe
existing = GeneratedDocument.objects.filter(id=4).first()
if existing:
    print(f"\n⚠️  El documento ID 4 ya existe: {existing.document_number}")
    print("No es necesario crear uno nuevo.")
    exit(0)

# Obtener datos necesarios
organization = Organizations.objects.get(id=1)
doc_type = DocumentType.objects.get(document_type_name="Constancia de Pertenencia", is_active=True)
person = Person.objects.filter(family_card__organization=organization, state=True).first()

if not person:
    print("❌ No hay personas disponibles")
    exit(1)

# Verificar junta directiva
today = date.today()
signers = BoardPosition.get_signers_on_date(organization, today)

if not signers.exists():
    print("❌ No hay junta directiva vigente")
    exit(1)

# Fechas
issue_date = today
expiration_date = today + timedelta(days=90)

# Generar contenido del documento
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

# Crear contenido
template = doc_type.template_content
document_content = template
for key, value in variables.items():
    document_content = document_content.replace(f'{{{key}}}', str(value))

print(f"\n📋 Creando documento para: {person.full_name}")
print(f"   Organización: {organization.organization_name}")
print(f"   Tipo: {doc_type.document_type_name}")

# Crear documento
doc = GeneratedDocument.objects.create(
    person=person,
    document_type=doc_type,
    organization=organization,
    document_content=document_content,
    issue_date=issue_date,
    expiration_date=expiration_date,
    status='ISSUED'
)

# Asignar firmantes
doc.signers.set(signers)
doc.save()

print(f"\n✅ Documento creado exitosamente")
print(f"   ID: {doc.id}")
print(f"   Número: {doc.document_number}")
print(f"   Hash: {doc.verification_hash}")
print(f"   Estado: {doc.get_status_display()}")
print(f"\n🔗 Vista previa: http://127.0.0.1:8000/documento/preview/{doc.id}/")
print("=" * 80)

