# 🚀 Deploy PythonAnywhere - 28 Abril 2026

## 📋 Cambios a Desplegar

### ✅ Cambios Implementados:
1. **Association Model**: Nuevo campo `is_active` + campos adicionales (migración 0034)
2. **Dropdowns**: Fix completo en navbar, fichas familiares y personas
3. **Organization Views**: Corrección de redirects con anchors
4. **JavaScript**: Eliminación de console.log (código limpio)
5. **Requirements**: Actualizados y verificados

---

## 🔒 IMPORTANTE: Archivos de Producción (NO TOCAR)

❌ **NO modificar estos archivos en producción:**
- `.env` - Variables de entorno de producción
- `censoProject/settings_pythonanywhere.py` - Configuración de producción
- `censoProject/wsgi.py` - Configuración WSGI de producción

---

## 🎯 Comandos de Deploy (Copia y Pega)

### Paso 1: Conectar a PythonAnywhere
1. Ve a: https://www.pythonanywhere.com
2. Abre una **Bash console**

### Paso 2: Ir al Directorio del Proyecto
```bash
cd ~/censo-django
```

### Paso 3: Verificar Rama Actual
```bash
git branch
```
**Resultado esperado:** Debe mostrar `* master`

Si estás en otra rama, cambiar a master:
```bash
git checkout master
```

### Paso 4: Actualizar Código desde GitHub
```bash
git pull origin master
```

**✅ Verificación:** Deberías ver mensajes indicando que se descargaron los cambios.

### Paso 5: Activar Entorno Virtual
```bash
source venv/bin/activate
```

**✅ Verificación:** El prompt debe cambiar mostrando `(venv)` al inicio.

### Paso 6: Verificar Dependencias
```bash
# Ver si hay cambios en requirements.txt
git log --oneline -1 requirements.txt
```

**Solo si requirements.txt cambió**, instalar dependencias:
```bash
pip install -r requirements.txt --no-cache-dir
```

### Paso 7: Ejecutar Migraciones (CRÍTICO)
```bash
# Ver migraciones pendientes
python manage.py showmigrations censoapp

# Aplicar migración 0034 (Association model)
python manage.py migrate censoapp 0034

# Aplicar todas las migraciones
python manage.py migrate
```

**✅ Verificación:** Debe mostrar:
```
Running migrations:
  Applying censoapp.0034_alter_association_options_association_created_at_and_more... OK
```

### Paso 8: Recolectar Archivos Estáticos
```bash
python manage.py collectstatic --noinput --clear
```

**✅ Verificación:** Debe copiar los nuevos archivos JavaScript (navbar-dropdown-fix.js, etc.)

### Paso 9: Verificar Base de Datos (Opcional pero Recomendado)
```bash
python manage.py shell
```

Dentro del shell:
```python
from censoapp.models import Association
# Verificar que el campo is_active existe
association = Association.objects.first()
if association:
    print(f"Association: {association.name}")
    print(f"Is Active: {association.is_active}")
    print("✅ Campo is_active funciona correctamente")
else:
    print("⚠️  No hay asociaciones en la base de datos")
exit()
```

### Paso 10: Recargar la Aplicación Web
```bash
# Salir del shell de Python si estás dentro
exit()  # Solo si estás en python shell

# Crear archivo de señal para recargar
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py
```

**O bien**, ve a la pestaña **Web** y click en el botón **"Reload"**

---

## ✅ Verificación Post-Deploy

### En PythonAnywhere - Revisar Logs
```bash
# Ver últimas líneas del log de errores
tail -50 /var/log/tuusuario.pythonanywhere.com.error.log

# Ver log de servidor
tail -50 /var/log/tuusuario.pythonanywhere.com.server.log
```

### En el Navegador:
1. **Limpiar caché del navegador**: `Ctrl + Shift + Delete` o `Ctrl + F5`
2. **Abrir la aplicación**: `https://tuusuario.pythonanywhere.com`
3. **Verificar funcionalidades:**
   - ✅ Dropdown del navbar (usuario)
   - ✅ Dropdowns "Acciones" en Fichas Familiares
   - ✅ Dropdowns "Acciones" en Personas
   - ✅ Editar Vereda (debe redirigir correctamente con anchor)
   - ✅ Lista de Asociaciones (debe mostrar estado "Activo")
4. **Abrir consola del navegador** (F12): No debe haber mensajes de console.log

---

## 🔍 Archivos Modificados en Este Deploy

### Backend (Python)
```
censoapp/models.py                    # Association model actualizado
censoapp/organization_views.py        # Redirects corregidos
censoapp/migrations/0034_*.py         # Nueva migración
```

### Frontend (JavaScript)
```
static/assets/js/censo/family-card/datatable-family-card.js  # Dropdowns fix
static/assets/js/censo/persons/datatable-person.js           # Dropdowns fix
static/js/navbar-dropdown-fix.js                             # Navbar fix
```

### Configuración
```
requirements.txt                      # Dependencias actualizadas
.gitignore                           # Actualizado
```

---

## 🚨 Troubleshooting

### Problema: "No module named 'X'"
**Solución:**
```bash
pip install -r requirements.txt --no-cache-dir
```

### Problema: "Migration already applied"
**Normal**, significa que la migración ya fue aplicada. Continúa con el siguiente paso.

### Problema: Error 500 en la web
**Solución:**
```bash
# Ver el error específico
tail -30 /var/log/tuusuario.pythonanywhere.com.error.log
```

### Problema: Dropdowns no funcionan
**Solución:**
1. Verificar que collectstatic se ejecutó correctamente
2. Limpiar caché del navegador (Ctrl + Shift + Delete)
3. Verificar que Bootstrap está cargado (F12 → Console)

### Problema: Base de datos bloqueada
**Solución:**
```bash
# Reiniciar la web app desde la pestaña Web
# O eliminar lock file
cd ~/censo-django
rm -f db.censo_Web-journal
```

---

## 📊 Checklist de Deploy

Marca cada paso conforme lo completes:

- [ ] Conectar a PythonAnywhere Bash console
- [ ] `cd ~/censo-django`
- [ ] `git checkout master`
- [ ] `git pull origin master`
- [ ] `source venv/bin/activate`
- [ ] `pip install -r requirements.txt` (si requirements cambió)
- [ ] `python manage.py migrate`
- [ ] `python manage.py collectstatic --noinput --clear`
- [ ] Verificar migración en shell de Django
- [ ] Recargar web app (botón Reload)
- [ ] Verificar logs de errores
- [ ] Probar en navegador (limpiar caché)
- [ ] Verificar dropdowns funcionan
- [ ] Verificar asociaciones muestran estado "Activo"
- [ ] Verificar consola sin mensajes de debug

---

## 📞 Comandos Rápidos de Referencia

```bash
# Estado de Git
git status

# Ver cambios recientes
git log --oneline -5

# Activar virtualenv
source venv/bin/activate

# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones
python manage.py migrate

# Collectstatic
python manage.py collectstatic --noinput --clear

# Ver logs
tail -50 /var/log/tuusuario.pythonanywhere.com.error.log

# Recargar web
touch /var/www/tuusuario_pythonanywhere_com_wsgi.py
```

---

## ✅ Deploy Completado

Si todos los pasos se completaron sin errores:

✅ **Backend actualizado** con Association.is_active  
✅ **JavaScript limpio** sin console.log  
✅ **Dropdowns funcionando** en todas las páginas  
✅ **Redirects corregidos** en veredas  
✅ **Producción estable** y optimizada  

---

**Fecha del Deploy:** 28 Abril 2026  
**Versión:** 1.8.0  
**Rama:** master (b4c24d1)  

---

## 🎯 Siguiente Sesión de Desarrollo

Cuando vuelvas a desarrollar:
```bash
# En tu máquina local
git checkout development
git pull origin development
# Continuar desarrollo...
```

**¡Deploy Exitoso!** 🚀

