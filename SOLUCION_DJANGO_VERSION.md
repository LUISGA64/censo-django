# 🚨 SOLUCIÓN URGENTE - Error de Django Session

## 🎯 Problema Identificado

**Error:** `'SessionStore' object has no attribute '_session_cache'`

**Causa:** Django 6.0.1 (versión inestable/incompatible) está instalado en tu entorno virtual.

**Solución:** Degradar a Django 5.0.x (versión estable)

---

## ✅ EJECUTA ESTOS COMANDOS EN PYTHONANYWHERE

### Copia y pega TODO esto en la consola Bash:

```bash
cd ~/censo-django
source venv/bin/activate

# 1. Ver versión actual de Django
echo "===== VERSIÓN ACTUAL DE DJANGO ====="
pip show django | grep Version

# 2. DOWNGRADE a Django 5.0 (versión estable)
pip uninstall django -y
pip install Django==5.0.0

# 3. Reinstalar dependencias críticas con versiones compatibles
pip install django-allauth==0.57.0
pip install django-mfa2==2.6.0

# 4. Verificar versión instalada
echo ""
echo "===== NUEVA VERSIÓN DE DJANGO ====="
pip show django | grep Version

# 5. Limpiar sesiones corruptas
python manage.py clearsessions

# 6. Migrar base de datos
python manage.py migrate

# 7. Verificar que todo está OK
python manage.py check

# 8. Verificar folium
pip install folium==0.15.1

echo ""
echo "===== VERIFICACIÓN FINAL ====="
echo "Django instalado:"
pip show django | grep Version
echo ""
echo "Folium instalado:"
pip list | grep folium
echo ""
echo "✅ Si no hay errores, hacer Reload en Web Tab"
```

---

## 🔄 DESPUÉS DE EJECUTAR

1. **En Web Tab** → Click **"Reload"** (botón verde)
2. **Probar homepage:** https://luisga64.pythonanywhere.com/
3. **Debe funcionar** sin error 500

---

## 📝 NOTA IMPORTANTE

Django 6.0.1 NO es una versión estable oficial. Probablemente se instaló por error durante el despliegue. Django 5.0.x es la versión estable actual (enero 2026).

---

## ✅ VERIFICACIÓN FINAL

Después de Reload, la aplicación debe funcionar correctamente:

- ✅ Homepage carga sin error 500
- ✅ Sidebar con íconos FontAwesome
- ✅ Mapas funcionando (después de configurar MEDIA)

---

**EJECUTA LOS COMANDOS Y LUEGO RELOAD.** 🚀
