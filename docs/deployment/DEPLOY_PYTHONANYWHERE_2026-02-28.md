# 🚀 GUÍA DE DESPLIEGUE SEGURO EN PYTHONANYWHERE

**Fecha:** 28 de Febrero de 2026  
**Cambios Principales:** Instalación de argon2-cffi para resolver error de login

---

## ⚠️ IMPORTANTE - ANTES DE EMPEZAR

**ESTE DESPLIEGUE ES SEGURO** porque:
1. ✅ Solo se instaló una dependencia nueva (`argon2-cffi`)
2. ✅ No hay cambios en estructura de base de datos
3. ✅ No hay cambios en archivos de configuración críticos
4. ✅ Solo se actualizó documentación y se limpió el repositorio

---

## 📋 PASOS PARA DESPLIEGUE SEGURO

### **PASO 1: Conectar por SSH a PythonAnywhere**

Abre la consola Bash en PythonAnywhere:
- Web Dashboard → Consoles → Bash

---

### **PASO 2: Navegar al Proyecto**

```bash
cd ~/censo-django
```

---

### **PASO 3: Verificar Rama Actual**

```bash
git branch
```

**Debe mostrar:** `* development`

Si no estás en `development`, ejecuta:
```bash
git checkout development
```

---

### **PASO 4: Hacer Backup de Configuración (SEGURIDAD)**

```bash
# Backup del archivo de configuración
cp censoProject/settings_pythonanywhere.py censoProject/settings_pythonanywhere.py.backup

# Verificar que se creó el backup
ls -la censoProject/settings_pythonanywhere.py*
```

**Debes ver:**
- `settings_pythonanywhere.py`
- `settings_pythonanywhere.py.backup`

---

### **PASO 5: Sincronizar con GitHub**

```bash
# Verificar cambios remotos
git fetch origin development

# Ver diferencias antes de aplicar
git log HEAD..origin/development --oneline

# Aplicar cambios
git pull origin development
```

**Cambios que se descargarán:**
- ✅ `requirements.txt` (agregado argon2-cffi==25.1.0)
- ✅ `RESUMEN_2026-02-28.md` (nuevo)
- ✅ `VALIDACION_COMPLETA_2026-02-27.md` (nuevo)
- ✅ Archivos .md obsoletos eliminados
- ✅ Archivos CSS/JS (sin cambios críticos)

---

### **PASO 6: Activar Entorno Virtual**

```bash
# Activar entorno virtual
workon censo-env

# Verificar que estás en el entorno (debe aparecer (censo-env) al inicio)
```

---

### **PASO 7: Instalar Nueva Dependencia**

```bash
# Instalar solo la dependencia nueva
pip install argon2-cffi==25.1.0

# Verificar instalación
pip show argon2-cffi
```

**Salida esperada:**
```
Name: argon2-cffi
Version: 25.1.0
Summary: Argon2 for Python
...
```

---

### **PASO 8: Verificar Configuración de Django**

```bash
# Verificar que no hay errores de configuración
python manage.py check
```

**Salida esperada:**
```
System check identified no issues (0 silenced).
```

Si aparecen errores, **NO CONTINUAR** y revisar el error.

---

### **PASO 9: Aplicar Migraciones (SEGURIDAD)**

```bash
# Ver migraciones pendientes (si las hay)
python manage.py showmigrations

# Aplicar migraciones (debería decir "No migrations to apply")
python manage.py migrate
```

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: admin, auth, account, censoapp, ...
Running migrations:
  No migrations to apply.
```

---

### **PASO 10: Recolectar Archivos Estáticos**

```bash
# Recolectar archivos estáticos (CSS, JS, imágenes)
python manage.py collectstatic --noinput
```

**Esto copiará los archivos CSS/JS actualizados al directorio de archivos estáticos.**

---

### **PASO 11: Reiniciar Aplicación Web**

**Opción A - Desde el Dashboard Web:**
1. Ve a: Web Dashboard → Web
2. Haz clic en el botón verde **"Reload luisga64.pythonanywhere.com"**

**Opción B - Desde la Consola:**
```bash
# Tocar el archivo WSGI para forzar recarga
touch /var/www/luisga64_pythonanywhere_com_wsgi.py
```

---

### **PASO 12: Verificar que la Aplicación Funciona**

Abre tu navegador y ve a:
```
https://luisga64.pythonanywhere.com/accounts/login/
```

**Verifica:**
1. ✅ La página de login carga correctamente
2. ✅ Los estilos se ven correctos (header azul oscuro)
3. ✅ Puedes hacer login sin errores
4. ✅ El dashboard se muestra correctamente

---

## 🛡️ PLAN DE ROLLBACK (SI ALGO SALE MAL)

### **Si aparece error después del despliegue:**

#### **1. Restaurar configuración de backup:**
```bash
cd ~/censo-django
cp censoProject/settings_pythonanywhere.py.backup censoProject/settings_pythonanywhere.py
```

#### **2. Volver a versión anterior:**
```bash
# Ver commits recientes
git log --oneline -5

# Volver al commit anterior (reemplaza HASH con el hash del commit anterior)
git reset --hard HASH

# Forzar actualización
touch /var/www/luisga64_pythonanywhere_com_wsgi.py
```

#### **3. Reinstalar dependencias de versión anterior:**
```bash
pip install -r requirements.txt
```

---

## ✅ VERIFICACIONES POST-DESPLIEGUE

### **1. Verificar Login:**
```
https://luisga64.pythonanywhere.com/accounts/login/
```
✅ Debe cargar sin errores  
✅ Debe permitir login

### **2. Verificar Dashboard:**
```
https://luisga64.pythonanywhere.com/
```
✅ Debe mostrar estadísticas  
✅ Gráficos deben cargarse correctamente  
✅ Estilos corporativos aplicados

### **3. Verificar Mapas:**
```
https://luisga64.pythonanywhere.com/mapa/
https://luisga64.pythonanywhere.com/mapa/calor/
https://luisga64.pythonanywhere.com/mapa/clusters/
```
✅ Mapas deben cargar correctamente  
✅ Estilos deben verse correctos

### **4. Verificar Admin:**
```
https://luisga64.pythonanywhere.com/admin/
```
✅ Debe permitir acceso  
✅ Interface debe funcionar

---

## 📊 LOGS A REVISAR (EN CASO DE ERROR)

### **Ver logs de error de PythonAnywhere:**

En el Dashboard Web → Files → `/var/log/`:
- `luisga64.pythonanywhere.com.error.log`
- `luisga64.pythonanywhere.com.server.log`

**Buscar líneas que contengan:**
- `ERROR`
- `CRITICAL`
- `Traceback`

---

## 🆘 SOLUCIÓN DE PROBLEMAS COMUNES

### **Error: "No module named 'argon2'"**

**Solución:**
```bash
workon censo-env
pip install argon2-cffi==25.1.0
touch /var/www/luisga64_pythonanywhere_com_wsgi.py
```

---

### **Error: "ModuleNotFoundError: No module named 'django_otp'"**

**Solución:**
```bash
workon censo-env
pip install django-mfa2==2.6.0
touch /var/www/luisga64_pythonanywhere_com_wsgi.py
```

---

### **Error: "Database connection failed"**

**Verificar:**
1. Base de datos MySQL está activa
2. Credenciales en `settings_pythonanywhere.py` son correctas
3. Usuario de base de datos tiene permisos

**Comando de verificación:**
```bash
mysql -u luisga64 -p -h luisga64.mysql.pythonanywhere-services.com luisga64$censo
```

---

### **Error: "Static files not found"**

**Solución:**
```bash
cd ~/censo-django
python manage.py collectstatic --noinput
```

---

## 📝 CHECKLIST COMPLETO DE DESPLIEGUE

- [ ] **PASO 1:** Conectado por SSH a PythonAnywhere
- [ ] **PASO 2:** Navegado a `~/censo-django`
- [ ] **PASO 3:** Verificado rama `development`
- [ ] **PASO 4:** Creado backup de `settings_pythonanywhere.py`
- [ ] **PASO 5:** Ejecutado `git pull origin development`
- [ ] **PASO 6:** Activado entorno virtual `censo-env`
- [ ] **PASO 7:** Instalado `argon2-cffi==25.1.0`
- [ ] **PASO 8:** Verificado con `python manage.py check` (sin errores)
- [ ] **PASO 9:** Ejecutado `python manage.py migrate`
- [ ] **PASO 10:** Ejecutado `python manage.py collectstatic --noinput`
- [ ] **PASO 11:** Reiniciado aplicación web
- [ ] **PASO 12:** Verificado que `/accounts/login/` funciona
- [ ] **VERIFICACIÓN 1:** Dashboard carga correctamente
- [ ] **VERIFICACIÓN 2:** Estilos se ven correctos
- [ ] **VERIFICACIÓN 3:** Login funciona sin errores
- [ ] **VERIFICACIÓN 4:** Mapas funcionan correctamente
- [ ] **VERIFICACIÓN 5:** Admin accesible

---

## ✅ RESULTADO ESPERADO

Después del despliegue:
1. ✅ Sistema de login funcional (error de Argon2 resuelto)
2. ✅ Todas las funcionalidades operativas
3. ✅ Estilos corporativos aplicados
4. ✅ Sin cambios en base de datos
5. ✅ Sin cambios en configuración crítica

---

## 📞 CONTACTO EN CASO DE EMERGENCIA

Si algo sale mal durante el despliegue:
1. **DETENTE inmediatamente**
2. **NO hagas más cambios**
3. **Aplica el Plan de Rollback** (sección anterior)
4. **Documenta el error** (copia los logs)
5. **Revisa los logs** en `/var/log/`

---

## 🎯 COMANDOS RÁPIDOS DE DESPLIEGUE

**Para copiar y pegar en PythonAnywhere Bash:**

```bash
# Navegar al proyecto
cd ~/censo-django

# Backup de configuración
cp censoProject/settings_pythonanywhere.py censoProject/settings_pythonanywhere.py.backup

# Sincronizar con GitHub
git pull origin development

# Activar entorno virtual
workon censo-env

# Instalar dependencia nueva
pip install argon2-cffi==25.1.0

# Verificar configuración
python manage.py check

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Reiniciar aplicación
touch /var/www/luisga64_pythonanywhere_com_wsgi.py

# Verificar en navegador
echo "Visita: https://luisga64.pythonanywhere.com/accounts/login/"
```

---

**✅ Despliegue preparado y documentado. Sigue los pasos y todo funcionará correctamente.**

**Última actualización:** 28 de Febrero de 2026  
**Validado por:** Sistema de Validación Automática

