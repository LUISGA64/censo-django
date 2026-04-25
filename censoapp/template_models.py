"""
Sistema de Plantillas Personalizables para Documentos
Permite a cada organización personalizar la estructura y contenido de sus documentos
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from simple_history.models import HistoricalRecords
import json


class DocumentTemplate(models.Model):
    """
    Plantillas personalizables para documentos de cada organización.
    Permite configurar estructura, estilos, logos, contenido, etc.
    """
    # Relación con organización y tipo de documento
    organization = models.ForeignKey(
        'censoapp.Organizations',
        on_delete=models.CASCADE,
        verbose_name="Organización",
        help_text="Organización propietaria de esta plantilla",
        related_name='document_templates'
    )

    document_type = models.ForeignKey(
        'censoapp.DocumentType',
        on_delete=models.CASCADE,
        verbose_name="Tipo de Documento",
        help_text="Tipo de documento al que aplica esta plantilla",
        related_name='templates'
    )

    # Información básica de la plantilla
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre de la Plantilla",
        help_text="Nombre descriptivo (ej: 'Aval Comunitario v2')"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción del propósito de esta plantilla"
    )

    version = models.CharField(
        max_length=20,
        default='1.0',
        verbose_name="Versión",
        help_text="Versión de la plantilla (ej: 1.0, 2.1)"
    )

    # Estado y activación
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si está activa, se usará para generar documentos"
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="Plantilla por Defecto",
        help_text="Si es la plantilla predeterminada para este tipo de documento"
    )

    # ========================================
    # CONFIGURACIÓN DE DISEÑO
    # ========================================

    # Logo de la organización
    logo_position = models.CharField(
        max_length=20,
        choices=[
            ('top-left', 'Superior Izquierda'),
            ('top-center', 'Superior Centro'),
            ('top-right', 'Superior Derecha'),
            ('none', 'Sin Logo'),
        ],
        default='top-left',
        verbose_name="Posición del Logo"
    )

    logo_width = models.IntegerField(
        default=100,
        verbose_name="Ancho del Logo (px)",
        help_text="Ancho del logo en píxeles"
    )

    # Encabezado
    show_organization_info = models.BooleanField(
        default=True,
        verbose_name="Mostrar Info Organización en Encabezado",
        help_text="Muestra nombre, NIT, dirección, etc."
    )

    organization_info_position = models.CharField(
        max_length=20,
        choices=[
            ('top-left', 'Superior Izquierda'),
            ('top-center', 'Superior Centro'),
            ('top-right', 'Superior Derecha'),
        ],
        default='top-right',
        verbose_name="Posición Info Organización"
    )

    header_custom_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto Personalizado Encabezado",
        help_text="Texto adicional en el encabezado (acepta HTML)"
    )

    # ========================================
    # CONTENIDO DEL DOCUMENTO
    # ========================================

    # Título del documento
    document_title = models.CharField(
        max_length=200,
        default='CERTIFICADO',
        verbose_name="Título del Documento",
        help_text="Título principal (ej: 'CERTIFICADO', 'CONSTANCIA')"
    )

    title_alignment = models.CharField(
        max_length=20,
        choices=[
            ('left', 'Izquierda'),
            ('center', 'Centro'),
            ('right', 'Derecha'),
        ],
        default='center',
        verbose_name="Alineación del Título"
    )

    # Introducción/Encabezado del contenido
    introduction_text = models.TextField(
        default='LA JUNTA DIRECTIVA DE {organizacion}',
        verbose_name="Texto de Introducción",
        help_text="Texto introductorio (puede usar variables con {})"
    )

    introduction_bold = models.BooleanField(
        default=True,
        verbose_name="Introducción en Negrita"
    )

    # Cuerpo principal (estructura JSON para bloques)
    content_blocks = models.JSONField(
        default=list,
        verbose_name="Bloques de Contenido",
        help_text="Estructura JSON con bloques de contenido configurables"
    )

    # Cierre/Despedida
    closing_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto de Cierre",
        help_text="Texto de cierre del documento"
    )

    # ========================================
    # PIE DE PÁGINA Y FIRMAS
    # ========================================

    show_signatures = models.BooleanField(
        default=True,
        verbose_name="Mostrar Firmas",
        help_text="Muestra espacios para firmas de la junta directiva"
    )

    signature_layout = models.CharField(
        max_length=20,
        choices=[
            ('horizontal', 'Horizontal (todas en una fila)'),
            ('two-columns', 'Dos Columnas'),
            ('vertical', 'Vertical (una debajo de otra)'),
        ],
        default='two-columns',
        verbose_name="Diseño de Firmas"
    )

    show_qr_code = models.BooleanField(
        default=True,
        verbose_name="Mostrar Código QR",
        help_text="Incluye código QR para verificación"
    )

    qr_position = models.CharField(
        max_length=20,
        choices=[
            ('bottom-left', 'Inferior Izquierda'),
            ('bottom-center', 'Inferior Centro'),
            ('bottom-right', 'Inferior Derecha'),
        ],
        default='bottom-right',
        verbose_name="Posición del QR"
    )

    footer_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto del Pie de Página",
        help_text="Texto adicional en el pie de página"
    )

    # ========================================
    # ESTILOS Y PERSONALIZACIÓN
    # ========================================

    # Colores
    primary_color = models.CharField(
        max_length=7,
        default='#2196F3',
        verbose_name="Color Primario",
        help_text="Color principal (formato hexadecimal #RRGGBB)"
    )

    secondary_color = models.CharField(
        max_length=7,
        default='#1976D2',
        verbose_name="Color Secundario",
        help_text="Color secundario (formato hexadecimal #RRGGBB)"
    )

    text_color = models.CharField(
        max_length=7,
        default='#000000',
        verbose_name="Color del Texto",
        help_text="Color del texto principal"
    )

    # Fuentes
    font_family = models.CharField(
        max_length=100,
        default='Arial, sans-serif',
        verbose_name="Familia de Fuente",
        help_text="Fuente del documento (ej: Arial, Times New Roman)"
    )

    font_size = models.IntegerField(
        default=12,
        verbose_name="Tamaño de Fuente Base (pt)",
        help_text="Tamaño base de la fuente en puntos"
    )

    # Márgenes (en milímetros)
    margin_top = models.IntegerField(
        default=25,
        verbose_name="Margen Superior (mm)"
    )

    margin_bottom = models.IntegerField(
        default=25,
        verbose_name="Margen Inferior (mm)"
    )

    margin_left = models.IntegerField(
        default=25,
        verbose_name="Margen Izquierdo (mm)"
    )

    margin_right = models.IntegerField(
        default=25,
        verbose_name="Margen Derecho (mm)"
    )

    # Tamaño de página
    page_size = models.CharField(
        max_length=20,
        choices=[
            ('A4', 'A4 (210 × 297 mm)'),
            ('Letter', 'Carta (216 × 279 mm)'),
            ('Legal', 'Oficio (216 × 356 mm)'),
        ],
        default='A4',
        verbose_name="Tamaño de Página"
    )

    page_orientation = models.CharField(
        max_length=20,
        choices=[
            ('portrait', 'Vertical'),
            ('landscape', 'Horizontal'),
        ],
        default='portrait',
        verbose_name="Orientación de Página"
    )

    # ========================================
    # CSS Y HTML PERSONALIZADO
    # ========================================

    custom_css = models.TextField(
        blank=True,
        null=True,
        verbose_name="CSS Personalizado",
        help_text="Estilos CSS adicionales para personalización avanzada"
    )

    custom_html = models.TextField(
        blank=True,
        null=True,
        verbose_name="HTML Personalizado",
        help_text="HTML adicional para estructura personalizada"
    )

    # ========================================
    # METADATOS Y AUDITORÍA
    # ========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='templates_created',
        verbose_name="Creado Por"
    )

    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='templates_modified',
        verbose_name="Última Modificación Por"
    )

    # Historial de cambios
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Plantilla de Documento"
        verbose_name_plural = "Plantillas de Documentos"
        ordering = ['-is_default', '-is_active', 'organization', 'document_type', 'name']
        unique_together = [
            ['organization', 'document_type', 'name'],
        ]
        indexes = [
            models.Index(fields=['organization', 'document_type', 'is_active']),
            models.Index(fields=['is_default', 'is_active']),
        ]

    def __str__(self):
        return f"{self.organization.organization_name} - {self.document_type.document_type_name} - {self.name}"

    def save(self, *args, **kwargs):
        """
        Override save para asegurar que solo haya una plantilla por defecto
        por organización y tipo de documento
        """
        if self.is_default:
            # Desactivar otras plantillas por defecto
            DocumentTemplate.objects.filter(
                organization=self.organization,
                document_type=self.document_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)

    def get_variables(self):
        """
        Retorna la lista de variables disponibles para usar en la plantilla
        """
        return [
            # Persona
            '{nombre_completo}', '{primer_nombre}', '{segundo_nombre}',
            '{primer_apellido}', '{segundo_apellido}',
            '{identificacion}', '{tipo_documento}', '{edad}', '{fecha_nacimiento}',
            '{genero}', '{estado_civil}',

            # Ubicación
            '{vereda}', '{zona}', '{direccion}',
            '{municipio}', '{departamento}',

            # Organización
            '{organizacion}', '{nit_organizacion}', '{direccion_organizacion}',
            '{telefono_organizacion}', '{email_organizacion}',

            # Fechas
            '{fecha_expedicion}', '{fecha_vencimiento}',
            '{año}', '{mes}', '{dia}',
            '{numero_documento}',

            # Documento
            '{tipo_documento_generado}', '{observaciones}',
        ]

    def render_content(self, person, issue_date, expiration_date=None, **extra_vars):
        """
        Renderiza el contenido de la plantilla con los datos proporcionados

        Args:
            person: Instancia de Person
            issue_date: Fecha de expedición
            expiration_date: Fecha de vencimiento (opcional)
            **extra_vars: Variables adicionales

        Returns:
            str: HTML renderizado del documento
        """
        from censoapp.document_views import generate_document_content_from_template
        return generate_document_content_from_template(
            template=self,
            person=person,
            organization=self.organization,
            issue_date=issue_date,
            expiration_date=expiration_date,
            **extra_vars
        )

    def duplicate(self, new_name=None, new_version=None):
        """
        Duplica esta plantilla para crear una nueva versión

        Args:
            new_name: Nombre para la nueva plantilla (opcional)
            new_version: Versión para la nueva plantilla (opcional)

        Returns:
            DocumentTemplate: Nueva plantilla duplicada
        """
        self.pk = None
        self.id = None
        self.is_default = False
        self.name = new_name or f"{self.name} (Copia)"
        self.version = new_version or f"{self.version}.1"
        self.created_at = None
        self.updated_at = None
        self.save()
        return self


class TemplateBlock(models.Model):
    """
    Bloques de contenido para plantillas.
    Permite crear estructura modular y reutilizable.
    """
    template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name="Plantilla"
    )

    BLOCK_TYPES = [
        ('text', 'Texto'),
        ('paragraph', 'Párrafo'),
        ('list', 'Lista'),
        ('table', 'Tabla'),
        ('image', 'Imagen'),
        ('spacer', 'Espaciador'),
        ('divider', 'Divisor'),
        ('custom', 'HTML Personalizado'),
    ]

    block_type = models.CharField(
        max_length=20,
        choices=BLOCK_TYPES,
        verbose_name="Tipo de Bloque"
    )

    order = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición en el documento"
    )

    content = models.TextField(
        verbose_name="Contenido",
        help_text="Contenido del bloque (puede contener variables)"
    )

    # Estilos del bloque
    is_bold = models.BooleanField(
        default=False,
        verbose_name="Negrita"
    )

    is_italic = models.BooleanField(
        default=False,
        verbose_name="Cursiva"
    )

    is_underline = models.BooleanField(
        default=False,
        verbose_name="Subrayado"
    )

    alignment = models.CharField(
        max_length=20,
        choices=[
            ('left', 'Izquierda'),
            ('center', 'Centro'),
            ('right', 'Derecha'),
            ('justify', 'Justificado'),
        ],
        default='justify',
        verbose_name="Alineación"
    )

    font_size_modifier = models.IntegerField(
        default=0,
        verbose_name="Modificador de Tamaño",
        help_text="Suma/resta al tamaño base de fuente (ej: +2, -1)"
    )

    custom_style = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Estilo CSS Personalizado",
        help_text="Estilos CSS inline adicionales"
    )

    # Configuración específica por tipo
    config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Configuración del Bloque",
        help_text="Configuración específica según el tipo de bloque"
    )

    class Meta:
        verbose_name = "Bloque de Plantilla"
        verbose_name_plural = "Bloques de Plantilla"
        ordering = ['template', 'order']

    def __str__(self):
        return f"{self.template.name} - {self.get_block_type_display()} #{self.order}"


class TemplateVariable(models.Model):
    """
    Variables personalizadas adicionales que puede definir cada organización.
    Ahora basadas en campos de modelos (Persona, Ficha Familiar, Asociación, Organización)
    """
    VARIABLE_TYPES = [
        ('person', 'Dato de Persona'),
        ('family_card', 'Dato de Ficha Familiar'),
        ('association', 'Dato de Asociación'),
        ('organization', 'Dato de Organización'),
    ]

    organization = models.ForeignKey(
        'censoapp.Organizations',
        on_delete=models.CASCADE,
        related_name='custom_variables',
        verbose_name="Organización"
    )

    variable_name = models.CharField(
        max_length=100,
        verbose_name="Nombre de la Variable",
        help_text="Nombre único sin llaves (ej: 'territorio', 'nombre_completo')"
    )

    variable_type = models.CharField(
        max_length=20,
        choices=VARIABLE_TYPES,
        verbose_name="Tipo de Variable",
        help_text="Tipo de dato (Persona, Ficha Familiar, Asociación, Organización)"
    )

    variable_value = models.CharField(
        max_length=200,
        verbose_name="Campo del Modelo",
        help_text="Nombre del campo del modelo (ej: 'organization_territory', 'full_name')"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción del propósito de esta variable"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    class Meta:
        verbose_name = "Variable Personalizada"
        verbose_name_plural = "Variables Personalizadas"
        unique_together = [['organization', 'variable_name']]
        ordering = ['organization', 'variable_type', 'variable_name']

    def __str__(self):
        return f"{{{self.variable_name}}} = {self.get_variable_type_display()}.{self.variable_value}"

    @property
    def full_variable_name(self):
        """Retorna el nombre de la variable con llaves"""
        return f"{{{self.variable_name}}}"

