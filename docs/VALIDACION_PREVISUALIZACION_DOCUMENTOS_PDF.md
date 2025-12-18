# 🔍 VALIDACIÓN Y ESTANDARIZACIÓN DE PREVISUALIZACIÓN DE DOCUMENTOS PDF

**Fecha:** 17 de Diciembre 2025  
**Objetivo:** Validar y estandarizar la funcionalidad de previsualización, descarga e impresión de PDFs en todo el sistema  
**Estado:** 🔄 **EN PROGRESO**

---

## 📋 UBICACIONES DONDE SE MUESTRAN DOCUMENTOS

### 1. **Lista de Documentos por Organización** ✅
**Archivo:** `templates/censo/documentos/organization_stats.html`  
**URL:** `/documentos/estadisticas/`

**Funcionalidades actuales:**
- ✅ Vista previa con `preview-document-pdf` (abre en nueva pestaña)
- ✅ Ver detalles con `view-document`
- ✅ Descargar PDF con `download-document-pdf?download=true`

**Estado:** ✅ **IMPLEMENTADO CORRECTAMENTE**

---

### 2. **Vista de Detalles del Documento** ⚠️
**Archivo:** `templates/censo/documentos/view_document.html`  
**URL:** `/documento/ver/<id>/`

**Funcionalidades actuales:**
- ⚠️ Vista previa usando `previewPDF()` → Abre en ventana nueva con `download-document-pdf`
- ⚠️ Descargar usando `downloadPDF()` → Descarga directa con parámetro `?download=true`
- ✅ Imprimir → `window.print()` (imprime la página HTML)

**Problemas identificados:**
1. ❌ No usa la vista previa dedicada con PDF.js (`preview-document-pdf`)
2. ❌ Funciones JavaScript diferentes a las demás vistas
3. ❌ Botón "Vista Previa PDF" redundante (ya está viendo el documento)
4. ❌ El botón imprimir imprime HTML, no el PDF

**Estado:** ⚠️ **NECESITA ACTUALIZACIÓN**

---

### 3. **Vista Previa Dedicada con PDF.js** ✅
**Archivo:** `templates/censo/documentos/preview_document.html`  
**URL:** `/documento/preview/<id>/`

**Funcionalidades:**
- ✅ Renderizado completo con PDF.js
- ✅ Navegación entre páginas
- ✅ Botón Descargar → Función `downloadPDF()`
- ✅ Botón Imprimir → `window.print()` del PDF
- ✅ Botón Volver → Regresa a detalles

**Estado:** ✅ **IMPLEMENTADO CORRECTAMENTE**

---

### 4. **Generación de Documentos** ✅
**Archivo:** `templates/censo/documentos/generate_document.html`  
**URL:** `/documento/generar/<person_id>/`

**Funcionalidades:**
- ✅ Formulario de generación
- ✅ Redirige a vista de detalles después de generar

**Estado:** ✅ **FUNCIONAL** (no requiere cambios)

---

### 5. **Detalle de Persona** ✅
**Archivo:** `templates/censo/persona/detail_person.html`  
**URL:** `/personas/detail/<id>/`

**Funcionalidades:**
- ✅ Botón "Generar Documento" → Redirige a `generate-document`
- ℹ️ No muestra lista de documentos generados (podría agregarse)

**Estado:** ✅ **FUNCIONAL** (mejora opcional: mostrar documentos)

---

## 🎯 PLAN DE ESTANDARIZACIÓN

### Cambios Necesarios:

#### 1. **Actualizar `view_document.html`** (PRIORIDAD ALTA)

**Problemas a resolver:**
- Eliminar botón "Vista Previa PDF" (ya está viendo el documento)
- Cambiar botón "Imprimir" para que imprima el PDF real
- Cambiar botón "Descargar" para que use la misma función que `preview_document.html`
- Agregar botón "Vista Previa PDF Completa" que redirija a `preview-document-pdf`

**Funcionalidad deseada:**
```html
<div>
    <!-- Botón para abrir vista previa con PDF.js -->
    <a href="{% url 'preview-document-pdf' document.id %}"
       class="btn btn-primary me-2"
       target="_blank">
        <i class="fas fa-eye me-2"></i>
        Vista Previa PDF
    </a>
    
    <!-- Botón para descargar -->
    <a href="{% url 'download-document-pdf' document.id %}?download=true"
       class="btn btn-success me-2"
       download>
        <i class="fas fa-download me-2"></i>
        Descargar PDF
    </a>
    
    <!-- Botón para imprimir (abre vista previa e imprime) -->
    <button onclick="printDocument()" class="btn btn-outline-primary me-2">
        <i class="fas fa-print me-2"></i>
        Imprimir PDF
    </button>
</div>

<script>
function printDocument() {
    // Abrir vista previa y ejecutar impresión
    const url = "{% url 'preview-document-pdf' document.id %}";
    const printWindow = window.open(url, '_blank');
    
    // Esperar a que cargue y ejecutar impresión
    printWindow.addEventListener('load', function() {
        setTimeout(() => {
            printWindow.print();
        }, 1000);
    });
}
</script>
```

---

#### 2. **Agregar sección de documentos en `detail_person.html`** (PRIORIDAD MEDIA)

**Mejora opcional:**
Mostrar lista de documentos generados para la persona en una nueva pestaña.

**Funcionalidad:**
- Tab adicional "Documentos"
- Lista de documentos con:
  - Tipo de documento
  - Número
  - Fecha de expedición
  - Estado
  - Botones: Vista Previa, Descargar

---

## 🔧 FUNCIONES JAVASCRIPT ESTANDARIZADAS

### Función para Descargar PDF:
```javascript
function downloadPDF(documentId, documentNumber) {
    const url = `/documento/download/${documentId}/?download=true`;
    const link = document.createElement('a');
    link.href = url;
    link.download = `documento_${documentNumber}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
```

### Función para Vista Previa:
```javascript
function previewPDF(documentId) {
    const url = `/documento/preview/${documentId}/`;
    window.open(url, '_blank');
}
```

### Función para Imprimir:
```javascript
function printPDF(documentId) {
    const url = `/documento/preview/${documentId}/`;
    const printWindow = window.open(url, '_blank');
    printWindow.addEventListener('load', function() {
        setTimeout(() => {
            printWindow.print();
        }, 1000);
    });
}
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### `view_document.html`:
- [x] Actualizar botones de acción
- [x] Implementar funciones JavaScript estandarizadas
- [x] Eliminar botón redundante "Vista Previa PDF"
- [x] Agregar botón "Vista Previa PDF Completa"
- [x] Actualizar botón Imprimir para imprimir PDF
- [x] Limpiar CSS no utilizado
- [ ] Testing en navegadores diferentes

### `detail_person.html` (Opcional):
- [ ] Agregar pestaña "Documentos"
- [ ] Mostrar lista de documentos generados
- [ ] Implementar botones de acción
- [ ] Aplicar filtros por estado
- [ ] Testing de funcionalidad

### Validación General:
- [ ] Verificar que todas las URLs funcionen
- [ ] Probar descarga en diferentes navegadores
- [ ] Probar impresión en diferentes navegadores
- [ ] Verificar permisos por organización
- [ ] Documentar cambios

---

## 🎨 DISEÑO ESTANDARIZADO DE BOTONES

### Botones en DataTables (organization_stats.html):
```html
<div class="btn-group" role="group">
    <a href="{% url 'preview-document-pdf' doc.id %}"
       class="btn btn-action-view"
       title="Vista Previa PDF"
       target="_blank">
        <i class="fas fa-eye"></i>
    </a>
    <a href="{% url 'view-document' doc.id %}"
       class="btn btn-action-details"
       title="Ver Detalles">
        <i class="fas fa-file-alt"></i>
    </a>
    <a href="{% url 'download-document-pdf' doc.id %}?download=true"
       class="btn btn-action-download"
       title="Descargar PDF">
        <i class="fas fa-download"></i>
    </a>
</div>
```

### Botones en Vista de Detalles (view_document.html):
```html
<div class="btn-group" role="group">
    <a href="{% url 'preview-document-pdf' document.id %}"
       class="btn btn-primary me-2"
       target="_blank">
        <i class="fas fa-eye me-2"></i>
        Vista Previa PDF
    </a>
    <a href="{% url 'download-document-pdf' document.id %}?download=true"
       class="btn btn-success me-2">
        <i class="fas fa-download me-2"></i>
        Descargar PDF
    </a>
    <button onclick="printDocument({{ document.id }}, '{{ document.document_number }}')"
            class="btn btn-outline-primary me-2">
        <i class="fas fa-print me-2"></i>
        Imprimir PDF
    </button>
</div>
```

---

## 📊 MATRIZ DE FUNCIONALIDADES

| Vista | Vista Previa | Descargar | Imprimir | Estado |
|-------|-------------|-----------|----------|---------|
| **organization_stats.html** | ✅ PDF.js | ✅ Directa | ➖ N/A | ✅ OK |
| **preview_document.html** | ✅ PDF.js | ✅ JS Function | ✅ PDF | ✅ OK |
| **view_document.html** | ✅ PDF.js | ✅ Directa | ✅ PDF | ✅ OK |
| **detail_person.html** | ➖ N/A | ➖ N/A | ➖ N/A | ℹ️ Mejorar |

**Leyenda:**
- ✅ Implementado correctamente
- ⚠️ Implementado pero necesita mejoras
- ❌ No funciona correctamente
- ➖ No aplica
- ℹ️ Funcionalidad opcional

---

## 🚀 PRIORIDADES

### Alta Prioridad:
1. ✅ Actualizar `view_document.html` con botones estandarizados
2. ✅ Implementar funciones JavaScript consistentes
3. ✅ Verificar funcionamiento en todos los navegadores

### Media Prioridad:
4. Agregar pestaña de documentos en `detail_person.html`
5. Implementar filtros en lista de documentos

### Baja Prioridad:
6. Agregar estadísticas de documentos por persona
7. Implementar búsqueda de documentos

---

## 📝 NOTAS TÉCNICAS

### URLs del Sistema:
- Vista previa PDF.js: `/documento/preview/<id>/`
- Descargar PDF: `/documento/download/<id>/?download=true`
- Ver detalles HTML: `/documento/ver/<id>/`
- Generar documento: `/documento/generar/<person_id>/`
- Estadísticas: `/documentos/estadisticas/`

### Permisos:
- Todos los endpoints validan organización del usuario
- Superusuarios pueden ver todos los documentos
- Usuarios normales solo ven documentos de su organización

---

**Siguiente paso:** Implementar cambios en `view_document.html`

