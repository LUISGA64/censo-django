# ✅ Configuración Compatible con PythonAnywhere

## 📋 Resumen

El proyecto **ya está completamente configurado** para PythonAnywhere. Se ha actualizado el archivo `settings_pythonanywhere.py` con todas las configuraciones necesarias.

---

## 🔧 Cambios Realizados en `settings_pythonanywhere.py`

### ✅ **1. Configuración Básica**
- ✅ `SECRET_KEY` desde variables de entorno
- ✅ `DEBUG = False` para producción
- ✅ `ALLOWED_HOSTS` configurado para PythonAnywhere
- ✅ `SITE_URL` para códigos QR y verificación de documentos

### ✅ **2. Apps Instaladas**
Se incluyeron **todas** las apps necesarias:
- ✅ Django core apps
- ✅ AllAuth (autenticación)
- ✅ REST Framework
- ✅ Crispy Forms
- ✅ CORS Headers
- ✅ Simple History
- ✅ Form Tools
- ✅ censoapp

### ✅ **3. Middleware**
- ✅ OrganizationFilterMiddleware (multi-organización)
- ✅ AllAuth middleware
- ✅ Simple History middleware

### ✅ **4. Templates**
- ✅ Context processors completos
- ✅ Backends de autenticación (Django + AllAuth)

### ✅ **5. Base de Datos**
- ✅ **SQLite** configurado (ideal para demo)
- ✅ MySQL comentado (para producción futura)

### ✅ **6. Archivos Estáticos y Media**
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### ✅ **7. Cache y Sesiones**
- ✅ Cache en memoria local (Redis no disponible en plan gratuito)
- ✅ Sesiones en base de datos (más confiable)

### ✅ **8. REST Framework**
- ✅ CoreAPI para schema (compatible con tu código)
- ✅ Django Filters
- ✅ Paginación configurada

### ✅ **9. Logging**
- ✅ Logs en archivo `django.log`
- ✅ Console logging para debug

---

## 🚀 Pasos para Despliegue en PythonAnywhere

### **1. Crear directorios necesarios**
```bash
# En la consola Bash de PythonAnywhere
cd ~/censo-django
mkdir -p static
mkdir -p staticfiles
mkdir -p media
mkdir -p media/documents
mkdir -p media/photos
mkdir -p media/temp
chmod 755 static staticfiles media
chmod -R 755 media/*
```

### **2. Configurar variables de entorno** *(Opcional)*
Editar: `/home/luisga64/.bashrc` o crear archivo `.env`
```bash
export SECRET_KEY='tu-secret-key-super-segura-aqui'
export DEBUG='False'
export ALLOWED_HOSTS='luisga64.pythonanywhere.com'
export SITE_URL='https://luisga64.pythonanywhere.com'
```

### **3. Instalar dependencias**
```bash
workon censo-env
pip install -r requirements.txt
```

### **4. Migraciones**
```bash
python manage.py migrate --settings=censoProject.settings_pythonanywhere
```

### **5. Recolectar archivos estáticos**
```bash
python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere
```

### **6. Crear datos de demo**
```bash
python crear_datos_demo.py
```

### **7. Configurar WSGI**
Editar: `/var/www/luisga64_pythonanywhere_com_wsgi.py`
```python
import os
import sys

# Añadir el directorio del proyecto
path = '/home/luisga64/censo-django'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'

# Importar la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### **8. Configurar archivos estáticos en Web Tab**
En el dashboard de PythonAnywhere → **Web** → **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/luisga64/censo-django/staticfiles` |
| `/media/` | `/home/luisga64/censo-django/media` |

### **9. Recargar la aplicación**
Click en el botón verde **Reload** en la pestaña Web.

---

## 🔐 Credenciales de Acceso Demo

Después de ejecutar `crear_datos_demo.py`:

### **👨‍💼 Administrador**
- **Usuario:** `admin_cabildo`
- **Password:** `Demo2024!`
- **Rol:** Administrador de Organización

### **👁️ Consulta**
- **Usuario:** `consulta_cabildo`
- **Password:** `Consulta2024!`
- **Rol:** Solo Consulta

---

## 📊 Estructura de Directorios

```
/home/luisga64/censo-django/
├── censoapp/
├── censoProject/
│   ├── settings.py (desarrollo)
│   ├── settings_pythonanywhere.py ✅ (producción)
│   └── wsgi.py
├── templates/
├── static/ (archivos fuente)
├── staticfiles/ (archivos recolectados) ✅
├── media/ (archivos subidos) ✅
├── db.censo_Web (base de datos SQLite)
├── manage.py
└── requirements.txt
```

---

## ⚠️ Notas Importantes

### **Diferencias con `settings.py` (desarrollo)**

| Característica | Desarrollo | PythonAnywhere |
|---------------|------------|----------------|
| DEBUG | True | False |
| ALLOWED_HOSTS | [] | ['luisga64...'] |
| Database | SQLite local | SQLite (demo) / MySQL (producción) |
| Cache | Redis (si disponible) | Local Memory |
| Sesiones | Database | Database |
| STATIC_ROOT | No definido | `/staticfiles` ✅ |
| Email | Console | Console (demo) |

### **¿Por qué SQLite para la demo?**
- ✅ **Más simple** de configurar
- ✅ **No requiere** configuración de MySQL
- ✅ **Ideal para demos** con datos limitados
- ✅ **Fácil de migrar** a MySQL después

### **Migrar a MySQL después**
Solo descomenta la configuración MySQL en `settings_pythonanywhere.py` y ejecuta:
```bash
python manage.py migrate --settings=censoProject.settings_pythonanywhere
```

---

## ✅ Checklist de Verificación

Antes de mostrar a los cabildos:

- [ ] Directorios `static`, `staticfiles`, `media` creados
- [ ] Migraciones aplicadas
- [ ] `collectstatic` ejecutado
- [ ] Datos de demo creados
- [ ] WSGI configurado correctamente
- [ ] Static files configurados en Web Tab
- [ ] Aplicación recargada
- [ ] Login funciona correctamente
- [ ] Dashboard muestra estadísticas
- [ ] Carga masiva funciona
- [ ] Generación de documentos funciona
- [ ] Plantillas personalizables funcionan

---

## 🆘 Solución de Problemas

### **Error: `STATIC_ROOT` not set**
```bash
# Crear el directorio
mkdir -p ~/censo-django/staticfiles
python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere
```

### **Error: No module named 'censoProject'**
Verificar que el path esté en WSGI:
```python
path = '/home/luisga64/censo-django'
if path not in sys.path:
    sys.path.insert(0, path)
```

### **Login no funciona (se queda cargando)**
Verificar en `settings_pythonanywhere.py`:
```python
SESSION_ENGINE = "django.contrib.sessions.backends.db"
```

### **Static files no cargan**
Verificar configuración en Web Tab:
- URL: `/static/`
- Directory: `/home/luisga64/censo-django/staticfiles`

---

## 🎯 Resultado Final

Después de seguir estos pasos, tendrás:

✅ **Aplicación funcionando** en: `https://luisga64.pythonanywhere.com`
✅ **Datos de demo** listos para mostrar
✅ **Todas las funcionalidades** operativas
✅ **Lista para presentar** a los cabildos

---

## 📝 Siguientes Pasos

1. **Mostrar a los cabildos** la demo
2. **Recopilar feedback**
3. **Ajustar según necesidades**
4. **Migrar a MySQL** si se requiere más capacidad
5. **Implementar backups** automáticos

---

**Fecha de actualización:** 23 de diciembre de 2024
**Configurado por:** Sistema de Censo Django
**Versión:** 1.0 Demo

