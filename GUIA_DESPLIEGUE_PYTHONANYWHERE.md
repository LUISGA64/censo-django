# 🚀 Guía Completa de Despliegue en PythonAnywhere

**Fecha:** 23 de diciembre de 2024  
**Versión del Sistema:** 1.0 - Demo para Cabildos  
**Plataforma:** PythonAnywhere (Plan Gratuito)

---

## 📋 **PARTE 1: PREPARACIÓN (Antes de empezar)**

### ✅ Checklist Previo
- [x] Base de datos limpia y probada
- [x] Carga masiva funcionando
- [x] Requirements.txt actualizado
- [ ] Cuenta en PythonAnywhere creada
- [ ] Repositorio en GitHub actualizado

---

## 🔧 **PARTE 2: CREAR CUENTA EN PYTHONANYWHERE**

### Paso 1: Registro
1. Ir a: https://www.pythonanywhere.com
2. Click en **"Pricing & signup"**
3. Seleccionar **"Create a Beginner account"** (GRATIS)
4. Llenar el formulario:
   - Username: `censoindigenademo` (o el que prefieras)
   - Email: tu email
   - Password: contraseña segura
5. Confirmar email

### Paso 2: Características del Plan Gratuito
✅ 512 MB de espacio en disco
✅ 1 aplicación web
✅ MySQL database incluida
✅ Subdominio: `censoindigenademo.pythonanywhere.com`
✅ HTTPS automático
✅ Suficiente para demos

---

## 📦 **PARTE 3: SUBIR EL CÓDIGO**

### Opción A: Desde GitHub (Recomendado)

#### 1. Subir código a GitHub
```powershell
# En tu PC local
cd C:\Users\LENOVO\PycharmProjects\censo-django

# Asegurar que estés en la rama correcta
git status

# Agregar cambios pendientes
git add .
git commit -m "Preparado para despliegue PythonAnywhere v1.0"
git push origin main
```

#### 2. En PythonAnywhere - Consola Bash
```bash
# Abrir nueva consola Bash desde el dashboard
# Clonar repositorio
git clone https://github.com/LUISGA64/censo-django.git
cd censo-django

# ⚠️ IMPORTANTE: Cambiar a la rama development
git checkout development
git pull origin development

# Verificar que estás en la rama correcta
git branch
# Debe mostrar: * development

# Verificar que existen los archivos necesarios
ls requirements.txt
ls censoProject/settings_pythonanywhere.py
```

### Opción B: Subir archivos ZIP
1. Comprimir carpeta del proyecto
2. En PythonAnywhere → Files → Upload
3. Descomprimir desde consola Bash

---

## 🐍 **PARTE 4: CONFIGURAR ENTORNO VIRTUAL**

```bash
# En consola Bash de PythonAnywhere

# Crear entorno virtual con Python 3.10
mkvirtualenv censo-env --python=/usr/bin/python3.10

# Activar entorno
workon censo-env

# Navegar al proyecto
cd censo-django

# Instalar dependencias
pip install -r requirements.txt

# Si hay errores con WeasyPrint, instalar sin ella primero
pip install -r requirements.txt --ignore-installed weasyprint
```

---

## 🗄️ **PARTE 5: CONFIGURAR BASE DE DATOS MySQL**

### Paso 1: Crear Base de Datos
1. Dashboard → Databases
2. Click en **"Initialize MySQL"**
3. Establecer password de MySQL
4. Anotar:
   - Host: `TU_USERNAME.mysql.pythonanywhere-services.com`
   - Database name: `TU_USERNAME$censodb`
   - Username: `TU_USERNAME`
   - Password: el que estableciste

### Paso 2: Crear archivo .env
```bash
# En consola Bash
cd ~/censo-django
nano .env
```

Contenido del archivo `.env`:
```ini
# Database
DB_NAME=censoindigenademo$censodb
DB_USER=censoindigenademo
DB_PASSWORD=TU_PASSWORD_MYSQL
DB_HOST=censoindigenademo.mysql.pythonanywhere-services.com
DB_PORT=3306

# Django
SECRET_KEY=genera-una-clave-secreta-nueva-aqui
DEBUG=False
ALLOWED_HOSTS=censoindigenademo.pythonanywhere.com

# Media y Static
MEDIA_ROOT=/home/censoindigenademo/censo-django/media
STATIC_ROOT=/home/censoindigenademo/censo-django/staticfiles

# Redis (deshabilitado en plan gratuito)
REDIS_ENABLED=False
```

Guardar: `Ctrl+O`, Enter, `Ctrl+X`

### Paso 3: Generar SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copiar el resultado y actualizar en `.env`

---

## ⚙️ **PARTE 6: ACTUALIZAR SETTINGS.PY**

El archivo `settings_pythonanywhere.py` ya está creado y listo.

---

## 🔄 **PARTE 7: MIGRACIONES Y DATOS INICIALES**

```bash
# Activar entorno
workon censo-env
cd ~/censo-django

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
# Username: admin
# Email: tu_email@example.com
# Password: (contraseña segura)

# Cargar datos iniciales (catálogos)
python manage.py loaddata censoapp/fixtures/initial_data.json

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

---

## 🌐 **PARTE 8: CONFIGURAR WEB APP**

### Paso 1: Crear Web App
1. Dashboard → Web
2. Click en **"Add a new web app"**
3. Seleccionar dominio: `censoindigenademo.pythonanywhere.com`
4. Framework: **Manual configuration**
5. Python version: **Python 3.10**

### Paso 2: Configurar WSGI
1. En la página Web → sección **Code**
2. Click en el archivo WSGI
3. **BORRAR TODO** y reemplazar con:

```python
import os
import sys

# Añadir el directorio del proyecto al path
path = '/home/censoindigenademo/censo-django'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'

# Activar entorno virtual
activate_this = '/home/censoindigenademo/.virtualenvs/censo-env/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Importar aplicación Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Guardar cambios.

### Paso 3: Configurar Virtual Environment
1. En sección **Virtualenv**:
2. Path: `/home/censoindigenademo/.virtualenvs/censo-env`

### Paso 4: Configurar Static Files
En sección **Static files**:

| URL | Directory |
|-----|-----------|
| /static/ | /home/censoindigenademo/censo-django/staticfiles |
| /media/ | /home/censoindigenademo/censo-django/media |

### Paso 5: Recargar Web App
Click en el botón verde **"Reload censoindigenademo.pythonanywhere.com"**

---

## 🧪 **PARTE 9: VERIFICACIÓN**

### Paso 1: Verificar la aplicación
1. Ir a: `https://censoindigenademo.pythonanywhere.com`
2. Verificar que carga la página de login

### Paso 2: Verificar Admin
1. Ir a: `https://censoindigenademo.pythonanywhere.com/admin`
2. Login con superusuario creado

### Paso 3: Crear datos de prueba
1. Crear Asociación
2. Crear Organización
3. Crear Usuario con perfil
4. Probar carga masiva

### Paso 4: Ver Logs (si hay errores)
Dashboard → Web → Log files:
- Error log
- Server log
- Access log

---

## 📊 **PARTE 10: DATOS INICIALES PARA DEMO**

### Opción A: Desde Admin
Crear manualmente:
1. Asociación de prueba
2. Organización de prueba  
3. Usuarios

### Opción B: Cargar datos desde script
```bash
workon censo-env
cd ~/censo-django
python manage.py shell

# Ejecutar script de datos demo
exec(open('crear_datos_demo.py').read())
```

---

## 🔧 **COMANDOS ÚTILES**

### Ver logs en tiempo real
```bash
tail -f /var/log/censoindigenademo.pythonanywhere.com.error.log
```

### Reiniciar aplicación
```bash
touch /var/www/censoindigenademo_pythonanywhere_com_wsgi.py
```

### Actualizar código desde GitHub
```bash
cd ~/censo-django
git checkout development
git pull origin development
python manage.py migrate
python manage.py collectstatic --noinput
# Reload desde dashboard Web
```

---

## ⚠️ **LIMITACIONES DEL PLAN GRATUITO**

1. ❌ **No Redis** - Cache en memoria local
2. ❌ **No tareas programadas** (scheduled tasks)
3. ❌ **512 MB espacio** - Suficiente para demo
4. ❌ **Dominio fijo** - No puedes usar dominio personalizado
5. ✅ **MySQL incluido** - Base de datos persistente
6. ✅ **HTTPS automático**

---

## 🆙 **ACTUALIZAR LA APLICACIÓN**

Cuando hagas cambios en tu código local:

```bash
# En tu PC
git add .
git commit -m "Descripción de cambios"
git push origin development

# En PythonAnywhere Bash
cd ~/censo-django
git checkout development
git pull origin development
workon censo-env
pip install -r requirements.txt  # Si hay nuevas dependencias
python manage.py migrate  # Si hay nuevas migraciones
python manage.py collectstatic --noinput  # Si cambiaron archivos estáticos

# Luego en Dashboard → Web → Reload
```

---

## 🎯 **CREDENCIALES PARA COMPARTIR CON CABILDOS**

### URL de la aplicación:
```
https://censoindigenademo.pythonanywhere.com
```

### Usuario de prueba (crear después):
```
Usuario: demo_cabildo
Contraseña: (la que definas)
Organización: (nombre del cabildo de prueba)
```

---

## 📞 **SOPORTE**

### Si algo falla:

1. **Revisar logs:**
   - Dashboard → Web → Error log
   - Dashboard → Web → Server log

2. **Consola Python:**
   ```bash
   workon censo-env
   python manage.py check
   python manage.py check --deploy
   ```

3. **Verificar configuración:**
   ```bash
   python manage.py diffsettings
   ```

---

## ✅ **CHECKLIST FINAL**

- [ ] Cuenta PythonAnywhere creada
- [ ] Código subido (GitHub o ZIP)
- [ ] Entorno virtual configurado
- [ ] Dependencias instaladas
- [ ] Base de datos MySQL creada
- [ ] Archivo .env configurado
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recolectados
- [ ] Web app configurada
- [ ] WSGI configurado
- [ ] Static files mapeados
- [ ] Aplicación recargada
- [ ] Sitio accesible desde navegador
- [ ] Admin funcional
- [ ] Datos de prueba cargados
- [ ] Carga masiva probada

---

## 🎉 **¡LISTO PARA MOSTRAR A LOS CABILDOS!**

Tu aplicación estará disponible en:
**https://TU_USERNAME.pythonanywhere.com**

Duración: Ilimitada (mientras mantengas la cuenta activa)
Costo: $0 USD

---

**Próximo paso:** Crear datos de demo y compartir URL con los cabildos.

