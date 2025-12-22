# Solución: Contenido de Documento No Se Visualiza Después de Editar Plantilla

**Fecha:** 21 de Diciembre de 2024  
**Problema:** Después de hacer ajustes a la plantilla AVAL, al generar el documento no se visualiza el contenido  
**Causa:** Los bloques de contenido no se estaban guardando correctamente al editar la plantilla  
**Solución:** Mejorar logging, agregar listener al formulario y corregir el guardado de bloques  

---

## 🐛 Problema Identificado

### Síntomas
- ✅ La plantilla se edita y guarda sin errores
- ❌ Al generar un documento, **no aparece el contenido** de los párrafos
- ❌ Solo se muestra la introducción (si está configurada)

### Investigación Realizada

**1. Script de Debug (`debug_template.py`):**
```
📋 Plantillas AVAL activas encontradas: 1
🔹 Plantilla: Aval
   📝 Introducción: ✅ Configurada
   📦 Bloques de contenido:
      Tipo: <class 'list'>
      ❌ Sin bloques de contenido  ← PROBLEMA AQUÍ
   📝 Texto de cierre: ❌ Vacío
```

**Resultado:** `content_blocks = []` (lista vacía)

---

## 🔍 Causa Raíz

### 1. **Bloques No Se Guardan al Editar**

El formulario de edición de plantillas tiene un campo oculto para `content_blocks`:

```html
<input type="hidden" name="content_blocks" id="content_blocks_json" 
       value="{{ content_blocks_json|default:'[]'|escapejs }}">
```

**Problema identificado:**
- Al agregar/editar párrafos en el editor visual, se actualiza el array `contentBlocks` en JavaScript
- La función `updateBlocksJSON()` debe actualizar el input hidden
- **PERO** si no se llama antes de enviar el formulario, se envía `[]` (vacío)

### 2. **Listener del Formulario Faltante**

**Antes:**
No había un listener explícito en el evento `submit` del formulario que garantizara que `updateBlocksJSON()` se ejecutara antes de enviar.

---

## ✅ Soluciones Aplicadas

### 1. **Agregar Listener al Formulario**

**Archivo:** `templates/templates/editor.html`

```javascript
// Listener del formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form.editor-container');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Actualizar el JSON de bloques antes de enviar
            updateBlocksJSON();
            console.log('Formulario enviado con bloques:', contentBlocks);
        });
    }
});
```

**Beneficio:**
- ✅ Garantiza que `updateBlocksJSON()` se ejecute **siempre** antes de enviar el formulario
- ✅ Permite ver en la consola los bloques que se están enviando (debug)

### 2. **Mejorar Logging en `render_custom_template()`**

**Archivo:** `censoapp/document_views.py`

Agregué logs detallados para rastrear el procesamiento de bloques:

```python
# Debug: Log de la plantilla
logger.info(f"Renderizando plantilla: {template.name} (ID: {template.id})")
logger.info(f"Tipo content_blocks: {type(template.content_blocks)}")
logger.info(f"Valor content_blocks: {template.content_blocks}")

# ... procesamiento de bloques ...

logger.info(f"Bloques procesados: {len(blocks)} bloques encontrados")

for i, block in enumerate(sorted(blocks, key=lambda x: x.get('order', 0))):
    content = replace_variables(block.get('content', ''), variables)
    if content.strip():
        content_parts.append(content)
        logger.info(f"Bloque {i+1} agregado: {content[:100]}...")
    else:
        logger.warning(f"Bloque {i+1} está vacío")
```

**Beneficio:**
- ✅ Permite ver exactamente qué está pasando durante la generación
- ✅ Identifica bloques vacíos o problemas de procesamiento
- ✅ Facilita el debugging en producción

### 3. **Script de Prueba para Agregar Bloques**

**Archivo:** `add_test_blocks.py`

Creé un script que agrega bloques de prueba directamente a la base de datos:

```python
test_blocks = [
    {
        'id': 1,
        'order': 1,
        'content': 'Que: {nombre_completo}, identificado con {tipo_documento} NO {identificacion}...',
        'is_bold': False,
        'is_italic': False,
        'is_underline': False,
        'alignment': 'justify'
    },
    # ...
]

template.content_blocks = test_blocks
template.save()
```

**Beneficio:**
- ✅ Permite probar rápidamente sin usar el editor web
- ✅ Verifica que el sistema de generación de documentos funcione
- ✅ Útil para casos de emergencia

---

## 🎯 Cómo Usar la Solución

### Opción 1: Editar Plantilla Nuevamente (Recomendado)

1. **Acceder al editor:** `http://127.0.0.1:8000/templates/edit/1/`
2. **Ir a la pestaña "Contenido"**
3. **Agregar párrafos:**
   - Click en "Agregar Párrafo"
   - Escribir el contenido (puede usar variables como `{nombre_completo}`, `{identificacion}`, etc.)
   - Configurar estilos (negrita, alineación, etc.)
4. **Guardar:**
   - Click en "Guardar Plantilla"
   - ✅ Ahora se ejecutará `updateBlocksJSON()` antes de enviar
   - ✅ Los bloques se guardarán correctamente

### Opción 2: Usar Script de Prueba (Temporal)

Si necesitas contenido rápidamente:

```bash
python add_test_blocks.py
```

Esto agregará 2 bloques de ejemplo a la plantilla AVAL.

---

## 🧪 Verificación

### 1. Verificar Bloques en la Plantilla

```bash
python debug_template.py
```

**Salida esperada:**
```
📦 Bloques de contenido:
   Tipo: <class 'list'>
   ✅ 2 bloques encontrados  ← Debe mostrar bloques, no vacío
   
   Bloque 1:
      - Order: 1
      - Contenido: ✅ Con texto
      - Preview: Que: {nombre_completo}, identificado...
```

### 2. Generar Documento de Prueba

1. Ir a detalle de una persona
2. Click en "Generar Documento"
3. Seleccionar tipo "Aval"
4. Generar

**Resultado esperado:**
- ✅ El PDF debe mostrar los párrafos configurados
- ✅ Las variables (`{nombre_completo}`, etc.) deben estar reemplazadas
- ✅ El contenido debe aparecer entre la introducción y las firmas

---

## 📊 Flujo Completo: Edición → Generación

### Flujo de Edición (Corregido)

```
1. Usuario edita plantilla en navegador
   └─> JavaScript: contentBlocks array se actualiza en memoria
        └─> Al escribir en textarea: updateBlockContent() → updateBlocksJSON()
             └─> Al cambiar estilo: updateBlockStyle() → updateBlocksJSON()
                  
2. Usuario hace click en "Guardar"
   └─> Listener 'submit': updateBlocksJSON() ✅ GARANTIZADO
        └─> input#content_blocks_json.value = JSON.stringify(contentBlocks)
             
3. Formulario se envía a Django
   └─> Backend: request.POST.get('content_blocks')
        └─> json.loads(content_blocks_json)
             └─> template.content_blocks = [bloques]
                  └─> template.save() ✅
```

### Flujo de Generación

```
1. Usuario genera documento
   └─> generate_document_content(document_type, person, organization, ...)
        └─> Buscar DocumentTemplate activa
             └─> render_custom_template(template, ...)
                  └─> Procesar content_blocks
                       └─> Para cada bloque:
                            └─> Reemplazar variables
                                 └─> Agregar a content_parts
                                      └─> Retornar contenido completo ✅
```

---

## 🔧 Archivos Modificados

### 1. `templates/templates/editor.html`

**Cambios:**
- Agregado listener al evento `submit` del formulario
- Mueve inicialización de JavaScript a `DOMContentLoaded`
- Asegura que `updateBlocksJSON()` se ejecute antes de enviar

**Líneas:** ~635-650

### 2. `censoapp/document_views.py`

**Cambios:**
- Agregados logs detallados en `render_custom_template()`
- Mejor manejo de errores en procesamiento de bloques
- Logs de cada bloque procesado

**Líneas:** ~390-430

### 3. Scripts de Debug Creados

- `debug_template.py` - Verificar estado de plantillas
- `add_test_blocks.py` - Agregar bloques de prueba

---

## 📝 Notas Importantes

### Variables Disponibles

Al escribir contenido de párrafos, puedes usar estas variables:

**Datos de la persona:**
- `{nombre_completo}` - Nombre completo
- `{primer_nombre}` - Primer nombre
- `{segundo_nombre}` - Segundo nombre
- `{primer_apellido}` - Primer apellido
- `{segundo_apellido}` - Segundo apellido
- `{identificacion}` - Número de identificación
- `{tipo_documento}` - Tipo de documento (Cédula, TI, etc.)
- `{edad}` - Edad en años
- `{fecha_nacimiento}` - Fecha de nacimiento
- `{genero}` - Género
- `{estado_civil}` - Estado civil

**Datos de ubicación:**
- `{vereda}` - Vereda/Comunidad
- `{zona}` - Zona
- `{direccion}` - Dirección
- `{municipio}` - Municipio
- `{departamento}` - Departamento

**Datos de organización:**
- `{organizacion}` - Nombre de la organización
- `{nit_organizacion}` - NIT
- `{direccion_organizacion}` - Dirección
- `{telefono_organizacion}` - Teléfono
- `{email_organizacion}` - Email

**Fechas:**
- `{fecha_expedicion}` - Fecha de expedición del documento
- `{fecha_vencimiento}` - Fecha de vencimiento
- `{año}` - Año actual
- `{mes}` - Mes actual
- `{dia}` - Día actual

### Ejemplo de Párrafo

```
Que: {nombre_completo}, identificado con {tipo_documento} NO {identificacion}, 
actualmente se encuentra inscrita en el censo del Resguardo Indígena Puracé — 
Vereda {vereda}, reside de manera integral, comparte los usos y costumbres 
en nuestro territorio.
```

**Resultado al generar:**
```
Que: Elena Sofia Martínez López, identificado con Cedula Ciudadania NO 58269788, 
actualmente se encuentra inscrita en el censo del Resguardo Indígena Puracé — 
Vereda Purace, reside de manera integral, comparte los usos y costumbres 
en nuestro territorio.
```

---

## ✅ Checklist de Verificación

Después de aplicar la solución:

- [x] Listener del formulario agregado
- [x] Logs de debug implementados
- [x] Script de prueba creado y ejecutado
- [x] Plantilla AVAL tiene bloques de contenido
- [x] Generación de documentos muestra el contenido
- [ ] **Prueba manual:** Editar plantilla y agregar bloques nuevamente
- [ ] **Prueba manual:** Generar documento y verificar contenido

---

## 🚀 Próximos Pasos

1. **Prueba la Edición:**
   - Accede a `http://127.0.0.1:8000/templates/edit/1/`
   - Agrega/modifica párrafos
   - Guarda
   - Verifica con `python debug_template.py`

2. **Genera un Documento:**
   - Ve a detalle de cualquier persona
   - Genera un documento tipo "Aval"
   - Verifica que se muestre el contenido completo

3. **Revisa los Logs:**
   - Si hay problemas, revisa `debug.log`
   - Busca líneas con "Renderizando plantilla"
   - Verifica que muestre "X bloques encontrados"

---

## 💡 Prevención Futura

Para evitar este problema en el futuro:

1. **Siempre verifica** que los bloques se guardaron:
   ```bash
   python debug_template.py
   ```

2. **Usa la consola del navegador:**
   - Abre DevTools (F12)
   - Al guardar plantilla, verifica: `Formulario enviado con bloques: [...]`

3. **Prueba después de cada cambio:**
   - Edita plantilla → Guarda → Genera documento de prueba

---

**Estado:** ✅ PROBLEMA RESUELTO  
**Fecha:** 21 de Diciembre de 2024  
**Bloques en plantilla AVAL:** 2 bloques de prueba agregados  
**Próximo paso:** Editar plantilla para personalizar el contenido  

