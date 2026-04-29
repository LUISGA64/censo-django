# 🔧 Solución: Error de Merge con Staticfiles

## ❌ Error Encontrado

```
error: Your local changes to the following files would be overwritten by merge:
        staticfiles/admin/css/changelists.css
        staticfiles/admin/css/forms.css
        staticfiles/assets/css/censo-corporate.css
Please commit your changes or stash them before you merge.
```

---

## 🎯 Causa del Problema

Los archivos en `staticfiles/` fueron rastreados por Git antes de que se agregaran al `.gitignore`. Estos son archivos **generados automáticamente** por `collectstatic` y no deberían estar en el control de versiones.

---

## ✅ Solución Rápida (Recomendada)

### En PythonAnywhere Bash Console:

```bash
# 1. Hacer stash de los cambios locales en staticfiles
git stash push -m "Stash staticfiles antes de merge"

# 2. Ahora hacer el pull
git pull origin master

# 3. Eliminar los archivos staticfiles del índice de Git (sin borrar físicamente)
git rm -r --cached staticfiles/

# 4. Crear un commit para eliminarlos del tracking
git commit -m "chore: eliminar staticfiles del tracking de Git"

# 5. Regenerar los archivos estáticos
python manage.py collectstatic --noinput --clear

# 6. Continuar con el deploy normal
```

---

## 📋 Solución Paso a Paso (Detallada)

### Paso 1: Guardar Cambios Locales Temporalmente
```bash
cd ~/censo-django
git stash push -m "Stash staticfiles temporalmente"
```
**Resultado esperado:** `Saved working directory and index state On master: Stash staticfiles temporalmente`

### Paso 2: Actualizar Código desde GitHub
```bash
git pull origin master
```
**Resultado esperado:** Los cambios se descargan sin conflictos.

### Paso 3: Limpiar Staticfiles del Tracking de Git
```bash
# Verificar que staticfiles/ está en .gitignore
grep -r "staticfiles" .gitignore

# Eliminar del índice de Git (no borra los archivos físicos)
git rm -r --cached staticfiles/

# Verificar qué se eliminará
git status
```

### Paso 4: Hacer Commit de la Limpieza
```bash
git commit -m "chore: eliminar staticfiles del tracking de Git - archivos generados automáticamente"
```

### Paso 5: Subir los Cambios (Opcional)
```bash
# Solo si quieres mantener esta limpieza en el repositorio
git push origin master
```

### Paso 6: Regenerar Archivos Estáticos
```bash
source venv/bin/activate
python manage.py collectstatic --noinput --clear
```

### Paso 7: Continuar con Deploy Normal
```bash
# Aplicar migraciones
python manage.py migrate

# Recargar la aplicación
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py
```

---

## 🚨 Solución Alternativa (Si la Anterior No Funciona)

### Opción A: Reset Hard (CUIDADO)

**⚠️ Advertencia:** Esto eliminará TODOS los cambios locales.

```bash
cd ~/censo-django

# Verificar que estás en master
git branch

# Descartar todos los cambios locales
git reset --hard origin/master

# Regenerar staticfiles
python manage.py collectstatic --noinput --clear
```

### Opción B: Eliminar y Reclonar (Último Recurso)

**⚠️ Advertencia:** Solo si todo lo demás falla.

```bash
# Hacer backup de archivos importantes (.env, base de datos)
cp ~/censo-django/.env ~/env_backup
cp ~/censo-django/db.censo_Web ~/db_backup

# Eliminar el directorio
cd ~
rm -rf censo-django

# Clonar de nuevo
git clone https://github.com/LUISGA64/censo-django.git censo-django
cd censo-django
git checkout master

# Restaurar archivos de producción
cp ~/env_backup .env
cp ~/db_backup db.censo_Web

# Crear virtualenv
python3.10 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Migrar
python manage.py migrate

# Collectstatic
python manage.py collectstatic --noinput --clear
```

---

## 🎯 Prevención Futura

Para evitar este problema en el futuro:

### 1. Verificar .gitignore
```bash
# Asegurarse de que staticfiles/ esté ignorado
echo "staticfiles/" >> .gitignore
git add .gitignore
git commit -m "chore: asegurar que staticfiles esté en .gitignore"
```

### 2. Limpiar Tracking en Local También
```bash
# En tu máquina local de desarrollo
cd ~/censo-django
git rm -r --cached staticfiles/
git commit -m "chore: eliminar staticfiles del tracking de Git"
git push origin development
git push origin master
```

### 3. Comandos Seguros para Deploy
```bash
# Siempre hacer stash antes de pull
git stash
git pull origin master
git stash pop  # Solo si necesitas recuperar cambios importantes
```

---

## 📋 Checklist de Verificación

- [ ] Archivos en conflicto guardados con `git stash`
- [ ] `git pull origin master` ejecutado sin errores
- [ ] `staticfiles/` eliminado del tracking con `git rm -r --cached`
- [ ] Commit creado para eliminar staticfiles del tracking
- [ ] `collectstatic` ejecutado para regenerar archivos
- [ ] Aplicación web recargada
- [ ] Sitio web funcionando correctamente

---

## 🔍 Diagnóstico

### Ver Archivos en Conflicto
```bash
git status
```

### Ver Archivos Rastreados en Staticfiles
```bash
git ls-files staticfiles/
```

### Verificar .gitignore
```bash
cat .gitignore | grep staticfiles
```

### Ver Historial de Stash
```bash
git stash list
```

### Recuperar del Stash (Si es Necesario)
```bash
# Ver contenido del stash
git stash show -p

# Aplicar el último stash
git stash pop

# Aplicar un stash específico
git stash apply stash@{0}
```

---

## ✅ Comando Todo-en-Uno (Copy-Paste)

**Para resolver rápidamente:**

```bash
cd ~/censo-django && \
git stash && \
git pull origin master && \
git rm -r --cached staticfiles/ 2>/dev/null && \
git commit -m "chore: eliminar staticfiles del tracking" 2>/dev/null && \
source venv/bin/activate && \
python manage.py migrate && \
python manage.py collectstatic --noinput --clear && \
touch /var/www/*_pythonanywhere_com_wsgi.py && \
echo "✅ Deploy completado exitosamente"
```

---

## 📞 Soporte

Si después de estos pasos sigues teniendo problemas:

1. **Ver logs de error:**
   ```bash
   tail -50 /var/log/tuusuario.pythonanywhere.com.error.log
   ```

2. **Verificar estado de Git:**
   ```bash
   git status
   git log --oneline -5
   ```

3. **Verificar archivos en conflicto:**
   ```bash
   git diff
   ```

---

## 🎉 Resultado Esperado

Después de aplicar la solución:

✅ `git pull origin master` funciona sin errores  
✅ `staticfiles/` ya no está en el tracking de Git  
✅ Archivos estáticos se regeneran correctamente  
✅ Deploy se completa sin problemas  
✅ Sitio web funciona correctamente  

---

**Última actualización:** 28 Abril 2026  
**Versión:** 1.0

