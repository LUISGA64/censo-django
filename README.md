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

#### 📦 Configuración Inicial (Solo Primera Vez)

**1. Instalar python-decouple:**
```bash
cd /home/tuusuario/censo-django
source /home/tuusuario/.virtualenvs/venv/bin/activate
pip install python-decouple
```

**2. Crear archivo .env:**
```bash
cd /home/tuusuario/censo-django
nano .env
```

Contenido del archivo `.env`:
```env
# DATABASE
DB_NAME=tuusuario$censodb
DB_USER=tuusuario
DB_PASSWORD=tu_password_mysql
DB_HOST=tuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306

# DJANGO
SECRET_KEY=generar_con_comando_abajo
DEBUG=False
ALLOWED_HOSTS=tuusuario.pythonanywhere.com

# SITE
SITE_URL=https://tuusuario.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://tuusuario.pythonanywhere.com

# SECURITY
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_AGE=86400
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
```

**3. Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Copiar y pegar el resultado en .env
```

**4. Proteger archivo .env:**
```bash
chmod 600 .env
```

**5. Configurar WSGI:**
- Web tab → Code → WSGI file
- Verificar que tenga: `os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'`

#### 🔄 Actualizar Producción (Cada Deploy)

**Comando completo (copy/paste):**
```bash
# Ir al proyecto
cd /home/tuusuario/censo-django

# Activar virtualenv
source /home/tuusuario/.virtualenvs/venv/bin/activate

# Configurar Django settings
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere

# Actualizar código
git pull origin main

# Instalar nuevas dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Verificar configuración
python manage.py check --deploy

# Importante: Ir a Web tab y hacer click en "Reload"
```

#### 🛠️ Script Helper (Recomendado)

Crear script para facilitar comandos Django:
```bash
cd /home/tuusuario/censo-django
cat > manage_prod.sh << 'EOF'
#!/bin/bash
source /home/tuusuario/.virtualenvs/venv/bin/activate
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere
python manage.py "$@"
EOF
chmod +x manage_prod.sh
```

Uso:
```bash
./manage_prod.sh migrate
./manage_prod.sh createsuperuser
./manage_prod.sh collectstatic
```

#### ✅ Verificación Post-Deploy

1. **Recargar aplicación:** Web tab → botón "Reload" verde
2. **Verificar sitio:** Visitar https://tuusuario.pythonanywhere.com
3. **Revisar logs:** Web tab → Error log (buscar errores nuevos)
4. **Probar funcionalidades críticas:**
   - Login/Logout
   - Mapas (verificar que no hay error 403)
   - Dashboard
   - CRUD básica

#### 🚨 Troubleshooting

**Error: "UndefinedValueError"**
```bash
# Verificar que .env existe
ls -la /home/tuusuario/censo-django/.env

# Verificar contenido
cat /home/tuusuario/censo-django/.env

# Si falta SECRET_KEY, generarla nuevamente
```

**Error: "Table doesn't exist"**
```bash
cd /home/tuusuario/censo-django
source /home/tuusuario/.virtualenvs/venv/bin/activate
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere
python manage.py migrate
```

**Mapas con error 403**
```bash
# Verificar que el código está actualizado
git log --oneline -3

# Verificar archivo específico
cat censoapp/geolocation_views.py | grep CartoDB
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
