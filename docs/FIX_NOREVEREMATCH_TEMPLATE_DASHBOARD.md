# Fix: NoReverseMatch 'template-dashboard' not found

**Fecha:** 21 de Diciembre de 2024  
**Error:** `NoReverseMatch at /documentos/estadisticas/ Reverse for 'template-dashboard' not found`  
**Ubicación:** `templates/includes/sidebar.html` línea 130  
**Solución:** Eliminada referencia al sistema de plantillas obsoleto del sidebar  

---

## 🐛 Problema

Después de eliminar el sistema de plantillas antiguo, el sidebar aún tenía un enlace a:

```html
<a href="{% url 'template-dashboard' %}">
    <span class="nav-link-text ms-1">Plantillas</span>
</a>
```

Esto causaba el error `NoReverseMatch` porque la URL `template-dashboard` ya no existe.

---

## ✅ Solución Aplicada

### Eliminada Sección Completa de Plantillas del Sidebar

**Archivo:** `templates/includes/sidebar.html`

**Código eliminado (líneas 124-151):**
```html
<li class="nav-item mt-3">
    <h6 class="ps-4 ms-2 text-uppercase text-xs font-weight-bolder opacity-6">Configuración</h6>
</li>
<li class="nav-item">
    <a class="nav-link {% if 'templates' in segment %} active {% endif %}"
       href="{% url 'template-dashboard' %}">
        <div class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center me-2 d-flex align-items-center justify-content-center">
            <svg>...</svg>
        </div>
        <span class="nav-link-text ms-1">Plantillas</span>
    </a>
</li>
```

**Resultado:** Ahora el sidebar solo muestra las secciones activas del sistema.

---

## 🔍 Verificación Realizada

### Búsqueda de Referencias Restantes

```bash
# Búsqueda en templates HTML
grep -r "template-dashboard" templates/
# Resultado: 0 resultados ✅

# Búsqueda en Python
grep -r "template-dashboard" censoapp/
# Resultado: 0 resultados ✅

# Búsqueda de otras URLs de plantillas
grep -r "template-" templates/
# Resultado: Solo CSS (grid-template-columns) ✅
```

---

## 📋 Sidebar Actualizado

### Estructura Actual del Menú

```
┌─────────────────────────────┐
│ MENÚ DE NAVEGACIÓN          │
├─────────────────────────────┤
│                             │
│ 📊 Dashboard                │
│ 🏛️ Gestión de fichas        │
│   - Asociación              │
│   - Fichas Familiares       │
│                             │
│ 👥 Personas                 │
│   - Listado Personas        │
│                             │
│ 📁 Documentos (superuser)   │
│   - Estadísticas            │
│                             │
└─────────────────────────────┘

❌ ELIMINADO: Configuración → Plantillas
```

### Solo para Superusuarios

```html
{% if user.is_superuser %}
<li class="nav-item mt-3">
    <h6>Documentos</h6>
</li>
<li class="nav-item">
    <a href="{% url 'documents-stats' %}">
        <span>Estadísticas</span>
    </a>
</li>
{% endif %}
```

---

## ✅ Estado Final

**Error original:**
```
NoReverseMatch at /documentos/estadisticas/
Reverse for 'template-dashboard' not found.
'template-dashboard' is not a valid view function or pattern name.
```

**Estado actual:**
- ✅ Error resuelto
- ✅ Sidebar limpio
- ✅ Sin referencias a sistema obsoleto
- ✅ Navegación funcional

---

## 🧪 Cómo Verificar

### 1. Acceder a Estadísticas de Documentos

```
http://127.0.0.1:8000/documentos/estadisticas/
```

**Antes:** ❌ Error `NoReverseMatch`  
**Ahora:** ✅ Página carga correctamente

### 2. Verificar Sidebar

```
1. Login como superusuario
2. Ir a cualquier página
3. Verificar sidebar:
   ✅ Dashboard
   ✅ Fichas Familiares
   ✅ Personas
   ✅ Documentos → Estadísticas
   ❌ NO aparece "Plantillas"
```

### 3. Verificar Usuarios Normales

```
1. Login como usuario normal
2. Verificar sidebar:
   ✅ Dashboard
   ✅ Fichas Familiares
   ✅ Personas
   ❌ NO aparece sección "Documentos"
   ❌ NO aparece "Plantillas"
```

---

## 📊 Referencias Eliminadas

### Completas
- ✅ `template-dashboard` - Dashboard de plantillas
- ✅ `template-create` - Crear plantilla
- ✅ `template-edit` - Editar plantilla
- ✅ `template-duplicate` - Duplicar plantilla
- ✅ `template-delete` - Eliminar plantilla
- ✅ `template-toggle-active` - Activar/desactivar
- ✅ `template-set-default` - Establecer por defecto
- ✅ `variable-manager` - Gestor de variables
- ✅ `variable-create` - Crear variable
- ✅ `variable-update` - Actualizar variable
- ✅ `variable-delete` - Eliminar variable
- ✅ `available-variables` - Variables disponibles
- ✅ `model-fields` - Campos del modelo

### URLs que SÍ Existen (Sistema Nuevo)
- ✅ `select-document-type` - Seleccionar tipo de documento
- ✅ `generate-aval-general` - Generar Aval General
- ✅ `generate-aval-estudio` - Generar Aval de Estudio
- ✅ `generate-constancia` - Generar Constancia
- ✅ `view-document` - Ver documento
- ✅ `documents-stats` - Estadísticas de documentos
- ✅ `verify-document` - Verificar documento con QR

---

## 🎯 Archivos Modificados

### 1. `templates/includes/sidebar.html`

**Líneas eliminadas:** 124-151 (28 líneas)

**Cambio:** Eliminada toda la sección "Configuración → Plantillas"

**Estado:**
- ✅ Sin errores
- ✅ Sin referencias obsoletas
- ✅ Navegación limpia

---

## 📝 Notas

### Por qué Ocurrió el Error

Cuando eliminamos el sistema de plantillas:
1. ❌ Eliminamos `censoapp/template_views.py`
2. ❌ Eliminamos las URLs en `urls.py`
3. ⚠️ **NO actualizamos el sidebar** (causó el error)

Django intentaba generar la URL `{% url 'template-dashboard' %}` pero ya no existía la vista ni la URL.

### Cómo Se Resolvió

1. ✅ Identificamos la referencia en `sidebar.html` línea 130
2. ✅ Eliminamos toda la sección de "Plantillas"
3. ✅ Verificamos que no hubiera más referencias
4. ✅ Reiniciamos el servidor

### Prevención Futura

Cuando se eliminen funcionalidades:
- ✅ Eliminar vistas (`.py`)
- ✅ Eliminar URLs (`urls.py`)
- ✅ Eliminar templates (`.html`)
- ✅ **Actualizar sidebar y navegación** ← Importante
- ✅ Buscar referencias en todo el proyecto

---

## ✅ Verificación Final

**Comando ejecutado:**
```bash
grep -r "template-dashboard\|template-create\|template-edit\|variable-manager" .
```

**Resultado:**
```
# 0 resultados en archivos activos ✅
# Solo en documentación y archivos eliminados
```

**Servidor:**
```bash
python manage.py runserver
# Iniciando servidor de desarrollo en http://127.0.0.1:8000/
# ✅ Sin errores
```

**Prueba de navegación:**
```
✅ http://127.0.0.1:8000/
✅ http://127.0.0.1:8000/documentos/estadisticas/
✅ http://127.0.0.1:8000/personas
✅ http://127.0.0.1:8000/familyCard/index
```

---

**Resuelto por:** GitHub Copilot  
**Fecha:** 21 de Diciembre de 2024  
**Tiempo de solución:** Inmediato  
**Estado:** ✅ COMPLETAMENTE RESUELTO  
**Archivos modificados:** 1 (`sidebar.html`)  
**Líneas eliminadas:** 28

