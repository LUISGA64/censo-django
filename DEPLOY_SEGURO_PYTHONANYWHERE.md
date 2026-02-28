# 🚀 GUÍA DE DESPLIEGUE SEGURO - PythonAnywhere

## ⚠️ IMPORTANTE: LEER ANTES DE DESPLEGAR

Esta guía te ayudará a desplegar los cambios de hoy en PythonAnywhere sin romper nada.

---

## 📋 Pre-requisitos

### Verificar en Local
```bash
✅ python manage.py check (sin errores)
✅ git push origin main (exitoso)
✅ RESUMEN_CAMBIOS_2026-01-25.md (creado)
```

---

## 🔧 PASO 1: Backup en PythonAnywhere

### 1.1 Crear Backup de Base de Datos
```bash
# Conectarse a PythonAnywhere
# Ir a Files > Open Bash Console

cd ~/censo-django

# Crear directorio de backups si no existe
mkdir -p backups

# Backup de la base de datos
cp db.censo_Web backups/db.censo_Web.backup_$(date +%Y%m%d_%H%M%S)

# Verificar que se creó
ls -lh backups/
```

### 1.2 Backup de Archivos Estáticos (opcional)
```bash
# Si tienes archivos importantes en static/media
cp -r media backups/media_backup_$(date +%Y%m%d_%H%M%S)
```

---

## 🔄 PASO 2: Actualizar Código

### 2.1 Verificar Rama Actual
```bash
cd ~/censo-django

# Ver rama actual
git branch
```

**Posibles salidas:**
- `* master` → Rama master (antigua)
- `* main` → Rama main (nueva)
- `* development` → Rama de desarrollo

### 2.2 Actualizar según tu Rama

#### Si estás en `master`:
```bash
# Opción A: Actualizar desde master
git pull origin master

# Opción B: Cambiar a main y actualizar
git fetch origin
git checkout main
git pull origin main
```

#### Si estás en `development`:
```bash
# Cambiar a master primero
git checkout master
git pull origin master

# O cambiar a main
git checkout main
git pull origin main
```

#### Si estás en `main`:
```bash
# Actualizar desde main
git pull origin main
```

**Salida esperada:**
```
Updating...
Fast-forward
 censoapp/geolocation_views.py | ...
 templates/maps/map.html | ...
 ...
 X files changed, Y insertions(+), Z deletions(-)
```

### 2.3 Si aparece error "fatal: couldn't find remote ref main"
```bash
# Esto significa que tu repo usa 'master' no 'main'
# Actualizar desde master:
git pull origin master

# O verificar qué ramas remotas existen:
git branch -r
```

---

## 📦 PASO 3: Instalar Nueva Dependencia

### 3.1 Activar Entorno Virtual
```bash
# En PythonAnywhere
cd ~/censo-django
source venv/bin/activate
```

**Verificar que el prompt cambie a:** `(venv) $`

### 3.2 Instalar Folium
```bash
pip install folium==0.15.1
```

**Salida esperada:**
```
Successfully installed folium-0.15.1
```

### 3.3 Verificar Instalación
```bash
pip list | grep folium
```

**Debe mostrar:** `folium 0.15.1`

---

## 📁 PASO 4: Crear Directorio para Mapas

### 4.1 Crear Directorio Temporal
```bash
cd ~/censo-django

# Crear directorio si no existe
mkdir -p media/temp_maps

# Dar permisos
chmod 755 media/temp_maps

# Verificar
ls -la media/
```

**Debe mostrar:** `drwxr-xr-x ... temp_maps`

---

## 🎨 PASO 5: Recolectar Archivos Estáticos

### 5.1 Collectstatic
```bash
cd ~/censo-django
source venv/bin/activate

python manage.py collectstatic --noinput
```

**Salida esperada:**
```
X static files copied to '/home/tu_usuario/censo-django/staticfiles'
```

### 5.2 Verificar CSS Actualizado
```bash
ls -lh staticfiles/assets/css/censo-corporate.css
```

**Debe mostrar fecha y hora recientes**

---

## ⚙️ PASO 6: Verificar Configuración WSGI

### 6.1 Revisar WSGI File
```
En PythonAnywhere:
1. Ir a Web tab
2. Click en WSGI configuration file
3. Verificar estas líneas:
```

```python
# STATIC
STATIC_URL = '/static/'
STATIC_ROOT = '/home/TU_USUARIO/censo-django/staticfiles'

# MEDIA (IMPORTANTE - Debe estar)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/TU_USUARIO/censo-django/media'
```

**Si no están, agregar después de STATIC_ROOT:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')
```

### 6.2 Guardar y Cerrar
- Click en "Save"
- Cerrar el editor

---

## 🌐 PASO 7: Configurar Static Files Mapping

### 7.1 En Web Tab
```
Ir a: Static files section

Verificar que existe:
URL: /static/
Directory: /home/TU_USUARIO/censo-django/staticfiles
```

### 7.2 Agregar Mapping para Media
```
Si no existe, agregar:

URL: /media/
Directory: /home/TU_USUARIO/censo-django/media

Click en el check verde ✓
```

---

## 🔄 PASO 8: Recargar la Aplicación

### 8.1 Reload
```
En Web tab:
1. Scroll hasta arriba
2. Click en el botón verde "Reload tu_usuario.pythonanywhere.com"
3. Esperar a que aparezca "Reloaded"
```

### 8.2 Verificar Consola de Errores
```
En la misma página Web:
1. Scroll hasta "Log files"
2. Click en "Error log"
3. Verificar que NO haya errores nuevos
```

**Errores esperados:** NINGUNO  
**Si hay errores:** Ver sección de Troubleshooting abajo

---

## ✅ PASO 9: Testing en Producción

### 9.1 Verificar Homepage
```
Abrir: https://tu_usuario.pythonanywhere.com
✓ Página carga sin errores
✓ No hay errores JavaScript en consola (F12)
```

### 9.2 Verificar Sidebar
```
✓ Ver íconos FontAwesome (no SVG)
✓ Ver sección "Mapas y Geolocalización"
✓ Colores suaves visibles
```

### 9.3 Verificar Mapas
```
Ir a cada mapa:

1. https://tu_usuario.pythonanywhere.com/mapa/
   ✓ Mapa carga
   ✓ Marcadores visibles
   
2. https://tu_usuario.pythonanywhere.com/mapa/calor/
   ✓ Mapa de calor carga
   ✓ Alert azul con texto blanco visible
   
3. https://tu_usuario.pythonanywhere.com/mapa/clusters/
   ✓ Clusters azules visibles
   ✓ Alert verde con texto blanco visible
```

### 9.4 Verificar Alerts
```
Navegar por el sistema:
✓ Todos los alerts tienen fondos sólidos
✓ Texto blanco legible
✓ Negritas destacadas
```

---

## 🐛 TROUBLESHOOTING

### Error: "No module named 'folium'"
```bash
# Solución:
cd ~/censo-django
source venv/bin/activate
pip install folium==0.15.1
# Luego reload en Web tab
```

### Error: "TemplateDoesNotExist: maps/map.html"
```bash
# Verificar que los templates se copiaron:
ls -la ~/censo-django/templates/maps/

# Debe mostrar:
# map.html
# heatmap.html
# clusters.html

# Si no están, hacer git pull de nuevo
```

### Error 404 en /mapa/
```bash
# Verificar URLs:
cd ~/censo-django
grep "map-view" censoapp/urls.py

# Debe existir la ruta
# Si no, hacer git pull de nuevo
```

### Mapas no cargan / Pantalla en blanco
```bash
# Verificar directorio media:
ls -la ~/censo-django/media/temp_maps/

# Verificar permisos:
chmod 755 ~/censo-django/media/temp_maps

# Verificar MEDIA_URL en WSGI
# Verificar Static files mapping en Web tab
```

### CSS no se actualiza / Colores viejos
```bash
# Limpiar caché y regenerar estáticos:
cd ~/censo-django
source venv/bin/activate
rm -rf staticfiles/*
python manage.py collectstatic --noinput

# Reload en Web tab
# Ctrl+Shift+R en navegador (hard refresh)
```

### Alerts siguen con texto oscuro
```bash
# Verificar que CSS se copió:
cat ~/censo-django/staticfiles/assets/css/censo-corporate.css | grep "alert-info"

# Debe mostrar:
# background-color: #2196F3 !important;

# Si no, hacer collectstatic de nuevo
```

---

## 🔙 ROLLBACK (Si algo sale mal)

### Si necesitas volver atrás:

```bash
cd ~/censo-django

# 1. Restaurar base de datos
cp backups/db.censo_Web.backup_FECHA db.censo_Web

# 2. Volver a commit anterior
git log --oneline -5
git reset --hard COMMIT_HASH_ANTERIOR

# 3. Desinstalar folium (opcional)
source venv/bin/activate
pip uninstall folium -y

# 4. Collectstatic
python manage.py collectstatic --noinput

# 5. Reload en Web tab
```

---

## ✅ CHECKLIST FINAL

### Antes de dar por terminado:

```
□ Backup de base de datos creado
□ git pull origin main exitoso
□ folium==0.15.1 instalado
□ Directorio media/temp_maps creado con permisos 755
□ collectstatic ejecutado sin errores
□ MEDIA_URL configurado en WSGI
□ Static files mapping configurado para /media/
□ Aplicación recargada (Reload)
□ Error log sin errores nuevos
□ Homepage carga correctamente
□ Sidebar muestra íconos FontAwesome
□ Sección "Mapas y Geolocalización" visible
□ Los 3 mapas cargan correctamente
□ Alerts tienen texto blanco sobre fondos sólidos
□ No hay errores JavaScript (F12)
```

---

## 📞 SOPORTE

### Si encuentras problemas:

1. **Revisar Error Log en PythonAnywhere**
2. **Verificar que seguiste todos los pasos**
3. **Usar sección de Troubleshooting**
4. **Si persiste, hacer rollback**

---

## 🎉 ¡DESPLIEGUE EXITOSO!

Si todos los checks están ✓, tu aplicación está actualizada con:

✅ Sistema de geolocalización completo  
✅ UI/UX modernizada  
✅ Accesibilidad mejorada  
✅ Fase 4 del roadmap completada  

**¡Felicidades! Tu aplicación está en producción con todas las mejoras.** 🚀

---

**Fecha de Guía:** 25 de Enero 2026  
**Versión Destino:** 4.0.0  
**Fase Implementada:** Geolocalización + UI/UX
