# 🚀 GUÍA DE DEPLOYMENT A PYTHONANYWHERE - PASO A PASO

**Fecha:** 4 de Febrero de 2026  
**Versión:** 2.0 - Fase 1 Completa  
**Tiempo estimado:** 1-2 horas

---

## 📋 PRE-REQUISITOS

### En tu cuenta de PythonAnywhere:
- ✅ Cuenta activa
- ✅ Acceso a consola Bash
- ✅ MySQL database disponible
- ✅ Web app configurada

---

## 🔑 PASO 1: PREPARAR VARIABLES DE ENTORNO

### 1.1 Crear archivo .env en PythonAnywhere

```bash
# Conectar a PythonAnywhere vía SSH o usar consola web
cd ~/censo-django

# Crear archivo .env
nano .env
```

### 1.2 Contenido del archivo .env:

```bash
# Django Settings
SECRET_KEY=tu-secret-key-super-segura-aqui-cambiar
DEBUG=False
ALLOWED_HOSTS=tuusuario.pythonanywhere.com,www.tuusuario.pythonanywhere.com

# Database MySQL
DB_NAME=tuusuario$censodb
DB_USER=tuusuario
DB_PASSWORD=tu_password_mysql_aqui
DB_HOST=tuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306

# Security
SESSION_COOKIE_AGE=86400
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Site
SITE_URL=https://tuusuario.pythonanywhere.com

# CORS (si es necesario)
CORS_ALLOWED_ORIGINS=https://tuusuario.pythonanywhere.com

# Email (opcional - configurar después)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=tu_email@gmail.com
# EMAIL_HOST_PASSWORD=tu_password_app

# Redis (opcional - si está disponible)
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=1

# Logs
LOG_LEVEL=INFO

# Sentry (opcional - para monitoreo de errores)
# SENTRY_DSN=
# SENTRY_ENVIRONMENT=production
```

**IMPORTANTE:** Cambia los valores marcados con "tuusuario" y "tu_password"

---

## 🗄️ PASO 2: ACTUALIZAR CÓDIGO DESDE GITHUB

```bash
# Conectar a PythonAnywhere
cd ~/censo-django

# Si es primera vez, clonar:
git clone https://github.com/LUISGA64/censo-django.git
cd censo-django

# Si ya existe, actualizar:
git fetch origin
git checkout development
git pull origin development

# Verificar que estás en la rama correcta
git branch
git log --oneline -5
```

---

## 🐍 PASO 3: CONFIGURAR ENTORNO VIRTUAL

```bash
# Crear entorno virtual (si no existe)
mkvirtualenv --python=/usr/bin/python3.10 censo-env

# Activar entorno virtual
workon censo-env

# Verificar versión de Python
python --version
# Debe mostrar: Python 3.10.x

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación de dependencias críticas
pip list | grep -E "Django|djangorestframework|simplejwt"
```

---

## 🗄️ PASO 4: CONFIGURAR MYSQL

### 4.1 Crear base de datos (si no existe)

1. Ir a PythonAnywhere → **Databases**
2. Click en **Initialize MySQL**
3. Crear nueva base de datos: `tuusuario$censodb`
4. Anotar: **usuario**, **password**, **host**

### 4.2 Verificar conexión

```bash
# Test de conexión a MySQL
mysql -u tuusuario -p -h tuusuario.mysql.pythonanywhere-services.com tuusuario$censodb

# Si conecta correctamente, salir:
exit
```

---

## 🔧 PASO 5: CONFIGURAR SETTINGS DE PRODUCCIÓN

El archivo `settings.py` ya está configurado para leer variables de `.env`, solo verifica:

```bash
cd ~/censo-django
cat .env | grep DB_NAME
# Debe mostrar: DB_NAME=tuusuario$censodb

# Verificar que Django puede leer el .env
python manage.py check
```

---

## 📊 PASO 6: EJECUTAR MIGRACIONES

```bash
cd ~/censo-django
workon censo-env

# Verificar migraciones pendientes
python manage.py showmigrations

# Ejecutar migraciones
python manage.py migrate

# Verificar que se aplicaron correctamente
python manage.py showmigrations | grep "\[X\]"
```

**Resultado esperado:** Todas las migraciones con `[X]` marcadas

---

## 👤 PASO 7: CREAR SUPERUSUARIO

```bash
# Crear superusuario para administración
python manage.py createsuperuser

# Seguir las instrucciones:
# Username: admin (o el que prefieras)
# Email: tu_email@example.com
# Password: (contraseña segura)
# Password (again): (repetir)
```

---

## 📁 PASO 8: RECOPILAR ARCHIVOS ESTÁTICOS

```bash
cd ~/censo-django
workon censo-env

# Recopilar todos los archivos estáticos
python manage.py collectstatic --noinput

# Verificar que se creó la carpeta
ls -la staticfiles/
```

**Resultado esperado:** Carpeta `staticfiles/` con todos los archivos CSS, JS, imágenes

---

## 🌐 PASO 9: CONFIGURAR WEB APP

### 9.1 En PythonAnywhere → Web

1. Click en tu aplicación web existente o crear nueva

2. **Source code:**
   ```
   /home/tuusuario/censo-django
   ```

3. **Working directory:**
   ```
   /home/tuusuario/censo-django
   ```

4. **Virtualenv:**
   ```
   /home/tuusuario/.virtualenvs/censo-env
   ```

### 9.2 Editar WSGI Configuration File

Click en **WSGI configuration file** y reemplazar TODO el contenido con:

```python
import os
import sys

# Agregar el proyecto al path
path = '/home/tuusuario/censo-django'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings'

# Cargar variables de entorno desde .env
from pathlib import Path
env_file = Path(path) / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Inicializar WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANTE:** Cambiar `tuusuario` por tu nombre de usuario real

---

## 📂 PASO 10: CONFIGURAR ARCHIVOS ESTÁTICOS

En PythonAnywhere → Web → **Static files**

Agregar dos entradas:

**Entrada 1 - Static:**
- URL: `/static/`
- Directory: `/home/tuusuario/censo-django/staticfiles/`

**Entrada 2 - Media:**
- URL: `/media/`
- Directory: `/home/tuusuario/censo-django/media/`

---

## 🔄 PASO 11: RECARGAR WEB APP

```bash
# En la interfaz web de PythonAnywhere
# Click en el botón verde: "Reload tuusuario.pythonanywhere.com"
```

**O desde consola:**
```bash
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py
```

---

## ✅ PASO 12: VERIFICAR DEPLOYMENT

### 12.1 Verificar que el sitio carga

Abrir en navegador:
```
https://tuusuario.pythonanywhere.com/
```

**Debe mostrar:** Página de login o home del censo

### 12.2 Verificar admin

```
https://tuusuario.pythonanywhere.com/admin/
```

**Debe mostrar:** Página de login de Django admin

### 12.3 Verificar archivos estáticos

```
https://tuusuario.pythonanywhere.com/static/assets/css/censo-corporate.css
```

**Debe mostrar:** Archivo CSS descargable o visible

### 12.4 Verificar API REST

```
https://tuusuario.pythonanywhere.com/api/token/
```

**Debe mostrar:** Interfaz de DRF para obtener token

---

## 🔐 PASO 13: CONFIGURAR BACKUPS AUTOMÁTICOS

```bash
# Editar crontab
crontab -e

# Agregar línea para backup diario a las 2 AM
0 2 * * * cd /home/tuusuario/censo-django && /home/tuusuario/.virtualenvs/censo-env/bin/python manage.py backup_db --compress --keep-days 30

# Guardar y salir (Ctrl+X, Y, Enter)

# Verificar crontab
crontab -l
```

**Crear carpeta de backups:**
```bash
mkdir -p ~/censo-django/backups
chmod 755 ~/censo-django/backups
```

---

## 🧪 PASO 14: PRUEBAS POST-DEPLOYMENT

### 14.1 Test de Login

1. Ir a: `https://tuusuario.pythonanywhere.com/`
2. Login con superusuario creado
3. ✅ Debe redirigir al dashboard

### 14.2 Test de Búsqueda Global

1. Usar el buscador en navbar
2. Buscar algo
3. ✅ Debe mostrar resultados

### 14.3 Test de API REST

```bash
# Desde tu máquina local
curl -X POST https://tuusuario.pythonanywhere.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"tu_password"}'

# Debe devolver:
# {"access":"...", "refresh":"..."}
```

### 14.4 Test de Dashboard

1. Ir a: `https://tuusuario.pythonanywhere.com/dashboard/analytics/`
2. ✅ Debe mostrar gráficos y KPIs

### 14.5 Test de Importación

1. Ir a: `https://tuusuario.pythonanywhere.com/importacion/`
2. ✅ Debe cargar sin errores

---

## 📊 PASO 15: MONITOREO Y LOGS

### Ver logs de errores:

```bash
# Log de Django
tail -f ~/censo-django/logs/django.log

# Log del servidor web
tail -f /var/log/tuusuario.pythonanywhere.com.error.log

# Log de acceso
tail -f /var/log/tuusuario.pythonanywhere.com.access.log
```

### Verificar archivos de log existen:

```bash
ls -la ~/censo-django/logs/
```

---

## 🔧 TROUBLESHOOTING

### Error: "Internal Server Error"

1. Verificar logs:
   ```bash
   tail -50 /var/log/tuusuario.pythonanywhere.com.error.log
   ```

2. Verificar configuración:
   ```bash
   python manage.py check --deploy
   ```

### Error: "Static files not loading"

```bash
python manage.py collectstatic --noinput
# Recargar web app
```

### Error: "Database connection failed"

1. Verificar .env:
   ```bash
   cat .env | grep DB_
   ```

2. Test de conexión MySQL:
   ```bash
   mysql -u tuusuario -p -h tuusuario.mysql.pythonanywhere-services.com
   ```

### Error: "ImportError: No module named..."

```bash
workon censo-env
pip install -r requirements.txt
```

---

## ✅ CHECKLIST FINAL

Antes de dar por terminado el deployment:

- [ ] ✅ Código actualizado desde GitHub
- [ ] ✅ .env configurado correctamente
- [ ] ✅ Entorno virtual creado y activado
- [ ] ✅ Dependencias instaladas (requirements.txt)
- [ ] ✅ MySQL database creada
- [ ] ✅ Migraciones ejecutadas
- [ ] ✅ Superusuario creado
- [ ] ✅ Collectstatic ejecutado
- [ ] ✅ WSGI configurado
- [ ] ✅ Static files configurados
- [ ] ✅ Web app recargada
- [ ] ✅ Sitio carga correctamente
- [ ] ✅ Admin accesible
- [ ] ✅ API REST funciona
- [ ] ✅ Backups configurados (crontab)
- [ ] ✅ Todas las funcionalidades probadas
- [ ] ✅ Logs funcionando

---

## 🎉 DEPLOYMENT COMPLETADO

Si todos los checks están marcados, el deployment está completo.

**URLs importantes:**

- **Sitio:** https://tuusuario.pythonanywhere.com/
- **Admin:** https://tuusuario.pythonanywhere.com/admin/
- **Dashboard:** https://tuusuario.pythonanywhere.com/dashboard/analytics/
- **Búsqueda:** https://tuusuario.pythonanywhere.com/search/
- **API Token:** https://tuusuario.pythonanywhere.com/api/token/
- **API Persons:** https://tuusuario.pythonanywhere.com/api/v1/persons/

---

## 📝 SIGUIENTE: CONFIGURACIÓN POST-DEPLOYMENT

1. **Cargar datos iniciales** (si es necesario)
2. **Configurar email** para notificaciones
3. **Configurar Sentry** para monitoreo de errores (opcional)
4. **Entrenar usuarios** en nuevas funcionalidades
5. **Documentar cambios** para el equipo

---

**¡Deployment completado exitosamente! 🚀**
