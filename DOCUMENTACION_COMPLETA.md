# 📚 DOCUMENTACIÓN COMPLETA - CENSO WEB

**Sistema de Gestión de Comunidades Indígenas**  
**Versión Actual:** 1.5 (Camino a 2.0)  
**Última Actualización:** 10 de Febrero de 2026  
**Estado:** ✅ PRODUCCIÓN

---

## 📋 TABLA DE CONTENIDO

1. [Introducción](#introducción)
2. [Características Principales](#características-principales)
3. [Inicio Rápido](#inicio-rápido)
4. [Stack Tecnológico](#stack-tecnológico)
5. [Funcionalidades Implementadas](#funcionalidades-implementadas)
6. [Configuración](#configuración)
7. [Deployment](#deployment)
8. [Mantenimiento](#mantenimiento)
9. [API REST](#api-rest)
10. [Seguridad](#seguridad)
11. [Roadmap](#roadmap)

---

## 🎯 INTRODUCCIÓN

CensoWeb es un sistema web integral para la administración de información de comunidades indígenas. El proyecto está diseñado para ser escalable y puede adaptarse a otros tipos de comunidades.

### Objetivo Principal
Gestionar de forma eficiente el registro de personas, familias, generar documentos oficiales, y proporcionar herramientas analíticas para la toma de decisiones.

---

## ✨ CARACTERÍSTICAS PRINCIPALES

### ✅ Funcionalidades Core

- **👥 Gestión de Personas y Familias** - Registro completo de miembros de la comunidad
- **🏠 Fichas Familiares** - Información detallada por hogar
- **📄 Generación de Documentos** - Certificados y constancias automáticas con QR
- **🔍 Búsqueda Global** - Búsqueda rápida con autocompletado en tiempo real
- **📊 Dashboard Analítico** - Estadísticas y métricas en tiempo real
- **🗺️ Geolocalización** - Mapas interactivos de veredas y familias
- **💾 Backups Automáticos** - Respaldos programados de la base de datos
- **📥 Importación Masiva** - Carga de datos desde Excel
- **🔐 API REST con JWT** - Integración con otras aplicaciones
- **👥 Multi-tenancy** - Soporte para múltiples organizaciones
- **📧 Sistema de Notificaciones** - Notificaciones in-app y por email
- **📱 Optimización Móvil** - PWA instalable con diseño responsive

---

## 🚀 INICIO RÁPIDO

### Requisitos Previos
- Python 3.11+
- MySQL (producción) o SQLite (desarrollo)
- Git

### Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/LUISGA64/censo-django.git
cd censo-django

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Migrar base de datos
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Colectar archivos estáticos
python manage.py collectstatic --noinput

# 8. Iniciar servidor
python manage.py runserver
```

Abrir navegador: http://127.0.0.1:8000/

---

## 🛠️ STACK TECNOLÓGICO

### Backend
- **Django:** 6.0.1 - Framework web principal
- **Django REST Framework:** 3.16.1 - API REST
- **Django REST Framework SimpleJWT:** 5.3.1 - Autenticación JWT
- **Django Allauth:** 65.14.0 - Autenticación y registro
- **Django Filter:** 24.3 - Filtros avanzados en API
- **Django Simple History:** 3.11.0 - Historial de cambios
- **Django Redis:** 5.4.0 - Sistema de caché (opcional)

### Base de Datos
- **Desarrollo:** SQLite
- **Producción:** MySQL (PythonAnywhere)

### Frontend
- **Bootstrap** - Framework CSS
- **Gentelella Theme** - Tema administrativo
- **Chart.js** - Gráficos y visualizaciones
- **Leaflet.js** - Mapas interactivos
- **jQuery** - Manipulación DOM
- **DataTables** - Tablas avanzadas

### Utilidades
- **openpyxl:** 3.1.5 - Lectura/escritura Excel
- **Folium:** 0.20.0 - Mapas Python
- **GeoPy:** 2.4.1 - Geolocalización
- **Gunicorn:** 21.2.0 - WSGI server
- **jsPDF** - Generación de PDFs en cliente

### Seguridad
- JWT para API
- CSRF Protection
- Hash SHA-256 para verificación de documentos
- Variables de entorno para credenciales

---

## 📦 FUNCIONALIDADES IMPLEMENTADAS

### 1. 👥 Gestión de Personas

**Características:**
- Registro completo con validaciones
- Listado con DataTable y filtros
- Búsqueda avanzada
- Edición y actualización
- Exportación a Excel
- Historial de cambios (django-simple-history)
- Vinculación a ficha familiar

**Datos Gestionados:**
- Información personal (nombres, apellidos, identificación)
- Fecha de nacimiento
- Género
- Estado civil
- Nivel educativo
- Ocupación
- EPS y seguridad social
- Discapacidades
- Parentesco
- Cargos en junta directiva

### 2. 🏠 Fichas Familiares

**Características:**
- Registro de núcleo familiar
- Ubicación geográfica (vereda, zona)
- Coordenadas GPS
- Datos de vivienda (opcional, parametrizable)
- Asignación de cabeza de familia
- Listado con filtros por organización
- Exportación de datos

**Datos de Vivienda (Opcionales):**
- Materiales de construcción
- Servicios públicos
- Tipo de propiedad
- Combustible para cocinar
- Tipo de iluminación

### 3. 📄 Sistema de Documentos

**Tipos de Documentos:**

#### 🔵 Aval General
- Para trabajo, prácticas, actividades
- Formulario: Entidad, Motivo, Cargo
- Validez: 1 año

#### 🎓 Aval de Estudio
- Para estudios académicos
- Formulario: Institución, Programa, Semestre, Proyecto
- Campos opcionales configurables

#### 🏘️ Constancia de Pertenencia
- Certificado de membresía
- Generación automática
- Sin formulario adicional

**Características del Sistema:**
- ✅ Generación de PDF con jsPDF
- ✅ Almacenamiento en base de datos
- ✅ Hash SHA-256 único por documento
- ✅ Código QR de verificación
- ✅ Vista previa en iframe
- ✅ Descarga personalizada
- ✅ Verificación pública: `/documento/verificar/<hash>/`
- ✅ Estadísticas con gráficos
- ✅ Fechas de emisión y vencimiento
- ✅ Firmas digitales de junta directiva

### 4. 🔍 Búsqueda Global

**Características:**
- Búsqueda desde navbar
- Autocompletado en tiempo real (mínimo 3 caracteres)
- Resultados agrupados por tipo
- Redirección automática al detalle de persona
- Case-insensitive
- Búsqueda por nombres, apellidos, identificación

**Endpoints:**
- `/search/` - Página de búsqueda
- `/api/search/` - API JSON para autocompletado

### 5. 📊 Dashboard Analítico

**KPIs Principales:**
- Total de personas censadas
- Total de fichas familiares
- Documentos generados
- Distribución por género
- Pirámide poblacional

**Gráficos:**
- Distribución por género (Pie chart)
- Pirámide de edad (Bar chart)
- Nivel educativo (Bar chart)
- Estado civil (Pie chart)
- Personas por vereda (Bar chart)
- Crecimiento poblacional (Line chart)

**Tecnologías:**
- Chart.js para visualizaciones
- APIs REST para datos
- Caché para optimización
- Diseño responsive

**Ruta:** `/dashboard/analytics/`

### 6. 🗺️ Geolocalización

**Características:**
- Mapas interactivos con Leaflet.js
- Visualización de veredas
- Mapa de calor
- Clustering de puntos
- Actualización de coordenadas
- Detalle por vereda

**Rutas:**
- `/mapa/` - Vista de mapa general
- `/mapa/calor/` - Mapa de calor
- `/mapa/clusters/` - Vista con clusters
- `/mapa/vereda/<id>/` - Detalle de vereda

### 7. 📧 Sistema de Notificaciones

**Características:**
- Notificaciones in-app
- Envío de emails con plantillas HTML
- Preferencias personalizables por usuario
- Panel interactivo en navbar
- Contador de no leídas

**Tipos de Notificaciones:**
- `DOCUMENT_EXPIRING` - Documento próximo a vencer
- `DOCUMENT_EXPIRED` - Documento vencido
- `DOCUMENT_GENERATED` - Documento generado
- `PERSON_ADDED` - Persona agregada
- `FAMILY_ADDED` - Familia agregada
- `SYSTEM` - Notificaciones del sistema
- `SECURITY` - Alertas de seguridad

**Modelos:**
- `Notification` - Almacena notificaciones
- `NotificationPreference` - Configuración de usuario

**Servicio:**
- `NotificationService` - Lógica de negocio
  - `create_notification()` - Crear notificación
  - `send_email_notification()` - Enviar email
  - `notify_document_expiring()` - Alertas de vencimiento
  - `check_expiring_documents()` - Verificación diaria

**Rutas:**
- `/notifications/` - Lista de notificaciones
- `/notifications/<id>/` - Detalle
- `/notifications/preferences/` - Configuración
- `/api/notifications/unread/` - API contador

### 8. 📥 Importación Masiva

**Características:**
- ✅ Template Excel descargable
- ✅ Validación de datos antes de importar
- ✅ Preview de datos a importar
- ✅ Importación por lotes (fichas y personas)
- ✅ Reporte de errores detallado
- ✅ Logs de importación
- ✅ Manejo de duplicados

**Proceso:**
1. Descargar template Excel
2. Llenar datos
3. Subir archivo
4. Validar datos
5. Preview y confirmación
6. Importación
7. Ver log de resultados

**Rutas:**
- `/importacion/` - Inicio
- `/importacion/template/` - Descargar template
- `/importacion/validar/` - Validar archivo
- `/importacion/confirmar/` - Confirmar importación
- `/importacion/log/` - Ver logs

**Archivo:** `censoapp/importador_masivo.py` (647 líneas)

### 9. 🔐 API REST con JWT

**Autenticación:**
- JWT (JSON Web Tokens)
- Access token y refresh token
- Blacklist de tokens

**Endpoints Principales:**

```
POST /api/token/ - Obtener tokens
POST /api/token/refresh/ - Refrescar token
GET  /api/v1/persons/ - Listar personas
GET  /api/v1/persons/<id>/ - Detalle persona
POST /api/v1/persons/ - Crear persona
PUT  /api/v1/persons/<id>/ - Actualizar persona
DELETE /api/v1/persons/<id>/ - Eliminar persona
GET  /api/v1/family-cards/ - Listar fichas
GET  /api/v1/documents/ - Listar documentos
GET  /api/v1/organizations/ - Listar organizaciones
GET  /api/v1/associations/ - Listar asociaciones
GET  /api/v1/sidewalks/ - Listar veredas
```

**Características:**
- Filtros avanzados con django-filter
- Paginación configurable
- Serializers optimizados
- Permisos por rol

### 10. 👥 Multi-tenancy

**Características:**
- Soporte para múltiples organizaciones
- Usuarios vinculados a organización
- Filtrado automático de datos
- Middleware de organización

**Modelos:**
- `Association` - Asociación (nivel superior)
- `Organizations` - Organizaciones (nivel medio)
- `UserProfile` - Perfil con organización

**Roles:**
- `ADMIN` - Administrador de organización
- `OPERATOR` - Operador
- `VIEWER` - Solo consulta

**Permisos:**
- `can_view_all_organizations` - Ver todas las organizaciones (super admin)

### 11. 📱 Optimización Móvil

**Características:**
- ✅ PWA (Progressive Web App) instalable
- ✅ Diseño responsive completo
- ✅ CSS móvil (700+ líneas)
- ✅ JavaScript móvil (600+ líneas)
- ✅ Service Worker para caché offline
- ✅ Manifest.json
- ✅ Touch optimizations
- ✅ Sidebar móvil sin scroll
- ✅ Tablas responsivas
- ✅ Formularios adaptados

**Archivos:**
- `static/css/mobile-optimizations.css`
- `static/js/mobile-enhancements.js`
- `static/manifest.json`
- `static/sw.js`

---

## ⚙️ CONFIGURACIÓN

### Variables de Entorno (.env)

**IMPORTANTE:** El archivo `.env` NO se sube a Git por seguridad.

```env
# Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de Datos (Producción - MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=nombre_base_datos
DB_USER=usuario_mysql
DB_PASSWORD=password_mysql
DB_HOST=localhost
DB_PORT=3306

# Email (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

# Configuración del Sitio
SITE_URL=https://tudominio.com
```

### Archivos de Configuración

**Desarrollo:** `censoProject/settings.py`
- SQLite
- DEBUG=True
- Configuración local

**Producción:** `censoProject/settings_pythonanywhere.py`
- MySQL
- DEBUG=False
- Configuración de seguridad
- ALLOWED_HOSTS configurado

---

## 🚀 DEPLOYMENT

### PythonAnywhere (Producción Actual)

```bash
# 1. Conectar por SSH
ssh usuario@ssh.pythonanywhere.com

# 2. Activar entorno virtual
workon censo-env

# 3. Ir al directorio del proyecto
cd ~/censo-django

# 4. Actualizar código
git pull origin development

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Migrar base de datos
python manage.py migrate

# 7. Colectar archivos estáticos
python manage.py collectstatic --noinput

# 8. Recargar aplicación
touch /var/www/usuario_pythonanywhere_com_wsgi.py
```

### Configuración WSGI

**Archivo:** `/var/www/usuario_pythonanywhere_com_wsgi.py`

```python
import os
import sys

# Agregar proyecto al path
path = '/home/usuario/censo-django'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

# Aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🔧 MANTENIMIENTO

### Scripts Disponibles

#### 1. Optimización de Base de Datos
```bash
python scripts/optimize_database.py
```
- Análisis de índices
- Limpieza de datos
- Estadísticas de tablas
- Recomendaciones de optimización

#### 2. Health Check
```bash
python scripts/health_check.py
```
- Verifica configuración
- Prueba conexión a BD
- Revisa permisos
- Estado del sistema

#### 3. Backup Manual
```bash
# Windows
.\scripts\backup_database.ps1

# Linux
bash scripts/backup_auto.sh
```
- Crea respaldo de BD
- Comprime con gzip
- Guarda en `/backups/`
- Genera archivo JSON con metadata

### Comandos Django Útiles

```bash
# Verificar configuración
python manage.py check --deploy

# Limpiar sesiones expiradas
python manage.py clearsessions

# Crear superusuario
python manage.py createsuperuser

# Migrar base de datos
python manage.py migrate

# Colectar estáticos
python manage.py collectstatic --noinput

# Shell de Django
python manage.py shell

# Ejecutar tests
python manage.py test
```

### Logs

**Ubicación:**
- `/logs/django.log` - Log general
- `/logs/security.log` - Log de seguridad
- `/media/importacion_logs/` - Logs de importación

**Configuración en settings.py:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## 🔐 SEGURIDAD

### Implementaciones de Seguridad

1. **Autenticación JWT** - Tokens seguros para API
2. **CSRF Protection** - Protección contra ataques CSRF
3. **Hash SHA-256** - Verificación de documentos
4. **Variables de Entorno** - Credenciales fuera del código
5. **HTTPS** - Conexión encriptada (producción)
6. **Permisos por Rol** - Control de acceso granular
7. **Historial de Cambios** - Auditoría con django-simple-history
8. **Validaciones** - Lado cliente y servidor

### Buenas Prácticas

- ✅ No subir `.env` a Git
- ✅ Usar `.env.example` como plantilla
- ✅ Cambiar `SECRET_KEY` en producción
- ✅ `DEBUG=False` en producción
- ✅ Configurar `ALLOWED_HOSTS`
- ✅ Mantener dependencias actualizadas
- ✅ Backups regulares
- ✅ Logs de seguridad activos

### Verificación de Documentos

Sistema público de verificación de autenticidad:

```
URL: /documento/verificar/<hash>/
Hash: SHA-256 (64 caracteres)
Acceso: Público (sin autenticación)
```

Cualquier persona puede verificar la autenticidad de un documento usando el código QR o el hash.

---

## 📡 ROADMAP

### ✅ Completado (Versión 1.5)

- ✅ Gestión de personas y familias
- ✅ Fichas familiares
- ✅ Generación de documentos con QR
- ✅ Búsqueda global avanzada
- ✅ Dashboard analítico
- ✅ Sistema de notificaciones (Email + In-app)
- ✅ Importación masiva de datos
- ✅ Exportación de personas a Excel
- ✅ API REST con JWT
- ✅ Multi-tenancy
- ✅ Optimización móvil (PWA)
- ✅ Geolocalización y mapas
- ✅ Backups automáticos

### 🔮 Futuras Mejoras (Opcionales)

#### Corto Plazo:
- Documentación API con Swagger/OpenAPI
- Rate limiting en API
- Más tipos de reportes personalizados

#### Medio Plazo:
- Inteligencia Artificial (OCR para documentos)
- Autenticación de dos factores (2FA)
- Multi-idioma (Español, Inglés, Lenguas indígenas)

#### Largo Plazo:
- Business Intelligence avanzado
- App móvil nativa (si PWA no es suficiente)
- Integración con otros sistemas gubernamentales

---

## 📞 SOPORTE Y CONTACTO

**Repositorio:** https://github.com/LUISGA64/censo-django  
**Rama Principal:** development  
**Licencia:** MIT (o según lo definas)

### Reportar Problemas

1. Crear issue en GitHub
2. Describir el problema detalladamente
3. Incluir pasos para reproducir
4. Adjuntar logs si es posible

---

## 📄 LICENCIA

Este proyecto está bajo licencia [MIT/Propietaria - Definir según corresponda].

---

**Última actualización:** 10 de Febrero de 2026  
**Versión del documento:** 2.0  
**Mantenido por:** Equipo de Desarrollo CensoWeb

