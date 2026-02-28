# Guía: Gestión de Settings.py con Git

## 📋 Resumen

Esta guía explica cómo manejar correctamente el archivo `settings.py` en Git cuando tienes configuraciones diferentes entre desarrollo y producción.

## ✅ Tu archivo .gitignore ya está configurado correctamente

El archivo `.gitignore` **ya incluye** la configuración necesaria:

```gitignore
# Archivos de configuración
settings.py
settings_*.py
local_settings.py

# Permitir versionar archivo de ejemplo
!settings.example.py
```

Esto significa que:
- ✅ `settings.py` NO se rastreará en Git
- ✅ `settings_production.py` NO se rastreará en Git
- ✅ `settings_pythonanywhere.py` NO se rastreará en Git
- ✅ `settings.example.py` SÍ se versionará como plantilla

## 🎯 ¿Afecta esto al despliegue en producción?

**NO afecta negativamente**, de hecho es la **mejor práctica** por estas razones:

### Ventajas ✅

1. **Seguridad**: Las credenciales, claves secretas y configuraciones sensibles NO se suben al repositorio
2. **Flexibilidad**: Cada entorno (desarrollo, producción) mantiene su propia configuración
3. **Sin conflictos**: No hay conflictos de Git cada vez que cambias configuraciones locales
4. **Estándar de la industria**: Es la forma recomendada por Django y la comunidad

### Cómo funciona el despliegue

1. **En desarrollo** (tu PC):
   - Usas `settings.py` con configuraciones locales
   - SQLite como base de datos
   - DEBUG = True

2. **En producción** (PythonAnywhere):
   - Usas `settings_pythonanywhere.py` o `settings_production.py`
   - MySQL como base de datos
   - DEBUG = False
   - Configuraciones específicas de PythonAnywhere

## 📁 Estructura recomendada

```
censoProject/
├── settings.py                      # ❌ NO versionado (desarrollo local)
├── settings.example.py              # ✅ Versionado (plantilla)
├── settings_production.py           # ❌ NO versionado (producción)
├── settings_pythonanywhere.py       # ❌ NO versionado (PythonAnywhere)
└── __init__.py
```

## 🔧 Configuración correcta en cada entorno

### 1. Desarrollo (Tu PC)

Edita `manage.py` para usar settings local:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
```

### 2. Producción (PythonAnywhere)

En la configuración WSGI de PythonAnywhere:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings_pythonanywhere')
```

## 📝 Proceso de actualización recomendado

### Paso 1: Actualizar código en producción

```bash
cd /home/tuusuario/censo-django
git pull origin main
```

### Paso 2: Verificar que settings de producción existe

```bash
# Si NO existe, créalo desde el ejemplo
cp censoProject/settings.example.py censoProject/settings_pythonanywhere.py

# Edita con tus configuraciones de producción
nano censoProject/settings_pythonanywhere.py
```

### Paso 3: Configuraciones específicas de producción

En `settings_pythonanywhere.py` asegúrate de tener:

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tuusuario.pythonanywhere.com']

# Database - MySQL en producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tuusuario$censodb',
        'USER': 'tuusuario',
        'PASSWORD': 'tu_password_mysql',
        'HOST': 'tuusuario.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files
STATIC_ROOT = '/home/tuusuario/censo-django/staticfiles'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/home/tuusuario/censo-django/media'
MEDIA_URL = '/media/'

# Secret key - GENERAR UNA NUEVA
SECRET_KEY = 'tu-clave-secreta-de-produccion-diferente-a-desarrollo'
```

## 🔐 Mejores prácticas de seguridad

### Opción 1: Variables de entorno (RECOMENDADO)

Crea un archivo `.env` (también ignorado por Git):

```bash
# .env (en producción)
SECRET_KEY=tu-clave-super-secreta
DATABASE_PASSWORD=tu-password-mysql
DEBUG=False
```

En `settings_pythonanywhere.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

Instala python-dotenv:
```bash
pip install python-dotenv
```

### Opción 2: Archivo de configuración JSON

```json
// config_production.json (no versionado)
{
    "secret_key": "tu-clave-secreta",
    "database_password": "tu-password",
    "debug": false
}
```

En settings:
```python
import json

with open('config_production.json') as f:
    config = json.load(f)

SECRET_KEY = config['secret_key']
DEBUG = config['debug']
```

## 🚀 Checklist de despliegue

Cada vez que despliegas a producción:

- [ ] Hacer `git pull` en el servidor
- [ ] Verificar que `settings_pythonanywhere.py` existe y está configurado
- [ ] Activar entorno virtual
- [ ] Instalar/actualizar dependencias: `pip install -r requirements.txt`
- [ ] Ejecutar migraciones: `python manage.py migrate`
- [ ] Recopilar archivos estáticos: `python manage.py collectstatic --noinput`
- [ ] Recargar aplicación web en PythonAnywhere
- [ ] Verificar logs de errores

## ⚠️ Importante

1. **NUNCA** versiones archivos con:
   - SECRET_KEY
   - Contraseñas de base de datos
   - API keys
   - Tokens de autenticación

2. **SIEMPRE** mantén backups de tus configuraciones de producción fuera del repositorio

3. **Documenta** las configuraciones necesarias en `settings.example.py`

## 🔄 Sincronización de configuraciones

Si agregas nuevas configuraciones:

1. Actualiza `settings.example.py` con la nueva configuración (con valores de ejemplo)
2. Documenta en comentarios qué debe configurarse
3. Actualiza manualmente `settings_pythonanywhere.py` en el servidor de producción

Ejemplo:

```python
# settings.example.py
# Configuración de correo electrónico
# Para Gmail: EMAIL_HOST = 'smtp.gmail.com'
# Para otro proveedor, consulta su documentación
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@example.com'
EMAIL_HOST_PASSWORD = 'tu-password-de-aplicacion'
```

## 📚 Recursos adicionales

- [Django Settings Best Practices](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [The Twelve-Factor App - Config](https://12factor.net/config)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

---

**Resumen**: No rastrear `settings.py` en Git es la **mejor práctica** y **NO afecta negativamente** el despliegue. De hecho, es más seguro y profesional. Solo asegúrate de mantener actualizados los archivos de configuración en cada entorno por separado.

