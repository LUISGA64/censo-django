"""
Vistas para gestión de plantillas de documentos desde el aplicativo web.
Permite a usuarios con privilegios configurar plantillas sin usar el Admin.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
import json

from censoapp.models import (
    DocumentTemplate,
    TemplateBlock,
    TemplateVariable,
    Organizations,
    DocumentType
)


def user_can_manage_templates(user):
    """Verifica si el usuario puede gestionar plantillas"""
    if user.is_superuser:
        return True
    if hasattr(user, 'userprofile'):
        # Aquí puedes agregar permisos específicos
        # Por ahora, cualquier usuario autenticado con perfil puede gestionar
        return True
    return False


@login_required
@user_passes_test(user_can_manage_templates)
def template_dashboard(request):
    """
    Dashboard principal de gestión de plantillas.
    Muestra todas las plantillas de la organización del usuario.
    """
    # Obtener organización del usuario
    if request.user.is_superuser:
        organization = None
        templates = DocumentTemplate.objects.all()
    else:
        organization = request.user.userprofile.organization
        templates = DocumentTemplate.objects.filter(organization=organization)

    # Filtros
    document_type_id = request.GET.get('document_type')
    is_active = request.GET.get('is_active')
    search = request.GET.get('search')

    if document_type_id:
        templates = templates.filter(document_type_id=document_type_id)

    if is_active is not None:
        templates = templates.filter(is_active=(is_active == '1'))

    if search:
        templates = templates.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(version__icontains=search)
        )

    # Ordenar
    templates = templates.order_by('-is_default', '-is_active', '-updated_at')

    # Paginación
    paginator = Paginator(templates, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tipos de documento disponibles
    if organization:
        document_types = DocumentType.objects.filter(
            Q(organization=organization) | Q(organization__isnull=True)
        )
    else:
        document_types = DocumentType.objects.all()

    context = {
        'segment': 'templates',
        'page_obj': page_obj,
        'document_types': document_types,
        'organization': organization,
        'filters': {
            'document_type': document_type_id,
            'is_active': is_active,
            'search': search
        }
    }

    return render(request, 'templates/dashboard.html', context)


@login_required
@user_passes_test(user_can_manage_templates)
def template_create(request):
    """Crear nueva plantilla"""

    # Obtener organización del usuario
    if request.user.is_superuser:
        organizations = Organizations.objects.all()
        organization = None
    else:
        organization = request.user.userprofile.organization
        organizations = [organization]

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            org_id = request.POST.get('organization')
            if request.user.is_superuser:
                org = Organizations.objects.get(id=org_id)
            else:
                org = organization

            doc_type = DocumentType.objects.get(id=request.POST.get('document_type'))

            # Procesar bloques de contenido
            content_blocks_json = request.POST.get('content_blocks', '[]')
            try:
                import json
                content_blocks = json.loads(content_blocks_json)
            except:
                content_blocks = []

            # Crear plantilla
            template = DocumentTemplate.objects.create(
                organization=org,
                document_type=doc_type,
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                version=request.POST.get('version', '1.0'),
                is_active=request.POST.get('is_active') == 'on',
                is_default=request.POST.get('is_default') == 'on',

                # Diseño
                logo_position=request.POST.get('logo_position', 'top-left'),
                logo_width=int(request.POST.get('logo_width', 100)),
                show_organization_info=request.POST.get('show_organization_info') == 'on',
                organization_info_position=request.POST.get('organization_info_position', 'top-right'),
                header_custom_text=request.POST.get('header_custom_text', ''),

                # Contenido
                document_title=request.POST.get('document_title', 'CERTIFICADO'),
                title_alignment=request.POST.get('title_alignment', 'center'),
                introduction_text=request.POST.get('introduction_text', 'LA JUNTA DIRECTIVA DE {organizacion}'),
                introduction_bold=request.POST.get('introduction_bold') == 'on',
                content_blocks=content_blocks,
                closing_text=request.POST.get('closing_text', ''),

                # Firmas
                show_signatures=request.POST.get('show_signatures') == 'on',
                signature_layout=request.POST.get('signature_layout', 'two-columns'),
                show_qr_code=request.POST.get('show_qr_code') == 'on',
                qr_position=request.POST.get('qr_position', 'bottom-right'),
                footer_text=request.POST.get('footer_text', ''),

                # Estilos
                primary_color=request.POST.get('primary_color', '#2196F3'),
                secondary_color=request.POST.get('secondary_color', '#1976D2'),
                text_color=request.POST.get('text_color', '#000000'),
                font_family=request.POST.get('font_family', 'Arial, sans-serif'),
                font_size=int(request.POST.get('font_size', 12)),

                # Márgenes
                margin_top=int(request.POST.get('margin_top', 25)),
                margin_bottom=int(request.POST.get('margin_bottom', 25)),
                margin_left=int(request.POST.get('margin_left', 25)),
                margin_right=int(request.POST.get('margin_right', 25)),

                # Página
                page_size=request.POST.get('page_size', 'A4'),
                page_orientation=request.POST.get('page_orientation', 'portrait'),

                # Auditoría
                created_by=request.user,
                last_modified_by=request.user
            )

            messages.success(request, f'Plantilla "{template.name}" creada exitosamente.')
            return redirect('template-edit', pk=template.pk)

        except Exception as e:
            messages.error(request, f'Error al crear plantilla: {str(e)}')

    # GET: Mostrar formulario
    document_types = DocumentType.objects.all()

    context = {
        'segment': 'templates',
        'organizations': organizations,
        'organization': organization,
        'document_types': document_types,
        'action': 'create'
    }

    return render(request, 'templates/editor.html', context)


@login_required
@user_passes_test(user_can_manage_templates)
def template_edit(request, pk):
    """Editar plantilla existente"""

    template = get_object_or_404(DocumentTemplate, pk=pk)

    # Verificar permisos
    if not request.user.is_superuser:
        if template.organization != request.user.userprofile.organization:
            messages.error(request, 'No tienes permiso para editar esta plantilla.')
            return redirect('template-dashboard')

    if request.method == 'POST':
        try:
            # Actualizar organización (solo si es superusuario)
            if request.user.is_superuser:
                org_id = request.POST.get('organization')
                if org_id:
                    template.organization = Organizations.objects.get(id=org_id)

            # Actualizar tipo de documento
            doc_type_id = request.POST.get('document_type')
            if doc_type_id:
                template.document_type = DocumentType.objects.get(id=doc_type_id)

            # Actualizar campos básicos
            template.name = request.POST.get('name')
            template.description = request.POST.get('description', '')
            template.version = request.POST.get('version', '1.0')
            template.is_active = request.POST.get('is_active') == 'on'
            template.is_default = request.POST.get('is_default') == 'on'

            # Diseño
            template.logo_position = request.POST.get('logo_position', 'top-left')
            template.logo_width = int(request.POST.get('logo_width', 100))
            template.show_organization_info = request.POST.get('show_organization_info') == 'on'
            template.organization_info_position = request.POST.get('organization_info_position', 'top-right')
            template.header_custom_text = request.POST.get('header_custom_text', '')

            # Contenido
            template.document_title = request.POST.get('document_title', 'CERTIFICADO')
            template.title_alignment = request.POST.get('title_alignment', 'center')
            template.introduction_text = request.POST.get('introduction_text', '')
            template.introduction_bold = request.POST.get('introduction_bold') == 'on'

            # Bloques de contenido (JSON)
            content_blocks_json = request.POST.get('content_blocks', '[]')
            try:
                import json
                template.content_blocks = json.loads(content_blocks_json)
            except:
                template.content_blocks = []

            template.closing_text = request.POST.get('closing_text', '')

            # Firmas
            template.show_signatures = request.POST.get('show_signatures') == 'on'
            template.signature_layout = request.POST.get('signature_layout', 'two-columns')
            template.show_qr_code = request.POST.get('show_qr_code') == 'on'
            template.qr_position = request.POST.get('qr_position', 'bottom-right')
            template.footer_text = request.POST.get('footer_text', '')

            # Estilos
            template.primary_color = request.POST.get('primary_color', '#2196F3')
            template.secondary_color = request.POST.get('secondary_color', '#1976D2')
            template.text_color = request.POST.get('text_color', '#000000')
            template.font_family = request.POST.get('font_family', 'Arial, sans-serif')
            template.font_size = int(request.POST.get('font_size', 12))

            # Márgenes
            template.margin_top = int(request.POST.get('margin_top', 25))
            template.margin_bottom = int(request.POST.get('margin_bottom', 25))
            template.margin_left = int(request.POST.get('margin_left', 25))
            template.margin_right = int(request.POST.get('margin_right', 25))

            # Página
            template.page_size = request.POST.get('page_size', 'A4')
            template.page_orientation = request.POST.get('page_orientation', 'portrait')

            # CSS/HTML personalizado
            template.custom_css = request.POST.get('custom_css', '')
            template.custom_html = request.POST.get('custom_html', '')

            # Auditoría
            template.last_modified_by = request.user

            template.save()

            messages.success(request, f'Plantilla "{template.name}" actualizada exitosamente.')
            return redirect('template-edit', pk=template.pk)

        except Exception as e:
            messages.error(request, f'Error al actualizar plantilla: {str(e)}')

    # GET: Mostrar formulario
    # Obtener organizaciones y tipos de documento disponibles
    if request.user.is_superuser:
        organizations = Organizations.objects.all()
    else:
        organizations = [request.user.userprofile.organization]

    document_types = DocumentType.objects.all()

    context = {
        'segment': 'templates',
        'template': template,
        'action': 'edit',
        'blocks': template.blocks.all().order_by('order'),
        'document_types': document_types,
        'organizations': organizations,
        'organization': template.organization
    }

    return render(request, 'templates/editor.html', context)


@login_required
@user_passes_test(user_can_manage_templates)
def template_duplicate(request, pk):
    """Duplicar plantilla para crear nueva versión"""

    template = get_object_or_404(DocumentTemplate, pk=pk)

    # Verificar permisos
    if not request.user.is_superuser:
        if template.organization != request.user.userprofile.organization:
            messages.error(request, 'No tienes permiso para duplicar esta plantilla.')
            return redirect('template-dashboard')

    try:
        # Duplicar plantilla
        old_pk = template.pk
        template.pk = None
        template.id = None
        template.name = f"{template.name} (Copia)"

        # Incrementar versión
        version_parts = template.version.split('.')
        if len(version_parts) >= 2:
            major, minor = version_parts[0], version_parts[1]
            template.version = f"{major}.{int(minor) + 1}"
        else:
            template.version = f"{template.version}.1"

        template.is_default = False
        template.created_by = request.user
        template.last_modified_by = request.user
        template.save()

        # Duplicar bloques
        original_template = DocumentTemplate.objects.get(pk=old_pk)
        for block in original_template.blocks.all():
            block.pk = None
            block.id = None
            block.template = template
            block.save()

        messages.success(request, f'Plantilla duplicada como "{template.name}".')
        return redirect('template-edit', pk=template.pk)

    except Exception as e:
        messages.error(request, f'Error al duplicar plantilla: {str(e)}')
        return redirect('template-dashboard')


@login_required
@user_passes_test(user_can_manage_templates)
def template_delete(request, pk):
    """Eliminar plantilla"""

    template = get_object_or_404(DocumentTemplate, pk=pk)

    # Verificar permisos
    if not request.user.is_superuser:
        if template.organization != request.user.userprofile.organization:
            messages.error(request, 'No tienes permiso para eliminar esta plantilla.')
            return redirect('template-dashboard')

    if request.method == 'POST':
        name = template.name
        template.delete()
        messages.success(request, f'Plantilla "{name}" eliminada exitosamente.')
        return redirect('template-dashboard')

    context = {
        'segment': 'templates',
        'template': template
    }

    return render(request, 'templates/delete_confirm.html', context)


@login_required
@user_passes_test(user_can_manage_templates)
def template_toggle_active(request, pk):
    """Activar/desactivar plantilla (AJAX)"""

    if request.method == 'POST':
        template = get_object_or_404(DocumentTemplate, pk=pk)

        # Verificar permisos
        if not request.user.is_superuser:
            if template.organization != request.user.userprofile.organization:
                return JsonResponse({'success': False, 'error': 'Sin permisos'}, status=403)

        template.is_active = not template.is_active
        template.last_modified_by = request.user
        template.save()

        return JsonResponse({
            'success': True,
            'is_active': template.is_active
        })

    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(user_can_manage_templates)
def template_set_default(request, pk):
    """Establecer como plantilla por defecto (AJAX)"""

    if request.method == 'POST':
        template = get_object_or_404(DocumentTemplate, pk=pk)

        # Verificar permisos
        if not request.user.is_superuser:
            if template.organization != request.user.userprofile.organization:
                return JsonResponse({'success': False, 'error': 'Sin permisos'}, status=403)

        # Desactivar otras plantillas por defecto
        DocumentTemplate.objects.filter(
            organization=template.organization,
            document_type=template.document_type,
            is_default=True
        ).update(is_default=False)

        # Activar esta
        template.is_default = True
        template.last_modified_by = request.user
        template.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(user_can_manage_templates)
@login_required
@user_passes_test(user_can_manage_templates)
def variable_manager(request):
    """Gestión de variables personalizadas"""

    # Obtener organización del usuario
    if request.user.is_superuser:
        # Para superusuarios, mostrar la primera organización por defecto
        # (en el futuro se podría agregar un selector)
        organization = Organizations.objects.first()
        if organization:
            variables = TemplateVariable.objects.filter(organization=organization)
        else:
            variables = TemplateVariable.objects.none()
    else:
        # Verificar que el usuario tenga perfil
        if not hasattr(request.user, 'userprofile'):
            messages.error(request, 'El usuario no tiene un perfil asociado. Contacte al administrador.')
            return redirect('dashboard')

        # Verificar que el perfil tenga organización
        if not request.user.userprofile.organization:
            messages.error(request, 'El usuario no tiene una organización asociada. Contacte al administrador.')
            return redirect('dashboard')

        organization = request.user.userprofile.organization
        variables = TemplateVariable.objects.filter(organization=organization)

    # Filtros
    is_active = request.GET.get('is_active')
    search = request.GET.get('search')

    if is_active is not None:
        variables = variables.filter(is_active=(is_active == '1'))

    if search:
        variables = variables.filter(
            Q(variable_name__icontains=search) |
            Q(variable_value__icontains=search) |
            Q(description__icontains=search)
        )

    # Ordenar
    variables = variables.order_by('variable_name')

    # Paginación
    paginator = Paginator(variables, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'segment': 'templates',
        'page_obj': page_obj,
        'organization': organization,
        'filters': {
            'is_active': is_active,
            'search': search
        }
    }

    return render(request, 'templates/variables.html', context)


@login_required
@user_passes_test(user_can_manage_templates)
def variable_create(request):
    """Crear nueva variable personalizada (AJAX)"""

    if request.method == 'POST':
        try:
            # Obtener organización
            if request.user.is_superuser:
                org_id = request.POST.get('organization_id')

                if org_id:
                    # Si se proporcionó ID, buscar esa organización
                    try:
                        organization = Organizations.objects.get(id=org_id)
                    except Organizations.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'error': 'La organización seleccionada no existe'
                        }, status=400)
                else:
                    # Si no se proporcionó ID, usar la primera organización disponible
                    organization = Organizations.objects.first()
                    if not organization:
                        return JsonResponse({
                            'success': False,
                            'error': 'No hay organizaciones en el sistema. Cree una organización primero.'
                        }, status=400)
            else:
                # Verificar que el usuario tenga perfil
                if not hasattr(request.user, 'userprofile'):
                    return JsonResponse({
                        'success': False,
                        'error': 'El usuario no tiene un perfil asociado. Contacte al administrador.'
                    }, status=400)

                # Verificar que el perfil tenga organización
                if not request.user.userprofile.organization:
                    return JsonResponse({
                        'success': False,
                        'error': 'El usuario no tiene una organización asociada. Contacte al administrador.'
                    }, status=400)

                organization = request.user.userprofile.organization

            variable_name = request.POST.get('variable_name', '').strip()
            variable_type = request.POST.get('variable_type')
            variable_value = request.POST.get('variable_value')

            # Validar que el nombre no esté vacío
            if not variable_name:
                return JsonResponse({
                    'success': False,
                    'error': 'El nombre de la variable es obligatorio'
                }, status=400)

            # Validar que no exista una variable con el mismo nombre
            if TemplateVariable.objects.filter(
                organization=organization,
                variable_name=variable_name
            ).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'Ya existe una variable con el nombre "{variable_name}" en esta organización'
                }, status=400)

            # Crear variable
            variable = TemplateVariable.objects.create(
                organization=organization,
                variable_name=variable_name,
                variable_type=variable_type,
                variable_value=variable_value,
                description=request.POST.get('description', ''),
                is_active=True
            )

            return JsonResponse({
                'success': True,
                'variable': {
                    'id': variable.id,
                    'name': variable.variable_name,
                    'type': variable.get_variable_type_display(),
                    'value': variable.variable_value,
                    'full_name': variable.full_variable_name
                }
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(user_can_manage_templates)
def variable_update(request, pk):
    """Actualizar variable personalizada (AJAX)"""

    if request.method == 'POST':
        variable = get_object_or_404(TemplateVariable, pk=pk)

        # Verificar permisos
        if not request.user.is_superuser:
            if variable.organization != request.user.userprofile.organization:
                return JsonResponse({'success': False, 'error': 'Sin permisos'}, status=403)

        try:
            variable_name = request.POST.get('variable_name', '').strip()

            # Validar que no exista otra variable con el mismo nombre (excepto la actual)
            if TemplateVariable.objects.filter(
                organization=variable.organization,
                variable_name=variable_name
            ).exclude(pk=pk).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'Ya existe otra variable con el nombre "{variable_name}" en esta organización'
                }, status=400)

            variable.variable_name = variable_name
            variable.variable_type = request.POST.get('variable_type')
            variable.variable_value = request.POST.get('variable_value')
            variable.description = request.POST.get('description', '')
            variable.is_active = request.POST.get('is_active') == 'true'
            variable.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(user_can_manage_templates)
def variable_delete(request, pk):
    """Eliminar variable personalizada (AJAX)"""

    if request.method == 'POST':
        variable = get_object_or_404(TemplateVariable, pk=pk)

        # Verificar permisos
        if not request.user.is_superuser:
            if variable.organization != request.user.userprofile.organization:
                return JsonResponse({'success': False, 'error': 'Sin permisos'}, status=403)

        variable.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(user_can_manage_templates)
def get_available_variables(request):
    """Obtener lista de variables disponibles (AJAX)"""

    # Variables del sistema
    system_variables = [
        {'name': 'nombre_completo', 'description': 'Nombre completo de la persona'},
        {'name': 'primer_nombre', 'description': 'Primer nombre'},
        {'name': 'segundo_nombre', 'description': 'Segundo nombre'},
        {'name': 'primer_apellido', 'description': 'Primer apellido'},
        {'name': 'segundo_apellido', 'description': 'Segundo apellido'},
        {'name': 'identificacion', 'description': 'Número de identificación'},
        {'name': 'tipo_documento', 'description': 'Tipo de documento'},
        {'name': 'edad', 'description': 'Edad en años'},
        {'name': 'fecha_nacimiento', 'description': 'Fecha de nacimiento'},
        {'name': 'genero', 'description': 'Género'},
        {'name': 'vereda', 'description': 'Vereda de residencia'},
        {'name': 'zona', 'description': 'Zona (Rural/Urbana)'},
        {'name': 'direccion', 'description': 'Dirección de residencia'},
        {'name': 'organizacion', 'description': 'Nombre de la organización'},
        {'name': 'nit_organizacion', 'description': 'NIT de la organización'},
        {'name': 'fecha_expedicion', 'description': 'Fecha de expedición del documento'},
        {'name': 'fecha_vencimiento', 'description': 'Fecha de vencimiento'},
        {'name': 'año', 'description': 'Año actual'},
        {'name': 'mes', 'description': 'Mes actual'},
        {'name': 'dia', 'description': 'Día actual'},
        {'name': 'numero_documento', 'description': 'Número del documento generado'},
    ]

    # Variables personalizadas de la organización
    if request.user.is_superuser:
        custom_variables = []
    else:
        organization = request.user.userprofile.organization
        custom_vars = TemplateVariable.objects.filter(
            organization=organization,
            is_active=True
        )
        custom_variables = [
            {
                'name': var.variable_name,
                'description': var.description or f'Variable personalizada: {var.variable_value[:50]}'
            }
            for var in custom_vars
        ]

    return JsonResponse({
        'system': system_variables,
        'custom': custom_variables
    })


@login_required
@user_passes_test(user_can_manage_templates)
def get_model_fields(request):
    """
    Obtener campos disponibles según el tipo de variable.
    Devuelve una lista de campos del modelo seleccionado.
    """
    variable_type = request.GET.get('type', '')

    fields = []

    if variable_type == 'organization':
        # Campos del modelo Organizations
        fields = [
            {'value': 'organization_name', 'label': 'Nombre de la organización', 'type': 'text'},
            {'value': 'organization_identification', 'label': 'NIT/Identificación', 'type': 'text'},
            {'value': 'organization_type_document', 'label': 'Tipo de documento', 'type': 'text'},
            {'value': 'organization_mobile_phone', 'label': 'Teléfono móvil', 'type': 'text'},
            {'value': 'organization_phone', 'label': 'Teléfono fijo', 'type': 'text'},
            {'value': 'organization_address', 'label': 'Dirección', 'type': 'text'},
            {'value': 'organization_departament', 'label': 'Departamento', 'type': 'text'},
            {'value': 'organization_municipality', 'label': 'Municipio', 'type': 'text'},
            {'value': 'organization_territory', 'label': 'Territorio', 'type': 'text'},
            {'value': 'organization_email', 'label': 'Email', 'type': 'text'},
            {'value': 'organization_web', 'label': 'Sitio web', 'type': 'text'},
        ]

    elif variable_type == 'person':
        # Campos del modelo Person
        fields = [
            {'value': 'full_name', 'label': 'Nombre completo', 'type': 'text'},
            {'value': 'first_name_1', 'label': 'Primer nombre', 'type': 'text'},
            {'value': 'first_name_2', 'label': 'Segundo nombre', 'type': 'text'},
            {'value': 'last_name_1', 'label': 'Primer apellido', 'type': 'text'},
            {'value': 'last_name_2', 'label': 'Segundo apellido', 'type': 'text'},
            {'value': 'identification_person', 'label': 'Número de identificación', 'type': 'text'},
            {'value': 'document_type.document_type', 'label': 'Tipo de documento', 'type': 'relation'},
            {'value': 'date_birth', 'label': 'Fecha de nacimiento', 'type': 'date'},
            {'value': 'calcular_anios', 'label': 'Edad en años', 'type': 'method'},
            {'value': 'gender.gender', 'label': 'Género', 'type': 'relation'},
            {'value': 'civil_state.state_civil', 'label': 'Estado civil', 'type': 'relation'},
            {'value': 'eps.eps', 'label': 'EPS', 'type': 'relation'},
            {'value': 'education_level.education_level', 'label': 'Nivel educativo', 'type': 'relation'},
            {'value': 'occupancy.occupancy', 'label': 'Ocupación', 'type': 'relation'},
            {'value': 'mobile_phone', 'label': 'Teléfono celular', 'type': 'text'},
            {'value': 'email', 'label': 'Email', 'type': 'text'},
        ]

    elif variable_type == 'family_card':
        # Campos del modelo FamilyCard
        fields = [
            {'value': 'family_card_number', 'label': 'Número de ficha familiar', 'type': 'number'},
            {'value': 'sidewalk_home.sidewalk_name', 'label': 'Vereda', 'type': 'relation'},
            {'value': 'zone', 'label': 'Zona (Rural/Urbana)', 'type': 'text'},
            {'value': 'address_home', 'label': 'Dirección de residencia', 'type': 'text'},
            {'value': 'homeownership.homeownership', 'label': 'Tipo de vivienda', 'type': 'relation'},
            {'value': 'water_source.water_source', 'label': 'Fuente de agua', 'type': 'relation'},
            {'value': 'water_treatment.water_treatment', 'label': 'Tratamiento del agua', 'type': 'relation'},
            {'value': 'lighting_type.lighting_type', 'label': 'Tipo de alumbrado', 'type': 'relation'},
            {'value': 'cooking_fuel.cooking_fuel', 'label': 'Combustible para cocinar', 'type': 'relation'},
            {'value': 'number_occupants', 'label': 'Número de ocupantes', 'type': 'number'},
        ]

    elif variable_type == 'association':
        # Campos del modelo Association (si existe)
        # Por ahora dejamos campos básicos - ajustar según el modelo real
        fields = [
            {'value': 'association_name', 'label': 'Nombre de la asociación', 'type': 'text'},
            {'value': 'association_code', 'label': 'Código de asociación', 'type': 'text'},
            {'value': 'president_name', 'label': 'Nombre del presidente', 'type': 'text'},
            {'value': 'secretary_name', 'label': 'Nombre del secretario', 'type': 'text'},
            {'value': 'creation_date', 'label': 'Fecha de creación', 'type': 'date'},
            {'value': 'total_members', 'label': 'Total de miembros', 'type': 'number'},
        ]

    return JsonResponse({'fields': fields})



