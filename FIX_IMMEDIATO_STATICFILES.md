# ⚡ SOLUCIÓN INMEDIATA - Copia y Pega en PythonAnywhere

## 🔥 Error que Estás Viendo

```
error: Your local changes to the following files would be overwritten by merge:
        staticfiles/admin/css/changelists.css
        staticfiles/admin/css/forms.css
        staticfiles/assets/css/censo-corporate.css
Please commit your changes or stash them before you merge.
```

---

## ✅ SOLUCIÓN (Copia TODO esto)

```bash
# 1. Ir al directorio
cd ~/censo-django

# 2. Guardar cambios temporalmente
git stash push -m "Stash staticfiles antes de merge"

# 3. Actualizar código desde GitHub
git pull origin master

# 4. Eliminar staticfiles del tracking de Git
git rm -r --cached staticfiles/ 2>/dev/null

# 5. Hacer commit de la limpieza (ignorar si da error)
git commit -m "chore: eliminar staticfiles del tracking" 2>/dev/null

# 6. Activar virtualenv
source venv/bin/activate

# 7. Regenerar archivos estáticos
python manage.py collectstatic --noinput --clear

# 8. Aplicar migraciones
python manage.py migrate

# 9. Recargar aplicación
touch /var/www/*_pythonanywhere_com_wsgi.py

echo ""
echo "✅ Deploy completado exitosamente"
echo "🌐 Abre tu sitio y limpia caché del navegador (Ctrl+Shift+Delete)"
```

---

## 📊 Qué Hace Cada Comando

1. **cd ~/censo-django** - Va al directorio del proyecto
2. **git stash** - Guarda temporalmente los cambios en staticfiles/
3. **git pull** - Descarga los cambios desde GitHub (ahora sin conflicto)
4. **git rm --cached** - Elimina staticfiles/ del tracking de Git (sin borrar archivos)
5. **git commit** - Guarda el cambio de no trackear staticfiles/
6. **source venv** - Activa el entorno virtual de Python
7. **collectstatic** - Regenera todos los archivos estáticos
8. **migrate** - Aplica las migraciones de base de datos (Association.is_active)
9. **touch wsgi** - Recarga la aplicación web

---

## ⏱️ Tiempo Total: 2-3 minutos

---

## ✅ Verificación

Después de ejecutar, verifica:

1. **En navegador:**
   - Limpiar caché: `Ctrl + Shift + Delete`
   - Abrir: `https://tuusuario.pythonanywhere.com`
   - Probar dropdowns (navbar, fichas, personas)

2. **Ver logs si hay error:**
   ```bash
   tail -50 /var/log/tuusuario.pythonanywhere.com.error.log
   ```

---

## 🎯 Resultado Esperado

```
✅ Deploy completado exitosamente
🌐 Abre tu sitio y limpia caché del navegador (Ctrl+Shift+Delete)
```

---

## 🔄 Script Automatizado Actualizado

**¡Buenas noticias!** El script `deploy_commands_pythonanywhere.sh` ahora detecta y resuelve este error automáticamente.

**Para la próxima vez:**
```bash
cd ~/censo-django
bash deploy_commands_pythonanywhere.sh
```

El script:
- ✅ Detecta conflictos con staticfiles
- ✅ Hace stash automático
- ✅ Limpia el tracking de Git
- ✅ Regenera archivos estáticos
- ✅ Completa el deploy

---

## 📞 Si Necesitas Ayuda

**Documentación completa:** `SOLUCION_ERROR_STATICFILES.md`  
**Guía rápida:** `DEPLOY_QUICKSTART.md`  
**Guía detallada:** `DEPLOY_ABRIL_28_2026.md`

---

**¡Copia los comandos de arriba y pégalos en PythonAnywhere Bash Console!** 🚀

