# 🔄 Guía de Actualización en PythonAnywhere

## 📋 Situación

Cuando intentas actualizar el código en PythonAnywhere con `git pull`, puedes encontrarte con este mensaje:

```
error: Your local changes to the following files would be overwritten by merge:
    [archivos modificados]
Please commit your changes or stash them before you merge.
```

---

## ✅ Solución Recomendada (Sin perder cambios locales)

### **Opción 1: Guardar cambios temporalmente (Stash)**

```bash
# 1. Activar entorno virtual
workon censo-env

# 2. Ir al proyecto
cd ~/censo-django

# 3. Guardar cambios locales temporalmente
git stash

# 4. Actualizar desde GitHub
git pull origin development

# 5. Recargar la aplicación web
# Dashboard → Web → Reload
```

**¿Cuándo usar esto?**
- Cuando quieres mantener cambios locales para revisarlos después
- Si hiciste configuraciones específicas en PythonAnywhere que no quieres perder

**Recuperar cambios guardados después:**
```bash
# Ver qué guardaste
git stash list

# Recuperar el último stash
git stash pop
```

---

### **Opción 2: Descartar cambios locales (Recomendado para demo)**

```bash
# 1. Activar entorno virtual
workon censo-env

# 2. Ir al proyecto
cd ~/censo-django

# 3. Ver qué archivos cambiaron localmente
git status

# 4. Descartar TODOS los cambios locales
git reset --hard HEAD

# 5. Actualizar desde GitHub
git pull origin development

# 6. Recargar la aplicación web
# Dashboard → Web → Reload
```

**¿Cuándo usar esto?**
- Para la demo (no hay cambios importantes en PythonAnywhere)
- Cuando quieres una copia exacta del repositorio
- Si los cambios locales son temporales o de prueba

---

## 🚀 Script de Actualización Automática

Crea un archivo para facilitar actualizaciones futuras:

### **Crear script en PythonAnywhere:**

```bash
# En la consola Bash de PythonAnywhere
cd ~/censo-django
nano actualizar.sh
```

### **Contenido del script:**

```bash
#!/bin/bash
# Script de actualización rápida para PythonAnywhere

echo "🔄 ACTUALIZANDO APLICACIÓN CENSO-DJANGO"
echo "========================================"
echo ""

# Activar entorno virtual
source ~/.virtualenvs/censo-env/bin/activate

# Ir al proyecto
cd ~/censo-django

# Verificar rama actual
echo "📍 Rama actual:"
git branch

# Mostrar cambios locales si existen
echo ""
echo "📝 Cambios locales:"
git status --short

# Preguntar si descartar cambios
echo ""
echo "⚠️  ¿Descartar cambios locales y actualizar? (s/n)"
read -r respuesta

if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
    echo ""
    echo "🗑️  Descartando cambios locales..."
    git reset --hard HEAD
    
    echo "📥 Actualizando desde GitHub..."
    git pull origin development
    
    echo "📦 Instalando/actualizando dependencias..."
    pip install -r requirements.txt
    
    echo "🔄 Aplicando migraciones..."
    python manage.py migrate --settings=censoProject.settings_pythonanywhere
    
    echo "📦 Recolectando archivos estáticos..."
    python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere
    
    echo ""
    echo "✅ ACTUALIZACIÓN COMPLETADA"
    echo ""
    echo "📝 SIGUIENTE PASO:"
    echo "   Ve al Dashboard → Web → Click en 'Reload' (botón verde)"
    echo ""
else
    echo ""
    echo "❌ Actualización cancelada"
    echo "   Revisa los cambios con: git status"
    echo "   Descarta manualmente con: git reset --hard HEAD"
fi
```

### **Dar permisos de ejecución:**

```bash
chmod +x actualizar.sh
```

### **Usar el script:**

```bash
./actualizar.sh
```

---

## 📋 Proceso Paso a Paso (Manual)

### **1. Conectarse a PythonAnywhere**

- Ir a: https://www.pythonanywhere.com
- Login
- Click en "Consoles" → "Bash"

### **2. Verificar estado actual**

```bash
# Activar entorno
workon censo-env

# Ir al proyecto
cd ~/censo-django

# Ver rama actual
git branch

# Ver cambios locales
git status
```

### **3. Decidir qué hacer con cambios locales**

**Si hay cambios y quieres descartarlos:**
```bash
git reset --hard HEAD
```

**Si hay cambios y quieres guardarlos:**
```bash
git stash
```

### **4. Actualizar código**

```bash
# Actualizar desde GitHub
git pull origin development

# Ver qué cambió
git log --oneline -5
```

### **5. Actualizar dependencias (si cambió requirements.txt)**

```bash
pip install -r requirements.txt
```

### **6. Aplicar migraciones (si hay nuevas)**

```bash
python manage.py migrate --settings=censoProject.settings_pythonanywhere
```

### **7. Recolectar archivos estáticos (si cambiaron templates/static)**

```bash
python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere
```

### **8. Recargar aplicación web**

- Dashboard → **Web**
- Click en botón verde **"Reload"**

---

## ⚠️ Problemas Comunes

### **Problema 1: "error: Your local changes would be overwritten"**

**Solución:**
```bash
# Opción A: Descartar cambios
git reset --hard HEAD

# Opción B: Guardar cambios
git stash
```

### **Problema 2: "Please commit your changes before merging"**

**Solución:**
```bash
# Ver qué cambió
git status

# Descartar todo
git reset --hard HEAD

# O hacer commit (solo si son cambios importantes)
git add .
git commit -m "Cambios locales en PythonAnywhere"
git pull origin development
```

### **Problema 3: Conflictos al hacer pull**

**Solución:**
```bash
# Abortar pull
git merge --abort

# Descartar cambios locales
git reset --hard origin/development

# Forzar actualización
git pull origin development
```

### **Problema 4: No se ven los cambios después de Reload**

**Solución:**
```bash
# Limpiar cache de Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Recargar de nuevo
# Dashboard → Web → Reload
```

---

## 🔍 Verificar Actualización

Después de actualizar, verifica:

### **1. Código actualizado:**
```bash
# Ver últimos commits
git log --oneline -5

# Ver archivos cambiados
git diff HEAD~1 --stat
```

### **2. Base de datos actualizada:**
```bash
# Ver migraciones aplicadas
python manage.py showmigrations --settings=censoProject.settings_pythonanywhere
```

### **3. Aplicación funcionando:**
- Abrir: `https://luisga64.pythonanywhere.com`
- Hacer login
- Verificar funcionalidades

---

## 📌 Comandos Rápidos de Referencia

```bash
# Ver estado
git status

# Descartar cambios locales
git reset --hard HEAD

# Guardar cambios temporalmente
git stash

# Actualizar código
git pull origin development

# Ver últimos cambios
git log --oneline -5

# Actualizar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate --settings=censoProject.settings_pythonanywhere

# Recolectar estáticos
python manage.py collectstatic --noinput --settings=censoProject.settings_pythonanywhere

# Limpiar cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
```

---

## 🎯 Recomendación para la Demo

**Para mantener la demo siempre actualizada:**

1. **Antes de mostrar a un cabildo:**
   ```bash
   cd ~/censo-django
   git reset --hard origin/development
   git pull origin development
   # Dashboard → Web → Reload
   ```

2. **Resetear datos si es necesario:**
   ```bash
   python crear_datos_demo.py
   ```

3. **Verificar que funciona:**
   - Login con `admin_cabildo` / `Demo2024!`
   - Revisar dashboard
   - Probar carga masiva

---

## 📝 Notas Importantes

### **¿Perderé los datos al actualizar?**
- ❌ **NO** - Los datos están en la base de datos
- ❌ **NO** - Los archivos subidos están en `media/`
- ✅ **Solo se actualiza el código**

### **¿Cuándo hacer backup?**
```bash
# Backup de base de datos
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Backup de media
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### **¿Cómo volver a una versión anterior?**
```bash
# Ver commits
git log --oneline

# Volver a un commit específico
git reset --hard <commit-hash>

# Recargar aplicación
# Dashboard → Web → Reload
```

---

**Fecha de creación:** 23 de diciembre de 2024  
**Versión:** 1.0  
**Última actualización:** 23/12/2024

