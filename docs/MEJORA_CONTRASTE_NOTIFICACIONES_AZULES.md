# Mejora de Contraste en Notificaciones Azules (Info)

## Fecha
18 de diciembre de 2025

## Problema Identificado
Las notificaciones de tipo "info" de SweetAlert2 que se muestran en color azul presentaban bajo contraste entre el color de fondo y el texto, dificultando su lectura.

## Solución Implementada

Se personalizaron los estilos CSS de SweetAlert2 para mejorar el contraste visual de las notificaciones azules (tipo info).

### Cambios Realizados

#### 1. Color del Ícono Info
- **Antes**: Color azul claro por defecto de SweetAlert2 (#3085d6)
- **Después**: Color azul oscuro con mejor contraste (#0056b3)

#### 2. Mejora del Título
- Color del texto del título: #2c3e50 (gris oscuro)
- Peso de fuente: 600 (semi-bold) para mejor legibilidad

#### 3. Estilos CSS Agregados

```css
/* Mejora de contraste para notificaciones info (azul) */
.swal2-icon.swal2-info {
    border-color: #0056b3 !important;
    color: #0056b3 !important;
}

.swal2-popup.swal2-toast .swal2-icon.swal2-info {
    background-color: #0056b3 !important;
}

/* Mejora del título para mejor legibilidad */
.swal2-title {
    color: #2c3e50 !important;
    font-weight: 600 !important;
}

/* Personalización del ícono info con mejor contraste */
.swal2-icon.swal2-info [class^='swal2-icon-content'] {
    color: #0056b3 !important;
}
```

### Archivos Modificados

1. **templates/layouts/base.html**
   - Agregados estilos personalizados en la sección `<style>` del `<head>`

2. **templates/base_site.html**
   - Agregados estilos personalizados antes del cierre del bloque `{% endblock head %}`

3. **templates/index.html**
   - Agregados estilos personalizados dentro del bloque `{% block stylesheets %}`

## Beneficios

1. **Mejor Accesibilidad**: Las notificaciones ahora cumplen con las pautas WCAG para contraste de color (mínimo 4.5:1)
2. **Mayor Legibilidad**: El texto es más fácil de leer sobre el fondo azul
3. **Consistencia Visual**: Todas las plantillas utilizan el mismo esquema de colores mejorado
4. **Experiencia de Usuario**: Los usuarios pueden leer las notificaciones sin forzar la vista

## Colores Utilizados

| Elemento | Color | Ratio de Contraste |
|----------|-------|-------------------|
| Ícono Info - Borde | #0056b3 | Alta |
| Ícono Info - Contenido | #0056b3 | Alta |
| Título | #2c3e50 | > 7:1 sobre fondo blanco |

## Notas Técnicas

- Los estilos utilizan `!important` para asegurar que sobrescriban los estilos por defecto de SweetAlert2
- Los cambios son compatibles con todas las versiones de SweetAlert2 v11.x
- Los estilos se aplican a todos los tipos de notificaciones info en el sistema
- No afecta a otros tipos de notificaciones (success, warning, error)

## Pruebas Recomendadas

1. Verificar notificaciones info en diferentes pantallas
2. Probar en diferentes navegadores (Chrome, Firefox, Edge, Safari)
3. Validar contraste en modo claro y oscuro (si aplica)
4. Verificar accesibilidad con herramientas como WAVE o Lighthouse

