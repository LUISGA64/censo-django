"""
Script para crear datos de prueba para la generación de documentos:
- Tipos de documentos
- Junta directiva
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import (
    DocumentType, BoardPosition, Organizations, Person
)

print("=" * 70)
print("📄 CREACIÓN DE DATOS PARA GENERACIÓN DE DOCUMENTOS")
print("=" * 70)

# 1. Crear tipos de documentos
print("\n1️⃣  Creando tipos de documentos...")

document_types_data = [
    {
        'document_type_name': 'Aval',
        'description': 'Aval comunitario para trámites externos',
        'requires_expiration': True,
        'template_content': """LA JUNTA DIRECTIVA DE {organizacion}

CERTIFICA QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion}, 
nacido(a) el {fecha_nacimiento}, residente en la vereda {vereda}, zona {zona}, 
es miembro activo de nuestra comunidad.

Por lo tanto, se expide el presente AVAL para los fines que la persona interesada 
estime conveniente.

Expedido en {vereda}, a los {dia} días del mes de {mes} de {año}.

Válido hasta: {fecha_vencimiento}"""
    },
    {
        'document_type_name': 'Constancia de Pertenencia',
        'description': 'Constancia de pertenencia a la comunidad indígena',
        'requires_expiration': True,
        'template_content': """LA JUNTA DIRECTIVA DE {organizacion}

HACE CONSTAR QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion},
nacido(a) el {fecha_nacimiento}, con {edad} de edad, es miembro perteneciente 
a nuestra comunidad indígena.

La persona reside en la vereda {vereda}, zona {zona}, y se encuentra registrada 
en nuestro censo comunitario.

Se expide la presente CONSTANCIA DE PERTENENCIA a solicitud del interesado(a) 
para los fines que estime conveniente.

Expedido en {vereda}, a los {dia} días del mes de {mes} de {año}.

Válido hasta: {fecha_vencimiento}"""
    },
    {
        'document_type_name': 'Certificado de Residencia',
        'description': 'Certificado que acredita la residencia en la comunidad',
        'requires_expiration': False,
        'template_content': """LA JUNTA DIRECTIVA DE {organizacion}

CERTIFICA QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion},
reside de manera permanente en la vereda {vereda}, zona {zona}, perteneciente 
a nuestra comunidad.

Dirección: {direccion}

Se expide el presente CERTIFICADO DE RESIDENCIA para los fines que el interesado(a) 
requiera.

Dado en {vereda}, a los {dia} días del mes de {mes} de {año}."""
    }
]

created_count = 0
for doc_data in document_types_data:
    doc_type, created = DocumentType.objects.get_or_create(
        document_type_name=doc_data['document_type_name'],
        defaults=doc_data
    )
    if created:
        print(f"   ✅ Creado: {doc_type.document_type_name}")
        created_count += 1
    else:
        # Actualizar plantilla si ya existe
        doc_type.template_content = doc_data['template_content']
        doc_type.description = doc_data['description']
        doc_type.requires_expiration = doc_data['requires_expiration']
        doc_type.save()
        print(f"   ✅ Actualizado: {doc_type.document_type_name}")

print(f"\n📊 Tipos de documentos creados: {created_count}")
print(f"📊 Total de tipos de documentos activos: {DocumentType.objects.filter(is_active=True).count()}")

# 2. Crear junta directiva de prueba
print("\n2️⃣  Verificando junta directiva...")

# Obtener organizaciones
organizations = Organizations.objects.all()

if not organizations.exists():
    print("   ⚠️  No hay organizaciones registradas. Salteando creación de junta directiva.")
else:
    for org in organizations:
        print(f"\n   🏛️  Organización: {org.organization_name}")

        # Verificar si ya tiene junta directiva vigente
        today = date.today()
        existing_board = BoardPosition.get_valid_positions_on_date(org, today)

        if existing_board.exists():
            print(f"      ✅ Ya tiene junta directiva vigente ({existing_board.count()} cargos)")

            # Mostrar cargos
            for position in existing_board:
                can_sign = "✓ Puede firmar" if position.can_sign_documents else "✗ No puede firmar"
                print(f"         - {position.get_position_name_display()}: {position.holder_person.full_name} ({can_sign})")
        else:
            print(f"      ⚠️  No tiene junta directiva vigente")

            # Obtener personas de la organización para asignar como junta
            personas = Person.objects.filter(
                family_card__organization=org,
                state=True,
                family_head=True  # Solo cabezas de familia
            )[:7]  # Necesitamos al menos 7 personas para los 7 cargos

            if personas.count() < 3:
                print(f"      ❌ No hay suficientes personas para crear junta directiva (mínimo 3)")
                continue

            # Crear junta directiva con personas disponibles
            positions_to_create = [
                ('GOBERNADOR', True),   # Puede firmar
                ('ALCALDE', True),      # Puede firmar
                ('SECRETARIO', True),   # Puede firmar
                ('TESORERO', False),
                ('CAPITAN', False),
                ('ALGUACIL', False),
                ('COMISARIO', False),
            ]

            start_date = today
            end_date = today + timedelta(days=365 * 2)  # 2 años

            created_positions = 0
            for idx, (position_name, can_sign) in enumerate(positions_to_create):
                if idx < personas.count():
                    person = personas[idx]

                    board_position = BoardPosition.objects.create(
                        organization=org,
                        position_name=position_name,
                        holder_person=person,
                        can_sign_documents=can_sign,
                        start_date=start_date,
                        end_date=end_date,
                        is_active=True
                    )

                    sign_info = "✓ Puede firmar" if can_sign else "✗ No puede firmar"
                    print(f"         ✅ {position_name}: {person.full_name} ({sign_info})")
                    created_positions += 1

            print(f"      📊 Cargos creados: {created_positions}")
            print(f"      📅 Vigencia: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")

print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)

# Resumen de tipos de documentos
total_doc_types = DocumentType.objects.filter(is_active=True).count()
print(f"\n📄 Tipos de documentos activos: {total_doc_types}")
for doc_type in DocumentType.objects.filter(is_active=True):
    exp_info = "Con vencimiento" if doc_type.requires_expiration else "Sin vencimiento"
    print(f"   - {doc_type.document_type_name} ({exp_info})")

# Resumen de juntas directivas
print(f"\n🏛️  Organizaciones con junta directiva vigente:")
for org in Organizations.objects.all():
    today = date.today()
    board = BoardPosition.get_valid_positions_on_date(org, today)
    signers = BoardPosition.get_signers_on_date(org, today)

    if board.exists():
        print(f"   ✅ {org.organization_name}:")
        print(f"      - Total cargos: {board.count()}")
        print(f"      - Firmantes: {signers.count()}")
    else:
        print(f"   ❌ {org.organization_name}: Sin junta directiva vigente")

print("\n" + "=" * 70)
print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
print("=" * 70)
print("\n💡 Ahora puedes:")
print("   1. Acceder al detalle de una persona")
print("   2. Hacer clic en 'Generar Documento'")
print("   3. Seleccionar el tipo de documento")
print("   4. Generar y visualizar el documento")
print("\n" + "=" * 70)

