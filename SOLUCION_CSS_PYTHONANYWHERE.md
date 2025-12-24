# 🎨 Solución: CSS No Carga en PythonAnywhere

## ❌ Problema

La aplicación carga pero **no se ven los estilos CSS** (la página se ve sin formato, solo texto plano).

---

## ✅ Solución Completa

### **Paso 1: Recolectar Archivos Estáticos**

En la consola Bash de PythonAnywhere:

```bash
# Activar entorno virtual
workon censo-env

# Ir al proyecto
cd ~/censo-django

# Recolectar archivos estáticos
python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere
```

**Deberías ver:**
```
X static files copied to '/home/luisga64/censo-django/staticfiles'
```

---

### **Paso 2: Verificar Directorios**

```bash
# Verificar que existan los directorios
ls -la ~/censo-django/ | grep static

# Verificar contenido de staticfiles
ls -la ~/censo-django/staticfiles/
```

**Deberías ver:**
- `static/` - Archivos fuente
- `staticfiles/` - Archivos recolectados

---

### **Paso 3: Configurar Static Files en Web Tab**

1. Ve al **Dashboard de PythonAnywhere**
2. Click en la pestaña **Web**
3. Scroll hasta la sección **Static files**
4. Haz click en **Add a new static file mapping**

**Configuración correcta:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/luisga64/censo-django/staticfiles` |
| `/media/` | `/home/luisga64/censo-django/media` |

**⚠️ IMPORTANTE:** 
- La URL debe ser `/static/` (con las barras)
- El directorio debe ser `/home/luisga64/censo-django/staticfiles` (¡staticfiles, NO static!)

---

### **Paso 4: Verificar WSGI Configuration**

Edita el archivo WSGI: `/var/www/luisga64_pythonanywhere_com_wsgi.py`

**Debe tener este contenido:**

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

---

### **Paso 5: Recargar la Aplicación**

1. Dashboard → **Web**
2. Click en el botón verde **"Reload luisga64.pythonanywhere.com"**

---

### **Paso 6: Verificar en el Navegador**

1. Abre: `https://luisga64.pythonanywhere.com`
2. **IMPORTANTE:** Haz **Ctrl + F5** (forzar recarga sin caché)
3. Verifica que carguen los estilos

---

## 🔍 Verificación Detallada

### **Verificar rutas de archivos estáticos:**

```bash
# En consola Bash de PythonAnywhere
cd ~/censo-django

# Verificar que existan archivos CSS
find staticfiles -name "*.css" | head -10

# Verificar permisos
ls -la staticfiles/

# Debería mostrar archivos como:
# staticfiles/vendors/bootstrap/dist/css/bootstrap.min.css
# staticfiles/build/css/custom.css
# etc.
```

---

## ⚠️ Errores Comunes y Soluciones

### **Error 1: staticfiles está vacío**

```bash
# Solución:
cd ~/censo-django
python manage.py collectstatic --clear --noinput --settings=censoProject.settings_pythonanywhere
```

### **Error 2: Ruta incorrecta en Static Files**

**❌ Incorrecto:**
- `/static/` → `/home/luisga64/censo-django/static`

**✅ Correcto:**
- `/static/` → `/home/luisga64/censo-django/staticfiles`

### **Error 3: CSS carga en desarrollo pero no en producción**

**Verificar DEBUG en settings_pythonanywhere.py:**
```python
DEBUG = False  # Debe ser False en producción
```

**Verificar que WhiteNoise NO esté habilitado:**
En `settings_pythonanywhere.py` el middleware NO debe incluir WhiteNoise (PythonAnywhere sirve estáticos directamente).

---

## 🛠️ Script de Diagnóstico

Crea este script para diagnosticar problemas:

```bash
# En PythonAnywhere, crear archivo de diagnóstico
cd ~/censo-django
nano diagnostico_static.sh
```

**Contenido:**

```bash
#!/bin/bash
echo "🔍 DIAGNÓSTICO DE ARCHIVOS ESTÁTICOS"
echo "===================================="
echo ""

echo "📁 Directorio del proyecto:"
pwd
echo ""

echo "📂 Directorios static:"
ls -la | grep static
echo ""

echo "📊 Cantidad de archivos en staticfiles:"
find staticfiles -type f | wc -l
echo ""

echo "🎨 Archivos CSS encontrados:"
find staticfiles -name "*.css" | wc -l
echo ""

echo "🖼️  Archivos JS encontrados:"
find staticfiles -name "*.js" | wc -l
echo ""

echo "📝 Configuración STATIC_ROOT en settings:"
python manage.py diffsettings --settings=censoProject.settings_pythonanywhere | grep STATIC
echo ""

echo "✅ Verificación completa"
```

**Ejecutar:**
```bash
chmod +x diagnostico_static.sh
./diagnostico_static.sh
```

---

## 🚀 Solución Rápida (Todo en Uno)

Si nada funciona, ejecuta este comando completo:

```bash
# En consola Bash de PythonAnywhere
cd ~/censo-django && \
workon censo-env && \
python manage.py collectstatic --clear --noinput --settings=censoProject.settings_pythonanywhere && \
echo "✅ Archivos estáticos recolectados" && \
echo "" && \
echo "📝 SIGUIENTE PASO:" && \
echo "1. Dashboard → Web" && \
echo "2. Verificar Static files:" && \
echo "   URL: /static/" && \
echo "   Directory: /home/luisga64/censo-django/staticfiles" && \
echo "3. Click en Reload"
```

---

## 📊 Verificar Configuración en Dashboard

### **En la pestaña Web:**

**Sección "Code":**
- ✅ Source code: `/home/luisga64/censo-django`
- ✅ Working directory: `/home/luisga64/censo-django`
- ✅ WSGI configuration file: `/var/www/luisga64_pythonanywhere_com_wsgi.py`

**Sección "Virtualenv":**
- ✅ `/home/luisga64/.virtualenvs/censo-env`

**Sección "Static files":**
- ✅ `/static/` → `/home/luisga64/censo-django/staticfiles`
- ✅ `/media/` → `/home/luisga64/censo-django/media`

---

## 🔧 Verificar en el Navegador

### **Abrir las Developer Tools (F12):**

1. Ir a la pestaña **Network**
2. Recargar la página (Ctrl + F5)
3. Filtrar por **CSS**
4. Ver si hay errores 404

**Si hay errores 404:**
- Verificar la ruta en Static files
- Verificar que `collectstatic` se ejecutó correctamente

**Si los archivos cargan pero no se aplican:**
- Limpiar caché del navegador (Ctrl + Shift + Delete)
- Probar en ventana de incógnito

---

## 📝 Checklist Final

- [ ] `python manage.py collectstatic` ejecutado sin errores
- [ ] Directorio `staticfiles/` existe y tiene archivos
- [ ] Static files configurado en Web Tab: `/static/` → `.../staticfiles`
- [ ] Media files configurado: `/media/` → `.../media`
- [ ] WSGI configurado correctamente
- [ ] Aplicación recargada (botón Reload)
- [ ] Navegador actualizado con Ctrl + F5
- [ ] CSS carga correctamente ✅

---

## 🎯 Resultado Esperado

Después de seguir estos pasos:

✅ La página debe verse con estilos Bootstrap
✅ El sidebar debe tener colores
✅ Los botones deben tener formato
✅ Las tablas deben verse ordenadas
✅ Los iconos deben mostrarse correctamente

---

## 🆘 Si Aún No Funciona

### **Verificar logs de error:**

```bash
# En PythonAnywhere
tail -50 /var/log/luisga64.pythonanywhere.com.error.log
```

### **Verificar permisos:**

```bash
cd ~/censo-django
chmod -R 755 staticfiles
chmod -R 755 media
```

### **Forzar limpieza total:**

```bash
cd ~/censo-django
rm -rf staticfiles
mkdir staticfiles
python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere
# Dashboard → Web → Reload
```

---

## 📞 Contacto

Si después de seguir todos estos pasos el problema persiste:

1. Comparte el output de `diagnostico_static.sh`
2. Comparte una captura de la configuración de Static files en Web Tab
3. Comparte los errores del navegador (F12 → Console)

---

**Fecha:** 23 de diciembre de 2024  
**Versión:** 1.0  
**Estado:** Solución verificada para PythonAnywhere

