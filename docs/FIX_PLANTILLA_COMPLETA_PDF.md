# Fix: Plantilla Completa en PDF de Documentos

**Fecha:** 21 de Diciembre de 2024  
**Problema:** El PDF generado solo muestra el contenido guardado en BD en lugar de usar la plantilla completa  
**Causa:** El campo `document_content` guarda un resumen en texto plano, no la estructura completa del documento  
**Solución:** Modificar los templates para poblar el formulario con datos guardados y regenerar el PDF con plantilla completa  

---

## 🐛 Problema Identificado

### Síntoma

Al generar un documento que ya existe en BD, el PDF muestra:

```
AVAL GENERAL
AVAL GENERAL para Andrés Sánchez López - Entidad: INSTITUCION EDUCATIVA MANUEL
MARIA MOSQUERA, Motivo: trabajar, Cargo: DOCENTE SECUNDARIA
```

### En lugar de:

```
AVAL

La AUTORIDAD Tradicional del Resguardo Indígena Puracé, de acuerdo a la Ley de Origen,
el Derecho Mayor, Derecho Propio y en uso de las facultades jurídicas, políticas,
territorial y administrativas que nos confiere la ley 89 de 1890 y la Constitución
Política de 1991, en sus artículos 7, 8, 10, 246, 286, 287, 329, 330 especialmente
y demás normas del fuero indígena vigente y a solicitud del comunero(a).

CERTIFICA

Que Andrés Sánchez López, identificado con Cedula Ciudadania No. 12345678,
actualmente se encuentra inscrito(a) en el censo del Resguardo Indígena Puracé...
```

### Causa

El campo `document.document_content` en la BD almacena:
```python
content = f"AVAL GENERAL para {person.full_name} - Entidad: {entidad}, Motivo: {motivo}, Cargo: {cargo}"
```

Este es solo un **resumen** para propósitos de búsqueda/auditoría, no el documento completo.

La función `generatePDF()` en JavaScript tiene la **plantilla completa** con todos los párrafos, pero cuando el documento ya existe, no se estaban poblando los campos del formulario correctamente.

---

## ✅ Soluciones Aplicadas

### 1. Aval General (`aval_general.html`)

**Modificación:** Parsear el `document_content` para extraer los datos y poblar el formulario antes de generar el PDF.

```javascript
{% if documento_generado %}
document.addEventListener('DOMContentLoaded', function() {
    // Extraer datos del contenido guardado
    const content = '{{ documento_generado.document_content|escapejs }}';
    
    // Parsear: "AVAL GENERAL para ... - Entidad: X, Motivo: Y, Cargo: Z"
    const entidadMatch = content.match(/Entidad:\s*([^,]+)/);
    const motivoMatch = content.match(/Motivo:\s*([^,]+)/);
    const cargoMatch = content.match(/Cargo:\s*(.+?)(?:\n|$)/);
    
    // Poblar formulario
    if (entidadMatch) document.getElementById('entidad').value = entidadMatch[1].trim();
    if (motivoMatch) {
        const motivoValue = motivoMatch[1].trim();
        const motivoSelect = document.getElementById('motivo');
        const motivoOption = Array.from(motivoSelect.options).find(opt => opt.value === motivoValue);
        if (motivoOption) {
            motivoSelect.value = motivoValue;
        } else {
            motivoSelect.value = 'otro';
            document.getElementById('motivoOtroDiv').style.display = 'block';
            document.getElementById('motivoOtro').value = motivoValue;
        }
    }
    if (cargoMatch) document.getElementById('cargo').value = cargoMatch[1].trim();
    
    // Generar PDF con plantilla completa
    setTimeout(() => generatePDF(), 100);
});
{% endif %}
```

**Resultado:**
- ✅ Extrae los datos del resumen en BD
- ✅ Llena el formulario con esos datos
- ✅ Llama a `generatePDF()` que usa la plantilla completa
- ✅ El PDF generado ahora incluye TODOS los párrafos

### 2. Aval de Estudio (`aval_estudio.html`)

**Modificación similar:**

```javascript
{% if documento_generado %}
document.addEventListener('DOMContentLoaded', function() {
    const content = '{{ documento_generado.document_content|escapejs }}';
    
    // Parsear: "AVAL DE ESTUDIO para ... - Institución: X, Programa: Y, Semestre: Z"
    const entidadMatch = content.match(/Institución:\s*([^,]+)/);
    const programaMatch = content.match(/Programa:\s*([^,]+)/);
    const semestreMatch = content.match(/Semestre:\s*(\d+)/);
    const proyectoMatch = content.match(/Proyecto:\s*([^,]+)/);
    const horasMatch = content.match(/Horas:\s*(\d+)/);
    
    // Poblar formulario
    if (entidadMatch) document.getElementById('entidad').value = entidadMatch[1].trim();
    if (programaMatch) document.getElementById('programa').value = programaMatch[1].trim();
    if (semestreMatch) document.getElementById('semestre').value = semestreMatch[1].trim();
    if (proyectoMatch) document.getElementById('proyecto').value = proyectoMatch[1].trim();
    if (horasMatch) document.getElementById('horas').value = horasMatch[1].trim();
    
    // Generar PDF con plantilla completa
    setTimeout(() => generatePDF(), 100);
});
{% endif %}
```

### 3. Constancia de Pertenencia

✅ Ya funciona correctamente porque siempre genera el PDF automáticamente sin depender de datos del formulario.

---

## 📊 Flujo Actualizado

### Antes (Incorrecto)

```
1. Usuario accede a documento existente
2. Backend envía document_content: "AVAL GENERAL para... - Entidad: X"
3. JavaScript usa document_content directamente en el PDF
4. ❌ PDF solo muestra el resumen, no la plantilla completa
```

### Ahora (Correcto)

```
1. Usuario accede a documento existente
2. Backend envía document_content: "AVAL GENERAL para... - Entidad: X"
3. JavaScript PARSEA el document_content
4. Extrae: entidad, motivo, cargo
5. Pobla el formulario con esos datos
6. Llama generatePDF() que usa la PLANTILLA COMPLETA
7. ✅ PDF muestra todos los párrafos correctamente
```

---

## 🎯 Comparación: Antes vs Ahora

### Contenido del PDF

**Antes:**
```
AVAL GENERAL
AVAL GENERAL para Andrés Sánchez López - Entidad: INSTITUCION EDUCATIVA...
```
(Solo 2 líneas)

**Ahora:**
```
AVAL

La AUTORIDAD Tradicional del Resguardo Indígena Puracé, de acuerdo a la Ley
de Origen, el Derecho Mayor, Derecho Propio y en uso de las facultades jurídicas,
políticas, territorial y administrativas que nos confiere la ley 89 de 1890...

CERTIFICA

Que Andrés Sánchez López, identificado con Cedula Ciudadania No. 12345678,
actualmente se encuentra inscrito(a) en el censo del Resguardo Indígena Puracé —
Vereda Campamento, reside de manera integral, comparte los usos y costumbres...

Se expide el presente AVAL para que Andrés Sánchez López pueda trabajar en
INSTITUCION EDUCATIVA MANUEL MARIA MOSQUERA, desempeñando el cargo de DOCENTE...

El presente aval se expide a solicitud del interesado para los fines que considere...

Dado en el Resguardo Indígena Puracé, a los 21 días del mes de diciembre de 2024.

FIRMAS AUTORIZADAS
[Firmas de la junta directiva]
[Código QR]
```
(Documento completo con todos los párrafos)

---

## 📝 Archivos Modificados

### 1. `templates/censo/documentos/aval_general.html`

**Cambio:** Líneas 353-395

**Modificación:** Agregar lógica de parseo y población del formulario

**Estado:** ✅ Actualizado

### 2. `templates/censo/documentos/aval_estudio.html`

**Cambio:** Líneas similares

**Modificación:** Agregar lógica de parseo para datos académicos

**Estado:** ✅ Actualizado

### 3. `templates/censo/documentos/constancia_pertenencia.html`

**Estado:** ✅ Ya funciona correctamente (sin cambios necesarios)

---

## ⚠️ Limitación Conocida: Vista Previa

### Problema Pendiente

La vista de **preview** (`/documento/preview/<id>/`) todavía puede mostrar solo el resumen porque usa `preview_document_jspdf.html` que no tiene acceso al formulario para parsear los datos.

### Soluciones Posibles

#### Opción A: Actualizar preview_document_jspdf.html (Complejo)
- Detectar tipo de documento
- Parsear document_content según el tipo
- Usar plantilla específica para cada tipo

#### Opción B: Redirigir a vista de generación (Simple)
- Cambiar el botón "Ver" en estadísticas
- En lugar de ir a `/preview/<id>/`
- Ir directamente a la URL de generación (`/documento/aval-general/<person_id>/`)
- El documento ya guardado se regenerará con la plantilla completa

#### Opción C: Mejorar almacenamiento (Mejor a largo plazo)
- Cambiar `document_content` de texto plano a JSON
- Guardar: `{"tipo": "aval_general", "datos": {"entidad": "...", "motivo": "..."}}`
- Permitir regeneración exacta del documento

### Recomendación Inmediata

**Opción B** - Cambiar el enlace en estadísticas:

```python
# En organization_stats.html
# Cambiar:
href="{% url 'preview-document-pdf' doc.id %}"

# Por:
{% if doc.document_type.document_type_name == 'Aval General' %}
    href="{% url 'generate-aval-general' doc.person.id %}"
{% elif doc.document_type.document_type_name == 'Aval de Estudio' %}
    href="{% url 'generate-aval-estudio' doc.person.id %}"
{% elif doc.document_type.document_type_name == 'Constancia de Pertenencia' %}
    href="{% url 'generate-constancia' doc.person.id %}"
{% else %}
    href="{% url 'preview-document-pdf' doc.id %}"
{% endif %}
```

---

## ✅ Estado Actual

### Funcionando Correctamente

- ✅ Generar Aval General (nuevo)
- ✅ Generar Aval de Estudio (nuevo)
- ✅ Generar Constancia de Pertenencia (nuevo)
- ✅ Regenerar documentos existentes (si se accede por URL de generación)

### Necesita Ajuste Menor

- ⚠️ Vista previa en `/documento/preview/<id>/` muestra solo resumen
- **Solución:** Cambiar enlaces en tabla de estadísticas para ir a URL de generación

---

## 🧪 Cómo Probar

### 1. Crear un Documento Nuevo

```
1. http://127.0.0.1:8000/personas/detail/1/
2. Generar Documento → Aval General
3. Llenar formulario
4. Generar y Guardar PDF
5. ✅ Verificar que muestra TODOS los párrafos
```

### 2. Acceder a Documento Existente

```
1. Usar la misma URL: /documento/aval-general/1/
2. El formulario se llena automáticamente con datos guardados
3. El PDF se genera automáticamente con plantilla completa
4. ✅ Verificar que muestra TODOS los párrafos
```

### 3. Verificar Contenido

El PDF debe incluir:
- ✅ Logo y datos de organización
- ✅ Título "AVAL"
- ✅ Párrafo 1 completo (Ley de Origen, Derecho Mayor, etc.)
- ✅ "CERTIFICA"
- ✅ Párrafo 2 (datos de la persona)
- ✅ Párrafo 3 (datos del formulario: entidad, motivo, cargo)
- ✅ Párrafo 4 (expedición del aval)
- ✅ Fecha
- ✅ Firmas
- ✅ Código QR

---

## 📋 Checklist

- [x] Identificado problema en aval_general.html
- [x] Agregado parseo de document_content
- [x] Implementado población automática del formulario
- [x] Actualizado aval_general.html
- [x] Actualizado aval_estudio.html
- [x] Verificado constancia_pertenencia.html
- [x] Documentado problema de vista previa
- [x] Propuesta solución para vista previa
- [ ] **Pendiente:** Actualizar enlaces en organization_stats.html (opcional)

---

**Implementado por:** GitHub Copilot  
**Fecha:** 21 de Diciembre de 2024  
**Archivos modificados:** 2 (aval_general.html, aval_estudio.html)  
**Estado:** ✅ PROBLEMA PRINCIPAL RESUELTO  
**Pendiente:** Vista previa (solución simple disponible)

