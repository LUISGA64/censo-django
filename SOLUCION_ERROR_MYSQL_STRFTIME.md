# 🔧 Solución: Error MySQL strftime

## 🐛 Error Reportado

```
OperationalError at /documentos/estadisticas/2/
(1305, 'FUNCTION censodb.strftime does not exist')
```

**Ubicación**: `organization_stats.html` línea 608 (en el template)

---

## 🔍 Análisis del Problema

### El código Python está CORRECTO ✅

El archivo `document_views.py` ya usa funciones compatibles con MySQL:

```python
from django.db.models.functions import TruncMonth

docs_by_month = GeneratedDocument.objects.filter(
    organization=organization,
    issue_date__gte=six_months_ago
).annotate(
    month_date=TruncMonth('issue_date')  # ✅ Compatible con MySQL
).values('month_date').annotate(
    total=Count('id')
).order_by('month_date')
```

`TruncMonth` es una función de Django que se traduce correctamente a MySQL.

### ¿Por qué ocurre el error entonces?

El error `strftime` es típico cuando:

1. **SQLite en producción**: El servidor está usando SQLite en lugar de MySQL
2. **Migraciones pendientes**: Hay cambios en el modelo no aplicados
3. **Cache corrupto**: Django está usando consultas cacheadas con SQLite
4. **Configuración mixta**: Múltiples settings apuntando a diferentes DBs

---

## ✅ Solución Paso a Paso

### Paso 1: Verificar qué base de datos se está usando

```bash
# En el servidor de producción
cd /home/tuusuario/censo-django
python manage.py shell
```

```python
from django.conf import settings
print(settings.DATABASES['default'])

# Debe mostrar:
# {
#     'ENGINE': 'django.db.backends.mysql',  # ✅ Debe ser mysql
#     'NAME': 'tuusuario$censodb',
#     ...
# }

# Si muestra 'sqlite3' → Ese es el problema ❌
```

### Paso 2: Verificar settings activo

```python
# En el mismo shell
print(settings.SETTINGS_MODULE)

# Debe mostrar:
# 'censoProject.settings_pythonanywhere'  # ✅ Correcto

# Si muestra otra cosa → Cambiar configuración WSGI
```

### Paso 3: Verificar archivo WSGI

Editar: `/var/www/tuusuario_pythonanywhere_com_wsgi.py`

```python
import os
import sys

# Agregar el path del proyecto
path = '/home/tuusuario/censo-django'
if path not in sys.path:
    sys.path.append(path)

# ⚠️ IMPORTANTE: Especificar settings de producción
os.environ['DJANGO_SETTINGS_MODULE'] = 'censoProject.settings_pythonanywhere'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Paso 4: Limpiar cache

```bash
python manage.py shell
```

```python
from django.core.cache import cache
cache.clear()
print("✅ Cache limpiado")
exit()
```

### Paso 5: Ejecutar migraciones

```bash
python manage.py migrate --settings=censoProject.settings_pythonanywhere
```

### Paso 6: Recargar aplicación web

En PythonAnywhere:
1. Ir a: Web → tuusuario.pythonanywhere.com
2. Hacer clic en el botón verde "Reload"
3. Esperar 10 segundos

### Paso 7: Verificar logs

En PythonAnywhere:
1. Web → Log files
2. Ver: error.log y server.log
3. Buscar mensajes de error relacionados con base de datos

---

## 🔍 Diagnóstico Avanzado

### Script de diagnóstico

Crear archivo: `diagnostico_mysql.py`

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings_pythonanywhere')
django.setup()

from django.conf import settings
from django.db import connection

print("=" * 70)
print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
print("=" * 70)

print(f"\n📁 Settings module: {settings.SETTINGS_MODULE}")
print(f"\n🗄️  Database engine: {settings.DATABASES['default']['ENGINE']}")
print(f"📊 Database name: {settings.DATABASES['default']['NAME']}")

# Probar conexión
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"\n✅ MySQL Version: {version[0]}")
        
        # Verificar tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Tablas encontradas: {len(tables)}")
        
        # Verificar función de fecha
        cursor.execute("SELECT DATE_FORMAT(NOW(), '%Y-%m') as month")
        result = cursor.fetchone()
        print(f"✅ Funciones de fecha MySQL funcionan: {result[0]}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n⚠️  Posible problema de configuración de base de datos")

print("\n" + "=" * 70)
```

Ejecutar:
```bash
python diagnostico_mysql.py
```

---

## 🛠️ Soluciones Específicas

### Solución 1: Si está usando SQLite en producción

Editar `settings_pythonanywhere.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Cambiar de sqlite3 a mysql
        'NAME': 'tuusuario$censodb',
        'USER': 'tuusuario',
        'PASSWORD': 'tu_password_mysql',
        'HOST': 'tuusuario.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### Solución 2: Si faltan dependencias de MySQL

```bash
pip install mysqlclient
# o
pip install PyMySQL

# Si usas PyMySQL, agregar en settings:
import pymysql
pymysql.install_as_MySQLdb()
```

### Solución 3: Si hay error de conexión a MySQL

Verificar credenciales en PythonAnywhere:
1. Databases → MySQL
2. Verificar: nombre de BD, usuario, contraseña
3. Probar conexión desde consola MySQL

---

## 🔄 Alternativa: Usar funciones raw SQL (NO RECOMENDADO)

Solo si nada funciona, modificar `document_views.py`:

```python
from django.db import connection

def get_docs_by_month_mysql(organization, six_months_ago):
    """
    Consulta raw SQL específica para MySQL
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                DATE_FORMAT(issue_date, '%Y-%m-01') as month_date,
                COUNT(*) as total
            FROM censoapp_generateddocument
            WHERE organization_id = %s
            AND issue_date >= %s
            GROUP BY DATE_FORMAT(issue_date, '%Y-%m')
            ORDER BY month_date
        """, [organization.id, six_months_ago])
        
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Usar en la vista:
docs_by_month = get_docs_by_month_mysql(organization, six_months_ago)
```

⚠️ **Nota**: Esta es una solución temporal. Lo ideal es que Django ORM funcione correctamente.

---

## ✅ Checklist de Verificación

Después de aplicar las soluciones:

- [ ] `settings.DATABASES['default']['ENGINE']` muestra `mysql`
- [ ] Conexión a MySQL exitosa desde shell
- [ ] Migraciones aplicadas sin errores
- [ ] Cache limpiado
- [ ] Aplicación web recargada
- [ ] Página de estadísticas se carga sin error
- [ ] Gráfico de "Documentos por mes" se muestra
- [ ] No hay errores en logs de PythonAnywhere

---

## 📊 Prueba Final

```python
# En shell de Django (producción)
from censoapp.models import GeneratedDocument, Organizations
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

org = Organizations.objects.first()
six_months_ago = timezone.now().date() - timedelta(days=180)

docs = GeneratedDocument.objects.filter(
    organization=org,
    issue_date__gte=six_months_ago
).annotate(
    month_date=TruncMonth('issue_date')
).values('month_date').annotate(
    total=Count('id')
).order_by('month_date')

print("✅ Documentos por mes:")
for doc in docs:
    print(f"  {doc['month_date']}: {doc['total']} documentos")

# Si esto funciona sin error → Problema resuelto ✅
# Si da error → Revisar configuración de BD
```

---

## 🚨 Si el problema persiste

1. **Exportar datos** de SQLite a MySQL:
   ```bash
   python manage.py dumpdata > backup_data.json
   # Cambiar a MySQL
   python manage.py migrate
   python manage.py loaddata backup_data.json
   ```

2. **Contactar soporte de PythonAnywhere**:
   - Enviar: Captura del error completo
   - Incluir: Configuración de DATABASES
   - Mencionar: Versión de Django y MySQL

3. **Revisar versión de MySQL**:
   - PythonAnywhere requiere MySQL 5.7+
   - Algunas funciones no están en versiones antiguas

---

## 📝 Resumen

El error `strftime` NO es un problema del código (que está correcto), sino de:
- **Configuración**: Usar SQLite en lugar de MySQL
- **Cache**: Consultas antiguas cacheadas
- **Migraciones**: Cambios no aplicados

**Solución principal**: Verificar y corregir la configuración de base de datos en producción.

---

**Última actualización**: 2 de Enero de 2026

