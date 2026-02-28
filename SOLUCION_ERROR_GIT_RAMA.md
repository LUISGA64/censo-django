# 🔧 SOLUCIÓN RÁPIDA - Error "couldn't find remote ref main"

## 🎯 Problema

Estás en la rama `development` o `master` en PythonAnywhere, pero los cambios se subieron a `main` en el repositorio local.

---

## ✅ Solución - Ejecuta estos comandos en PythonAnywhere

### PASO 1: Verificar qué ramas remotas existen
```bash
cd ~/censo-django
git branch -r
```

**Esto te mostrará las ramas disponibles, por ejemplo:**
- `origin/master`
- `origin/main`
- `origin/development`

---

### PASO 2: Sincronizar con la rama correcta

#### Opción A: Si existe `origin/main` (recomendado)
```bash
cd ~/censo-django

# Traer todos los cambios
git fetch origin

# Cambiar a la rama main
git checkout main

# Actualizar
git pull origin main
```

#### Opción B: Si solo existe `origin/master`
```bash
cd ~/censo-django

# Actualizar desde master
git checkout master
git pull origin master
```

#### Opción C: Si quieres traer main desde tu repo local
```bash
cd ~/censo-django

# Traer todas las ramas
git fetch origin

# Ver si main existe ahora
git branch -r

# Si apareció origin/main:
git checkout -b main origin/main
git pull origin main
```

---

### PASO 3: Verificar que los archivos se actualizaron

```bash
# Verificar que existen los nuevos archivos
ls -la templates/maps/

# Debe mostrar:
# map.html
# heatmap.html
# clusters.html

# Verificar la vista de geolocalización
grep "def map_view" censoapp/geolocation_views.py

# Debe mostrar la función
```

---

## 🚀 Continuar con el Despliegue

Una vez que `git pull` funcione correctamente, continúa con los siguientes pasos:

### 1. Instalar Folium
```bash
source venv/bin/activate
pip install folium==0.15.1
```

### 2. Crear directorio para mapas
```bash
mkdir -p media/temp_maps
chmod 755 media/temp_maps
```

### 3. Collectstatic
```bash
python manage.py collectstatic --noinput
```

### 4. Reload
- Ir a Web tab
- Click en "Reload"

---

## 📝 Nota Importante

**En el futuro, asegúrate de usar la misma rama en local y en PythonAnywhere:**

- Si usas `main` en local → usa `main` en PythonAnywhere
- Si usas `master` en local → usa `master` en PythonAnywhere

**Para cambiar de master a main permanentemente en PythonAnywhere:**
```bash
cd ~/censo-django
git checkout main
git branch --set-upstream-to=origin/main main
```

---

## ✅ Verificación Final

Después de `git pull` exitoso, verifica:
```bash
# Ver último commit
git log --oneline -1

# Debe mostrar algo como:
# abc1234 Fase 4 completada: Geolocalización + UI/UX mejorados - v4.0.0
```

**¡Listo! Ahora puedes continuar con el resto del despliegue.**

---

**Fecha:** 25 de Enero 2026  
**Problema:** Error "couldn't find remote ref main"  
**Solución:** Usar rama correcta (master o main)  
**Estado:** ✅ RESUELTO
