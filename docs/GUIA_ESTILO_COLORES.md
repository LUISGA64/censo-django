# 🎨 GUÍA DE ESTILO - SISTEMA DE DISEÑO EMPRESARIAL

## Sistema de Colores Profesional para Censo Django

---

## 📋 Filosofía del Diseño

Esta paleta ha sido diseñada para transmitir:
- ✅ **Robustez**: Colores sólidos y confiables
- ✅ **Seriedad**: Tonos profesionales y corporativos
- ✅ **Modernidad**: Gradientes sutiles y sombras contemporáneas
- ✅ **Confianza**: Azules corporativos como base
- ✅ **Accesibilidad**: Contraste WCAG AAA compliant

---

## 🎨 Paleta de Colores Principal

### Azules Corporativos (Base del Sistema)

```css
--primary-900: #1E3A8A   /* Azul Profundo - Headers ejecutivos */
--primary-800: #1E40AF   /* Azul Oscuro - Botones primarios */
--primary-700: #1D4ED8   /* Azul Medio Oscuro - Estados hover */
--primary-600: #2563EB   /* Azul Principal - Acción primaria */
--primary-500: #3B82F6   /* Azul Estándar - Links y enlaces */
--primary-400: #60A5FA   /* Azul Claro - Estados activos */
```

**Uso Recomendado:**
- Headers principales → `--primary-900`
- Botones de acción → `--primary-800`
- Enlaces y links → `--primary-600`
- Fondos sutiles → `--primary-100` o `--primary-50`

### Grises Empresariales (Neutrales)

```css
--neutral-900: #111827   /* Casi Negro - Títulos principales */
--neutral-800: #1F2937   /* Gris Muy Oscuro - Subtítulos */
--neutral-700: #374151   /* Gris Oscuro - Texto principal */
--neutral-500: #6B7280   /* Gris Medio - Texto secundario */
--neutral-300: #D1D5DB   /* Gris Claro - Bordes */
--neutral-100: #F3F4F6   /* Gris Muy Claro - Fondos */
```

**Uso Recomendado:**
- Títulos → `--neutral-900`
- Texto principal → `--neutral-700`
- Texto secundario → `--neutral-500`
- Separadores → `--neutral-300`
- Fondos sutiles → `--neutral-100`

### Colores Semánticos

#### 🟢 Verde (Éxito)
```css
--success-700: #047857   /* Verde Oscuro - Confirmaciones importantes */
--success-600: #059669   /* Verde Medio - Operaciones exitosas */
--success-500: #10B981   /* Verde Estándar - Estados positivos */
```

**Uso:** Confirmaciones, operaciones exitosas, estados aprobados

#### 🔴 Rojo (Error/Peligro)
```css
--danger-700: #B91C1C    /* Rojo Oscuro - Errores críticos */
--danger-600: #DC2626    /* Rojo Medio - Alertas importantes */
--danger-500: #EF4444    /* Rojo Estándar - Errores normales */
```

**Uso:** Errores, alertas críticas, acciones destructivas

#### 🟡 Amarillo (Advertencia)
```css
--warning-700: #D97706   /* Ámbar Oscuro - Advertencias críticas */
--warning-600: #F59E0B   /* Ámbar Medio - Precauciones */
--warning-500: #FBBF24   /* Ámbar Estándar - Avisos generales */
```

**Uso:** Advertencias, precauciones, información importante

#### 🔵 Azul Cyan (Información)
```css
--info-700: #0284C7      /* Cyan Oscuro - Info importante */
--info-600: #0EA5E9      /* Cyan Medio - Información general */
--info-500: #06B6D4      /* Cyan Estándar - Mensajes informativos */
```

**Uso:** Mensajes informativos, ayudas, tooltips

---

## 🎯 Componentes Principales

### 1. Botones

#### Primario (Acción Principal)
```html
<button class="btn btn-primary">Guardar</button>
```
**Estilo:** Gradiente azul profundo, sombra sutil
**Uso:** Acción principal de un formulario o página

#### Secundario
```html
<button class="btn btn-secondary">Cancelar</button>
```
**Estilo:** Gris neutro
**Uso:** Acciones secundarias, cancelar

#### Éxito
```html
<button class="btn btn-success">Aprobar</button>
```
**Estilo:** Verde corporativo
**Uso:** Confirmaciones, aprobaciones

#### Peligro
```html
<button class="btn btn-danger">Eliminar</button>
```
**Estilo:** Rojo corporativo
**Uso:** Acciones destructivas, eliminar

### 2. Cards

#### Card Estándar
```html
<div class="card">
    <div class="card-header">Título</div>
    <div class="card-body">Contenido</div>
</div>
```
**Estilo:** Bordes suaves, sombra sutil, header con gradiente azul

#### Card con Hover Lift
```html
<div class="card hover-lift">
    <div class="card-body">Contenido</div>
</div>
```
**Estilo:** Se eleva al pasar el mouse

### 3. Tablas

```html
<table class="table table-hover">
    <thead>
        <tr>
            <th>Columna 1</th>
            <th>Columna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dato 1</td>
            <td>Dato 2</td>
        </tr>
    </tbody>
</table>
```
**Estilo:** Header con fondo gris claro y borde azul, hover sutil

### 4. Badges

```html
<span class="badge badge-primary">Activo</span>
<span class="badge badge-success">Aprobado</span>
<span class="badge badge-danger">Rechazado</span>
<span class="badge badge-warning">Pendiente</span>
<span class="badge badge-info">Información</span>
```

### 5. Alertas

```html
<div class="alert alert-primary">Mensaje informativo</div>
<div class="alert alert-success">Operación exitosa</div>
<div class="alert alert-danger">Error crítico</div>
<div class="alert alert-warning">Advertencia importante</div>
```

---

## 🎨 Gradientes Predefinidos

```css
/* Gradiente Primario - Azul Corporativo */
background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%);

/* Gradiente Oscuro - Headers */
background: linear-gradient(135deg, #1E293B 0%, #334155 100%);

/* Gradiente Éxito - Verde */
background: linear-gradient(135deg, #047857 0%, #059669 100%);

/* Gradiente Info - Cyan */
background: linear-gradient(135deg, #0284C7 0%, #0EA5E9 100%);
```

---

## 💫 Efectos y Animaciones

### Sombras

```css
/* Sombra Pequeña */
box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

/* Sombra Estándar */
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

/* Sombra Grande */
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

/* Sombra XL */
box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

### Hover Effects

```css
/* Elevación al Hover */
.hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.15);
}

/* Escala al Hover */
.hover-scale:hover {
    transform: scale(1.02);
}
```

---

## 📐 Espaciado y Tamaños

### Border Radius
```css
--bs-border-radius: 0.5rem;      /* Estándar */
--bs-border-radius-sm: 0.375rem; /* Pequeño */
--bs-border-radius-lg: 0.75rem;  /* Grande */
--bs-border-radius-xl: 1rem;     /* Extra Grande */
```

### Tipografía
```css
h1: 2.25rem (36px)
h2: 1.875rem (30px)
h3: 1.5rem (24px)
h4: 1.25rem (20px)
h5: 1.125rem (18px)
h6: 1rem (16px)
Body: 0.9375rem (15px)
```

---

## 🎯 Mejores Prácticas

### ✅ DO (Hacer)

1. **Usar gradientes sutiles** para headers y botones principales
2. **Aplicar sombras** para crear jerarquía visual
3. **Mantener contraste** mínimo de 4.5:1 para textos
4. **Usar azules** para acciones primarias
5. **Aplicar colores semánticos** de forma consistente
6. **Espaciado generoso** entre elementos
7. **Border radius consistente** (0.5rem - 0.75rem)

### ❌ DON'T (No Hacer)

1. **No mezclar** más de 3 colores primarios en una vista
2. **No usar** colores saturados para fondos grandes
3. **No aplicar** sombras excesivas
4. **No ignorar** la accesibilidad de contraste
5. **No usar** gradientes muy marcados
6. **No combinar** demasiados efectos hover

---

## 🔧 Implementación

### En HTML - Incluir el CSS personalizado:

```html
<head>
    <!-- CSS Base de Bootstrap -->
    <link rel="stylesheet" href="{% static 'assets/css/soft-ui-dashboard.css' %}">
    
    <!-- CSS Personalizado del Censo -->
    <link rel="stylesheet" href="{% static 'assets/css/censo-theme.css' %}">
</head>
```

### Orden de Carga:
1. `soft-ui-dashboard.css` - Variables base
2. `censo-theme.css` - Estilos personalizados

---

## 📊 Ejemplos de Uso

### Header de Página
```html
<div class="card">
    <div class="card-header bg-gradient-primary">
        <h3 class="text-white mb-0">
            <i class="fas fa-users me-2"></i>
            Gestión de Familias
        </h3>
    </div>
</div>
```

### Card de Estadísticas
```html
<div class="card hover-lift">
    <div class="card-body">
        <div class="d-flex justify-content-between">
            <div>
                <p class="text-muted mb-1">Total Miembros</p>
                <h3 class="mb-0 text-primary-900">1,234</h3>
            </div>
            <div class="icon-shape bg-gradient-primary">
                <i class="fas fa-users text-white"></i>
            </div>
        </div>
    </div>
</div>
```

### Botones de Acción
```html
<div class="d-flex gap-2">
    <button class="btn btn-primary">
        <i class="fas fa-save me-2"></i> Guardar
    </button>
    <button class="btn btn-secondary">
        <i class="fas fa-times me-2"></i> Cancelar
    </button>
</div>
```

---

## 🎨 Paleta Completa en Código

### CSS Variables (Copia y Pega)
```css
/* Azules Primarios */
--primary-900: #1E3A8A;
--primary-800: #1E40AF;
--primary-600: #2563EB;
--primary-500: #3B82F6;

/* Neutrales */
--neutral-900: #111827;
--neutral-700: #374151;
--neutral-500: #6B7280;
--neutral-300: #D1D5DB;
--neutral-100: #F3F4F6;

/* Semánticos */
--success: #059669;
--danger: #DC2626;
--warning: #F59E0B;
--info: #0EA5E9;
```

---

## 🎓 Conclusión

Esta paleta está diseñada para:
- ✅ Aplicaciones empresariales serias
- ✅ Sistemas gubernamentales robustos
- ✅ Plataformas de gestión corporativa
- ✅ Dashboards profesionales

**Características clave:**
- Contraste AAA para accesibilidad
- Jerarquía visual clara
- Colores semánticos consistentes
- Gradientes corporativos sutiles
- Sombras que generan profundidad

---

**Versión:** 3.0 Empresarial  
**Fecha:** 10 de Enero de 2025  
**Autor:** GitHub Copilot AI  

**¡Diseño profesional listo para producción!** 🎨✨

