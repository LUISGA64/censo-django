# 🚀 Despliegue Rápido en PythonAnywhere - Pasos Esenciales

## ⏱️ Tiempo estimado: 30-45 minutos

---

## 1️⃣ CREAR CUENTA (5 min)

1. Ir a: https://www.pythonanywhere.com
2. **"Pricing & signup"** → **"Create a Beginner account"** (GRATIS)
3. Username: `censoindigenademo` (o el que prefieras)
4. Confirmar email

---

## 2️⃣ SUBIR CÓDIGO (5 min)

### Opción A: Desde tu PC - Subir a GitHub primero
```powershell
cd C:\Users\LENOVO\PycharmProjects\censo-django
git add .
git commit -m "Deploy PythonAnywhere v1.0"
git push origin main
```

### En PythonAnywhere - Consola Bash
```bash
git clone https://github.com/TU_USUARIO/censo-django.git
cd censo-django
```

---

## 3️⃣ ENTORNO VIRTUAL (5 min)

```bash
mkvirtualenv censo-env --python=/usr/bin/python3.10
workon censo-env
cd censo-django
pip install -r requirements.txt
```

---

## 4️⃣ BASE DE DATOS MySQL (10 min)

### Crear BD
- Dashboard → **Databases** → **"Initialize MySQL"**
- Establecer password y anotar credenciales

### Crear archivo .env
```bash
cd ~/censo-django
nano .env
```

Contenido (ajustar con TUS datos):
```ini
DB_NAME=TU_USERNAME$censodb
DB_USER=TU_USERNAME
DB_PASSWORD=TU_PASSWORD_MYSQL
DB_HOST=TU_USERNAME.mysql.pythonanywhere-services.com
DB_PORT=3306

SECRET_KEY=GENERAR_NUEVA_CLAVE
DEBUG=False
ALLOWED_HOSTS=TU_USERNAME.pythonanywhere.com

MEDIA_ROOT=/home/TU_USERNAME/censo-django/media
STATIC_ROOT=/home/TU_USERNAME/censo-django/staticfiles
```

### Generar SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copiar resultado en .env

Guardar: `Ctrl+O`, Enter, `Ctrl+X`

---

## 5️⃣ MIGRACIONES (5 min)

```bash
workon censo-env
cd ~/censo-django

python manage.py migrate
python manage.py createsuperuser
# Username: admin | Email: tu@email.com | Password: (segura)

python manage.py loaddata censoapp/fixtures/initial_data.json
python manage.py collectstatic --noinput
```

---

## 6️⃣ CONFIGURAR WEB APP (10 min)

### Crear Web App
- Dashboard → **Web** → **"Add a new web app"**
- Dominio: `TU_USERNAME.pythonanywhere.com`
- Framework: **Manual configuration**
- Python: **3.10**

### Configurar WSGI
Click en archivo WSGI, **BORRAR TODO** y poner:

```python
import os
import sys

path = '/home/TU_USERNAME/censo-django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'

activate_this = '/home/TU_USERNAME/.virtualenvs/censo-env/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Configurar Virtualenv
Path: `/home/TU_USERNAME/.virtualenvs/censo-env`

### Configurar Static Files

| URL | Directory |
|-----|-----------|
| /static/ | /home/TU_USERNAME/censo-django/staticfiles |
| /media/ | /home/TU_USERNAME/censo-django/media |

### Recargar
Botón verde: **"Reload TU_USERNAME.pythonanywhere.com"**

---

## 7️⃣ CREAR DATOS DEMO (5 min)

```bash
workon censo-env
cd ~/censo-django
python crear_datos_demo.py
```

---

## 8️⃣ VERIFICAR (2 min)

1. Ir a: `https://TU_USERNAME.pythonanywhere.com`
2. Login con: `admin_cabildo` / `Demo2024!`
3. ¡Listo! 🎉

---

## 🔑 CREDENCIALES PARA CABILDOS

**URL:** `https://TU_USERNAME.pythonanywhere.com`

**Usuario Admin:**
- Username: `admin_cabildo`
- Password: `Demo2024!`

**Usuario Consulta:**
- Username: `consulta_cabildo`
- Password: `Consulta2024!`

---

## 🆘 SI HAY ERRORES

Ver logs:
- Dashboard → Web → Error log
- Dashboard → Web → Server log

Comandos útiles:
```bash
workon censo-env
cd ~/censo-django
python manage.py check
python manage.py check --deploy
```

---

## 🔄 ACTUALIZAR DESPUÉS

```bash
cd ~/censo-django
git pull origin main
workon censo-env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Dashboard → Web → Reload
```

---

## ✅ LISTO PARA DEMO

- URL pública con HTTPS ✅
- Base de datos persistente ✅
- Usuarios de prueba creados ✅
- Costo: $0 USD ✅

**¡Comparte la URL con los cabildos!** 🎉

