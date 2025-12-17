"""
Script para probar la generación de documentos con código QR
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import Person, GeneratedDocument, DocumentType, BoardPosition
from datetime import date, timedelta

def test_document_generation():
    """Prueba la generación de documentos con código QR"""

    print("\n" + "="*70)
    print("🧪 PRUEBA DE GENERACIÓN DE DOCUMENTOS CON CÓDIGO QR")
    print("="*70 + "\n")

    # Obtener una persona de prueba
    try:
        person = Person.objects.filter(state=True).first()
        if not person:
            print("❌ No hay personas en la base de datos")
            return

        print(f"✅ Persona seleccionada: {person.full_name}")
        print(f"   Identificación: {person.identification_person}")
        print(f"   Organización: {person.family_card.organization.organization_name}\n")

    except Exception as e:
        print(f"❌ Error al obtener persona: {e}")
        return

    # Obtener tipo de documento
    try:
        doc_type = DocumentType.objects.filter(is_active=True).first()
        if not doc_type:
            print("❌ No hay tipos de documentos activos")
            return

        print(f"✅ Tipo de documento: {doc_type.document_type_name}\n")

    except Exception as e:
        print(f"❌ Error al obtener tipo de documento: {e}")
        return

    # Verificar junta directiva
    try:
        organization = person.family_card.organization
        today = date.today()

        board_positions = BoardPosition.get_valid_positions_on_date(organization, today)
        signers = BoardPosition.get_signers_on_date(organization, today)

        if not board_positions.exists():
            print("⚠️  No hay junta directiva vigente")
            print("   Creando junta directiva de prueba...\n")
            # Aquí podrías crear una junta de prueba si lo necesitas
            return

        print(f"✅ Junta directiva vigente: {board_positions.count()} cargos")
        print(f"✅ Firmantes autorizados: {signers.count()}\n")

        for signer in signers:
            print(f"   - {signer.position_name}: {signer.holder_person.full_name}")
        print()

    except Exception as e:
        print(f"❌ Error al verificar junta directiva: {e}")
        return

    # Generar documento
    try:
        from censoapp.document_views import generate_document_content

        issue_date = today
        expiration_date = today + timedelta(days=365) if doc_type.requires_expiration else None

        # Generar contenido
        content = generate_document_content(
            document_type=doc_type,
            person=person,
            organization=organization,
            issue_date=issue_date,
            expiration_date=expiration_date
        )

        # Crear documento
        document = GeneratedDocument.objects.create(
            document_type=doc_type,
            person=person,
            organization=organization,
            document_content=content,
            issue_date=issue_date,
            expiration_date=expiration_date,
            status='ISSUED'
        )

        # Agregar firmantes
        document.signers.set(signers)

        print(f"✅ Documento generado exitosamente!")
        print(f"   Número: {document.document_number}")
        print(f"   ID: {document.id}")
        print(f"   Estado: {document.get_status_display()}\n")

    except Exception as e:
        print(f"❌ Error al generar documento: {e}")
        import traceback
        traceback.print_exc()
        return

    # Probar generación de código QR
    try:
        from censoapp.document_views import generate_document_qr

        qr_buffer = generate_document_qr(document)

        # Recargar documento para obtener el hash
        document.refresh_from_db()

        print(f"✅ Código QR generado exitosamente!")
        print(f"   Hash de verificación: {document.verification_hash}")
        print(f"   Tamaño del buffer: {len(qr_buffer.getvalue())} bytes\n")

    except Exception as e:
        print(f"❌ Error al generar código QR: {e}")
        import traceback
        traceback.print_exc()
        return

    # Mostrar URLs de acceso
    print("🌐 URLs para probar:")
    print(f"   Ver documento: http://127.0.0.1:8000/documento/ver/{document.id}/")
    print(f"   Descargar PDF: http://127.0.0.1:8000/documento/descargar/{document.id}/")
    print(f"   Estadísticas: http://127.0.0.1:8000/documentos/estadisticas/{organization.id}/\n")

    # Mostrar estadísticas
    try:
        total_docs = GeneratedDocument.objects.filter(organization=organization).count()
        print(f"📊 Estadísticas de {organization.organization_name}:")
        print(f"   Total de documentos: {total_docs}")
        print(f"   Documentos de {person.full_name}: {GeneratedDocument.objects.filter(person=person).count()}\n")

    except Exception as e:
        print(f"⚠️  Error al obtener estadísticas: {e}\n")

    print("="*70)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("="*70 + "\n")

    print("💡 Próximos pasos:")
    print("   1. Inicia el servidor: python manage.py runserver")
    print("   2. Accede a las URLs mostradas arriba")
    print("   3. Prueba los botones: Vista Previa, Descargar, Imprimir")
    print("   4. Verifica el código QR en el PDF")
    print("   5. Revisa las estadísticas\n")

if __name__ == '__main__':
    test_document_generation()

