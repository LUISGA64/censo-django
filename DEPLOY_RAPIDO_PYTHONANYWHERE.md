# 🚀 GUÍA RÁPIDA: Actualizar Producción en PythonAnywhere

## ⚡ Opción 1: Usar el Script Automático (RECOMENDADO)

### Paso 1: Conectar a PythonAnywhere
1. Ir a: https://www.pythonanywhere.com
2. Iniciar sesión
3. Click en **"Consoles"** (menú superior)
4. Click en **"Bash"** (o abrir console existente)

### Paso 2: Subir el Script
**En tu PC local (PowerShell):**
```powershell
# Nota: El script ya está creado en:
# C:\Users\luisg\PycharmProjects\censo-django\deploy_pythonanywhere.sh
```

**En PythonAnywhere Bash Console:**
```bash
# Ir al directorio
cd /home/luisga64/censo-django

# Crear el script
nano deploy_pythonanywhere.sh

# Pegar el contenido del script (copiar de deploy_pythonanywhere.sh)
# Guardar: Ctrl+O, Enter, Ctrl+X

# Dar permisos de ejecución
chmod +x deploy_pythonanywhere.sh

# Ejecutar
./deploy_pythonanywhere.sh
```

### Paso 3: Recargar Aplicación
1. Ir a pestaña **"Web"**
2. Click en botón verde **"Reload luisga64.pythonanywhere.com"**
3. Esperar 15-20 segundos
4. Visitar: https://luisga64.pythonanywhere.com

---

## 🔧 Opción 2: Comandos Manuales (Paso a Paso)

Si prefieres ejecutar los comandos uno por uno:

### En PythonAnywhere Bash Console:

```bash
# 1. Ir al proyecto
cd /home/luisga64/censo-django

# 2. Cambiar a master
git checkout master

# 3. Pull de cambios
git pull origin master

# 4. Activar virtualenv
source /home/luisga64/.virtualenvs/venv/bin/activate

# 5. Configurar settings
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere

# 6. Verificar versión
cat VERSION
# Debe mostrar: 2.1.0

# 7. Instalar dependencias
pip install -r requirements.txt

# 8. Ejecutar migraciones
python manage.py migrate

# 9. Recolectar estáticos
python manage.py collectstatic --noinput

# 10. Verificar configuración
python manage.py check --deploy
```

### Después de ejecutar los comandos:
1. Ir a **Web tab**
2. Click en **"Reload"**
3. Verificar sitio

---

## 📋 Checklist de Verificación

### Antes de Actualizar:
- [ ] Backup de base de datos realizado (opcional pero recomendado)
- [ ] Archivo .env existe en `/home/luisga64/censo-django/.env`
- [ ] python-decouple instalado
- [ ] Variables de entorno correctas en .env

### Durante la Actualización:
- [ ] git checkout master ejecutado
- [ ] git pull origin master ejecutado
- [ ] Sin errores en pip install
- [ ] Migraciones aplicadas sin errores
- [ ] Collectstatic completado
- [ ] check --deploy sin warnings críticos

### Después de Actualizar:
- [ ] Aplicación recargada (botón Reload)
- [ ] Sitio carga correctamente
- [ ] Login funciona
- [ ] Mapas cargan sin error 403
- [ ] Dashboard muestra datos
- [ ] No hay errores en Error log

---

## 🚨 Si Algo Sale Mal - Rollback Rápido

```bash
# Volver a commit anterior
cd /home/luisga64/censo-django
git checkout master
git reset --hard HEAD~1

# O volver a un commit específico
git reset --hard <hash_del_commit_anterior>

# Migrar BD
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere
python manage.py migrate

# Recargar en Web tab
```

---

## 📱 Accesos Directos

### URLs Útiles:
- **Dashboard:** https://www.pythonanywhere.com/user/luisga64/
- **Consoles:** https://www.pythonanywhere.com/user/luisga64/consoles/
- **Web:** https://www.pythonanywhere.com/user/luisga64/webapps/
- **Files:** https://www.pythonanywhere.com/user/luisga64/files/
- **Databases:** https://www.pythonanywhere.com/user/luisga64/databases/

### Error Logs:
```bash
# Ver últimos errores
tail -n 50 /var/log/luisga64.pythonanywhere.com.error.log

# Ver logs en tiempo real
tail -f /var/log/luisga64.pythonanywhere.com.error.log
```

---

## 🔍 Verificación Post-Deploy

### 1. Verificar Versión
```bash
cd /home/luisga64/censo-django
cat VERSION
# Esperado: 2.1.0
```

### 2. Verificar Rama
```bash
git branch --show-current
# Esperado: master
```

### 3. Verificar Último Commit
```bash
git log -1 --oneline
# Debe mostrar el merge commit
```

### 4. Verificar Variables de Entorno
```bash
cat .env | head -n 5
# Verificar que existen las variables
```

### 5. Test de Django
```bash
source /home/luisga64/.virtualenvs/venv/bin/activate
export DJANGO_SETTINGS_MODULE=censoProject.settings_pythonanywhere
python manage.py check
# Debe mostrar: System check identified no issues
```

---

## 💡 Consejos

### Buenas Prácticas:
1. **Siempre hacer backup** antes de actualizar (opcional)
2. **Verificar error logs** después del reload
3. **Probar funcionalidades críticas** (login, mapas, CRUD)
4. **Monitorear** durante las primeras horas

### Si tienes dudas:
1. Revisa el error log
2. Verifica que .env esté completo
3. Confirma que estás en rama master
4. Asegúrate de haber recargado la app

---

## ⏱️ Tiempo Estimado

- **Opción 1 (Script):** ~5 minutos
- **Opción 2 (Manual):** ~10 minutos
- **Verificación:** ~5 minutos
- **Total:** 10-20 minutos

---

## 📞 Soporte

Si después de seguir estos pasos aún tienes errores:

1. Copia el **error log completo**:
   ```bash
   cat /var/log/luisga64.pythonanywhere.com.error.log | tail -n 100
   ```

2. Verifica el **estado del sistema**:
   ```bash
   git status
   pip list | grep django
   python --version
   ```

3. Comparte esa información para diagnóstico

---

**¡Éxito en tu deploy! 🚀**

