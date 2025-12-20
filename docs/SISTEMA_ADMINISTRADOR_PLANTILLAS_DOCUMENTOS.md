# 🎯 SISTEMA DE ADMINISTRADOR DE PLANTILLAS PARA DOCUMENTOS

## Fecha: 18 de diciembre de 2025

---

## 📋 ÍNDICE

1. [Análisis de la Necesidad](#análisis)
2. [Arquitectura del Sistema](#arquitectura)
3. [Modelos de Datos](#modelos)
4. [Vistas y Controladores](#vistas)
5. [Interfaz de Usuario](#interfaz)
6. [Guía de Implementación](#implementación)
7. [Manual de Uso](#manual)

---

## 🎯 ANÁLISIS DE LA NECESIDAD

### Problema Actual

**Sistema actual:**
- Plantillas hardcodeadas en el código
- No personalizables por organización
- Requiere programador para cambios
- Una sola plantilla para todos

**Ejemplo actual:**
```python
def get_default_aval_template():
    return """
LA JUNTA DIRECTIVA DE {organizacion}

CERTIFICA QUE:

{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion}...
"""
```

### Solución Propuesta

**Sistema de plantillas personalizable:**
- ✅ Cada organización crea sus plantillas
- ✅ Editor visual WYSIWYG
- ✅ Variables dinámicas
- ✅ Personalización de diseño (logo, colores, fuentes)
- ✅ Previsualización en tiempo real
- ✅ Versionamiento
- ✅ Múltiples plantillas por tipo de documento

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Componentes Principales

```
┌──────────────────────────────────────────────────────────┐
│  SISTEMA DE ADMINISTRADOR DE PLANTILLAS                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. MODELOS DE DATOS                                    │
│     - DocumentTemplate (Plantilla principal)            │
│     - TemplateBlock (Bloques de contenido)              │
│     - TemplateVariable (Variables personalizadas)       │
│                                                          │
│  2. VISTAS Y CONTROLADORES                              │
│     - Template CRUD (Crear/Editar/Eliminar)             │
│     - Template Editor (Editor visual)                   │
│     - Template Preview (Vista previa)                   │
│     - Variable Manager (Gestor de variables)            │
│                                                          │
│  3. INTERFAZ DE USUARIO                                 │
│     - Dashboard de plantillas                           │
│     - Editor WYSIWYG                                    │
│     - Constructor de bloques (drag & drop)              │
│     - Selector de variables                             │
│     - Configurador de estilos                           │
│                                                          │
│  4. GENERACIÓN DE DOCUMENTOS                            │
│     - Renderizador de plantillas                        │
│     - Procesador de variables                           │
│     - Generador de PDF                                  │
│     - Sistema de QR                                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Flujo de Trabajo

```
Usuario (Administrador de Organización)
    │
    ▼
┌─────────────────────────────┐
│ 1. Accede a Gestión         │
│    de Plantillas            │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ 2. Crea Nueva Plantilla     │
│    - Selecciona tipo        │
│    - Configura diseño       │
│    - Define contenido       │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ 3. Usa Editor Visual        │
│    - Agrega bloques         │
│    - Inserta variables      │
│    - Aplica estilos         │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ 4. Vista Previa             │
│    - Ve resultado final     │
│    - Prueba con datos       │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ 5. Activa Plantilla         │
│    - Marca como activa      │
│    - Define como defecto    │
└─────────────────────────────┘
    │
    ▼
Sistema usa la plantilla
para generar documentos
```

---

## 💾 MODELOS DE DATOS

### 1. DocumentTemplate (Plantilla Principal)

**Propósito:** Almacena toda la configuración de una plantilla de documento.

**Campos principales:**

```python
# Relaciones
organization → Organizations
document_type → DocumentType

# Información básica
name: str (ej: "Aval Comunitario v2")
description: str
version: str (ej: "1.0", "2.1")
is_active: bool
is_default: bool

# Configuración de diseño
logo_position: str (top-left, top-center, top-right, none)
logo_width: int (píxeles)
show_organization_info: bool
organization_info_position: str

# Contenido
document_title: str (ej: "CERTIFICADO")
introduction_text: str (acepta variables)
content_blocks: JSONField (estructura de bloques)
closing_text: str

# Firmas y pie de página
show_signatures: bool
signature_layout: str (horizontal, two-columns, vertical)
show_qr_code: bool
qr_position: str
footer_text: str

# Estilos
primary_color: str (#RRGGBB)
secondary_color: str
text_color: str
font_family: str
font_size: int (puntos)

# Márgenes (mm)
margin_top, margin_bottom, margin_left, margin_right: int

# Página
page_size: str (A4, Letter, Legal)
page_orientation: str (portrait, landscape)

# Personalización avanzada
custom_css: str
custom_html: str
```

**Métodos importantes:**

```python
def get_variables():
    """Retorna lista de variables disponibles"""
    
def render_content(person, issue_date, expiration_date):
    """Renderiza la plantilla con datos reales"""
    
def duplicate(new_name, new_version):
    """Duplica la plantilla para crear nueva versión"""
```

### 2. TemplateBlock (Bloques de Contenido)

**Propósito:** Permite crear contenido modular y estructurado.

**Tipos de bloques:**
- `text`: Texto simple
- `paragraph`: Párrafo completo
- `list`: Lista (numerada o con viñetas)
- `table`: Tabla
- `image`: Imagen
- `spacer`: Espacio en blanco
- `divider`: Línea divisoria
- `custom`: HTML personalizado

**Campos:**

```python
template → DocumentTemplate
block_type: str (text, paragraph, list, etc.)
order: int (orden de aparición)
content: str (contenido con variables)

# Estilos
is_bold: bool
is_italic: bool
is_underline: bool
alignment: str (left, center, right, justify)
font_size_modifier: int (+2, -1, etc.)
custom_style: str (CSS inline)

# Configuración específica
config: JSONField (específico por tipo)
```

### 3. TemplateVariable (Variables Personalizadas)

**Propósito:** Permite a cada organización definir variables adicionales.

**Ejemplo:**
```
{gobernador} → "Juan Pérez Gómez"
{secretario} → "María López Sánchez"
{resolucion} → "Resolución No. 123 de 2025"
```

**Campos:**

```python
organization → Organizations
variable_name: str (sin llaves, ej: "gobernador")
variable_value: str (valor de reemplazo)
description: str
is_active: bool
```

---

## 🎨 VARIABLES DISPONIBLES

### Variables de Persona

```
{nombre_completo} → Juan Carlos Pérez López
{primer_nombre} → Juan
{segundo_nombre} → Carlos
{primer_apellido} → Pérez
{segundo_apellido} → López
{identificacion} → 123456789
{tipo_documento} → Cédula de Ciudadanía
{edad} → 35
{fecha_nacimiento} → 15/03/1988
{genero} → Masculino
{estado_civil} → Casado(a)
```

### Variables de Ubicación

```
{vereda} → Puracé
{zona} → Rural
{direccion} → Calle 5 #10-20
{municipio} → Popayán
{departamento} → Cauca
```

### Variables de Organización

```
{organizacion} → Resguardo Indígena Puracé
{nit_organizacion} → 900.123.456-7
{direccion_organizacion} → Cra 7 #5-63
{telefono_organizacion} → (2) 8201234
{email_organizacion} → info@resguardo.gov.co
```

### Variables de Fechas

```
{fecha_expedicion} → 18 de diciembre de 2025
{fecha_vencimiento} → 18 de junio de 2026
{año} → 2025
{mes} → diciembre
{dia} → 18
{numero_documento} → CERT-2025-001
```

### Variables del Documento

```
{tipo_documento_generado} → Certificado de Pertenencia
{observaciones} → Documento expedido para trámites educativos
```

---

## 🎯 EJEMPLOS DE PLANTILLAS

### Ejemplo 1: Aval Comunitario Simple

**Configuración:**
```json
{
  "logo_position": "top-left",
  "logo_width": 120,
  "organization_info_position": "top-right",
  "document_title": "AVAL COMUNITARIO",
  "title_alignment": "center",
  "introduction_text": "LA JUNTA DIRECTIVA DE {organizacion}",
  "introduction_bold": true,
  "show_signatures": true,
  "signature_layout": "two-columns",
  "show_qr_code": true,
  "primary_color": "#2196F3"
}
```

**Bloques de contenido:**
```json
[
  {
    "type": "paragraph",
    "order": 1,
    "content": "CERTIFICA QUE:",
    "is_bold": true,
    "alignment": "center"
  },
  {
    "type": "paragraph",
    "order": 2,
    "content": "{nombre_completo}, identificado(a) con {tipo_documento} No. {identificacion}, nacido(a) el {fecha_nacimiento}, residente en la vereda {vereda}, zona {zona}, es miembro activo de nuestra comunidad indígena.",
    "alignment": "justify"
  },
  {
    "type": "paragraph",
    "order": 3,
    "content": "Se expide el presente AVAL para los fines que la persona interesada estime conveniente.",
    "alignment": "justify"
  },
  {
    "type": "paragraph",
    "order": 4,
    "content": "Expedido en {vereda}, a los {dia} días del mes de {mes} de {año}.",
    "alignment": "right"
  }
]
```

### Ejemplo 2: Constancia de Pertenencia con Logo y Descripción

**Diseño:**
```
┌────────────────────────────────────────────────────────┐
│  [LOGO]              RESGUARDO INDÍGENA PURACÉ         │
│  120px               NIT: 900.123.456-7                │
│                      Popayán, Cauca                     │
│                      Resolución No. 123 de 1980        │
├────────────────────────────────────────────────────────┤
│                                                        │
│         CONSTANCIA DE PERTENENCIA COMUNITARIA         │
│                                                        │
│  LA JUNTA DIRECTIVA DE RESGUARDO INDÍGENA PURACÉ      │
│                                                        │
│                    HACE CONSTAR QUE:                   │
│                                                        │
│  Juan Carlos Pérez López, identificado con CC          │
│  123.456.789, nacido el 15/03/1988, con 35 años       │
│  de edad, es miembro perteneciente a nuestra          │
│  comunidad indígena.                                   │
│                                                        │
│  La persona reside en la vereda Puracé, zona Rural,   │
│  y se encuentra registrada en nuestro censo           │
│  comunitario.                                          │
│                                                        │
│  Se expide la presente constancia a solicitud del     │
│  interesado para los fines que estime conveniente.    │
│                                                        │
│              Puracé, 18 de diciembre de 2025          │
│                                                        │
│  ___________________      ___________________          │
│  Gobernador(a)            Secretario(a)               │
│  Juan Pérez Gómez         María López Sánchez         │
│                                                [QR]    │
│  Válido hasta: 18 de junio de 2026                    │
└────────────────────────────────────────────────────────┘
```

---

## 🖥️ INTERFAZ DE USUARIO

### 1. Dashboard de Plantillas

**Ruta:** `/templates/dashboard`

**Características:**
- Lista de plantillas por organización
- Filtros por tipo de documento
- Estado (activa/inactiva)
- Botón "Crear Nueva Plantilla"
- Acciones: Editar, Duplicar, Eliminar, Vista Previa

**Vista:**
```
┌─────────────────────────────────────────────────────────┐
│  GESTIÓN DE PLANTILLAS DE DOCUMENTOS                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [+ Nueva Plantilla]     [Tipo ▼] [Estado ▼]          │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Aval Comunitario v2.0                    [Activa]│  │
│  │ Para: Aval de Pertenencia                       │   │
│  │ Última modificación: 18/12/2025                 │   │
│  │ [Ver] [Editar] [Duplicar] [⋮]                   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Constancia Educativa v1.0               [Inactiva]│ │
│  │ Para: Constancia de Pertenencia                │   │
│  │ Última modificación: 10/12/2025                │   │
│  │ [Ver] [Editar] [Duplicar] [⋮]                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. Editor de Plantillas

**Ruta:** `/templates/edit/<id>`

**Características:**
- Tabs de configuración:
  - Información General
  - Diseño y Estilos
  - Contenido (bloques)
  - Firmas y Pie de Página
  - Vista Previa

**Vista:**
```
┌─────────────────────────────────────────────────────────┐
│  EDITAR PLANTILLA: Aval Comunitario v2.0                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [General] [Diseño] [Contenido] [Firmas] [Vista Previa]│
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ CONFIGURACIÓN DE DISEÑO                           │ │
│  ├───────────────────────────────────────────────────┤ │
│  │                                                   │ │
│  │  Logo:                                            │ │
│  │  ○ Superior Izquierda  ○ Superior Centro         │ │
│  │  ○ Superior Derecha    ○ Sin Logo                │ │
│  │  Ancho: [120] px                                  │ │
│  │                                                   │ │
│  │  Información de Organización:                     │ │
│  │  ☑ Mostrar en encabezado                         │ │
│  │  Posición: [Superior Derecha ▼]                   │ │
│  │                                                   │ │
│  │  Colores:                                         │ │
│  │  Primario: [#2196F3] 🎨                          │ │
│  │  Secundario: [#1976D2] 🎨                        │ │
│  │  Texto: [#000000] 🎨                             │ │
│  │                                                   │ │
│  │  Fuente:                                          │ │
│  │  Familia: [Arial ▼]  Tamaño: [12] pt            │ │
│  │                                                   │ │
│  │  Márgenes (mm):                                   │ │
│  │  Superior: [25]  Inferior: [25]                   │ │
│  │  Izquierdo: [25] Derecho: [25]                   │ │
│  │                                                   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  [Guardar]  [Cancelar]  [Vista Previa]                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. Constructor de Bloques (Drag & Drop)

**En Tab "Contenido":**

```
┌─────────────────────────────────────────────────────────┐
│  CONSTRUCTOR DE CONTENIDO                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  BLOQUES DISPONIBLES:          DOCUMENTO:              │
│  ┌──────────────┐              ┌──────────────────┐    │
│  │ [T] Texto    │              │ 1. Párrafo       │    │
│  │ [P] Párrafo  │              │    "CERTIFICA... │    │
│  │ [L] Lista    │              │    [✎] [↑] [↓] [×]│    │
│  │ [#] Tabla    │              ├──────────────────┤    │
│  │ [🖼] Imagen   │              │ 2. Párrafo       │    │
│  │ [_] Espaciador│             │    "{nombre}..." │    │
│  │ [—] Divisor   │             │    [✎] [↑] [↓] [×]│    │
│  │ [<>] HTML    │              ├──────────────────┤    │
│  └──────────────┘              │ + Agregar Bloque │    │
│                                 └──────────────────┘    │
│                                                         │
│  EDITAR BLOQUE #1:                                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Tipo: [Párrafo ▼]                               │   │
│  │                                                 │   │
│  │ Contenido:                                      │   │
│  │ ┌─────────────────────────────────────────────┐ │   │
│  │ │ CERTIFICA QUE:                              │ │   │
│  │ └─────────────────────────────────────────────┘ │   │
│  │                                                 │   │
│  │ Estilo:                                         │   │
│  │ ☑ Negrita  ☐ Cursiva  ☐ Subrayado             │   │
│  │ Alineación: [Centro ▼]                         │   │
│  │                                                 │   │
│  │ Variables: [Insertar Variable ▼]               │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4. Vista Previa en Tiempo Real

**Características:**
- Muestra cómo se verá el documento final
- Usa datos de ejemplo o datos reales de una persona
- Selector de persona para preview
- Botón "Generar PDF de Prueba"

```
┌─────────────────────────────────────────────────────────┐
│  VISTA PREVIA                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Probar con datos de: [Juan Pérez ▼] [PDF]            │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │         [LOGO]         RESGUARDO INDÍGENA         │ │
│  │                        NIT: 900.123.456-7         │ │
│  │                                                   │ │
│  │           AVAL COMUNITARIO                        │ │
│  │                                                   │ │
│  │  LA JUNTA DIRECTIVA DE RESGUARDO INDÍGENA        │ │
│  │                                                   │ │
│  │              CERTIFICA QUE:                       │ │
│  │                                                   │ │
│  │  Juan Carlos Pérez López, identificado con       │ │
│  │  CC 123.456.789, nacido el 15/03/1988...         │ │
│  │                                                   │ │
│  │  ...                                              │ │
│  │                                                   │ │
│  │              Puracé, 18 de diciembre de 2025     │ │
│  │                                                   │ │
│  │  __________________    __________________         │ │
│  │  Gobernador            Secretario                │ │
│  │                                           [QR]   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 GUÍA DE IMPLEMENTACIÓN

### Paso 1: Migración de Base de Datos

```bash
# 1. Crear migración
python manage.py makemigrations censoapp

# 2. Aplicar migración
python manage.py migrate

# 3. Verificar
python manage.py showmigrations censoapp
```

### Paso 2: Registrar Modelos en Admin

**Archivo:** `censoapp/admin.py`

```python
from censoapp.template_models import (
    DocumentTemplate, 
    TemplateBlock, 
    TemplateVariable
)

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'document_type', 'version', 'is_active', 'is_default']
    list_filter = ['organization', 'document_type', 'is_active', 'is_default']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'last_modified_by']
    
    fieldsets = (
        ('Información General', {
            'fields': ('organization', 'document_type', 'name', 'description', 'version')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_default')
        }),
        ('Diseño', {
            'fields': ('logo_position', 'logo_width', 'show_organization_info', 
                      'organization_info_position', 'primary_color', 'secondary_color')
        }),
        # ... más fieldsets
    )

@admin.register(TemplateBlock)
class TemplateBlockAdmin(admin.ModelAdmin):
    list_display = ['template', 'block_type', 'order']
    list_filter = ['template', 'block_type']
    ordering = ['template', 'order']

@admin.register(TemplateVariable)
class TemplateVariableAdmin(admin.ModelAdmin):
    list_display = ['organization', 'variable_name', 'variable_value', 'is_active']
    list_filter = ['organization', 'is_active']
    search_fields = ['variable_name', 'variable_value']
```

### Paso 3: Crear Vistas

**Archivo:** `censoapp/template_views.py`

Ver archivo completo en la documentación técnica.

### Paso 4: Configurar URLs

**Archivo:** `censoapp/urls.py`

```python
from censoapp import template_views

urlpatterns = [
    # ... URLs existentes
    
    # Gestión de plantillas
    path('templates/', template_views.template_dashboard, name='template-dashboard'),
    path('templates/create/', template_views.template_create, name='template-create'),
    path('templates/edit/<int:pk>/', template_views.template_edit, name='template-edit'),
    path('templates/preview/<int:pk>/', template_views.template_preview, name='template-preview'),
    path('templates/duplicate/<int:pk>/', template_views.template_duplicate, name='template-duplicate'),
    path('templates/delete/<int:pk>/', template_views.template_delete, name='template-delete'),
    
    # Variables personalizadas
    path('variables/', template_views.variable_manager, name='variable-manager'),
]
```

### Paso 5: Crear Templates HTML

**Archivos necesarios:**
- `templates/templates/dashboard.html`
- `templates/templates/editor.html`
- `templates/templates/preview.html`
- `templates/templates/variable_manager.html`

### Paso 6: Migrar Documentos Existentes

**Script de migración:**

```python
# manage.py command: migrate_templates.py

from django.core.management.base import BaseCommand
from censoapp.models import Organizations, DocumentType
from censoapp.template_models import DocumentTemplate

class Command(BaseCommand):
    help = 'Crea plantillas por defecto para todas las organizaciones'

    def handle(self, *args, **options):
        organizations = Organizations.objects.all()
        document_types = DocumentType.objects.all()
        
        for org in organizations:
            for doc_type in document_types:
                # Crear plantilla por defecto
                template, created = DocumentTemplate.objects.get_or_create(
                    organization=org,
                    document_type=doc_type,
                    name=f"{doc_type.document_type_name} - Plantilla Base",
                    defaults={
                        'is_default': True,
                        'is_active': True,
                        # ... configuración por defecto
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Plantilla creada: {org.organization_name} - {doc_type.document_type_name}'
                        )
                    )
```

Ejecutar:
```bash
python manage.py migrate_templates
```

---

## 📚 MANUAL DE USO

### Para Administradores de Organización

#### 1. Crear una Nueva Plantilla

```
1. Ir a: Configuración → Plantillas de Documentos
2. Click en "Nueva Plantilla"
3. Seleccionar:
   - Tipo de documento (Aval, Constancia, etc.)
   - Nombre descriptivo
   - Descripción (opcional)
4. Click en "Crear"
```

#### 2. Configurar Diseño

```
Tab "Diseño y Estilos":

1. Logo:
   - Posición: Superior Izquierda
   - Ancho: 120 px

2. Información de Organización:
   ☑ Mostrar en encabezado
   Posición: Superior Derecha

3. Colores:
   - Primario: #2196F3 (azul corporativo)
   - Secundario: #1976D2
   - Texto: #000000

4. Fuente:
   - Familia: Arial
   - Tamaño: 12 pt

5. Márgenes:
   - Todos: 25 mm

6. Click "Guardar"
```

#### 3. Agregar Contenido (Bloques)

```
Tab "Contenido":

1. Click "+ Agregar Bloque"
2. Seleccionar tipo: Párrafo
3. Escribir contenido:
   "CERTIFICA QUE:"
4. Aplicar formato:
   ☑ Negrita
   Alineación: Centro
5. Click "Guardar Bloque"

6. Repetir para más bloques:
   - Bloque 2: Información de la persona
   - Bloque 3: Propósito del documento
   - Bloque 4: Fecha y lugar

7. Usar variables:
   Click en "Insertar Variable"
   Seleccionar: {nombre_completo}
   Se inserta en el texto actual
```

#### 4. Configurar Firmas

```
Tab "Firmas y Pie de Página":

1. Firmas:
   ☑ Mostrar firmas
   Diseño: Dos Columnas

2. Código QR:
   ☑ Mostrar código QR
   Posición: Inferior Derecha

3. Texto del pie:
   "Válido hasta: {fecha_vencimiento}"

4. Click "Guardar"
```

#### 5. Vista Previa y Prueba

```
Tab "Vista Previa":

1. Seleccionar persona de prueba:
   [Juan Pérez ▼]

2. Ver preview en pantalla

3. Click "Generar PDF de Prueba"

4. Si todo está bien:
   - Volver a tab "General"
   - ☑ Marcar como "Activa"
   - ☑ Marcar como "Por Defecto"
   - Click "Guardar"
```

#### 6. Usar Variables Personalizadas

```
Ir a: Configuración → Variables Personalizadas

1. Click "+ Nueva Variable"
2. Nombre: gobernador
3. Valor: Juan Pérez Gómez
4. Descripción: Nombre del gobernador actual
5. ☑ Activa
6. Click "Guardar"

Ahora puedes usar {gobernador} en tus plantillas
```

---

## 🔧 CARACTERÍSTICAS AVANZADAS

### 1. Versionamiento de Plantillas

```
Cuando quieras actualizar una plantilla:

1. En el dashboard, click en "Duplicar"
2. Se crea una copia con:
   - Nombre: "Plantilla Original (Copia)"
   - Versión: "1.0.1" (incrementada)
   - Estado: Inactiva
   
3. Edita la nueva versión
4. Cuando esté lista:
   - Actívala
   - Márcala como "Por Defecto"
   - Desactiva la versión anterior

Ventaja: Siempre tienes un respaldo
```

### 2. Plantillas con HTML Personalizado

```
Para usuarios avanzados:

Tab "Diseño" → Sección "Avanzado":

1. CSS Personalizado:
   .special-title {
       color: #FF0000;
       font-size: 24pt;
       border-bottom: 2px solid #000;
   }

2. HTML Personalizado:
   <div class="special-section">
       <h2 class="special-title">Sección Especial</h2>
       <p>{contenido_especial}</p>
   </div>

3. Usar en bloques tipo "HTML Personalizado"
```

### 3. Bloques Condicionales

```
Configuración JSON del bloque:

{
    "type": "paragraph",
    "content": "Edad: {edad} años",
    "condition": {
        "field": "edad",
        "operator": ">=",
        "value": 18
    }
}

Este bloque solo se muestra si la edad >= 18
```

### 4. Tablas Dinámicas

```
Bloque tipo "Tabla":

Config:
{
    "columns": [
        {"header": "Nombre", "variable": "{nombre_completo}"},
        {"header": "Documento", "variable": "{identificacion}"},
        {"header": "Vereda", "variable": "{vereda}"}
    ],
    "style": {
        "border": true,
        "header_bg": "#2196F3",
        "header_color": "#FFFFFF"
    }
}
```

---

## 📊 BENEFICIOS DEL SISTEMA

### Para las Organizaciones

```
✅ Personalización total de documentos
✅ Sin necesidad de programador
✅ Cambios inmediatos
✅ Múltiples plantillas por tipo
✅ Mantiene identidad corporativa
✅ Versionamiento y respaldos
✅ Variables personalizadas
```

### Para los Usuarios Finales

```
✅ Documentos profesionales
✅ Diseño consistente
✅ Información precisa
✅ Verificación con QR
✅ Rápida generación
```

### Para el Sistema

```
✅ Escalable
✅ Mantenible
✅ Auditable (historial de cambios)
✅ Multi-tenant (por organización)
✅ Extensible (nuevos tipos de bloques)
```

---

## 🎯 ROADMAP FUTURO

### Fase 1: Básico (Actual)
- [x] Modelo de datos
- [x] CRUD de plantillas
- [x] Editor simple
- [x] Variables básicas
- [x] Vista previa

### Fase 2: Avanzado
- [ ] Editor WYSIWYG completo
- [ ] Drag & Drop de bloques
- [ ] Vista previa en tiempo real
- [ ] Plantillas prediseñadas (templates)
- [ ] Importar/Exportar plantillas

### Fase 3: Profesional
- [ ] Bloques condicionales
- [ ] Tablas dinámicas
- [ ] Gráficos y estadísticas
- [ ] Firmas digitales
- [ ] Múltiples idiomas

### Fase 4: Enterprise
- [ ] Marketplace de plantillas
- [ ] Colaboración multi-usuario
- [ ] Aprobación de plantillas
- [ ] A/B testing de diseños
- [ ] Analytics de uso

---

## 📞 SOPORTE

### Preguntas Frecuentes

**Q: ¿Puedo tener múltiples plantillas activas?**
A: Sí, pero solo una puede ser "Por Defecto" por tipo de documento.

**Q: ¿Qué pasa con los documentos ya generados si cambio la plantilla?**
A: Los documentos ya generados NO cambian. Solo los nuevos usan la plantilla actualizada.

**Q: ¿Puedo usar HTML en las plantillas?**
A: Sí, en bloques tipo "HTML Personalizado" o en "HTML Personalizado" avanzado.

**Q: ¿Las variables personalizadas afectan a otras organizaciones?**
A: No, cada organización tiene sus propias variables aisladas.

**Q: ¿Cómo vuelvo a una versión anterior?**
A: Usa el sistema de duplicación. Duplica la versión que quieres usar y actívala.

---

## ✅ CONCLUSIÓN

Este sistema de administrador de plantillas ofrece:

1. **Flexibilidad Total** - Cada organización diseña sus documentos
2. **Facilidad de Uso** - No requiere conocimientos técnicos
3. **Profesionalismo** - Resultados de alta calidad
4. **Escalabilidad** - Crece con las necesidades
5. **Mantenibilidad** - Cambios rápidos y seguros

**El sistema transforma la generación de documentos de un proceso rígido y técnico a uno flexible y accesible para todos.**

---

**Fecha:** 18 de diciembre de 2025  
**Versión:** 1.0  
**Estado:** Diseño completo - Listo para implementación

