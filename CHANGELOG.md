# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## Formato

```
## [X.Y.Z] - YYYY-MM-DD

### Added (Agregado)
- Nuevas funcionalidades

### Changed (Cambiado)
- Cambios en funcionalidades existentes

### Deprecated (Obsoleto)
- Funcionalidades que pronto serán removidas

### Removed (Removido)
- Funcionalidades removidas

### Fixed (Corregido)
- Correcciones de bugs

### Security (Seguridad)
- Correcciones de vulnerabilidades
```

---

## [Unreleased]

### Pendiente
- Implementación de notificaciones en tiempo real
- Dashboard de analíticas avanzado

---

## [2.1.0] - 2026-04-25

### Added
- Script helper `manage_prod.sh` para facilitar comandos Django en producción
- Sección completa de deployment en README.md con instrucciones paso a paso
- Sistema de versionamiento semántico con archivo VERSION
- Documentación consolidada de troubleshooting en README.md

### Changed
- Consolidadas todas las instrucciones de deploy en README.md
- Optimizado proceso de actualización en producción
- Mejorada documentación de configuración de .env

### Fixed
- Corregida configuración de variables de entorno en producción
- Solucionado error de tabla `censoapp_loginattempt` no encontrada
- Corregida configuración de WSGI para usar settings_pythonanywhere

### Removed
- Eliminados archivos .md redundantes (GUIA_DEPLOY_PRODUCCION.md, GUIA_IMPLEMENTACION_ENV_PRODUCCION.md, etc.)
- Reducido ~39KB de documentación innecesaria

---

## [2.0.0] - 2026-04-20

### Added
- Diseño moderno y consistente para mapas (Clusters y Heatmap)
- Barra de estadísticas horizontal en todas las vistas de mapas
- Controles de navegación integrados en barra de estadísticas
- Info Box profesional reemplazando alertas de Bootstrap
- Selector de estilos de mapa flotante (esquina superior izquierda)
- Leyenda de mapa flotante (esquina inferior derecha)
- Botón de pantalla completa para mapas
- Variables de contexto en vistas de geolocalización

### Changed
- Rediseñados templates: clusters.html, heatmap.html, map_view.html
- Optimizado espacio del mapa con controles flotantes internos
- Mapa ahora ocupa 100% del ancho disponible (eliminado sidebar)
- Altura mínima de mapas aumentada a 650px
- Mejorado responsive design para dispositivos móviles

### Fixed
- Corregido error 403 en carga de mapas
- Corregida configuración de tiles de CartoDB
- Solucionados problemas de visualización en vistas de mapas
- Corregidos estilos CSS duplicados en templates

### Security
- Implementado python-decouple para variables de entorno
- Separadas credenciales del código fuente
- Configuración segura de SECRET_KEY

---

## [1.2.0] - 2026-02-27

### Added
- Sistema multi-tenancy (múltiples organizaciones)
- API REST completa con autenticación JWT
- Dashboard analítico con métricas en tiempo real
- Generación automática de documentos PDF
- Sistema de geolocalización con mapas interactivos
- Importación masiva de datos
- Búsqueda global con autocompletado

### Changed
- Migrado a Django 6.0.1
- Actualizado sistema de autenticación con django-allauth
- Mejorado sistema de caché

### Fixed
- Optimizaciones de rendimiento en consultas de base de datos
- Correcciones de seguridad en autenticación

---

## [1.1.0] - 2026-01-15

### Added
- Recuperación de contraseñas privada (solo admins)
- Registro de intentos de login
- Tokens de recuperación con expiración
- Rate limiting para prevenir ataques

### Security
- Headers de seguridad configurados
- HTTPS obligatorio en producción
- CSRF y XSS protection habilitados

---

## [1.0.0] - 2025-12-01

### Added
- Lanzamiento inicial del sistema CensoWeb
- Gestión de personas y familias
- Fichas familiares
- Sistema de autenticación básico
- Panel administrativo Django
- Base de datos SQLite (desarrollo)

---

## Guía de Versionamiento

### Semantic Versioning (X.Y.Z)

- **X (Major)**: Cambios incompatibles con versiones anteriores
  - Ejemplo: 1.0.0 → 2.0.0 (cambio de estructura de BD, API breaking changes)
  
- **Y (Minor)**: Nueva funcionalidad compatible con versión anterior
  - Ejemplo: 1.0.0 → 1.1.0 (nuevo módulo de reportes, nueva API endpoint)
  
- **Z (Patch)**: Corrección de bugs, sin nuevas funcionalidades
  - Ejemplo: 1.0.0 → 1.0.1 (fix de bug, corrección de estilos)

### Cuándo incrementar cada número:

**Major (X):**
- Cambio de base de datos incompatible
- Cambio en API que rompe compatibilidad
- Rediseño completo de módulos principales
- Migración a nueva versión mayor de Django

**Minor (Y):**
- Nueva funcionalidad (nuevo módulo de mapas)
- Mejoras significativas a funcionalidades existentes
- Nuevos endpoints de API
- Actualización de dependencias menores

**Patch (Z):**
- Corrección de bugs
- Mejoras de rendimiento
- Correcciones de seguridad menores
- Actualización de documentación
- Refactoring sin cambios funcionales

### Ejemplo Práctico:

```
1.0.0 → 1.0.1  (Fix: Corrección error en login)
1.0.1 → 1.1.0  (Feature: Agregado módulo de reportes)
1.1.0 → 2.0.0  (Breaking: Migración a Django 6, cambios en API)
```

---

## Tipos de Cambios

### Added (Agregado) 🟢
- Nuevas funcionalidades
- Nuevos módulos
- Nuevas API endpoints
- Nuevos comandos de Django

### Changed (Cambiado) 🔵
- Cambios en funcionalidades existentes
- Mejoras de rendimiento
- Refactorizaciones
- Cambios en configuración

### Deprecated (Obsoleto) 🟡
- Funcionalidades que se removerán pronto
- APIs antiguas aún funcionales
- Métodos marcados para eliminación

### Removed (Removido) 🔴
- Funcionalidades eliminadas
- APIs eliminadas
- Dependencias removidas

### Fixed (Corregido) 🟣
- Correcciones de bugs
- Fixes de errores
- Correcciones de typos

### Security (Seguridad) 🔒
- Correcciones de vulnerabilidades
- Mejoras de seguridad
- Actualizaciones de dependencias por CVEs

---

## Comandos Útiles

### Ver versión actual:
```bash
cat VERSION
```

### Crear nueva versión (tag):
```bash
# Patch (fix)
git tag -a v2.1.1 -m "Fix: Corrección error en mapas"

# Minor (feature)
git tag -a v2.2.0 -m "Feature: Nuevo módulo de reportes"

# Major (breaking change)
git tag -a v3.0.0 -m "Breaking: Migración a Django 7"

# Pushear tags
git push origin --tags
```

### Ver todas las versiones:
```bash
git tag -l
```

### Ver cambios entre versiones:
```bash
git log v2.0.0..v2.1.0 --oneline
```

