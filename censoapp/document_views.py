"""
Vista y funciones para generación de documentos
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.conf import settings
from datetime import date, timedelta
from censoapp.models import (
    Person, DocumentType, GeneratedDocument,
    BoardPosition, Organizations
)
import logging
import hashlib
import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import html

logger = logging.getLogger(__name__)


def sanitize_text_for_pdf(text):
    """
    Sanitiza texto para uso seguro en PDFs.
    Escapa caracteres especiales XML/HTML y remueve caracteres problemáticos.
    """
    if text is None:
        return ""

    # Convertir a string si no lo es
    text = str(text)

    # Escapar caracteres HTML/XML especiales
    text = html.escape(text)

    # Reemplazar caracteres problemáticos
    replacements = {
        '\r\n': '<br/>',
        '\n': '<br/>',
        '\r': '<br/>',
        '\t': '    ',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


@login_required
def generate_document_view(request, person_id):
    """
    Vista para generar un documento para una persona.
    Muestra formulario con tipos de documentos disponibles.
    """
    person = get_object_or_404(Person, pk=person_id, state=True)

    # Obtener organización de la persona
    organization = person.family_card.organization

    # VALIDACIÓN: Verificar que el usuario tenga permiso para generar documentos de esta organización
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if user_profile.organization != organization:
                messages.error(
                    request,
                    f"No tiene permisos para generar documentos para personas de {organization.organization_name}. "
                    f"Solo puede generar documentos para su organización: {user_profile.organization.organization_name}."
                )
                return redirect('detail-person', pk=person_id)
        except AttributeError:
            messages.error(request, "No tiene un perfil de usuario configurado. Contacte al administrador.")
            return redirect('home')

    # Obtener tipos de documentos activos
    document_types = DocumentType.objects.filter(is_active=True)

    # Verificar que exista junta directiva vigente
    today = date.today()
    board_positions = BoardPosition.get_valid_positions_on_date(organization, today)
    signers = BoardPosition.get_signers_on_date(organization, today)

    if request.method == 'POST':
        document_type_id = request.POST.get('document_type')
        expiration_days = request.POST.get('expiration_days', 365)

        try:
            document_type = get_object_or_404(DocumentType, pk=document_type_id, is_active=True)

            # Verificar que haya firmantes disponibles
            if not signers.exists():
                messages.error(
                    request,
                    "No hay junta directiva vigente autorizada para firmar documentos. "
                    "Por favor, contacte al administrador."
                )
                return redirect('detail-person', pk=person_id)

            # Calcular fecha de vencimiento
            issue_date = today
            expiration_date = None
            if document_type.requires_expiration:
                try:
                    days = int(expiration_days)
                    expiration_date = issue_date + timedelta(days=days)
                except (ValueError, TypeError):
                    expiration_date = issue_date + timedelta(days=365)

            # Generar contenido del documento
            content = generate_document_content(
                document_type=document_type,
                person=person,
                organization=organization,
                issue_date=issue_date,
                expiration_date=expiration_date
            )

            # Crear el documento (el número se genera automáticamente)
            generated_doc = GeneratedDocument.objects.create(
                document_type=document_type,
                person=person,
                organization=organization,
                document_content=content,
                issue_date=issue_date,
                expiration_date=expiration_date,
                status='ISSUED'
            )

            # Agregar firmantes
            generated_doc.signers.set(signers)

            # Generar y guardar hash de verificación inmediatamente
            verification_data = f"{generated_doc.id}|{generated_doc.document_number}|{generated_doc.issue_date.isoformat()}"
            verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]
            generated_doc.verification_hash = verification_hash
            generated_doc.save(update_fields=['verification_hash'])

            logger.info(
                f"Documento creado: {generated_doc.document_number} - "
                f"Hash: {verification_hash} - "
                f"Persona: {person.full_name}"
            )

            messages.success(
                request,
                f"Documento '{document_type.document_type_name}' generado exitosamente. "
                f"Número: {generated_doc.document_number}"
            )

            # Redirigir a vista de descarga del documento
            return redirect('view-document', document_id=generated_doc.id)

        except Exception as e:
            logger.error(f"Error al generar documento: {e}")
            messages.error(
                request,
                f"Error al generar el documento: {str(e)}"
            )
            return redirect('detail-person', pk=person_id)

    context = {
        'person': person,
        'document_types': document_types,
        'organization': organization,
        'has_board': board_positions.exists(),
        'has_signers': signers.exists(),
        'signers': signers,
        'segment': 'personas'
    }

    return render(request, 'censo/documentos/generate_document.html', context)


def generate_document_content(document_type, person, organization, issue_date, expiration_date):
    """
    Genera el contenido del documento basado en la plantilla.

    Args:
        document_type: Tipo de documento
        person: Persona beneficiaria
        organization: Organización que expide
        issue_date: Fecha de expedición
        expiration_date: Fecha de vencimiento (puede ser None)

    Returns:
        str: Contenido del documento con variables reemplazadas
    """
    # Obtener plantilla o usar plantilla por defecto
    template = document_type.template_content

    if not template:
        # Plantilla por defecto según tipo de documento
        if 'aval' in document_type.document_type_name.lower():
            template = get_default_aval_template()
        elif 'constancia' in document_type.document_type_name.lower():
            template = get_default_constancia_template()
        else:
            template = get_default_document_template()

    # Variables disponibles para reemplazo
    variables = {
        # Datos de la persona
        '{nombre_completo}': person.full_name,
        '{primer_nombre}': person.first_name_1,
        '{segundo_nombre}': person.first_name_2 or '',
        '{primer_apellido}': person.last_name_1,
        '{segundo_apellido}': person.last_name_2 or '',
        '{identificacion}': person.identification_person,
        '{tipo_documento}': person.document_type.document_type,
        '{edad}': person.calcular_anios,
        '{fecha_nacimiento}': person.date_birth.strftime('%d/%m/%Y'),

        # Datos de ubicación
        '{vereda}': person.family_card.sidewalk_home.sidewalk_name,
        '{zona}': person.family_card.zone,
        '{direccion}': person.family_card.address_home or 'No especificada',

        # Datos de la organización
        '{organizacion}': organization.organization_name,
        '{nit_organizacion}': getattr(organization, 'nit', 'No especificado'),

        # Fechas
        '{fecha_expedicion}': issue_date.strftime('%d de %B de %Y'),
        '{fecha_vencimiento}': expiration_date.strftime('%d de %B de %Y') if expiration_date else 'No aplica',
        '{año}': str(issue_date.year),
        '{mes}': issue_date.strftime('%B'),
        '{dia}': str(issue_date.day),
    }

    # Reemplazar variables en la plantilla
    content = template
    for variable, value in variables.items():
        content = content.replace(variable, str(value))

    return content


def get_default_aval_template():
    """Plantilla por defecto para Aval"""
    return """
LA JUNTA DIRECTIVA DE {organizacion}

CERTIFICA QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion}, 
nacido(a) el {fecha_nacimiento}, residente en la vereda {vereda}, zona {zona}, 
es miembro activo de nuestra comunidad.

Por lo tanto, se expide el presente AVAL para los fines que la persona interesada 
estime conveniente.

Expedido en {vereda}, a los {dia} días del mes de {mes} de {año}.

Válido hasta: {fecha_vencimiento}
"""


def get_default_constancia_template():
    """Plantilla por defecto para Constancia de Pertenencia"""
    return """
LA JUNTA DIRECTIVA DE {organizacion}

HACE CONSTAR QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion},
nacido(a) el {fecha_nacimiento}, con {edad} de edad, es miembro perteneciente 
a nuestra comunidad indígena.

La persona reside en la vereda {vereda}, zona {zona}, y se encuentra registrada 
en nuestro censo comunitario.

Se expide la presente CONSTANCIA DE PERTENENCIA a solicitud del interesado(a) 
para los fines que estime conveniente.

Expedido en {vereda}, a los {dia} días del mes de {mes} de {año}.

Válido hasta: {fecha_vencimiento}
"""


def get_default_document_template():
    """Plantilla genérica por defecto"""
    return """
{organizacion}

CERTIFICA QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion},
es miembro de nuestra comunidad.

Datos adicionales:
- Fecha de nacimiento: {fecha_nacimiento}
- Edad: {edad}
- Vereda: {vereda}
- Zona: {zona}

Se expide el presente documento a los {dia} días del mes de {mes} de {año}.

Válido hasta: {fecha_vencimiento}
"""


@login_required
def view_document(request, document_id):
    """
    Vista para visualizar un documento generado.
    """
    document = get_object_or_404(GeneratedDocument, pk=document_id)

    # VALIDACIÓN: Verificar permisos (solo organización propietaria o admin)
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if user_profile.organization != document.organization:
                messages.error(
                    request,
                    f"No tiene permisos para ver este documento. "
                    f"El documento pertenece a {document.organization.organization_name}."
                )
                return redirect('home')
        except AttributeError:
            messages.error(request, "No tiene un perfil de usuario configurado. Contacte al administrador.")
            return redirect('home')

    context = {
        'document': document,
        'person': document.person,
        'organization': document.organization,
        'signers': document.signers.all(),
        'segment': 'personas'
    }

    return render(request, 'censo/documentos/view_document.html', context)


@login_required
def list_person_documents(request, person_id):
    """
    Lista todos los documentos generados para una persona.
    """
    person = get_object_or_404(Person, pk=person_id, state=True)

    # VALIDACIÓN: Verificar que el usuario tenga permiso para ver documentos de esta organización
    person_organization = person.family_card.organization
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if user_profile.organization != person_organization:
                messages.error(
                    request,
                    f"No tiene permisos para ver documentos de personas de {person_organization.organization_name}."
                )
                return redirect('personas')
        except AttributeError:
            messages.error(request, "No tiene un perfil de usuario configurado. Contacte al administrador.")
            return redirect('home')

    documents = GeneratedDocument.objects.filter(
        person=person
    ).select_related('document_type', 'organization').prefetch_related('signers').order_by('-issue_date')

    context = {
        'person': person,
        'documents': documents,
        'segment': 'personas'
    }

    return render(request, 'censo/documentos/list_documents.html', context)


@login_required
def preview_document_pdf(request, document_id):
    """
    Vista previa del PDF en una página dedicada con PDF.js
    Permite visualizar, descargar e imprimir el documento.
    """
    document = get_object_or_404(GeneratedDocument, pk=document_id)

    # VALIDACIÓN: Verificar permisos por organización
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if user_profile.organization != document.organization:
                messages.error(
                    request,
                    f"No tiene permisos para ver este documento. "
                    f"El documento pertenece a {document.organization.organization_name}."
                )
                return redirect('home')
        except AttributeError:
            messages.error(request, "No tiene un perfil de usuario configurado. Contacte al administrador.")
            return redirect('home')

    context = {
        'document': document,
        'person': document.person,
        'organization': document.organization,
        'segment': 'documentos'
    }

    return render(request, 'censo/documentos/preview_document.html', context)


@login_required
def organization_documents_stats(request, organization_id=None):
    """
    Muestra estadísticas de documentos generados por organización.
    """
    # Determinar la organización a mostrar
    organization = None

    if organization_id:
        # Se especificó una organización específica
        organization = get_object_or_404(Organizations, pk=organization_id)

        # Verificar permisos
        if not request.user.is_superuser:
            user_profile = getattr(request.user, 'userprofile', None)
            if not user_profile or user_profile.organization != organization:
                messages.error(request, "No tiene permisos para ver estas estadísticas.")
                return redirect('home')
    else:
        # No se especificó organización
        if request.user.is_superuser:
            # Admin: Mostrar todas las organizaciones
            organizations = Organizations.objects.all()

            stats_by_org = []
            for org in organizations:
                stats = GeneratedDocument.objects.filter(organization=org).aggregate(
                    total=Count('id'),
                    emitidos=Count('id', filter=Q(status='ISSUED')),
                    anulados=Count('id', filter=Q(status='REVOKED')),
                    vencidos=Count('id', filter=Q(status='EXPIRED'))
                )

                # Estadísticas por tipo de documento
                by_type = GeneratedDocument.objects.filter(
                    organization=org
                ).values(
                    'document_type__document_type_name'
                ).annotate(
                    total=Count('id')
                ).order_by('-total')

                stats_by_org.append({
                    'organization': org,
                    'stats': stats,
                    'by_type': by_type
                })

            context = {
                'stats_by_org': stats_by_org,
                'segment': 'documentos'
            }

            return render(request, 'censo/documentos/all_organizations_stats.html', context)
        else:
            # Usuario regular: Obtener su organización
            try:
                user_profile = request.user.userprofile
                if not user_profile.organization:
                    messages.error(request, "No tiene una organización asignada.")
                    return redirect('home')

                organization = user_profile.organization
            except AttributeError:
                messages.error(request, "No tiene un perfil de usuario configurado. Contacte al administrador.")
                return redirect('home')

    # Si llegamos aquí, tenemos una organización específica para mostrar
    # Estadísticas generales
    stats = GeneratedDocument.objects.filter(organization=organization).aggregate(
        total=Count('id'),
        emitidos=Count('id', filter=Q(status='ISSUED')),
        anulados=Count('id', filter=Q(status='REVOKED')),
        vencidos=Count('id', filter=Q(status='EXPIRED'))
    )

    # Estadísticas por tipo de documento
    stats_by_type = GeneratedDocument.objects.filter(
        organization=organization
    ).values(
        'document_type__document_type_name'
    ).annotate(
        total=Count('id'),
        emitidos=Count('id', filter=Q(status='ISSUED')),
        anulados=Count('id', filter=Q(status='REVOKED'))
    ).order_by('-total')

    # Últimos documentos generados (para gráficos)
    recent_documents = GeneratedDocument.objects.filter(
        organization=organization
    ).select_related(
        'document_type', 'person'
    ).order_by('-issue_date')[:10]

    # TODOS los documentos de la organización (para DataTable)
    all_documents = GeneratedDocument.objects.filter(
        organization=organization
    ).select_related(
        'document_type', 'person'
    ).order_by('-issue_date')

    # Documentos por mes (últimos 6 meses)
    from django.utils import timezone
    from datetime import timedelta

    six_months_ago = timezone.now().date() - timedelta(days=180)

    docs_by_month = GeneratedDocument.objects.filter(
        organization=organization,
        issue_date__gte=six_months_ago
    ).extra(
        select={'month': "strftime('%%Y-%%m', issue_date)"}
    ).values('month').annotate(
        total=Count('id')
    ).order_by('month')

    context = {
        'organization': organization,
        'stats': stats,
        'stats_by_type': stats_by_type,
        'recent_documents': recent_documents,
        'all_documents': all_documents,  # Nuevo: todos los documentos para DataTable
        'docs_by_month': docs_by_month,
        'segment': 'documentos'
    }

    return render(request, 'censo/documentos/organization_stats.html', context)


def generate_document_qr(document):
    """
    Genera código QR para verificación del documento.

    Args:
        document: Instancia de GeneratedDocument

    Returns:
        BytesIO: Buffer con la imagen del código QR
    """
    # Crear hash único del documento para verificación
    verification_data = f"{document.id}|{document.document_number}|{document.issue_date.isoformat()}"
    doc_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]

    # Guardar hash en el documento si no existe o está vacío
    if not document.verification_hash:
        document.verification_hash = doc_hash
        document.save(update_fields=['verification_hash'])
        logger.info(f"Hash de verificación generado y guardado para documento {document.document_number}: {doc_hash}")
    else:
        # Usar el hash existente
        doc_hash = document.verification_hash
        logger.debug(f"Usando hash de verificación existente para documento {document.document_number}: {doc_hash}")

    # URL de verificación (ajustar según tu dominio en producción)
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    verification_url = f"{site_url}/documento/verificar/{doc_hash}/"

    # Generar código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(verification_url)
    qr.make(fit=True)

    # Crear imagen
    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar en buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer


@login_required
def download_document_pdf(request, document_id):
    """
    Genera y muestra un documento en formato PDF con código QR.
    El PDF se muestra en el navegador (inline) para previsualización.
    """
    document = get_object_or_404(GeneratedDocument, pk=document_id)

    # VALIDACIÓN: Verificar permisos por organización
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if user_profile.organization != document.organization:
                messages.error(
                    request,
                    f"No tiene permisos para descargar este documento. "
                    f"El documento pertenece a {document.organization.organization_name}."
                )
                return JsonResponse({'error': 'No autorizado'}, status=403)
        except AttributeError:
            return JsonResponse({'error': 'No tiene un perfil de usuario configurado'}, status=403)

    try:
        # Crear buffer para el PDF
        buffer = BytesIO()

        # Crear documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Contenedor para los elementos del PDF
        elements = []

        # Estilos
        styles = getSampleStyleSheet()

        # Estilo para el título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2196F3'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Estilo para subtítulos
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#424242'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Estilo para el contenido
        content_style = ParagraphStyle(
            'CustomContent',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=16
        )

        # Estilo para información adicional
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT,
            fontName='Helvetica'
        )

        # Encabezado con nombre de la organización
        org_name = Paragraph(
            f"<b>{sanitize_text_for_pdf(document.organization.organization_name.upper())}</b>",
            title_style
        )
        elements.append(org_name)
        elements.append(Spacer(1, 12))

        # Tipo de documento
        doc_type = Paragraph(
            f"<b>{sanitize_text_for_pdf(document.document_type.document_type_name.upper())}</b>",
            subtitle_style
        )
        elements.append(doc_type)
        elements.append(Spacer(1, 20))

        # Número de documento
        doc_number = Paragraph(
            f"<b>Documento No: {sanitize_text_for_pdf(document.document_number)}</b>",
            info_style
        )
        elements.append(doc_number)
        elements.append(Spacer(1, 20))

        # Contenido del documento
        content_lines = document.document_content.split('\n')
        for line in content_lines:
            if line.strip():
                sanitized_line = sanitize_text_for_pdf(line)
                p = Paragraph(sanitized_line, content_style)
                elements.append(p)

        elements.append(Spacer(1, 30))

        # Información de fechas
        date_info = [
            ['<b>Fecha de Expedición:</b>', document.issue_date.strftime('%d de %B de %Y')],
        ]

        if document.expiration_date:
            date_info.append(
                ['<b>Válido hasta:</b>', document.expiration_date.strftime('%d de %B de %Y')]
            )

        date_table = Table(date_info, colWidths=[2*inch, 3*inch])
        date_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#424242')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(date_table)
        elements.append(Spacer(1, 30))

        # Firmas
        if document.signers.exists():
            elements.append(Spacer(1, 20))
            firma_title = Paragraph("<b>FIRMAS AUTORIZADAS</b>", subtitle_style)
            elements.append(firma_title)
            elements.append(Spacer(1, 20))

            signer_data = []
            for signer in document.signers.all():
                # Usar holder_person ya que BoardPosition tiene holder_person, no person
                if signer.holder_person:
                    signer_data.append([
                        f"_______________________________",
                        f"_______________________________"
                    ])
                    signer_data.append([
                        f"<b>{sanitize_text_for_pdf(signer.holder_person.full_name)}</b>",
                        f"<b>C.C. {sanitize_text_for_pdf(signer.holder_person.identification_person)}</b>"
                    ])
                    signer_data.append([
                        f"{sanitize_text_for_pdf(signer.get_position_name_display())}",
                        ""
                    ])
                    signer_data.append(['', ''])  # Espacio entre firmantes

            signer_table = Table(signer_data, colWidths=[3*inch, 3*inch])
            signer_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#424242')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(signer_table)

        # Generar código QR
        qr_buffer = generate_document_qr(document)
        qr_img = Image(qr_buffer, width=1.5*inch, height=1.5*inch)

        # Tabla para QR y texto de verificación
        verification_hash = document.verification_hash if hasattr(document, 'verification_hash') else 'N/A'
        qr_data = [
            [qr_img, Paragraph(
                f"<b>Código de Verificación</b><br/>"
                f"Escanea este código QR para verificar la autenticidad del documento.<br/>"
                f"<b>Hash:</b> {sanitize_text_for_pdf(verification_hash)}",
                info_style
            )]
        ]

        qr_table = Table(qr_data, colWidths=[2*inch, 4*inch])
        qr_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))

        elements.append(Spacer(1, 30))
        elements.append(qr_table)

        # Pie de página con información adicional
        elements.append(Spacer(1, 20))
        footer_text = Paragraph(
            f"<i>Este documento fue generado electrónicamente por el sistema de censo de {sanitize_text_for_pdf(document.organization.organization_name)}. "
            f"Para verificar su autenticidad, escanee el código QR o visite nuestro portal de verificación.</i>",
            info_style
        )
        elements.append(footer_text)

        # Construir PDF
        doc.build(elements)

        # Obtener el PDF del buffer
        pdf = buffer.getvalue()
        buffer.close()

        # Determinar si es descarga o previsualización
        is_download = request.GET.get('download', 'false').lower() == 'true'

        # Retornar PDF
        response = HttpResponse(pdf, content_type='application/pdf')

        # Agregar cabeceras necesarias para PDF.js
        response['Content-Length'] = len(pdf)
        response['Accept-Ranges'] = 'bytes'

        # Cabeceras CORS para permitir la carga desde PDF.js
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type'

        if is_download:
            # Forzar descarga
            response['Content-Disposition'] = f'attachment; filename="documento_{document.document_number}.pdf"'
        else:
            # Previsualización en navegador
            response['Content-Disposition'] = f'inline; filename="documento_{document.document_number}.pdf"'
            # Cache control para previsualización
            response['Cache-Control'] = 'public, max-age=3600'

        return response

    except Exception as e:
        logger.error(f"Error al generar PDF: {e}")
        messages.error(request, f"Error al generar el PDF: {str(e)}")
        return redirect('view-document', document_id=document_id)


def verify_document(request, hash):
    """
    Verifica la autenticidad de un documento mediante su hash de verificación.
    Esta vista es de acceso público para permitir verificación por terceros.

    Args:
        request: HttpRequest
        hash: Hash de verificación del documento (extraído del código QR)

    Returns:
        render: Página de verificación con resultado (válido/vencido/inválido)
    """
    try:
        # Buscar documento por hash de verificación
        document = GeneratedDocument.objects.select_related(
            'document_type', 'person', 'person__document_type',
            'person__family_card', 'person__family_card__sidewalk_home',
            'organization'
        ).get(verification_hash=hash)

        # Determinar estado del documento
        today = date.today()
        is_issued = document.status == 'ISSUED'
        is_expired = document.expiration_date and document.expiration_date < today
        is_revoked = document.status == 'REVOKED'

        # Calcular estado de verificación
        if is_revoked:
            verification_status = 'REVOCADO'
            status_class = 'danger'
            status_icon = 'fa-ban'
        elif is_expired:
            verification_status = 'VENCIDO'
            status_class = 'warning'
            status_icon = 'fa-clock'
        elif is_issued:
            verification_status = 'VÁLIDO'
            status_class = 'success'
            status_icon = 'fa-check-circle'
        else:
            verification_status = 'INVÁLIDO'
            status_class = 'danger'
            status_icon = 'fa-times-circle'

        # Determinar si el usuario está autenticado para mostrar información completa o limitada
        is_authenticated = request.user.is_authenticated

        # Información básica (siempre visible para todos)
        basic_info = {
            'document_type': document.document_type.document_type_name,
            'document_number': document.document_number,
            'issue_date': document.issue_date,
            'expiration_date': document.expiration_date,
            'organization_name': document.organization.organization_name,
            'status': verification_status,
        }

        # Información sensible (solo para usuarios autenticados)
        sensitive_info = {
            'person_full_name': document.person.full_name,
            'person_identification': document.person.identification_person,
            'person_document_type': document.person.document_type.document_type,
            'organization_nit': getattr(document.organization, 'nit', None),
            'verification_hash': document.verification_hash,
        } if is_authenticated else {}

        # Preparar contexto
        context = {
            'found': True,
            'document': document,
            'person': document.person if is_authenticated else None,
            'organization': document.organization,
            'verification_status': verification_status,
            'status_class': status_class,
            'status_icon': status_icon,
            'is_valid': is_issued and not is_expired and not is_revoked,
            'is_expired': is_expired,
            'is_revoked': is_revoked,
            'is_authenticated': is_authenticated,
            'basic_info': basic_info,
            'sensitive_info': sensitive_info,
            'segment': 'verificacion'
        }

        # Logging diferenciado
        if is_authenticated:
            logger.info(
                f"Verificación autenticada de documento {document.document_number} - "
                f"Hash: {hash} - Usuario: {request.user.username}"
            )
        else:
            logger.info(
                f"Verificación pública de documento {document.document_number} - "
                f"Hash: {hash} - IP: {request.META.get('REMOTE_ADDR', 'desconocida')}"
            )

    except GeneratedDocument.DoesNotExist:
        # Documento no encontrado - hash inválido o documento falsificado
        context = {
            'found': False,
            'verification_status': 'NO ENCONTRADO',
            'status_class': 'danger',
            'status_icon': 'fa-exclamation-triangle',
            'error_message': 'El código QR escaneado no corresponde a ningún documento registrado en el sistema.',
            'segment': 'verificacion'
        }

        logger.warning(f"Intento de verificación con hash inválido: {hash}")

    except Exception as e:
        # Error inesperado
        logger.error(f"Error al verificar documento con hash {hash}: {e}")
        context = {
            'found': False,
            'verification_status': 'ERROR',
            'status_class': 'danger',
            'status_icon': 'fa-exclamation-circle',
            'error_message': 'Ocurrió un error al verificar el documento. Por favor, intente nuevamente.',
            'segment': 'verificacion'
        }

    return render(request, 'censo/documentos/verify_document.html', context)
