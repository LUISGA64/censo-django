# Mejora: Listar Plantillas Personalizadas en Generación de Documentos

**Fecha:** 20 de Diciembre de 2024  
**Módulo:** Generación de Documentos  
**Archivos Modificados:** 2

---

## 📋 Problema Identificado

Al generar documentos para personas, el sistema solo listaba los **tipos de documentos genéricos** (DocumentType), sin dar la opción de seleccionar entre las **plantillas personalizadas** (DocumentTemplate) que cada organización puede haber configurado.

### Antes:
- ❌ Solo se mostraban tipos genéricos (Aval, Constancia de Pertenencia)
- ❌ No se aprovechaban las plantillas personalizadas creadas
- ❌ No se daba feedback sobre si existen plantillas personalizadas

---

## ✅ Solución Implementada

Se modificó el flujo de generación de documentos para **priorizar las plantillas personalizadas** sobre los tipos genéricos.

### Lógica Implementada:

```
1. Si la organización tiene plantillas personalizadas activas:
   → Mostrar plantillas personalizadas
   
2. Si NO tiene plantillas personalizadas:
   → Mostrar tipos de documentos genéricos (fallback)
```

---

## 🔧 Cambios Realizados

### 1. Vista: `censoapp/document_views.py`

#### Función: `generate_document_view()`

**Cambios:**

✅ **Consulta de plantillas personalizadas:**
```python
# PRIORIDAD 1: Obtener plantillas personalizadas de la organización (activas)
custom_templates = DocumentTemplate.objects.filter(
    organization=organization,
    is_active=True
).select_related('document_type').order_by('document_type__document_type_name', '-is_default')

# PRIORIDAD 2: Si no hay plantillas personalizadas, obtener tipos de documentos genéricos
document_types = DocumentType.objects.filter(is_active=True) if not custom_templates.exists() else None

# Determinar qué mostrar: plantillas personalizadas o tipos genéricos
use_custom_templates = custom_templates.exists()
available_documents = custom_templates if use_custom_templates else document_types
```

✅ **Manejo de POST actualizado:**
```python
# Determinar si se usa plantilla personalizada o tipo genérico
if template_id:
    # Usar plantilla personalizada
    custom_template = get_object_or_404(
        DocumentTemplate, 
        pk=template_id, 
        organization=organization,
        is_active=True
    )
    document_type = custom_template.document_type
    using_custom_template = True
else:
    # Usar tipo de documento genérico
    document_type = get_object_or_404(DocumentType, pk=document_type_id, is_active=True)
    custom_template = None
    using_custom_template = False
```

✅ **Contexto actualizado:**
```python
context = {
    'person': person,
    'organization': organization,
    'has_board': board_positions.exists(),
    'has_signers': signers.exists(),
    'signers': signers,
    'segment': 'personas',
    # Plantillas personalizadas o tipos genéricos
    'use_custom_templates': use_custom_templates,
    'custom_templates': custom_templates if use_custom_templates else None,
    'document_types': document_types if not use_custom_templates else None,
}
```

✅ **Mensaje de éxito mejorado:**
```python
template_msg = f" (plantilla: {custom_template.name})" if using_custom_template else ""
messages.success(
    request,
    f"Documento '{document_type.document_type_name}'{template_msg} generado exitosamente. "
    f"Número: {generated_doc.document_number}"
)
```

---

### 2. Template: `templates/censo/documentos/generate_document.html`

**Cambios:**

✅ **Título dinámico:**
```django
<h5 class="mb-3">
    <i class="fas fa-clipboard-list me-2"></i>
    {% if use_custom_templates %}
    Seleccione la Plantilla de Documento
    {% else %}
    Seleccione el Tipo de Documento
    {% endif %}
</h5>
```

✅ **Sección para plantillas personalizadas:**
```django
{% if use_custom_templates %}
<!-- Mostrar plantillas personalizadas -->
<div class="alert alert-info mb-3">
    <i class="fas fa-info-circle me-2"></i>
    <strong>Plantillas Personalizadas:</strong> Su organización ha configurado plantillas personalizadas.
</div>
<div class="row">
    {% for template in custom_templates %}
    <div class="col-md-6">
        <label class="document-type-card" for="template_{{ template.id }}">
            <div class="d-flex align-items-start">
                <input
                    type="radio"
                    name="template_id"
                    id="template_{{ template.id }}"
                    value="{{ template.id }}"
                    required
                >
                <div class="flex-grow-1">
                    <h6 class="mb-2">
                        <i class="fas fa-file-alt text-primary me-2"></i>
                        {{ template.name }}
                        {% if template.is_default %}
                        <span class="badge bg-success ms-2">Por defecto</span>
                        {% endif %}
                    </h6>
                    <p class="mb-1 small text-muted">
                        <strong>Tipo:</strong> {{ template.document_type.document_type_name }}
                    </p>
                    {% if template.description %}
                    <p class="mb-2 text-muted small">{{ template.description }}</p>
                    {% endif %}
                    <p class="mb-0 small">
                        <i class="fas fa-tag text-info me-1"></i>
                        Versión: {{ template.version }}
                    </p>
                </div>
            </div>
        </label>
    </div>
    {% endfor %}
</div>
{% endif %}
```

✅ **Sección para tipos genéricos (fallback):**
```django
{% else %}
<!-- Mostrar tipos de documentos genéricos -->
<div class="alert alert-info mb-3">
    <i class="fas fa-info-circle me-2"></i>
    <strong>Nota:</strong> Su organización aún no ha configurado plantillas personalizadas. 
    Se usarán las plantillas predeterminadas del sistema.
</div>
<!-- ... código de tipos genéricos ... -->
{% endif %}
```

---

## 🎨 Mejoras en la UI

### Información Mostrada para Plantillas Personalizadas:

1. **Nombre de la plantilla** (ej: "Aval Comunitario v2")
2. **Badge "Por defecto"** si es la plantilla predeterminada
3. **Tipo de documento** asociado
4. **Descripción** de la plantilla (si existe)
5. **Versión** de la plantilla

### Alertas Informativas:

- ✅ **Con plantillas personalizadas:** Informa que la organización tiene plantillas configuradas
- ✅ **Sin plantillas personalizadas:** Informa que se usarán las plantillas predeterminadas del sistema

---

## 📊 Flujo de Decisión

```
┌─────────────────────────────────────┐
│  Usuario solicita generar documento │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ ¿Organización tiene plantillas      │
│ personalizadas activas?              │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
       SÍ            NO
        │             │
        ▼             ▼
┌──────────────┐  ┌──────────────────┐
│ Mostrar      │  │ Mostrar tipos    │
│ plantillas   │  │ de documentos    │
│ personalizadas│  │ genéricos        │
└──────┬───────┘  └────────┬─────────┘
       │                   │
       └─────────┬─────────┘
                 │
                 ▼
     ┌───────────────────────┐
     │ Usuario selecciona    │
     │ plantilla/tipo        │
     └───────────┬───────────┘
                 │
                 ▼
     ┌───────────────────────┐
     │ Generar documento     │
     │ con contenido         │
     │ personalizado         │
     └───────────────────────┘
```

---

## 🔍 Validaciones Implementadas

### En la Vista:

1. ✅ Verificar que el usuario tenga permisos para la organización
2. ✅ Validar que la plantilla pertenezca a la organización
3. ✅ Verificar que la plantilla esté activa
4. ✅ Verificar que exista junta directiva vigente
5. ✅ Verificar que haya firmantes autorizados

### En el Template:

1. ✅ Mostrar advertencias si no hay junta directiva
2. ✅ Mostrar advertencias si no hay firmantes
3. ✅ Deshabilitar generación si no hay documentos disponibles
4. ✅ Mostrar mensajes claros sobre el tipo de plantillas disponibles

---

## 📈 Ventajas de la Implementación

### Para el Usuario:

✅ **Claridad:** Sabe si está usando plantillas personalizadas o genéricas  
✅ **Opciones:** Puede elegir entre múltiples plantillas de un mismo tipo  
✅ **Información:** Ve la versión y descripción de cada plantilla  
✅ **Control:** Identifica fácilmente la plantilla por defecto  

### Para la Organización:

✅ **Personalización:** Puede crear plantillas específicas para sus necesidades  
✅ **Versionado:** Mantiene múltiples versiones de plantillas  
✅ **Flexibilidad:** Puede tener múltiples plantillas del mismo tipo de documento  
✅ **Gestión:** Puede activar/desactivar plantillas sin eliminarlas  

### Para el Sistema:

✅ **Escalabilidad:** Soporta múltiples organizaciones con plantillas independientes  
✅ **Fallback:** Si no hay plantillas personalizadas, usa las genéricas  
✅ **Auditoría:** Registra qué tipo de plantilla se usó en cada documento  
✅ **Seguridad:** Valida permisos por organización  

---

## 🧪 Pruebas Sugeridas

### Caso 1: Organización con Plantillas Personalizadas

1. Acceder como usuario de una organización con plantillas
2. Ir a detalle de una persona
3. Click en "Generar Documento"
4. **Verificar:** Se muestran las plantillas personalizadas
5. **Verificar:** Aparece mensaje informativo
6. **Verificar:** Se muestra versión y descripción
7. Seleccionar una plantilla y generar
8. **Verificar:** Mensaje de éxito incluye nombre de la plantilla

### Caso 2: Organización sin Plantillas Personalizadas

1. Acceder como usuario de una organización sin plantillas
2. Ir a detalle de una persona
3. Click en "Generar Documento"
4. **Verificar:** Se muestran tipos de documentos genéricos
5. **Verificar:** Aparece mensaje informando uso de plantillas predeterminadas
6. Seleccionar un tipo y generar
7. **Verificar:** Documento se genera correctamente

### Caso 3: Plantilla por Defecto

1. Organización con múltiples plantillas del mismo tipo
2. Una marcada como "por defecto"
3. **Verificar:** Badge "Por defecto" visible
4. **Verificar:** Aparece primero en el listado

---

## 📝 Notas Técnicas

### Campos de Formulario:

- **Plantillas personalizadas:** `template_id` (input radio)
- **Tipos genéricos:** `document_type` (input radio)

La vista detecta automáticamente cuál campo fue enviado.

### Orden de Listado:

Las plantillas se ordenan por:
1. Nombre del tipo de documento (alfabético)
2. Plantilla por defecto primero (`-is_default`)

### Consulta Optimizada:

Se usa `select_related('document_type')` para evitar consultas N+1.

---

## 🎯 Estado Actual

### Base de Datos:

- ✅ **1 plantilla personalizada** registrada
- ✅ Organización: Resguardo Indígena Purací
- ✅ Tipo: Aval
- ✅ Estado: Activa

### Compatibilidad:

- ✅ Compatible con organizaciones sin plantillas (fallback)
- ✅ Compatible con múltiples plantillas por organización
- ✅ Compatible con el sistema de generación existente

---

## 🚀 Próximos Pasos Sugeridos

1. **Crear más plantillas personalizadas** para probar el listado múltiple
2. **Marcar una como "por defecto"** para verificar el badge
3. **Probar con diferentes organizaciones** para validar aislamiento
4. **Agregar más tipos de documento** (Certificados, Cartas, etc.)

---

## ✅ Resumen

Se implementó exitosamente la funcionalidad para **listar y seleccionar plantillas personalizadas** al generar documentos, con fallback automático a tipos genéricos cuando no existan plantillas configuradas.

**Beneficio principal:** Las organizaciones ahora pueden aprovechar completamente sus plantillas personalizadas al generar documentos oficiales.

---

**Implementado por:** GitHub Copilot  
**Fecha:** 20 de Diciembre de 2024  
**Versión:** 1.0

