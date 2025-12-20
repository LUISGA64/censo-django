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
from io import BytesIO

# Importar qrcode de forma segura
try:
    import qrcode
    from qrcode.image.pil import PilImage
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    logger.warning("Módulo qrcode no disponible. Instalar con: pip install qrcode[pil]")
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
    Genera el contenido del documento basado en la plantilla personalizada.

    Args:
        document_type: Tipo de documento
        person: Persona beneficiaria
        organization: Organización que expide
        issue_date: Fecha de expedición
        expiration_date: Fecha de vencimiento (puede ser None)

    Returns:
        str: Contenido del documento con variables reemplazadas
    """
    from censoapp.models import DocumentTemplate, TemplateVariable

    # ========================================
    # BUSCAR PLANTILLA PERSONALIZADA
    # ========================================
    # Intentar obtener plantilla personalizada de la organización
    custom_template = DocumentTemplate.objects.filter(
        organization=organization,
        document_type=document_type,
        is_active=True
    ).order_by('-is_default', '-updated_at').first()

    if custom_template:
        # Usar plantilla personalizada
        return render_custom_template(custom_template, person, organization, issue_date, expiration_date)

    # ========================================
    # FALLBACK: PLANTILLA POR DEFECTO (legacy)
    # ========================================
    # Si no hay plantilla personalizada, usar el sistema antiguo
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
        '{edad}': str(person.calcular_anios),
        '{fecha_nacimiento}': person.date_birth.strftime('%d/%m/%Y'),

        # Datos de ubicación
        '{vereda}': person.family_card.sidewalk_home.sidewalk_name,
        '{zona}': person.family_card.zone,
        '{direccion}': person.family_card.address_home or 'No especificada',

        # Datos de la organización
        '{organizacion}': organization.organization_name,
        '{nit_organizacion}': getattr(organization, 'organization_identification', 'No especificado'),

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


def render_custom_template(template, person, organization, issue_date, expiration_date):
    """
    Renderiza una plantilla personalizada con todos sus bloques y estilos.

    Args:
        template: Instancia de DocumentTemplate
        person: Persona beneficiaria
        organization: Organización que expide
        issue_date: Fecha de expedición
        expiration_date: Fecha de vencimiento

    Returns:
        str: HTML del documento renderizado
    """
    from censoapp.models import TemplateVariable

    # ========================================
    # PREPARAR VARIABLES
    # ========================================
    variables = {
        # Datos de la persona
        '{nombre_completo}': person.full_name,
        '{primer_nombre}': person.first_name_1,
        '{segundo_nombre}': person.first_name_2 or '',
        '{primer_apellido}': person.last_name_1,
        '{segundo_apellido}': person.last_name_2 or '',
        '{identificacion}': person.identification_person,
        '{tipo_documento}': person.document_type.document_type,
        '{edad}': str(person.calcular_anios),
        '{fecha_nacimiento}': person.date_birth.strftime('%d/%m/%Y'),
        '{genero}': person.gender.gender if person.gender else '',
        '{estado_civil}': person.civil_state.state_civil if person.civil_state else '',

        # Datos de ubicación
        '{vereda}': person.family_card.sidewalk_home.sidewalk_name,
        '{zona}': person.family_card.zone,
        '{direccion}': person.family_card.address_home or 'No especificada',
        '{municipio}': getattr(person.family_card.sidewalk_home, 'municipio', 'Popayán'),
        '{departamento}': getattr(person.family_card.sidewalk_home, 'departamento', 'Cauca'),

        # Datos de la organización
        '{organizacion}': organization.organization_name,
        '{nit_organizacion}': getattr(organization, 'organization_identification', 'No especificado'),
        '{direccion_organizacion}': getattr(organization, 'organization_address', ''),
        '{telefono_organizacion}': getattr(organization, 'organization_mobile_phone', ''),
        '{email_organizacion}': getattr(organization, 'organization_email', ''),

        # Fechas
        '{fecha_expedicion}': issue_date.strftime('%d de %B de %Y'),
        '{fecha_vencimiento}': expiration_date.strftime('%d de %B de %Y') if expiration_date else 'No aplica',
        '{año}': str(issue_date.year),
        '{mes}': issue_date.strftime('%B'),
        '{dia}': str(issue_date.day),

        # Documento
        '{tipo_documento_generado}': template.document_type.document_type_name,
    }

    # Agregar variables personalizadas de la organización
    # Ahora soporta variables dinámicas que traen datos de modelos relacionados
    custom_vars = TemplateVariable.objects.filter(
        organization=organization,
        is_active=True
    )
    for var in custom_vars:
        # Usar el método get_value() que procesa variables estáticas y dinámicas
        variables[f'{{{var.variable_name}}}'] = var.get_value(
            person=person,
            organization=organization,
            family_card=person.family_card if person else None
        )

    # ========================================
    # CONSTRUIR HTML DEL DOCUMENTO
    # ========================================
    html_parts = []

    # Estilos CSS
    html_parts.append(f'''
    <style>
        body {{
            font-family: {template.font_family};
            font-size: {template.font_size}pt;
            color: {template.text_color};
            margin: {template.margin_top}mm {template.margin_right}mm {template.margin_bottom}mm {template.margin_left}mm;
        }}
        .document-title {{
            text-align: {template.title_alignment};
            font-size: {template.font_size + 4}pt;
            font-weight: bold;
            color: {template.primary_color};
            margin-bottom: 20px;
        }}
        .introduction {{
            text-align: center;
            margin-bottom: 15px;
            {f"font-weight: bold;" if template.introduction_bold else ""}
        }}
        .content-block {{
            margin-bottom: 10px;
        }}
        .closing {{
            margin-top: 20px;
        }}
        {template.custom_css or ''}
    </style>
    ''')

    # Logo y encabezado de organización
    if template.logo_position != 'none' or template.show_organization_info:
        html_parts.append('<div style="margin-bottom: 30px;">')

        if template.logo_position != 'none' and organization.organization_logo:
            position_style = {
                'top-left': 'float: left;',
                'top-right': 'float: right;',
                'top-center': 'text-align: center;'
            }.get(template.logo_position, '')

            html_parts.append(f'''
            <div style="{position_style} width: {template.logo_width}px;">
                <img src="{organization.organization_logo.url}" width="{template.logo_width}" />
            </div>
            ''')

        if template.show_organization_info:
            info_align = {
                'top-left': 'left',
                'top-center': 'center',
                'top-right': 'right'
            }.get(template.organization_info_position, 'right')

            html_parts.append(f'''
            <div style="text-align: {info_align};">
                <strong>{organization.organization_name}</strong><br>
                NIT: {getattr(organization, 'organization_identification', '')}<br>
                {getattr(organization, 'organization_address', '')}<br>
                Tel: {getattr(organization, 'organization_mobile_phone', '')}
            </div>
            ''')

        if template.header_custom_text:
            html_parts.append(replace_variables(template.header_custom_text, variables))

        html_parts.append('<div style="clear: both;"></div>')
        html_parts.append('</div>')

    # Título del documento
    title = replace_variables(template.document_title, variables)
    html_parts.append(f'<div class="document-title">{title}</div>')

    # Introducción
    if template.introduction_text:
        intro = replace_variables(template.introduction_text, variables)
        html_parts.append(f'<div class="introduction">{intro}</div>')

    # ========================================
    # BLOQUES DE CONTENIDO
    # ========================================
    if template.content_blocks:
        import json
        try:
            blocks = template.content_blocks if isinstance(template.content_blocks, list) else json.loads(template.content_blocks)

            for block in sorted(blocks, key=lambda x: x.get('order', 0)):
                content = replace_variables(block.get('content', ''), variables)

                # Construir estilos del bloque
                styles = []
                styles.append(f"text-align: {block.get('alignment', 'justify')};")

                if block.get('is_bold'):
                    styles.append('font-weight: bold;')
                if block.get('is_italic'):
                    styles.append('font-style: italic;')
                if block.get('is_underline'):
                    styles.append('text-decoration: underline;')

                modifier = block.get('font_size_modifier', 0)
                if modifier != 0:
                    styles.append(f'font-size: {template.font_size + modifier}pt;')

                if block.get('custom_style'):
                    styles.append(block.get('custom_style'))

                style_str = ' '.join(styles)
                html_parts.append(f'<div class="content-block" style="{style_str}">{content}</div>')

        except Exception as e:
            # Si hay error procesando bloques, continuar sin ellos
            print(f"Error procesando bloques: {e}")

    # Texto de cierre
    if template.closing_text:
        closing = replace_variables(template.closing_text, variables)
        html_parts.append(f'<div class="closing">{closing}</div>')

    # Firmas
    if template.show_signatures:
        html_parts.append('<div style="margin-top: 40px;">')
        # Aquí se podrían agregar las firmas de la junta directiva
        # Por ahora dejamos espacio para firmas
        html_parts.append('<div style="margin-top: 60px; text-align: center;">')
        html_parts.append('<div style="display: inline-block; margin: 0 30px;">')
        html_parts.append('_________________________<br>')
        html_parts.append('Firma Autorizada')
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</div>')

    # Pie de página
    if template.footer_text:
        footer = replace_variables(template.footer_text, variables)
        html_parts.append(f'<div style="margin-top: 20px; font-size: {template.font_size - 2}pt; text-align: center;">{footer}</div>')

    # HTML personalizado
    if template.custom_html:
        html_parts.append(replace_variables(template.custom_html, variables))

    return '\n'.join(html_parts)


def replace_variables(text, variables):
    """
    Reemplaza todas las variables en el texto.

    Args:
        text: Texto con variables
        variables: Diccionario de variables y sus valores

    Returns:
        str: Texto con variables reemplazadas
    """
    result = text
    for var, value in variables.items():
        result = result.replace(var, str(value))
    return result


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
    # Verificar si el documento existe
    try:
        document = GeneratedDocument.objects.get(pk=document_id)
    except GeneratedDocument.DoesNotExist:
        messages.error(
            request,
            f"El documento con ID {document_id} no existe. "
            f"Es posible que haya sido eliminado o que el enlace sea incorrecto."
        )
        return redirect('documents-stats')

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
    # Verificar si el documento existe
    try:
        document = GeneratedDocument.objects.get(pk=document_id)
    except GeneratedDocument.DoesNotExist:
        messages.error(
            request,
            f"El documento con ID {document_id} no existe. "
            f"Es posible que haya sido eliminado o que el enlace sea incorrecto."
        )
        # Redirigir a estadísticas de documentos
        return redirect('documents-stats')

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
        BytesIO: Buffer con la imagen del código QR o una imagen placeholder
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

    try:
        # Verificar que qrcode esté disponible
        if not QRCODE_AVAILABLE:
            raise ImportError("Módulo qrcode no disponible")

        # Generar código QR usando la API correcta
        import qrcode

        # Crear instancia de QRCode
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

        logger.debug(f"QR generado exitosamente para documento {document.document_number}")
        return buffer

    except Exception as e:
        logger.error(f"Error al generar QR para documento {document.document_number}: {e}")

        # Crear una imagen placeholder simple con PIL
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Crear imagen placeholder
            img = Image.new('RGB', (300, 300), color='white')
            draw = ImageDraw.Draw(img)

            # Dibujar borde
            draw.rectangle([(10, 10), (290, 290)], outline='black', width=2)

            # Texto placeholder
            text_lines = [
                "QR Code",
                f"Doc: {document.document_number}",
                f"Hash: {doc_hash[:8]}...",
                "Verificar manualmente"
            ]

            y = 80
            for line in text_lines:
                # Calcular posición centrada aproximada
                text_width = len(line) * 7
                x = (300 - text_width) // 2
                draw.text((x, y), line, fill='black')
                y += 40

            # Guardar en buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            logger.warning(f"Usando imagen placeholder para QR de documento {document.document_number}")
            return buffer

        except Exception as pil_error:
            logger.error(f"Error al crear imagen placeholder: {pil_error}")

            # Último recurso: buffer vacío
            buffer = BytesIO()
            buffer.write(b'')
            buffer.seek(0)
            return buffer

    return buffer


@login_required
def download_document_pdf(request, document_id):
    """
    Genera y muestra un documento en formato PDF usando WeasyPrint.
    Convierte HTML a PDF correctamente respetando todos los estilos y etiquetas.
    El PDF se muestra en el navegador (inline) para previsualización.
    """
    from weasyprint import HTML
    from django.template.loader import render_to_string
    import base64
    
    # Verificar si el documento existe
    try:
        document = GeneratedDocument.objects.get(pk=document_id)
    except GeneratedDocument.DoesNotExist:
        messages.error(
            request,
            f"El documento con ID {document_id} no existe. "
            f"Es posible que haya sido eliminado o que el enlace sea incorrecto."
        )
        return redirect('documents-stats')

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
        # Generar código QR y convertirlo a base64
        qr_buffer = generate_document_qr(document)
        qr_buffer.seek(0)
        qr_base64 = base64.b64encode(qr_buffer.read()).decode()
        
        # Preparar contexto para el template HTML
        context = {
            'document': document,
            'organization': document.organization,
            'person': document.person,
            'signers': document.signers.all(),
            'qr_code': qr_base64,
            'issue_date_formatted': document.issue_date.strftime('%d de %B de %Y'),
            'expiration_date_formatted': document.expiration_date.strftime('%d de %B de %Y') if document.expiration_date else None,
        }
        
        # Renderizar HTML del documento usando el template
        html_string = render_to_string('censo/documentos/pdf_template.html', context)
        
        # Generar PDF con WeasyPrint
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_bytes = pdf_file.write_pdf()
        
        # Determinar si es descarga o previsualización
        is_download = request.GET.get('download', 'false').lower() == 'true'
        
        # Crear respuesta HTTP con el PDF
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Length'] = len(pdf_bytes)
        response['Accept-Ranges'] = 'bytes'
        
        # Cabeceras CORS para permitir la carga desde PDF.js
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type'
        
        if is_download:
            # Forzar descarga
            response['Content-Disposition'] = f'attachment; filename="Documento_{document.document_number}.pdf"'
        else:
            # Previsualización en navegador
            response['Content-Disposition'] = f'inline; filename="Documento_{document.document_number}.pdf"'
            # Cache control para previsualización
            response['Cache-Control'] = 'public, max-age=3600'
        
        return response
        
    except Exception as e:
        logger.error(f"Error al generar PDF con WeasyPrint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
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
