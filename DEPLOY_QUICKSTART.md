# ⚡ DEPLOY RÁPIDO - Comandos Esenciales

## 🎯 Solo Copia y Pega Esto en PythonAnywhere

```bash
# 1. Ir al directorio
cd ~/censo-django

# 2. Cambiar a master
git checkout master

# 3. Descargar cambios
git pull origin master

# 4. Activar virtualenv
source venv/bin/activate

# 5. Aplicar migraciones (CRITICAL)
python manage.py migrate

# 6. Recolectar estáticos
python manage.py collectstatic --noinput --clear

# 7. Recargar app
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py
```

**Reemplaza:** `tuusuario` por tu nombre de usuario real en PythonAnywhere

---

## ✅ Verificación Rápida

**En navegador:**
1. Limpiar caché: `Ctrl + Shift + Delete`
2. Abrir tu sitio: `https://tuusuario.pythonanywhere.com`
3. Probar dropdowns: Navbar usuario, Fichas Familiares, Personas
4. Consola (F12): No debe haber mensajes de console.log

**Ver errores:**
```bash
tail -50 /var/log/tuusuario.pythonanywhere.com.error.log
```

---

## 🚨 Si Algo Sale Mal

**Error de migración:**
```bash
python manage.py showmigrations censoapp
python manage.py migrate --fake-initial
```

**Error 500:**
```bash
# Ver el error
tail -30 /var/log/tuusuario.pythonanywhere.com.error.log

# Recargar manualmente
# Ir a: Web tab → botón "Reload"
```

**Archivos estáticos no cargan:**
```bash
python manage.py collectstatic --noinput --clear
# Luego recargar la web app
```

---

## 📋 Cambios en Este Deploy

✅ **Association.is_active** - Nuevo campo (migración 0034)  
✅ **Dropdowns** - Fix completo (navbar + dataTables)  
✅ **Veredas** - Redirects corregidos  
✅ **Console limpia** - Sin console.log  

---

## 🔒 Archivos Protegidos (NO TOCAR)

❌ `.env`  
❌ `settings_pythonanywhere.py`  
❌ `wsgi.py`  

Estos archivos ya están configurados en producción.

---

## ⏱️ Tiempo Estimado

**Deploy completo:** 3-5 minutos

---

**¿Listo?** Abre PythonAnywhere Bash console y empieza! 🚀

