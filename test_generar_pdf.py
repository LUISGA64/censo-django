"""
Script para probar la generación de PDF directamente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument
from censoapp.document_views import download_document_pdf
from django.test import RequestFactory
from django.contrib.auth.models import User

# Obtener el documento
document_id = 3
doc = GeneratedDocument.objects.get(id=document_id)

print(f"Documento: {doc.document_number}")
print(f"Tipo: {doc.document_type.document_type_name}")
print(f"Persona: {doc.person.full_name}")
print(f"Organización: {doc.organization.organization_name}")
print(f"Contenido: {len(doc.document_content)} caracteres")
print(f"Firmantes: {doc.signers.count()}")

# Crear una petición falsa
factory = RequestFactory()
request = factory.get(f'/documento/download/{document_id}/')

# Obtener un usuario (superuser para evitar problemas de permisos)
user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.first()

request.user = user

print(f"\nProbando generación de PDF...")

try:
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import html

    # Crear buffer para el PDF
    buffer = BytesIO()

    # Crear documento PDF simple
    doc_pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Estilos
    styles = getSampleStyleSheet()
    elements = []

    # Agregar título
    title = Paragraph(f"<b>{html.escape(doc.organization.organization_name)}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Agregar contenido
    content_lines = doc.document_content.split('\n')
    for line in content_lines[:5]:  # Solo primeras 5 líneas para prueba
        if line.strip():
            p = Paragraph(html.escape(line), styles['BodyText'])
            elements.append(p)

    # Construir PDF
    doc_pdf.build(elements)

    # Obtener tamaño
    pdf_size = buffer.tell()

    print(f"✅ PDF generado exitosamente")
    print(f"   Tamaño: {pdf_size} bytes")

    # Guardar en archivo para verificar
    buffer.seek(0)
    with open('test_documento.pdf', 'wb') as f:
        f.write(buffer.read())

    print(f"   PDF guardado en: test_documento.pdf")

except Exception as e:
    print(f"❌ Error al generar PDF: {e}")
    import traceback
    traceback.print_exc()

