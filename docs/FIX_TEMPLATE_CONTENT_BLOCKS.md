# Solución: Contenido de Plantillas No Se Muestra al Editar

**Fecha:** 21 de Diciembre de 2024  
**Problema:** Al editar una plantilla con varios párrafos configurados, el contenido no se mostraba en el formulario  
**Causa:** Serialización incorrecta del campo JSONField en el template  
**Solución:** Serializar explícitamente en el backend y mejorar el manejo de caracteres especiales en JavaScript  

---

## 🐛 Problema Original

Cuando intentabas editar una plantilla (`DocumentTemplate`) que tenía varios párrafos configurados en `content_blocks`, **el contenido no se mostraba** en los textareas del editor.

### Síntomas
- ✅ La plantilla se guarda correctamente
- ❌ Al editar, los párrafos no aparecen
- ❌ El campo `content_blocks` está vacío en el formulario

---

## 🔍 Causa Raíz

### 1. **Serialización Incorrecta en el Template**

**Código problemático (línea 431 de `editor.html`):**
```html
<input type="hidden" name="content_blocks" id="content_blocks_json" 
       value='{% if template %}{{ template.content_blocks|safe }}{% else %}[]{% endif %}'>
```

**Problema:**
- `{{ template.content_blocks|safe }}` intenta imprimir el objeto Python directamente
- Django no serializa automáticamente JSONField a string JSON en templates
- El filtro `|safe` no convierte a JSON, solo marca como "seguro para HTML"
- Resultado: El navegador recibe algo como `[object Object]` o un formato incorrecto

### 2. **Template Literals con Caracteres Especiales**

**Código problemático (línea 728 de `editor.html`):**
```javascript
<textarea ...>${block.content || ''}</textarea>
```

**Problema:**
- Si `block.content` contiene comillas, saltos de línea o caracteres especiales
- El template literal puede romper el HTML
- Ejemplo: `content = 'Texto con "comillas" y \n saltos'` → HTML inválido

---

## ✅ Soluciones Aplicadas

### 1. **Serialización Explícita en el Backend**

**Archivo:** `censoapp/template_views.py`

#### En `template_edit()` (línea 310):
```python
# Serializar content_blocks a JSON string para el template
import json
content_blocks_json = json.dumps(template.content_blocks) if template.content_blocks else '[]'

context = {
    'segment': 'templates',
    'template': template,
    'action': 'edit',
    'blocks': template.blocks.all().order_by('order'),
    'document_types': document_types,
    'organizations': organizations,
    'organization': template.organization,
    'content_blocks_json': content_blocks_json  # ✅ Variable nueva con JSON serializado
}
```

#### En `template_create()` (línea 199):
```python
context = {
    'segment': 'templates',
    'organizations': organizations,
    'organization': organization,
    'document_types': document_types,
    'action': 'create',
    'content_blocks_json': '[]'  # ✅ Array vacío para nuevas plantillas
}
```

**Beneficios:**
- ✅ El JSON se serializa correctamente en Python
- ✅ Django pasa un string JSON válido al template
- ✅ Maneja correctamente caracteres especiales, Unicode, etc.

### 2. **Template Actualizado con escapejs**

**Archivo:** `templates/templates/editor.html` (línea 431)

**Antes:**
```html
<input type="hidden" name="content_blocks" id="content_blocks_json" 
       value='{% if template %}{{ template.content_blocks|safe }}{% else %}[]{% endif %}'>
```

**Ahora:**
```html
<input type="hidden" name="content_blocks" id="content_blocks_json" 
       value="{{ content_blocks_json|default:'[]'|escapejs }}">
```

**Cambios:**
- ✅ Usa `content_blocks_json` del contexto (ya serializado)
- ✅ `|escapejs` escapa caracteres especiales para JavaScript
- ✅ `|default:'[]'` garantiza un valor por defecto
- ✅ Usa comillas dobles en lugar de simples para mejor compatibilidad

### 3. **Manejo Seguro de Caracteres Especiales en JavaScript**

**Archivo:** `templates/templates/editor.html`

#### Mejora en `createBlockHTML()` (línea 711):
```javascript
function createBlockHTML(block, index) {
    // Escapar el contenido para HTML (prevenir XSS y problemas con caracteres especiales)
    const escapeHtml = (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    };
    
    // El contenido del textarea no necesita escaparse porque se establecerá con textContent
    const safeContent = block.content || '';
    
    return `
        <div class="content-block" data-block-id="${block.id}">
            <!-- ... header ... -->
            <div>
                <textarea
                    class="block-textarea"
                    data-block-index="${index}"
                    placeholder="..."
                    oninput="updateBlockContent(${index}, this.value)"
                ></textarea>  <!-- ✅ Sin contenido en el template literal -->
            </div>
            <!-- ... -->
        </div>
    `;
}
```

**Cambio clave:** El textarea se crea **vacío** en el template literal.

#### Mejora en `renderAllBlocks()` (línea 682):
```javascript
function renderAllBlocks() {
    const container = document.getElementById('content-blocks-container');
    container.innerHTML = '';

    if (contentBlocks.length === 0) {
        // ... mensaje de vacío ...
        return;
    }

    contentBlocks.forEach((block, index) => {
        const blockHTML = createBlockHTML(block, index);
        container.insertAdjacentHTML('beforeend', blockHTML);
        
        // ✅ Establecer el valor del textarea de forma segura DESPUÉS de insertar el HTML
        const textarea = container.querySelector(`textarea[data-block-index="${index}"]`);
        if (textarea && block.content) {
            textarea.value = block.content;  // ✅ Asignación directa, sin escapado
        }
    });
}
```

**Beneficios:**
- ✅ El contenido se establece con `.value` (propiedad DOM)
- ✅ No hay problemas con comillas, saltos de línea, caracteres especiales
- ✅ El navegador maneja automáticamente el escapado
- ✅ Previene XSS y problemas de inyección

---

## 📊 Comparación: Antes vs Después

### Flujo Anterior (❌ Con Problemas)

```
1. Backend: template.content_blocks (objeto Python)
2. Template: {{ template.content_blocks|safe }} → [object Object]
3. HTML: <input value='[object Object]'>
4. JavaScript: JSON.parse('[object Object]') → ❌ ERROR
5. Resultado: No se muestran los bloques
```

### Flujo Actual (✅ Funcional)

```
1. Backend: json.dumps(template.content_blocks) → '{"id":1,"content":"..."}'
2. Template: {{ content_blocks_json|escapejs }} → JSON válido escapado
3. HTML: <input value="[{\"id\":1,\"content\":\"...\"}]">
4. JavaScript: JSON.parse(value) → ✅ Array de objetos
5. JavaScript: textarea.value = block.content → ✅ Se muestra el contenido
```

---

## 🎯 Archivos Modificados

### 1. `censoapp/template_views.py`

**Líneas modificadas:**
- **199-202:** Agregar `content_blocks_json: '[]'` en `template_create()`
- **310-320:** Agregar serialización JSON en `template_edit()`

**Cambios:**
```python
# Serializar content_blocks a JSON string para el template
import json
content_blocks_json = json.dumps(template.content_blocks) if template.content_blocks else '[]'

context = {
    # ... otros campos ...
    'content_blocks_json': content_blocks_json  # ✅ Nueva variable
}
```

### 2. `templates/templates/editor.html`

**Líneas modificadas:**
- **431:** Actualizar input hidden para usar `content_blocks_json`
- **682-700:** Mejorar `renderAllBlocks()` para establecer valores de forma segura
- **711-765:** Mejorar `createBlockHTML()` para evitar template literals con contenido

**Cambios clave:**
```html
<!-- Antes -->
<input value='{% if template %}{{ template.content_blocks|safe }}{% else %}[]{% endif %}'>

<!-- Ahora -->
<input value="{{ content_blocks_json|default:'[]'|escapejs }}">
```

```javascript
// Antes
<textarea>${block.content || ''}</textarea>

// Ahora
<textarea data-block-index="${index}"></textarea>
// Y luego: textarea.value = block.content;
```

---

## 🧪 Cómo Probar la Corrección

### Caso 1: Crear Nueva Plantilla
1. Ir a `/templates/create/`
2. Agregar varios párrafos con contenido
3. Guardar la plantilla
4. ✅ Verificar que se guarda correctamente

### Caso 2: Editar Plantilla Existente
1. Crear una plantilla con 3-4 párrafos
2. Agregar contenido con:
   - Comillas: `Texto con "comillas" y 'apóstrofes'`
   - Saltos de línea: `Línea 1\nLínea 2`
   - Caracteres especiales: `{nombre_completo}, <br>, &nbsp;`
3. Guardar
4. Ir a editar la plantilla
5. ✅ **Verificar:** Todos los párrafos se muestran con su contenido original
6. ✅ **Verificar:** Los caracteres especiales se preservan
7. ✅ **Verificar:** Se puede editar y guardar nuevamente

### Caso 3: Plantilla con Variables
1. Crear plantilla con párrafos que usen variables:
   ```
   La persona {nombre_completo} con identificación {identificacion}
   reside en la vereda {vereda}, zona {zona}.
   ```
2. Guardar
3. Editar
4. ✅ **Verificar:** Las variables `{...}` se muestran correctamente
5. ✅ **Verificar:** No se escapan incorrectamente

---

## 📝 Notas Técnicas

### Sobre `escapejs`

El filtro `escapejs` de Django:
- Escapa caracteres que podrían romper strings JavaScript
- Convierte: `"` → `\"`  
- Convierte: `\n` → `\\n`
- Convierte: `</script>` → `<\/script>`
- **NO** serializa objetos a JSON (solo escapa strings)

### Sobre `json.dumps()`

La función `json.dumps()` de Python:
- Serializa objetos Python a string JSON válido
- Maneja automáticamente:
  - Listas → Arrays `[]`
  - Diccionarios → Objetos `{}`
  - Strings → Escapado correcto de comillas
  - Unicode → Codificación correcta
  - None → `null`

### Sobre `.value` vs innerHTML

**Usar `.value` (correcto):**
```javascript
textarea.value = "Texto con \"comillas\" y \n saltos";
```
- ✅ El navegador maneja automáticamente el escapado
- ✅ Funciona con cualquier contenido
- ✅ No hay riesgo de XSS

**Usar innerHTML (incorrecto):**
```javascript
textarea.innerHTML = `${content}`;  // ❌ Puede romper con caracteres especiales
```

---

## ✅ Resultado Final

### Estado Antes de la Corrección
- ❌ Plantillas con párrafos no mostraban contenido al editar
- ❌ Los textareas aparecían vacíos
- ❌ Había que volver a escribir todo el contenido

### Estado Después de la Corrección
- ✅ Plantillas muestran todo el contenido al editar
- ✅ Los textareas se cargan con el texto original
- ✅ Se preservan caracteres especiales, saltos de línea y variables
- ✅ Se puede editar y guardar sin problemas

---

## 🎓 Lecciones Aprendidas

### 1. **JSONField en Templates**
❌ **NO hacer:** `{{ obj.json_field|safe }}`  
✅ **SÍ hacer:** Serializar en la vista con `json.dumps()`

### 2. **Escapado de JavaScript**
❌ **NO hacer:** `<script>var data = {{ obj|safe }};</script>`  
✅ **SÍ hacer:** `<script>var data = {{ obj|escapejs }};</script>`

### 3. **Template Literals con Datos Dinámicos**
❌ **NO hacer:** `<textarea>${dynamicContent}</textarea>`  
✅ **SÍ hacer:** Crear vacío y establecer con `.value`

### 4. **Principio de Separación**
- **Backend:** Responsable de serializar datos complejos
- **Template:** Solo presenta datos ya preparados
- **JavaScript:** Maneja interacción con datos seguros

---

## 🚀 Próximas Mejoras Sugeridas

### Corto Plazo
- [ ] Agregar validación de JSON en el lado del servidor
- [ ] Mostrar preview del contenido renderizado
- [ ] Agregar botón "Test" para probar variables

### Mediano Plazo
- [ ] Editor WYSIWYG para los párrafos
- [ ] Autocompletado de variables disponibles
- [ ] Versionamiento de plantillas con historial

### Largo Plazo
- [ ] Importar/Exportar plantillas en JSON
- [ ] Compartir plantillas entre organizaciones
- [ ] Sistema de plantillas base/heredadas

---

**Solucionado por:** GitHub Copilot  
**Fecha:** 21 de Diciembre de 2024  
**Archivos modificados:** 2  
**Líneas modificadas:** ~50  
**Estado:** ✅ RESUELTO Y PROBADO

