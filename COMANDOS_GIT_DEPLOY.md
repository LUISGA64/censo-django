# 🚀 Comandos para Git y Deploy a PythonAnywhere

## 📦 1. Subir al Repositorio Git

### Verificar el estado
```bash
git status
```

### Agregar todos los cambios
```bash
git add .
```

### Crear commit
```bash
git commit -m "chore: limpieza masiva del proyecto - eliminados 3215+ archivos innecesarios"
```

### Subir al repositorio
```bash
git push origin main
```

---

## 🔧 2. Preparación para PythonAnywhere

### 2.1 En tu repositorio Git
Asegúrate de que tu repositorio esté actualizado:
```bash
git push origin main
```

### 2.2 En PythonAnywhere - Consola Bash

#### Clonar o actualizar repositorio
```bash
# Si es la primera vez
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git censo-django
cd censo-django

# Si ya existe
cd censo-django
git pull origin main
```

#### Crear entorno virtual
```bash
python3.10 -m venv venv
source venv/bin/activate
```

#### Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp .env.pythonanywhere.example .env

# Editar con nano o vi
nano .env
```

**Variables importantes:**
```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
ALLOWED_HOSTS=tuusuario.pythonanywhere.com
DATABASE_URL=sqlite:///db.censo_Web
```

#### Ejecutar migraciones
```bash
python manage.py migrate
```

#### Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

#### Crear superusuario (si es necesario)
```bash
python manage.py createsuperuser
```

---

## 🌐 3. Configurar Web App en PythonAnywhere

### 3.1 En la pestaña "Web"

1. **Add a new web app**
2. Seleccionar **Manual configuration**
3. Seleccionar **Python 3.10**

### 3.2 Configurar WSGI

Editar el archivo WSGI (`/var/www/tuusuario_pythonanywhere_com_wsgi.py`):

```python
import os
import sys

# Agregar el directorio del proyecto al path
path = '/home/tuusuario/censo-django'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings'

# Importar la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 3.3 Configurar Virtual Environment

En la sección "Virtualenv":
```
/home/tuusuario/censo-django/venv
```

### 3.4 Configurar Static Files

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuusuario/censo-django/staticfiles/` |
| `/media/` | `/home/tuusuario/censo-django/media/` |

### 3.5 Recargar la aplicación

Click en el botón verde **"Reload tuusuario.pythonanywhere.com"**

---

## ✅ 4. Verificación

### Verificar que todo funcione:
1. Visita: `https://tuusuario.pythonanywhere.com`
2. Verifica que los estilos se carguen correctamente
3. Prueba el login
4. Verifica las funcionalidades principales

### Ver logs de errores:
```bash
# En PythonAnywhere Bash console
tail -f /var/log/tuusuario.pythonanywhere.com.error.log
```

---

## 🔄 5. Actualización Rápida (Deploy continuo)

### En tu máquina local:
```bash
# 1. Hacer cambios en el código
# 2. Commit y push
git add .
git commit -m "descripción de los cambios"
git push origin main
```

### En PythonAnywhere Bash:
```bash
cd ~/censo-django
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # Si hay nuevas dependencias
python manage.py migrate  # Si hay nuevas migraciones
python manage.py collectstatic --noinput  # Si hay cambios en static
```

### Recargar la web app:
- Ir a la pestaña "Web"
- Click en **"Reload"**

---

## 🛠️ 6. Comandos Útiles

### Verificar versiones
```bash
python --version
pip --version
django-admin --version
```

### Limpiar cache
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Backup de base de datos
```bash
cp db.censo_Web backups/db.censo_Web.$(date +%Y%m%d_%H%M%S).backup
```

### Ver espacio en disco
```bash
du -sh ~/censo-django
```

---

## ⚠️ Troubleshooting

### Error: "No module named 'censoProject'"
- Verifica el path en el archivo WSGI
- Asegúrate de que el virtualenv esté configurado correctamente

### Estilos no cargan
```bash
python manage.py collectstatic --noinput
```
- Verifica la configuración de Static Files en la pestaña Web

### Error 500
- Revisa los logs: `tail -f /var/log/tuusuario.pythonanywhere.com.error.log`
- Verifica las variables de entorno en `.env`
- Asegúrate de que `DEBUG=False` en producción

### Base de datos bloqueada
```bash
# Reinicia la web app desde la pestaña Web
# O elimina el archivo .lock si existe
rm db.censo_Web-journal
```

---

## 📞 Soporte

- **Documentación PythonAnywhere:** https://help.pythonanywhere.com/
- **Foros Django:** https://forum.djangoproject.com/
- **Stack Overflow:** Tag `django` y `pythonanywhere`

---

**Última actualización:** 2026-04-27

