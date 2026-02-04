# 🗄️ CONFIGURACIÓN DE MYSQL EN PYTHONANYWHERE

## ✅ CONFIGURACIÓN ACTUALIZADA

La configuración de base de datos ahora cambia automáticamente:

- **Desarrollo (DEBUG=True):** Usa SQLite
- **Producción (DEBUG=False):** Usa MySQL

---

## 📋 PASOS PARA CONFIGURAR MYSQL EN PYTHONANYWHERE

### 1. Crear Base de Datos MySQL

1. **Acceder a PythonAnywhere**
   - Login en https://www.pythonanywhere.com/

2. **Ir a la sección Databases**
   - En el menú superior → **Databases**

3. **Inicializar MySQL** (si es primera vez)
   - Click en **"Initialize MySQL"**
   - Establecer password de MySQL
   - **IMPORTANTE:** Guardar este password, lo necesitarás después

4. **Crear Base de Datos**
   - En la sección "Create a new database"
   - Nombre: `tuusuario$censodb` (reemplazar "tuusuario" con tu username)
   - Click en **"Create"**

5. **Anotar Credenciales**
   ```
   Database name: tuusuario$censodb
   Username: tuusuario
   Password: (el que estableciste)
   Host: tuusuario.mysql.pythonanywhere-services.com
   Port: 3306
   ```

---

### 2. Configurar Variables de Entorno (.env)

En PythonAnywhere, editar el archivo `.env`:

```bash
# Conectar a PythonAnywhere bash console
cd ~/censo-django
nano .env
```

**Agregar/actualizar estas líneas:**

```bash
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=False
ALLOWED_HOSTS=tuusuario.pythonanywhere.com

# MySQL Database - REEMPLAZAR CON TUS DATOS
DB_NAME=tuusuario$censodb
DB_USER=tuusuario
DB_PASSWORD=tu_password_mysql_aqui
DB_HOST=tuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Site
SITE_URL=https://tuusuario.pythonanywhere.com
```

**Guardar:** Ctrl+X → Y → Enter

---

### 3. Verificar Conexión a MySQL

```bash
# Test de conexión
mysql -u tuusuario -p -h tuusuario.mysql.pythonanywhere-services.com tuusuario$censodb

# Si conecta, deberías ver:
# MySQL [(tuusuario$censodb)]>

# Salir:
exit
```

---

### 4. Ejecutar Migraciones

```bash
cd ~/censo-django
workon censo-env

# Verificar que Django puede conectar a MySQL
python manage.py check

# Ejecutar migraciones
python manage.py migrate

# Resultado esperado:
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, sessions, censoapp...
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   ...
```

---

### 5. Crear Superusuario (si es nueva base de datos)

```bash
python manage.py createsuperuser

# Seguir instrucciones:
# Username: admin
# Email: tu_email@example.com
# Password: (contraseña segura)
```

---

### 6. Recargar Web App

```bash
# Opción 1: Desde consola
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py

# Opción 2: Desde interfaz web
# Web → Click en botón verde "Reload tuusuario.pythonanywhere.com"
```

---

## ✅ VERIFICAR QUE FUNCIONA

### Verificación 1: Django Check
```bash
python manage.py check
# Debe mostrar: System check identified no issues (0 silenced).
```

### Verificación 2: Conectar a MySQL
```bash
python manage.py dbshell
# Debe abrir shell de MySQL

# Probar query:
SHOW TABLES;

# Debe mostrar tablas de Django
# Salir:
exit
```

### Verificación 3: Acceder al Sitio
```
https://tuusuario.pythonanywhere.com/
```

**Debe cargar correctamente**

---

## 🔧 MIGRAR DATOS DE SQLITE A MYSQL (Opcional)

Si ya tienes datos en SQLite y quieres migrarlos a MySQL:

### Opción A: Exportar/Importar con fixtures

```bash
# 1. En local (con SQLite), exportar datos
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude=contenttypes --exclude=auth.Permission \
  -o data_backup.json

# 2. Copiar data_backup.json a PythonAnywhere
# Usar Files → Upload o scp

# 3. En PythonAnywhere (con MySQL), importar datos
python manage.py loaddata data_backup.json
```

### Opción B: Backup/Restore manual

```bash
# 1. Hacer backup de SQLite
python manage.py backup_db --compress

# 2. Configurar MySQL
# (seguir pasos anteriores)

# 3. Usar herramienta de migración
# O recrear datos manualmente
```

---

## ⚠️ TROUBLESHOOTING

### Error: "Access denied for user"

**Causa:** Credenciales incorrectas en .env

**Solución:**
```bash
# Verificar .env
cat ~/censo-django/.env | grep DB_

# Verificar que coinciden con PythonAnywhere → Databases
```

### Error: "Can't connect to MySQL server"

**Causa:** HOST incorrecto

**Solución:**
```bash
# El HOST debe ser:
DB_HOST=tuusuario.mysql.pythonanywhere-services.com

# NO debe ser:
# DB_HOST=localhost
# DB_HOST=127.0.0.1
```

### Error: "Unknown database"

**Causa:** Base de datos no existe

**Solución:**
```bash
# Crear base de datos en PythonAnywhere → Databases
# Nombre exacto: tuusuario$censodb
```

### Error: "No module named MySQLdb"

**Causa:** mysqlclient no instalado

**Solución:**
```bash
workon censo-env
pip install mysqlclient
```

---

## 📊 VERIFICAR CONFIGURACIÓN ACTUAL

### Comando para ver qué base de datos se está usando:

```bash
python manage.py shell

# En el shell:
from django.conf import settings
print(settings.DATABASES['default'])

# Debe mostrar:
# Si DEBUG=False → MySQL
# Si DEBUG=True → SQLite
```

---

## 🎯 RESUMEN

**Configuración Automática:**
- ✅ **Desarrollo local:** SQLite (DEBUG=True)
- ✅ **Producción PythonAnywhere:** MySQL (DEBUG=False)

**Archivo .env en PythonAnywhere debe tener:**
```bash
DEBUG=False
DB_NAME=tuusuario$censodb
DB_USER=tuusuario
DB_PASSWORD=tu_password_mysql
DB_HOST=tuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

**Comandos clave:**
```bash
# Verificar conexión
python manage.py check

# Ver qué BD se usa
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES)"

# Ejecutar migraciones
python manage.py migrate

# Recargar web app
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py
```

---

**¡MySQL configurado correctamente! 🎉**
