# 🏛️ CensoWeb - Sistema de Gestión de Comunidades

Sistema web integral para la administración de información de comunidades indígenas y otros tipos de organizaciones.

## 🚀 Inicio Rápido

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

# 5. Configurar base de datos
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

Abrir navegador: http://127.0.0.1:8000/

## ✨ Características Principales

- 👥 **Gestión de Personas y Familias** - Registro completo de miembros
- 🏠 **Fichas Familiares** - Información detallada por hogar
- 📄 **Generación de Documentos** - Certificados y constancias automáticas
- 🔍 **Búsqueda Global** - Búsqueda rápida con autocompletado
- 📊 **Dashboard Analítico** - Estadísticas y métricas en tiempo real
- 🗺️ **Geolocalización** - Mapas interactivos
- 💾 **Backups Automáticos** - Respaldos programados
- 📥 **Importación Masiva** - Carga de datos en lote
- 🔐 **API REST con JWT** - Integración con otras aplicaciones
- 👥 **Multi-tenancy** - Múltiples organizaciones

## 🛠️ Herramientas de Mantenimiento

```bash
# Análisis completo de base de datos
python scripts/optimize_database.py

# Backup manual
python manage.py dumpdata > backup.json

# Verificar configuración
python manage.py check --deploy

# Limpiar sesiones
python manage.py clearsessions
```

## 🔐 Seguridad

### Características de Seguridad Implementadas

- **Autenticación robusta** con django-allauth
- **Recuperación de contraseñas** privada (solo admins pueden solicitar)
- **Registro de intentos de login** para detectar ataques de fuerza bruta
- **Tokens de recuperación** con expiración automática
- **Seguridad de sesiones** con monitoreo de IP y user agent
- **Rate limiting** para prevenir ataques
- **HTTPS obligatorio** en producción
- **CSRF y XSS protection** habilitados
- **Headers de seguridad** configurados

### Configuración de Email

El sistema usa Gmail para envío de notificaciones. Configura en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=tu_email@gmail.com
ADMIN_EMAIL=admin_email@gmail.com
```

**Importante:** Usa "App Passwords" de Gmail, no tu contraseña regular.

## 📊 Stack Tecnológico

- **Backend:** Django 6.0.1
- **Database:** MySQL (prod) / SQLite (dev)
- **Frontend:** Bootstrap + Gentelella Theme
- **API:** Django REST Framework
- **Auth:** JWT + Django Allauth
- **Maps:** Leaflet.js
- **Cache:** Redis (recomendado)

## 🚀 Deployment

### Desarrollo Local
```bash
python manage.py runserver
```

### Producción (PythonAnywhere)
```bash
# 1. Conectar por SSH y activar entorno
workon censo-env
cd ~/censo-django

# 2. Actualizar código
git pull origin development

# 3. Instalar dependencias y migrar
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# 4. Recargar aplicación
touch /var/www/*_pythonanywhere_com_wsgi.py
```

### Variables de Entorno Requeridas

Crea un archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=tu_secret_key_aqui
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de datos (Producción MySQL)
DB_NAME=tu_base_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=tu_host
DB_PORT=3306

# Email (Gmail)
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
ADMIN_EMAIL=admin@tudominio.com

# API
JWT_SECRET_KEY=tu_jwt_secret_key
```

## 📱 Optimización Móvil

El sistema está optimizado para dispositivos móviles:
- Diseño responsive
- Menú lateral adaptativo
- Búsqueda optimizada para táctil
- Formularios adaptados a móviles

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📝 Licencia

Proyecto propietario - Todos los derechos reservados

## 👤 Contacto

- **Repositorio:** https://github.com/LUISGA64/censo-django
- **Issues:** https://github.com/LUISGA64/censo-django/issues
- **Email:** webcenso@gmail.com

---

**Versión:** 2.0  
**Última actualización:** 2026-02-27  
**Estado:** ✅ En producción
