# ✅ CHECKLIST DE DEPLOYMENT - PYTHONANYWHERE

## 📋 PRE-DEPLOYMENT (Local)

- [ ] Código probado localmente sin errores
- [ ] Todos los tests pasan
- [ ] Migrations creadas y funcionando
- [ ] Archivos estáticos funcionan
- [ ] .gitignore actualizado
- [ ] Commit de últimos cambios
- [ ] Push a GitHub (rama development o main)

---

## 🚀 DEPLOYMENT EN PYTHONANYWHERE

### 1. Preparación Inicial
- [ ] Cuenta de PythonAnywhere activa
- [ ] MySQL database creada
- [ ] Virtualenv configurado

### 2. Actualizar Código
```bash
cd ~/censo-django
git pull origin development
```
- [ ] Código actualizado

### 3. Configurar .env
```bash
nano ~/censo-django/.env
```
- [ ] SECRET_KEY configurado
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] DB_NAME configurado
- [ ] DB_USER configurado
- [ ] DB_PASSWORD configurado
- [ ] DB_HOST configurado
- [ ] SITE_URL configurado

### 4. Instalar Dependencias
```bash
workon censo-env
pip install -r requirements.txt
```
- [ ] Dependencias instaladas

### 5. Migraciones
```bash
python manage.py migrate
```
- [ ] Migraciones ejecutadas

### 6. Superusuario
```bash
python manage.py createsuperuser
```
- [ ] Superusuario creado

### 7. Archivos Estáticos
```bash
python manage.py collectstatic --noinput
```
- [ ] Collectstatic ejecutado

### 8. Configurar WSGI
- [ ] WSGI file editado
- [ ] Path del proyecto correcto
- [ ] Virtualenv path correcto
- [ ] Settings module correcto

### 9. Static Files (Web config)
- [ ] /static/ → /home/tuusuario/censo-django/staticfiles/
- [ ] /media/ → /home/tuusuario/censo-django/media/

### 10. Recargar Web App
- [ ] Click en botón "Reload"

---

## ✅ POST-DEPLOYMENT

### Verificaciones Básicas
- [ ] Sitio carga: https://tuusuario.pythonanywhere.com/
- [ ] Login funciona
- [ ] Admin accesible: /admin/
- [ ] Archivos estáticos cargan (CSS, JS)

### Verificaciones de Funcionalidades
- [ ] Dashboard Analytics funciona
- [ ] Búsqueda Global funciona
- [ ] API REST accesible: /api/token/
- [ ] Personas listado funciona
- [ ] Fichas familiares funcionan
- [ ] Documentos funcionan
- [ ] Mapas cargan correctamente
- [ ] Importación masiva funciona

### API REST Tests
```bash
# Test de autenticación
curl -X POST https://tuusuario.pythonanywhere.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```
- [ ] API token se obtiene correctamente

```bash
# Test de listado
curl https://tuusuario.pythonanywhere.com/api/v1/persons/ \
  -H "Authorization: Bearer TOKEN"
```
- [ ] API persons funciona

### Configurar Backups Automáticos
```bash
crontab -e
# Agregar:
# 0 2 * * * cd /home/tuusuario/censo-django && /home/tuusuario/.virtualenvs/censo-env/bin/python manage.py backup_db --compress --keep-days 30
```
- [ ] Crontab configurado
- [ ] Carpeta backups/ existe
- [ ] Permisos correctos (755)

### Verificar Logs
```bash
tail -f /var/log/tuusuario.pythonanywhere.com.error.log
tail -f ~/censo-django/logs/django.log
```
- [ ] No hay errores críticos
- [ ] Logs funcionan correctamente

---

## 📊 PRUEBAS FUNCIONALES

### Búsqueda Global
- [ ] Buscar desde navbar
- [ ] Buscar desde /search/
- [ ] Resultados correctos
- [ ] Click redirige correctamente

### Dashboard
- [ ] KPIs se muestran
- [ ] Gráficos cargan
- [ ] Datos correctos

### API REST
- [ ] POST /api/token/ funciona
- [ ] GET /api/v1/persons/ funciona
- [ ] GET /api/v1/family-cards/ funciona
- [ ] GET /api/v1/documents/ funciona
- [ ] Filtros funcionan
- [ ] Búsqueda funciona
- [ ] Paginación funciona

### Sidebar
- [ ] Todos los nav-items visibles
- [ ] Sin scroll
- [ ] Responsive en móvil

---

## 🔒 SEGURIDAD

- [ ] DEBUG=False
- [ ] SECRET_KEY única y segura
- [ ] ALLOWED_HOSTS configurado
- [ ] SSL/HTTPS activo
- [ ] Cookies seguras
- [ ] CSRF protection activo
- [ ] Rate limiting activo en API

---

## 📝 DOCUMENTACIÓN

- [ ] Actualizar documentación con URLs de producción
- [ ] Documentar credenciales de admin (seguro)
- [ ] Documentar proceso de deployment
- [ ] Crear guía para usuarios finales

---

## 🎯 OPTIMIZACIONES OPCIONALES

- [ ] Configurar Redis cache (si disponible)
- [ ] Configurar Sentry monitoring
- [ ] Configurar email SMTP
- [ ] Optimizar queries lentas
- [ ] Comprimir assets
- [ ] CDN para archivos estáticos

---

## ✅ DEPLOYMENT COMPLETO

Cuando TODOS los checks anteriores estén marcados:

**DEPLOYMENT EXITOSO** ✅

**URLs Importantes:**
- Sitio: https://tuusuario.pythonanywhere.com/
- Admin: https://tuusuario.pythonanywhere.com/admin/
- Dashboard: https://tuusuario.pythonanywhere.com/dashboard/analytics/
- Búsqueda: https://tuusuario.pythonanywhere.com/search/
- API: https://tuusuario.pythonanywhere.com/api/v1/

**Siguiente:**
- Entrenar usuarios
- Monitorear errores
- Backup manual inicial
- Configurar email notifications

---

**Fecha de deployment:** _______________
**Deployado por:** _______________
**Versión:** 2.0 - Fase 1 Completa
