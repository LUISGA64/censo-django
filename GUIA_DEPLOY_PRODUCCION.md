# 🚀 GUÍA DE DEPLOY A PRODUCCIÓN

## ✅ LIMPIEZA COMPLETADA

### Archivos Organizados
- ✅ Documentación movida a `docs/`
- ✅ Archivos temporales eliminados
- ✅ Tests organizados en `tests/`
- ✅ Código optimizado y limpio

### Commit Realizado
```bash
commit: feat: Corregir error 403 en mapas y optimizar estructura del proyecto
branch: development
files changed: 43 files
insertions: 6651+
deletions: 76-
```

---

## 📋 CHECKLIST PRE-DEPLOY

### ✅ 1. Verificaciones Locales
- [x] Commit exitoso en development
- [x] Push a origin/development
- [x] Archivos innecesarios eliminados
- [x] Documentación organizada
- [x] Tests mantenidos
- [ ] Merge a main/master
- [ ] Crear tag de versión
- [ ] Deploy a PythonAnywhere

### ✅ 2. Archivos Críticos Verificados
- [x] `requirements.txt` - Actualizado
- [x] `.gitignore` - Actualizado
- [x] `censoapp/geolocation_views.py` - Corregido
- [x] `templates/maps/*.html` - Corregidos
- [x] Tests - Mantenidos y actualizados

---

## 🔀 PASO 1: MERGE A PRODUCCIÓN

### Opción A: Merge Directo (Recomendado)

```powershell
# 1. Cambiar a rama main
git checkout main

# 2. Pull últimos cambios
git pull origin main

# 3. Merge desde development
git merge development

# 4. Resolver conflictos (si hay)
# Editar archivos en conflicto manualmente

# 5. Commit del merge
git add .
git commit -m "chore: Merge development - Corrección mapas y optimización"

# 6. Push a main
git push origin main

# 7. Crear tag de versión
git tag -a v1.2.0 -m "Release v1.2.0 - Mapas optimizados"
git push origin v1.2.0

# 8. Volver a development
git checkout development
```

### Opción B: Pull Request (GitHub)

1. Ir a: https://github.com/LUISGA64/censo-django
2. Click en "Pull requests"
3. Click en "New pull request"
4. Base: `main` ← Compare: `development`
5. Crear Pull Request
6. Revisar cambios
7. Merge pull request
8. Eliminar rama development (opcional)

---

## 🌐 PASO 2: DEPLOY A PYTHONANYWHERE

### 2.1. Preparación

```bash
# En tu local, crear backup de BD
python manage.py dumpdata > backup_pre_deploy_$(Get-Date -Format "yyyyMMdd").json
```

### 2.2. Conectar a PythonAnywhere

#### Opción A: Console de PythonAnywhere

1. Ir a https://www.pythonanywhere.com
2. Login con tu cuenta
3. Click en "Consoles" → "Bash"

#### Opción B: SSH (si está habilitado)

```bash
ssh <tu_usuario>@ssh.pythonanywhere.com
```

### 2.3. Actualizar Código en PythonAnywhere

```bash
# En PythonAnywhere Bash Console

# 1. Navegar al directorio del proyecto
cd ~/censo-django

# 2. Hacer backup de archivos importantes
cp -r ~/censo-django ~/censo-django-backup-$(date +%Y%m%d)

# 3. Pull de los cambios
git fetch origin
git pull origin main

# 4. Activar virtual environment
source ~/venv/bin/activate

# 5. Instalar/actualizar dependencias
pip install -r requirements.txt

# 6. Ejecutar migraciones (si las hay)
python manage.py migrate

# 7. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 8. Verificar configuración
python manage.py check --deploy
```

### 2.4. Actualizar Variables de Entorno

```bash
# En PythonAnywhere

# Verificar .env
nano ~/.env

# Asegurarse de que estén:
DEBUG=False
ALLOWED_HOSTS=tu-dominio.pythonanywhere.com
SECRET_KEY=tu_secret_key_produccion
# ... otras variables
```

### 2.5. Recargar la Aplicación

#### Método 1: Web Interface
1. Ir a "Web" en PythonAnywhere
2. Click en el botón "Reload" verde

#### Método 2: API (si está configurado)
```bash
curl -X POST https://www.pythonanywhere.com/api/v0/user/<usuario>/webapps/<dominio>/reload/ \
  -H "Authorization: Token <tu_token>"
```

#### Método 3: Console
```bash
touch /var/www/<usuario>_pythonanywhere_com_wsgi.py
```

---

## 🧪 PASO 3: VERIFICACIÓN POST-DEPLOY

### 3.1. Verificaciones Básicas

```bash
# En PythonAnywhere console

# 1. Verificar que el servidor responde
curl https://tu-dominio.pythonanywhere.com/

# 2. Verificar logs de error
cat /var/log/<usuario>.pythonanywhere.com.error.log | tail -n 50

# 3. Verificar logs de acceso
cat /var/log/<usuario>.pythonanywhere.com.access.log | tail -n 20
```

### 3.2. Verificaciones Funcionales

#### ✅ Checklist de Verificación

1. **Página Principal**
   - [ ] Carga correctamente
   - [ ] Estilos se ven bien
   - [ ] No hay errores en consola

2. **Autenticación**
   - [ ] Login funciona
   - [ ] Logout funciona
   - [ ] Sesiones se mantienen

3. **Mapas (CRÍTICO)**
   - [ ] `https://tu-dominio.pythonanywhere.com/mapa/`
     - [ ] Mapa carga sin error 403
     - [ ] Selector de estilos funciona
     - [ ] Marcadores visibles
   - [ ] `https://tu-dominio.pythonanywhere.com/mapa/calor/`
     - [ ] Mapa de calor carga sin errores
     - [ ] Gradiente visible
   - [ ] `https://tu-dominio.pythonanywhere.com/mapa/clusters/`
     - [ ] Clusters funcionan
     - [ ] Marcadores expanden

4. **Funcionalidades Principales**
   - [ ] CRUD de personas
   - [ ] CRUD de fichas familiares
   - [ ] Búsqueda funciona
   - [ ] Dashboard muestra datos

### 3.3. Test de Rendimiento

```bash
# Desde tu máquina local

# Test de respuesta
curl -o /dev/null -s -w "Time: %{time_total}s\nStatus: %{http_code}\n" \
  https://tu-dominio.pythonanywhere.com/

# Debe responder en < 2 segundos
# Status debe ser 200
```

---

## 🛠️ PASO 4: TROUBLESHOOTING

### Problema 1: Error 500 después del deploy

**Solución:**
```bash
# En PythonAnywhere

# 1. Verificar logs
cat /var/log/<usuario>.pythonanywhere.com.error.log | tail -n 100

# 2. Verificar DEBUG está en False
python manage.py check --deploy

# 3. Verificar collectstatic
python manage.py collectstatic --noinput

# 4. Reload
touch /var/www/<usuario>_pythonanywhere_com_wsgi.py
```

### Problema 2: Mapas siguen con error 403

**Verificar:**
```bash
# En PythonAnywhere console

# 1. Verificar que el código está actualizado
cd ~/censo-django
git log --oneline -5

# 2. Verificar archivo específico
cat censoapp/geolocation_views.py | grep "CartoDB"

# Debe mostrar: tiles='CartoDB positron'
```

### Problema 3: Estilos no se ven

**Solución:**
```bash
# 1. Recolectar estáticos
python manage.py collectstatic --noinput --clear

# 2. Verificar STATIC_ROOT en settings
python manage.py diffsettings | grep STATIC

# 3. Verificar permisos
ls -la ~/censo-django/staticfiles/

# 4. Reload
touch /var/www/<usuario>_pythonanywhere_com_wsgi.py
```

### Problema 4: Base de datos no actualizada

**Solución:**
```bash
# 1. Verificar migraciones pendientes
python manage.py showmigrations

# 2. Aplicar migraciones
python manage.py migrate

# 3. Si falla, revisar
python manage.py migrate --plan
```

---

## 📊 PASO 5: MONITOREO POST-DEPLOY

### 5.1. Primeras 24 Horas

**Cada 2 horas:**
- [ ] Verificar logs de error
- [ ] Verificar tiempo de respuesta
- [ ] Verificar funcionalidad de mapas

### 5.2. Primera Semana

**Diariamente:**
- [ ] Revisar logs de error
- [ ] Verificar uso de recursos (CPU, RAM)
- [ ] Feedback de usuarios

### 5.3. Comandos Útiles

```bash
# En PythonAnywhere

# Ver últimos errores
cat /var/log/<usuario>.pythonanywhere.com.error.log | tail -n 50

# Ver accesos recientes
cat /var/log/<usuario>.pythonanywhere.com.access.log | tail -n 20

# Ver uso de disco
df -h

# Ver procesos
ps aux | grep python
```

---

## 🔄 ROLLBACK (Si algo sale mal)

### Plan de Rollback Rápido

```bash
# En PythonAnywhere

# 1. Volver al código anterior
cd ~/censo-django
git reset --hard <commit_anterior>

# 2. Restaurar backup de BD (si es necesario)
python manage.py loaddata backup_pre_deploy_YYYYMMDD.json

# 3. Reload
touch /var/www/<usuario>_pythonanywhere_com_wsgi.py

# 4. Verificar que funciona
curl https://tu-dominio.pythonanywhere.com/
```

---

## 📝 DOCUMENTACIÓN POST-DEPLOY

### Crear Registro de Deploy

```markdown
# Deploy Log - [FECHA]

## Versión: v1.2.0

### Cambios Principales:
- ✅ Corregido error 403 en mapas
- ✅ Implementado selector de estilos
- ✅ Optimizada estructura de archivos

### Deploy Info:
- **Fecha:** [YYYY-MM-DD HH:MM]
- **Usuario:** [tu_usuario]
- **Branch:** main
- **Commit:** [hash_commit]

### Verificaciones:
- [x] Mapas funcionando
- [x] Sin errores 403
- [x] Tests pasando
- [x] Logs limpios

### Issues:
- Ninguno

### Próximos Pasos:
- Monitorear rendimiento
- Recopilar feedback de usuarios
```

---

## ✅ CHECKLIST FINAL

- [ ] Código en development actualizado
- [ ] Tests pasando localmente
- [ ] Commit realizado
- [ ] Push a origin/development
- [ ] Merge a main
- [ ] Tag de versión creado
- [ ] Deploy a PythonAnywhere
- [ ] Migraciones aplicadas
- [ ] Static files recolectados
- [ ] Aplicación recargada
- [ ] Verificación de mapas ✅
- [ ] Verificación de funcionalidades ✅
- [ ] Logs revisados ✅
- [ ] Documentación actualizada ✅
- [ ] Backup creado ✅

---

## 📞 SOPORTE

### Si algo falla:

1. **Revisar logs primero**
   ```bash
   cat /var/log/<usuario>.pythonanywhere.com.error.log | tail -n 100
   ```

2. **Hacer rollback si es crítico**
   ```bash
   git reset --hard <commit_anterior>
   touch /var/www/<usuario>_pythonanywhere_com_wsgi.py
   ```

3. **Documentar el problema**
   - Capturas de pantalla
   - Logs de error
   - Pasos para reproducir

---

## 🎉 ¡ÉXITO!

Una vez completados todos los pasos:

✅ **Tu aplicación está en producción**
✅ **Mapas funcionando sin errores**
✅ **Código optimizado y limpio**
✅ **Documentación actualizada**

---

**Última actualización:** 2026-04-20  
**Versión objetivo:** v1.2.0  
**Estado:** ✅ Listo para deploy

