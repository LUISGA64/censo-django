from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Association, Organizations, Sidewalks, IdentificationDocumentType, Gender, Eps, Kinship, Occupancy, CivilState,
    EducationLevel, SecuritySocial, Handicap, Charge, SystemParameters, MaterialConstruction,
    WaterTreatment, LightingType, WaterSource, CookingFuel, HomeOwnership, FamilyCard, Person,
    MaterialConstructionFamilyCard, UserProfile, DocumentType, BoardPosition, GeneratedDocument,
    DocumentTemplate, TemplateBlock, TemplateVariable
)
from .utils import invalidate_system_parameters_cache

# Register your models here.
admin.site.register(Association)
admin.site.register(Organizations)
admin.site.register(Sidewalks)
admin.site.register(IdentificationDocumentType)
admin.site.register(Gender)
admin.site.register(Eps)
admin.site.register(Kinship)
admin.site.register(Occupancy)
admin.site.register(CivilState)
admin.site.register(EducationLevel)
admin.site.register(SecuritySocial)
admin.site.register(Handicap)
admin.site.register(Charge)
# SystemParameters se registra mas abajo con admin personalizado
admin.site.register(MaterialConstruction)
admin.site.register(HomeOwnership)
admin.site.register(WaterTreatment)
admin.site.register(LightingType)
admin.site.register(WaterSource)
admin.site.register(CookingFuel)


# SystemParameters con invalidacion automatica de cache
@admin.register(SystemParameters)
class SystemParametersAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    search_fields = ['key', 'value']
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        """Invalida cache al guardar"""
        super().save_model(request, obj, form, change)
        invalidate_system_parameters_cache()
        self.message_user(request, f"Parametro '{obj.key}' guardado. Cache invalidado.", level='SUCCESS')

    def delete_model(self, request, obj):
        """Invalida cache al eliminar"""
        key = obj.key
        super().delete_model(request, obj)
        invalidate_system_parameters_cache()
        self.message_user(request, f"Parametro '{key}' eliminado. Cache invalidado.", level='SUCCESS')

    def delete_queryset(self, request, queryset):
        """Invalida cache al eliminar multiples"""
        count = queryset.count()
        super().delete_queryset(request, queryset)
        invalidate_system_parameters_cache()
        self.message_user(request, f"{count} parametros eliminados. Cache invalidado.", level='SUCCESS')


# Modelos con auditoria usando SimpleHistoryAdmin
@admin.register(FamilyCard)
class FamilyCardAdmin(SimpleHistoryAdmin):
    list_display = ['family_card_number', 'sidewalk_home', 'zone', 'organization', 'state', 'created_at']
    list_filter = ['zone', 'state', 'organization']
    search_fields = ['family_card_number', 'address_home']
    history_list_display = ['state', 'zone']

@admin.register(Person)
class PersonAdmin(SimpleHistoryAdmin):
    list_display = ['identification_person', 'first_name_1', 'last_name_1', 'family_head', 'state', 'family_card']
    list_filter = ['family_head', 'state', 'gender']
    search_fields = ['identification_person', 'first_name_1', 'last_name_1']
    history_list_display = ['family_head', 'state']

@admin.register(MaterialConstructionFamilyCard)
class MaterialConstructionFamilyCardAdmin(SimpleHistoryAdmin):
    list_display = ['family_card', 'material_roof', 'material_wall', 'material_floor', 'number_bedrooms']
    list_filter = ['home_ownership', 'cooking_fuel']
    search_fields = ['family_card__family_card_number']
    history_list_display = ['number_bedrooms', 'ventilation', 'lighting']


# UserProfile admin con gestion de multi-organizacion
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'can_view_all_organizations', 'is_active', 'created_at']
    list_filter = ['role', 'organization', 'can_view_all_organizations', 'is_active']
    search_fields = ['user__username', 'user__email', 'organization__organization_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'organization')
        }),
        ('Permisos', {
            'fields': ('role', 'can_view_all_organizations', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Filtrar perfiles segun organizacion del usuario admin.
        Superusuarios ven todos.
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'profile'):
            if request.user.profile.can_view_all_organizations:
                return qs
            return qs.filter(organization=request.user.profile.organization)

        return qs.none()


# ========================================
# ADMINISTRACIÓN DE PLANTILLAS DE DOCUMENTOS
# ========================================



@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    """
    Administración de plantillas de documentos.
    Permite configurar plantillas personalizadas por organización.
    """
    list_display = [
        'name',
        'organization',
        'document_type',
        'version',
        'is_active',
        'is_default',
        'updated_at'
    ]
    list_filter = [
        'organization',
        'document_type',
        'is_active',
        'is_default',
        'created_at'
    ]
    search_fields = [
        'name',
        'description',
        'organization__organization_name',
        'document_type__document_type_name'
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'created_by',
        'last_modified_by'
    ]
    list_per_page = 20
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información General', {
            'fields': (
                'organization',
                'document_type',
                'name',
                'description',
                'version'
            )
        }),
        ('Estado', {
            'fields': (
                'is_active',
                'is_default'
            )
        }),
        ('Configuración de Diseño', {
            'fields': (
                'logo_position',
                'logo_width',
                'show_organization_info',
                'organization_info_position',
                'header_custom_text',
            ),
            'classes': ('collapse',)
        }),
        ('Contenido del Documento', {
            'fields': (
                'document_title',
                'title_alignment',
                'introduction_text',
                'introduction_bold',
                'content_blocks',
                'closing_text',
            )
        }),
        ('Firmas y Pie de Página', {
            'fields': (
                'show_signatures',
                'signature_layout',
                'show_qr_code',
                'qr_position',
                'footer_text',
            ),
            'classes': ('collapse',)
        }),
        ('Estilos y Colores', {
            'fields': (
                'primary_color',
                'secondary_color',
                'text_color',
                'font_family',
                'font_size',
            ),
            'classes': ('collapse',)
        }),
        ('Configuración de Página', {
            'fields': (
                'margin_top',
                'margin_bottom',
                'margin_left',
                'margin_right',
                'page_size',
                'page_orientation',
            ),
            'classes': ('collapse',)
        }),
        ('Personalización Avanzada', {
            'fields': (
                'custom_css',
                'custom_html',
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at',
                'updated_at',
                'created_by',
                'last_modified_by',
            ),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Guardar usuario que crea/modifica la plantilla"""
        if not change:  # Nuevo objeto
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Filtrar plantillas por organización del usuario"""
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'userprofile'):
            return qs.filter(organization=request.user.userprofile.organization)

        return qs.none()


@admin.register(TemplateBlock)
class TemplateBlockAdmin(admin.ModelAdmin):
    """Administración de bloques de contenido de plantillas"""
    list_display = [
        'template',
        'block_type',
        'order',
        'alignment',
        'is_bold'
    ]
    list_filter = [
        'template',
        'block_type',
        'alignment',
        'is_bold'
    ]
    search_fields = [
        'template__name',
        'content'
    ]
    ordering = ['template', 'order']
    list_per_page = 50

    fieldsets = (
        ('Información del Bloque', {
            'fields': (
                'template',
                'block_type',
                'order',
                'content',
            )
        }),
        ('Estilos del Bloque', {
            'fields': (
                'is_bold',
                'is_italic',
                'is_underline',
                'alignment',
                'font_size_modifier',
                'custom_style',
            )
        }),
        ('Configuración Adicional', {
            'fields': (
                'config',
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(TemplateVariable)
class TemplateVariableAdmin(admin.ModelAdmin):
    """Administración de variables personalizadas"""
    list_display = [
        'organization',
        'variable_name',
        'variable_type',
        'variable_value_preview',
        'is_active'
    ]
    list_filter = [
        'organization',
        'variable_type',
        'is_active'
    ]
    search_fields = [
        'variable_name',
        'variable_value',
        'organization__organization_name'
    ]
    list_per_page = 30

    fieldsets = (
        ('Variable', {
            'fields': (
                'organization',
                'variable_name',
                'variable_type',
                'variable_value',
                'description',
            ),
            'description': '''
                <div style="background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 15px;">
                    <h4 style="color: #0d47a1; margin-top: 0;">💡 Tipos de Variables:</h4>
                    <ul style="color: #1565c0;">
                        <li><strong>Valor Estático:</strong> Texto fijo (ej: "Juan Pérez")</li>
                        <li><strong>Dato de Organización:</strong> Campo del modelo Organizations (ej: "organization_territory", "organization_mobile_phone")</li>
                        <li><strong>Dato de Persona:</strong> Campo del modelo Person (ej: "full_name", "identification_person")</li>
                        <li><strong>Dato de Ficha Familiar:</strong> Campo del modelo FamilyCard (ej: "family_card_number", "address_home", "sidewalk_home.sidewalk_name")</li>
                    </ul>
                    <p style="color: #0d47a1;"><strong>Nota:</strong> Para relaciones, usa punto (ej: "sidewalk_home.sidewalk_name")</p>
                </div>
            '''
        }),
        ('Estado', {
            'fields': (
                'is_active',
            )
        }),
    )

    def variable_value_preview(self, obj):
        """Mostrar preview del valor (máximo 50 caracteres)"""
        if len(obj.variable_value) > 50:
            return f"{obj.variable_value[:50]}..."
        return obj.variable_value
    variable_value_preview.short_description = 'Valor'

    def get_queryset(self, request):
        """Filtrar variables por organización del usuario"""
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'userprofile'):
            return qs.filter(organization=request.user.userprofile.organization)

        return qs.none()



# ============================================================================
# ADMINISTRACIÓN DE DOCUMENTOS Y JUNTA DIRECTIVA
# ============================================================================

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    """Administración de tipos de documentos"""
    list_display = ['document_type_name', 'requires_expiration', 'is_active', 'created_at']
    list_filter = ['is_active', 'requires_expiration', 'created_at']
    search_fields = ['document_type_name', 'description']
    list_per_page = 20

    fieldsets = (
        ('Información Básica', {
            'fields': ('document_type_name', 'description', 'is_active')
        }),
        ('Configuración', {
            'fields': ('requires_expiration', 'template_content')
        }),
    )


@admin.register(BoardPosition)
class BoardPositionAdmin(SimpleHistoryAdmin):
    """Administración de cargos de junta directiva"""
    list_display = ['position_name', 'organization', 'holder_person_name', 'alternate_person_name',
                   'can_sign_documents', 'is_active', 'start_date']
    list_filter = ['organization', 'position_name', 'is_active', 'can_sign_documents']
    search_fields = ['holder_person__first_name_1', 'holder_person__last_name_1',
                    'alternate_person__first_name_1', 'alternate_person__last_name_1']
    list_per_page = 20
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Organización y Cargo', {
            'fields': ('organization', 'position_name')
        }),
        ('Titular y Suplente', {
            'fields': ('holder_person', 'alternate_person')
        }),
        ('Permisos', {
            'fields': ('can_sign_documents',)
        }),
        ('Vigencia', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Información Adicional', {
            'fields': ('observations',),
            'classes': ('collapse',)
        }),
    )

    def holder_person_name(self, obj):
        return obj.holder_person.full_name if obj.holder_person else "-"
    holder_person_name.short_description = "Titular"

    def alternate_person_name(self, obj):
        return obj.alternate_person.full_name if obj.alternate_person else "-"
    alternate_person_name.short_description = "Suplente"

    def get_queryset(self, request):
        """Filtrar por organización del usuario"""
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'profile'):
            if request.user.profile.can_view_all_organizations:
                return qs
            return qs.filter(organization=request.user.profile.organization)

        return qs.none()


@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(SimpleHistoryAdmin):
    """Administración de documentos generados"""
    list_display = ['document_number', 'document_type', 'person_name', 'organization',
                   'status', 'issue_date', 'expiration_date', 'created_by']
    list_filter = ['status', 'document_type', 'organization', 'issue_date']
    search_fields = ['document_number', 'person__first_name_1', 'person__last_name_1',
                    'person__identification_person']
    list_per_page = 20
    date_hierarchy = 'issue_date'
    filter_horizontal = ['signers']

    fieldsets = (
        ('Tipo y Beneficiario', {
            'fields': ('document_type', 'person', 'organization')
        }),
        ('Contenido', {
            'fields': ('document_content',)
        }),
        ('Fechas y Número', {
            'fields': ('document_number', 'issue_date', 'expiration_date')
        }),
        ('Firmantes', {
            'fields': ('signers',)
        }),
        ('Estado', {
            'fields': ('status', 'observations')
        }),
        ('Auditoría', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['document_number', 'created_by']

    def person_name(self, obj):
        return obj.person.full_name
    person_name.short_description = "Persona"

    def save_model(self, request, obj, form, change):
        """Asignar usuario creador automáticamente y validar"""
        if not change:  # Solo en creación
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Validar firmantes después de guardar relaciones ManyToMany"""
        super().save_related(request, form, formsets, change)

        # Validar que los firmantes estén vigentes en la fecha de expedición
        try:
            form.instance.validate_signers()
        except Exception as e:
            # Mostrar error al usuario
            from django.contrib import messages
            messages.error(
                request,
                f"Error en la validación de firmantes: {str(e)}"
            )

    def get_queryset(self, request):
        """Filtrar por organización del usuario"""
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'profile'):
            if request.user.profile.can_view_all_organizations:
                return qs
            return qs.filter(organization=request.user.profile.organization)

        return qs.none()

