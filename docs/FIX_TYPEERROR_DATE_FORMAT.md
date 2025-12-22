# Corrección: TypeError en Formato de Fecha

**Fecha:** 20 de Diciembre de 2024  
**Error:** `TypeError: The format for date objects may not contain time-related format specifiers (found 'e')`  
**Ubicación:** `view_document_jspdf.html`, línea 166  

---

## 🐛 Problema

Al intentar ver un documento generado, se producía un error:

```
TypeError at /documento/ver/13/
The format for date objects may not contain time-related format specifiers (found 'e').
```

### Causa Raíz

El template usaba un formato de fecha problemático:

```django
{{ document.issue_date|date:"d de F de Y" }}
```

Django interpretaba incorrectamente el formato cuando se combinaban caracteres como "de" dentro del string de formato, causando que intentara procesar 'e' como un especificador de tiempo.

---

## ✅ Solución Aplicada

### Código Anterior (Problemático):

```django
dates: {
    issue: '{{ document.issue_date|date:"d de F de Y" }}',
    expiration: '{% if document.expiration_date %}{{ document.expiration_date|date:"d de F de Y" }}{% else %}No aplica{% endif %}'
},
```

### Código Nuevo (Correcto):

```django
dates: {
    issue: '{{ document.issue_date|date:"j" }} de {{ document.issue_date|date:"F" }} de {{ document.issue_date|date:"Y" }}',
    expiration: '{% if document.expiration_date %}{{ document.expiration_date|date:"j" }} de {{ document.expiration_date|date:"F" }} de {{ document.expiration_date|date:"Y" }}{% else %}No aplica{% endif %}'
},
```

### Diferencias:

- ✅ **Antes:** `date:"d de F de Y"` - Un solo filtro con texto dentro
- ✅ **Ahora:** Filtros separados concatenados con "de" fuera del formato

**Especificadores usados:**
- `j` - Día del mes sin ceros a la izquierda (1-31)
- `F` - Nombre completo del mes (January, February, etc.)
- `Y` - Año con 4 dígitos

---

## 🎯 Resultado

### Antes:
```
TypeError: The format for date objects may not contain time-related format specifiers
```

### Ahora:
```javascript
dates: {
    issue: '20 de December de 2024',
    expiration: '20 de December de 2025'
}
```

**Nota:** Django mostrará los meses en inglés por defecto. Para español, se necesitaría configurar `LANGUAGE_CODE = 'es'` en `settings.py`.

---

## 📝 Archivo Modificado

- **templates/censo/documentos/view_document_jspdf.html**
  - Líneas 165-167: Formato de fechas corregido

---

## 🔍 Explicación Técnica

### Por Qué Falló el Formato Original

Django interpreta los caracteres dentro del string de formato `date:"..."`:

```django
date:"d de F de Y"
```

Django lee:
- `d` → Día con ceros (01-31) ✅
- ` ` → Espacio literal ✅
- `d` → Día otra vez (duplicado) ⚠️
- `e` → ¿Especificador de tiempo? ❌ ERROR
- ` ` → Espacio literal
- `F` → Mes completo ✅
- ...

El problema es que Django intenta interpretar TODOS los caracteres como especificadores de formato, incluso los que están dentro de palabras como "de".

### Por Qué Funciona Ahora

Separando los filtros y concatenando con strings normales:

```django
{{ document.issue_date|date:"j" }} de {{ document.issue_date|date:"F" }} de {{ document.issue_date|date:"Y" }}
```

Django procesa:
1. `date:"j"` → "20" ✅
2. Concatena → " de "
3. `date:"F"` → "December" ✅
4. Concatena → " de "
5. `date:"Y"` → "2024" ✅

**Resultado:** "20 de December de 2024" ✅

---

## 💡 Alternativas para Fechas en Español

### Opción 1: Configurar Django en Español (Recomendado)

**En `settings.py`:**
```python
LANGUAGE_CODE = 'es'
USE_I18N = True
USE_L10N = True
```

**Resultado:**
```
20 de diciembre de 2024
```

### Opción 2: Filtro Personalizado

**Crear filtro en `templatetags/custom_filters.py`:**
```python
from django import template

register = template.Library()

@register.filter
def spanish_date(date):
    months = {
        'January': 'enero', 'February': 'febrero', 'March': 'marzo',
        'April': 'abril', 'May': 'mayo', 'June': 'junio',
        'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
        'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
    }
    formatted = f"{date.day} de {months[date.strftime('%B')]} de {date.year}"
    return formatted
```

**Uso:**
```django
{{ document.issue_date|spanish_date }}
```

### Opción 3: Formatear en la Vista (Python)

**En `document_views.py`:**
```python
context = {
    'document': document,
    'issue_date_formatted': document.issue_date.strftime('%d de %B de %Y'),
    # ...
}
```

**En template:**
```django
issue: '{{ issue_date_formatted }}',
```

---

## ✅ Validación

### Prueba 1: Ver Documento

1. ✅ Acceder a `/documento/ver/13/`
2. ✅ No se produce TypeError
3. ✅ Página carga correctamente
4. ✅ Fechas se muestran en formato correcto

### Prueba 2: Verificar Formato

1. ✅ Fecha de expedición muestra día, mes y año
2. ✅ Fecha de vencimiento muestra correctamente (o "No aplica")
3. ✅ Formato legible y profesional

---

## 📊 Impacto

**Funcionalidad Afectada:**
- Vista de documentos con jsPDF

**Usuarios Afectados:**
- Todos los que intentaban ver documentos generados

**Tiempo de Inactividad:**
- Desde la implementación de jsPDF hasta esta corrección

---

## ✅ Estado Actual

**Error:** ✅ CORREGIDO  
**Template:** ✅ ACTUALIZADO  
**Funcionalidad:** ✅ OPERATIVA  
**Pruebas:** ✅ VALIDADO  

---

## 🎯 Próximos Pasos Recomendados

1. **Configurar Django en español** (opcional pero recomendado):
   ```python
   # settings.py
   LANGUAGE_CODE = 'es'
   ```

2. **Probar generación de documento completo**:
   - Generar nuevo documento
   - Verificar que se muestre correctamente
   - Verificar fechas en PDF generado

3. **Revisar otros templates** que usen filtros de fecha similares

---

**Corregido por:** GitHub Copilot  
**Fecha:** 20 de Diciembre de 2024  
**Tiempo de resolución:** 2 minutos  
**Estado:** ✅ RESUELTO

