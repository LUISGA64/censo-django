# 📚 GUÍA COMPLETA DE MANTENIMIENTO Y OPTIMIZACIÓN - CENSO WEB

**Última actualización:** 2026-02-06  
**Versión:** 1.0

---

## 📋 TABLA DE CONTENIDOS

1. [Análisis y Optimización de Base de Datos](#análisis-y-optimización-de-base-de-datos)
2. [Monitoreo de Salud del Sistema](#monitoreo-de-salud-del-sistema)
3. [Backups y Recuperación](#backups-y-recuperación)
4. [Seguridad](#seguridad)
5. [Optimización de Rendimiento](#optimización-de-rendimiento)
6. [Deployment y Producción](#deployment-y-producción)
7. [Mejoras Futuras](#mejoras-futuras)

---

## 🔍 ANÁLISIS Y OPTIMIZACIÓN DE BASE DE DATOS

### Script de Análisis Automático

```bash
# Ejecutar análisis completo de la base de datos
python scripts/optimize_database.py
```

**Este script proporciona:**
- ✅ Estadísticas de registros
- ✅ Tamaño de tablas
- ✅ Índices actuales
- ✅ Sugerencias de optimización
- ✅ Análisis de rendimiento de consultas

### Comandos Útiles de Django

```bash
# 1. Verificar integridad del sistema
python manage.py check --deploy

# 2. Limpiar sesiones expiradas (ejecutar semanalmente)
python manage.py clearsessions

# 3. Ver migraciones pendientes
python manage.py showmigrations | grep "\[ \]"

# 4. Crear migraciones
python manage.py makemigrations

# 5. Aplicar migraciones
python manage.py migrate
```

### Optimización de MySQL (Solo Producción)

```bash
# Conectar a MySQL
python manage.py dbshell

# Dentro de MySQL:
# 1. Optimizar tablas principales
OPTIMIZE TABLE censoapp_person, censoapp_familycard, censoapp_organizations;

# 2. Actualizar estadísticas
ANALYZE TABLE censoapp_person, censoapp_familycard;

# 3. Ver tamaño de tablas
SELECT 
    TABLE_NAME,
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'Size (MB)',
    TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'tu_base_datos'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

# 4. Salir
exit;
```

### Índices Recomendados

Agregar estos índices en `censoapp/models.py` para mejorar el rendimiento:

```python
class Person(models.Model):
    # ... campos existentes ...
    
    class Meta:
        indexes = [
            models.Index(fields=['identification_person'], name='person_ident_idx'),
            models.Index(fields=['first_name_1', 'last_name_1'], name='person_name_idx'),
            models.Index(fields=['family_card', 'state'], name='person_family_state_idx'),
        ]

class FamilyCard(models.Model):
    # ... campos existentes ...
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', '-family_card_number'], name='family_org_num_idx'),
            models.Index(fields=['sidewalk_home'], name='family_sidewalk_idx'),
        ]
```

---

## 🏥 MONITOREO DE SALUD DEL SISTEMA

### Verificación Rápida

```bash
# Estado de la aplicación
python manage.py check

# Con deployment checks
python manage.py check --deploy
```

### Métricas Clave a Monitorear

**1. Rendimiento de Consultas**
- Activar `DEBUG = True` temporalmente para ver queries
- Usar Django Debug Toolbar en desarrollo
- Buscar N+1 queries con `select_related()` y `prefetch_related()`

**2. Logs del Sistema**
```bash
# Ver últimos 50 registros
tail -n 50 logs/django.log

# Ver errores
grep "ERROR" logs/django.log

# Monitoreo en tiempo real
tail -f logs/django.log
```

**3. Espacio en Disco**
```bash
# Windows PowerShell
Get-PSDrive C | Select-Object Used,Free

# Linux (PythonAnywhere)
df -h
```

---

## 💾 BACKUPS Y RECUPERACIÓN

### Backup Automático (Configurado)

```bash
# Verificar configuración en crontab (Linux)
crontab -l

# Debería mostrar:
0 2 * * * cd ~/censo-django && workon censo-env && python manage.py backup_db --compress
```

### Backup Manual

```bash
# 1. Backup completo de base de datos
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude contenttypes --exclude auth.permission \
    --exclude sessions.session \
    > backups/backup_$(date +%Y%m%d_%H%M%S).json

# 2. Backup solo de datos de censoapp
python manage.py dumpdata censoapp --indent 2 > backups/censoapp_backup.json

# 3. Backup de MySQL directo
mysqldump -u usuario -p censodb > backups/mysql_backup.sql

# 4. Comprimir backup
gzip backups/mysql_backup.sql
```

### Restauración

```bash
# 1. Desde JSON
python manage.py loaddata backups/backup_20260206.json

# 2. Desde MySQL dump
mysql -u usuario -p censodb < backups/mysql_backup.sql

# 3. Desde dump comprimido
gunzip < backups/mysql_backup.sql.gz | mysql -u usuario -p censodb
```

### Limpieza de Backups Antiguos

```bash
# Eliminar backups mayores a 30 días
find backups/ -name "*.json" -mtime +30 -delete
find backups/ -name "*.sql.gz" -mtime +30 -delete
```

---

## 🔒 SEGURIDAD

### Checklist de Seguridad

#### Producción (OBLIGATORIO)

```python
# En .env de producción
DEBUG=False
SECRET_KEY=<generar-una-nueva-clave-muy-larga>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

#### Generar Claves Seguras

```bash
# SECRET_KEY
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# DATA_ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

#### Actualizar Dependencias

```bash
# 1. Ver paquetes desactualizados
pip list --outdated

# 2. Actualizar Django (con precaución)
pip install --upgrade Django

# 3. Actualizar Django REST Framework
pip install --upgrade djangorestframework

# 4. Actualizar todas las dependencias (PELIGROSO)
pip install --upgrade -r requirements.txt

# 5. Congelar versiones actualizadas
pip freeze > requirements_frozen.txt
```

#### Auditoría de Seguridad

```bash
# Instalar safety
pip install safety

# Verificar vulnerabilidades
safety check

# Verificar con bandit (análisis estático)
pip install bandit
bandit -r censoapp/ censoProject/
```

---

## ⚡ OPTIMIZACIÓN DE RENDIMIENTO

### 1. Caché

#### Configurar Redis (Recomendado)

```bash
# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Windows (con WSL o Docker)
docker run --name redis -p 6379:6379 -d redis
```

```python
# En settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

#### Usar Caché en Vistas

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutos
def mi_vista(request):
    # ... código ...
    pass
```

### 2. Optimizar Consultas

```python
# ❌ MAL - N+1 queries
persons = Person.objects.all()
for person in persons:
    print(person.family_card.organization.organization_name)  # Query por cada persona

# ✅ BIEN - 1 query
persons = Person.objects.select_related(
    'family_card',
    'family_card__organization'
).all()
for person in persons:
    print(person.family_card.organization.organization_name)  # Sin queries extra

# ✅ Para relaciones many-to-many
families = FamilyCard.objects.prefetch_related('person_set').all()
```

### 3. Paginación

```python
# En API viewsets
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class PersonViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
```

### 4. Archivos Estáticos

```bash
# Producción - Comprimir y servir archivos estáticos
pip install whitenoise

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Comprimir (si usas django-compressor)
python manage.py compress
```

---

## 🚀 DEPLOYMENT Y PRODUCCIÓN

### Pre-Deployment Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` única y segura
- [ ] `ALLOWED_HOSTS` configurado
- [ ] SSL/HTTPS activado
- [ ] Base de datos en MySQL/PostgreSQL (no SQLite)
- [ ] Archivos estáticos colectados
- [ ] Migraciones aplicadas
- [ ] Backup reciente creado
- [ ] Variables de entorno verificadas
- [ ] Logs configurados
- [ ] Email configurado (notificaciones)

### Deploy a PythonAnywhere

```bash
# 1. Conectar por SSH
ssh usuario@ssh.pythonanywhere.com

# 2. Ir al directorio del proyecto
cd ~/censo-django

# 3. Activar entorno virtual
workon censo-env

# 4. Pull de cambios
git pull origin development

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Aplicar migraciones
python manage.py migrate

# 7. Colectar archivos estáticos
python manage.py collectstatic --noinput

# 8. Recargar aplicación web
touch /var/www/tu_usuario_pythonanywhere_com_wsgi.py

# O desde el dashboard de PythonAnywhere: Web > Reload
```

### Monitoreo Post-Deployment

```bash
# Ver logs en tiempo real
tail -f /var/log/tu_usuario.pythonanywhere.com.error.log
tail -f /var/log/tu_usuario.pythonanywhere.com.server.log

# Verificar procesos
ps aux | grep python

# Verificar espacio
df -h
```

---

## 🎯 MEJORAS FUTURAS RECOMENDADAS

### Corto Plazo (1-2 semanas)

1. **Configurar Email** para notificaciones
   - Password recovery
   - Notificaciones de cambios
   - Alertas del sistema

2. **Implementar Sentry** para monitoreo de errores
   ```bash
   pip install sentry-sdk
   ```

3. **Agregar Tests Automatizados**
   ```bash
   python manage.py test censoapp
   ```

### Mediano Plazo (1-2 meses)

4. **API Completa con JWT**
   - ✅ Ya implementado parcialmente
   - Documentación con Swagger
   - Rate limiting

5. **Dashboard de Analytics**
   - Gráficos de estadísticas
   - Reportes automáticos
   - Exportación a Excel/PDF

6. **Sistema de Permisos Granular**
   - Permisos por módulo
   - Roles personalizados
   - Auditoría de accesos

### Largo Plazo (3-6 meses)

7. **Migrar Frontend a React/Vue**
   - SPA moderna
   - Mejor UX
   - PWA (Progressive Web App)

8. **Microservicios**
   - Separar documentos
   - API Gateway
   - Escalabilidad horizontal

9. **Machine Learning**
   - Predicciones demográficas
   - Detección de anomalías
   - Recomendaciones inteligentes

---

## 📊 COMANDOS DE REFERENCIA RÁPIDA

```bash
# === DESARROLLO ===
python manage.py runserver                    # Iniciar servidor de desarrollo
python manage.py makemigrations              # Crear migraciones
python manage.py migrate                     # Aplicar migraciones
python manage.py createsuperuser            # Crear superusuario
python manage.py shell                       # Shell interactivo

# === BASE DE DATOS ===
python scripts/optimize_database.py          # Análisis completo de BD
python manage.py dumpdata > backup.json     # Backup
python manage.py loaddata backup.json       # Restaurar
python manage.py dbshell                    # Conectar a BD

# === MANTENIMIENTO ===
python manage.py check --deploy             # Verificar configuración
python manage.py clearsessions              # Limpiar sesiones
python manage.py collectstatic --noinput    # Colectar estáticos

# === TESTS ===
python manage.py test                       # Ejecutar tests
python manage.py test censoapp             # Tests de una app

# === GIT ===
git status                                  # Ver estado
git add .                                   # Agregar cambios
git commit -m "mensaje"                    # Commit
git push origin development                # Push a GitHub
git pull origin development                # Pull de GitHub
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "TemplateSyntaxError: Invalid block tag 'static'"
```python
# Agregar al inicio del template
{% load static %}
```

### Error: "ImproperlyConfigured: mysqlclient"
```bash
pip install mysqlclient
# O en Windows:
pip install pymysql
# Luego en __init__.py:
import pymysql
pymysql.install_as_MySQLdb()
```

### Error: "CSRF verification failed"
```python
# En settings.py
CSRF_TRUSTED_ORIGINS = ['https://tu-dominio.com']
```

### Error: "Static files not found"
```bash
python manage.py collectstatic --noinput
```

---

## 📞 CONTACTO Y SOPORTE

- **Repositorio:** https://github.com/LUISGA64/censo-django
- **Issues:** https://github.com/LUISGA64/censo-django/issues
- **Email:** webcenso@gmail.com

---

## 📝 REGISTRO DE CAMBIOS

### 2026-02-06
- ✅ API REST con JWT implementada
- ✅ Búsqueda global mejorada
- ✅ Scripts de optimización creados
- ✅ Documentación consolidada
- ✅ Deploy a PythonAnywhere con MySQL

---

**Última revisión:** 2026-02-06  
**Autor:** Equipo Censo Web  
**Versión del documento:** 1.0
