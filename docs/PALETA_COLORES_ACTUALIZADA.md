# 🎨 Paleta de Colores Corporativos Actualizada - Censo

## 📋 Resumen de Actualización

Se ha actualizado la paleta de colores corporativos para incluir:
- ✅ **Verde #4CAF50** para botones de guardar/confirmar (éxito)
- ✅ **Amarillo #FFC107** para advertencias
- ✅ **Azul #2196F3** como color principal (información)

---

## 🎨 Paleta de Colores Completa

### 1. Azul (Principal) - Información y Navegación

| Variante | Código | Uso |
|----------|--------|-----|
| **Primary** | `#2196F3` | Botones primarios, links, tabs activos |
| **Primary Dark** | `#1976D2` | Hover de botones primarios |
| **Primary Light** | `#42A5F5` | Variantes y decoraciones |
| **Primary Lighter** | `#E3F2FD` | Backgrounds sutiles, hover tablas |

**Variable CSS:** `var(--color-primary)`

### 2. Verde (Éxito) - Guardar y Confirmaciones

| Variante | Código | Uso |
|----------|--------|-----|
| **Success** | `#4CAF50` | Botones de guardar, confirmaciones, badges de jefe |
| **Success Dark** | `#388E3C` | Hover de botones verdes |
| **Success Light** | `#66BB6A` | Variantes |
| **Success Lighter** | `#C8E6C9` | Backgrounds de alertas success |

**Variable CSS:** `var(--color-success)`

### 3. Amarillo (Advertencia) - Alertas y Avisos

| Variante | Código | Uso |
|----------|--------|-----|
| **Warning** | `#FFC107` | Botones de advertencia, badges de pendiente |
| **Warning Dark** | `#FFA000` | Hover de botones amarillos |
| **Warning Lighter** | `#FFF9C4` | Backgrounds de alertas warning |

**Variable CSS:** `var(--color-warning)`

### 4. Rojo (Peligro) - Errores y Eliminaciones

| Variante | Código | Uso |
|----------|--------|-----|
| **Danger** | `#EF4444` | Botones de eliminar, alertas de error |

**Variable CSS:** `var(--color-danger)`

### 5. Grises Corporativos

| Variante | Código | Uso |
|----------|--------|-----|
| **Gray 50** | `#F9FAFB` | Fondos muy claros |
| **Gray 100** | `#F3F4F6` | Fondos claros |
| **Gray 200** | `#E5E7EB` | Bordes |
| **Gray 500** | `#6B7280` | Texto secundario |
| **Gray 700** | `#374151` | Texto principal |
| **Gray 900** | `#111827` | Texto oscuro |

---

## 🎯 Uso de Colores por Contexto

### Botones

#### Azul - Acciones Informativas
```html
<button class="btn btn-primary">Ver Detalle</button>
<button class="btn btn-outline-primary">Ver Más</button>
```
**Uso:** Ver, consultar, navegar, información

#### Verde - Acciones de Confirmación
```html
<button class="btn btn-success">Guardar</button>
<button class="btn btn-save">Guardar Cambios</button>
<button class="btn btn-outline-success">Confirmar</button>
```
**Uso:** Guardar, confirmar, aceptar, crear exitosamente

#### Amarillo - Advertencias
```html
<button class="btn btn-warning">Advertencia</button>
<button class="btn btn-outline-warning">Revisar</button>
```
**Uso:** Advertir, revisar, pendiente, atención requerida

#### Rojo - Acciones Destructivas
```html
<button class="btn btn-danger">Eliminar</button>
<button class="btn btn-outline-danger">Cancelar</button>
```
**Uso:** Eliminar, cancelar, rechazar

---

### Badges

#### Azul - Información Principal
```html
<span class="badge badge-primary">#123</span>
<span class="badge badge-ficha">#456</span>
```
**Uso:** Números de ficha, identificadores, información general

#### Verde - Estados Positivos
```html
<span class="badge badge-success">Activo</span>
<span class="badge badge-family-head">👑 Jefe</span>
```
**Uso:** Jefe de familia, activo, completado, registrado

#### Amarillo - Estados de Advertencia
```html
<span class="badge badge-warning">Pendiente</span>
<span class="badge badge-warning">Revisar</span>
```
**Uso:** Pendiente, incompleto, requiere atención

#### Rojo - Estados Negativos
```html
<span class="badge badge-danger">Inactivo</span>
<span class="badge badge-danger">Error</span>
```
**Uso:** Inactivo, error, eliminado

---

### Alertas

#### Verde - Éxito
```html
<div class="alert alert-success">
    <i class="fas fa-check-circle"></i>
    Ficha guardada correctamente
</div>
```
**Fondo:** `#C8E6C9` (verde muy claro)  
**Borde:** `#4CAF50` (verde)  
**Texto:** `#388E3C` (verde oscuro)

#### Azul - Información
```html
<div class="alert alert-info">
    <i class="fas fa-info-circle"></i>
    Información importante
</div>
```
**Fondo:** `#E3F2FD` (azul muy claro)  
**Borde:** `#2196F3` (azul)  
**Texto:** `#1976D2` (azul oscuro)

#### Amarillo - Advertencia
```html
<div class="alert alert-warning">
    <i class="fas fa-exclamation-triangle"></i>
    Por favor revise los datos
</div>
```
**Fondo:** `#FFF9C4` (amarillo muy claro)  
**Borde:** `#FFC107` (amarillo)  
**Texto:** `#F57F17` (amarillo oscuro)

#### Rojo - Error
```html
<div class="alert alert-danger">
    <i class="fas fa-times-circle"></i>
    Error al guardar
</div>
```
**Fondo:** `#FFEBEE` (rojo muy claro)  
**Borde:** `#EF4444` (rojo)  
**Texto:** `#C62828` (rojo oscuro)

---

## 📊 Ejemplos Visuales

### Paleta Completa
```
┌──────────────────────────────────────────────────┐
│ AZUL (Primary)    - #2196F3  ███████████         │
│ Información, navegación, principal               │
├──────────────────────────────────────────────────┤
│ VERDE (Success)   - #4CAF50  ███████████         │
│ Guardar, confirmar, éxito                        │
├──────────────────────────────────────────────────┤
│ AMARILLO (Warning)- #FFC107  ███████████         │
│ Advertencias, pendiente                          │
├──────────────────────────────────────────────────┤
│ ROJO (Danger)     - #EF4444  ███████████         │
│ Errores, eliminar                                │
└──────────────────────────────────────────────────┘
```

### Botones en Formularios
```
┌─────────────────────────────────────┐
│ Editar Ficha Familiar               │
├─────────────────────────────────────┤
│ [Campos del formulario...]          │
│                                     │
│ [◀ Volver]  [✓ Guardar Cambios]   │
│  Gris        Verde #4CAF50          │
└─────────────────────────────────────┘
```

### Estados con Badges
```
Ficha #123  [👑 Jefe]    [✓ Registrado]  [⚠ Pendiente]
            Verde         Verde            Amarillo
```

---

## 🎯 Guía de Decisión Rápida

### ¿Qué color usar?

| Acción | Color | Clase |
|--------|-------|-------|
| **Ver/Consultar** | Azul | `.btn-primary` |
| **Guardar/Crear** | Verde | `.btn-success` o `.btn-save` |
| **Editar** | Azul | `.btn-primary` |
| **Advertir** | Amarillo | `.btn-warning` |
| **Eliminar** | Rojo | `.btn-danger` |
| **Cancelar** | Gris | `.btn-secondary` |
| **Volver** | Gris | `.btn-outline-secondary` |

### Estados

| Estado | Color | Clase |
|--------|-------|-------|
| **Activo/Registrado** | Verde | `.badge-success` |
| **Pendiente** | Amarillo | `.badge-warning` |
| **Inactivo** | Rojo | `.badge-danger` |
| **Info General** | Azul | `.badge-primary` |

---

## 💡 Mejores Prácticas

### 1. Botones de Acción
```html
<!-- ✅ CORRECTO -->
<button class="btn btn-success">Guardar</button>
<button class="btn btn-primary">Ver Detalle</button>
<button class="btn btn-secondary">Cancelar</button>

<!-- ❌ INCORRECTO -->
<button class="btn btn-primary">Guardar</button>  <!-- Debería ser verde -->
<button class="btn btn-warning">Ver</button>      <!-- Debería ser azul -->
```

### 2. Jerarquía Visual
```html
<!-- Acción principal (verde) más prominente -->
<div class="d-flex justify-content-between">
    <button class="btn btn-outline-secondary">Volver</button>
    <button class="btn btn-save">Guardar Cambios</button>
</div>
```

### 3. Consistencia en Badges
```html
<!-- Usar siempre el mismo color para el mismo estado -->
<span class="badge badge-success">Registrado</span>
<span class="badge badge-warning">Pendiente</span>
<span class="badge badge-danger">Inactivo</span>
```

---

## 🔄 Comparación: Antes vs Después

### Antes
```
Botón Guardar: Azul #2196F3
Advertencia: Naranja #FFA726
```

### Después
```
Botón Guardar: Verde #4CAF50 ✅
Advertencia: Amarillo #FFC107 ✅
```

**Beneficios:**
- ✅ Verde más visible y reconocible para "guardar"
- ✅ Amarillo más claro y apropiado para advertencias
- ✅ Mejor contraste y legibilidad
- ✅ Paleta más armoniosa

---

## 📁 Implementación

### Archivos Actualizados

```
✅ static/assets/css/censo-corporate.css
   └── Paleta completa actualizada con verde y amarillo

✅ templates/censo/censo/edit-family-card.html
   └── Botón .btn-save actualizado a verde
```

### Aplicación Automática

Los nuevos colores se aplican automáticamente a:
- ✅ Todos los `<button class="btn btn-success">`
- ✅ Todos los `<button class="btn btn-save">`
- ✅ Todos los `<span class="badge badge-success">`
- ✅ Todos los `<div class="alert alert-success">`
- ✅ Todos los `<button class="btn btn-warning">`
- ✅ Todos los `<span class="badge badge-warning">`

---

## ✅ Resultado Final

### Paleta Corporativa Censo

```css
/* Principal */
--color-primary: #2196F3;      /* Azul Material */

/* Éxito */
--color-success: #4CAF50;      /* Verde Material */

/* Advertencia */
--color-warning: #FFC107;      /* Amarillo Amber */

/* Peligro */
--color-danger: #EF4444;       /* Rojo */
```

**Imagen:** 🏢 Profesional, Moderna, Armoniosa

---

**Versión:** 4.0 - Paleta Actualizada  
**Fecha:** 2025-12-12  
**Estado:** ✅ Aplicado Globalmente

