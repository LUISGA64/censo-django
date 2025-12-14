# 🚀 Guía de Despliegue - Datos de Vivienda

## Checklist Pre-Despliegue

### ✅ 1. Verificaciones Locales

```bash
# Ejecutar tests
python manage.py test censoapp -v 2

# Verificar migraciones
python manage.py makemigrations --dry-run
python manage.py migrate --plan

# Colectar archivos estáticos
python manage.py collectstatic --noinput
```

### ✅ 2. Backup de Base de Datos

**SQLite (desarrollo):**
```bash
cp db.censo_Web db.censo_Web.backup_$(date +%Y%m%d_%H%M%S)
```

**PostgreSQL (producción):**
```bash
pg_dump -U usuario -d censo_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

---

## 📦 Pasos de Despliegue

### Paso 1: Actualizar Código
```bash
git pull origin main
# o subir archivos modificados vía FTP/SFTP
```

### Paso 2: Activar Entorno Virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar/Actualizar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar Migraciones
```bash
python manage.py migrate censoapp
```

**Migración esperada:**
```
Applying censoapp.0020_alter_materialconstructionfamilycard_unique_together_and_more... OK
```

### Paso 5: Crear/Verificar Parámetro del Sistema

**Opción A: Django Admin**
1. Ir a `/admin/censoapp/systemparameters/`
2. Buscar: "Datos de Vivienda"
3. Si existe: Verificar value = 'S' o 'N'
4. Si no existe: Crear nuevo:
   - Key: `Datos de Vivienda`
   - Value: `S` (para habilitar)

**Opción B: Django Shell**
```python
python manage.py shell

from censoapp.models import SystemParameters

# Crear o actualizar
param, created = SystemParameters.objects.get_or_create(
    key='Datos de Vivienda',
    defaults={'value': 'S'}
)

if not created:
    param.value = 'S'  # o 'N' para deshabilitar
    param.save()
    
print(f"Parámetro: {param.key} = {param.value}")
exit()
```

### Paso 6: Cargar Datos de Materiales (Si es necesario)

**Verificar si existen materiales:**
```python
python manage.py shell

from censoapp.models import MaterialConstruction, HomeOwnership, CookingFuel

print(f"Materiales: {MaterialConstruction.objects.count()}")
print(f"Tipos de propiedad: {HomeOwnership.objects.count()}")
print(f"Combustibles: {CookingFuel.objects.count()}")
```

**Si están vacíos, crear datos básicos:**
```python
# Materiales de Techo
MaterialConstruction.objects.create(material_name='Zinc', roof=True, wall=False, floor=False)
MaterialConstruction.objects.create(material_name='Teja', roof=True, wall=False, floor=False)
MaterialConstruction.objects.create(material_name='Eternit', roof=True, wall=False, floor=False)

# Materiales de Pared
MaterialConstruction.objects.create(material_name='Ladrillo', roof=False, wall=True, floor=False)
MaterialConstruction.objects.create(material_name='Madera', roof=False, wall=True, floor=False)
MaterialConstruction.objects.create(material_name='Adobe', roof=False, wall=True, floor=False)

# Materiales de Piso
MaterialConstruction.objects.create(material_name='Cemento', roof=False, wall=False, floor=True)
MaterialConstruction.objects.create(material_name='Baldosa', roof=False, wall=False, floor=True)
MaterialConstruction.objects.create(material_name='Tierra', roof=False, wall=False, floor=True)

# Tipos de Propiedad
HomeOwnership.objects.create(ownership_type='Propia')
HomeOwnership.objects.create(ownership_type='Arrendada')
HomeOwnership.objects.create(ownership_type='Familiar')

# Combustibles
CookingFuel.objects.create(fuel_type='Gas Natural')
CookingFuel.objects.create(fuel_type='Gas Propano')
CookingFuel.objects.create(fuel_type='Leña')
CookingFuel.objects.create(fuel_type='Eléctrico')
```

### Paso 7: Colectar Archivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### Paso 8: Reiniciar Servidor

**Gunicorn:**
```bash
sudo systemctl restart gunicorn
```

**Apache:**
```bash
sudo service apache2 restart
```

**Nginx + uWSGI:**
```bash
sudo systemctl restart uwsgi
sudo systemctl restart nginx
```

**Desarrollo (runserver):**
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Verificaciones Post-Despliegue

### 1. Verificar Migración
```bash
python manage.py showmigrations censoapp
```

Debe mostrar:
```
[X] 0020_alter_materialconstructionfamilycard_unique_together_and_more
```

### 2. Verificar Parámetro
```bash
python manage.py shell -c "from censoapp.models import SystemParameters; print(SystemParameters.objects.get(key='Datos de Vivienda').value)"
```

### 3. Probar Funcionalidad (Manual)
1. Login al sistema
2. Ir a "Fichas Familiares"
3. Seleccionar una ficha y click "Editar"
4. Verificar que aparece pestaña "Datos de Vivienda"
5. Completar formulario de prueba
6. Guardar y verificar mensaje de éxito
7. Recargar página y verificar que datos persisten

### 4. Ejecutar Tests en Producción (Opcional)
```bash
python manage.py test censoapp.tests.UpdateFamilyMaterialFormTests --keepdb
```

---

## ⚠️ Rollback (Si algo sale mal)

### Opción 1: Revertir Migración
```bash
# Listar migraciones
python manage.py showmigrations censoapp

# Revertir a migración anterior
python manage.py migrate censoapp 0019_avalgenerated
```

### Opción 2: Restaurar Backup
```bash
# SQLite
cp db.censo_Web.backup_YYYYMMDD_HHMMSS db.censo_Web

# PostgreSQL
psql -U usuario -d censo_db < backup_YYYYMMDD_HHMMSS.sql
```

### Opción 3: Deshabilitar Funcionalidad
```python
python manage.py shell

from censoapp.models import SystemParameters
param = SystemParameters.objects.get(key='Datos de Vivienda')
param.value = 'N'
param.save()
```

---

## 🔍 Monitoreo Post-Despliegue

### Logs a Revisar:

**Django:**
```bash
tail -f /var/log/django/application.log
```

**Nginx:**
```bash
tail -f /var/log/nginx/error.log
```

**Gunicorn:**
```bash
journalctl -u gunicorn -f
```

### Métricas a Monitorear:
- ✅ Tiempo de respuesta de edición de fichas
- ✅ Errores 500 en logs
- ✅ Uso de memoria/CPU
- ✅ Queries lentas en base de datos
- ✅ Feedback de usuarios

---

## 📊 Verificación de Integridad de Datos

```python
python manage.py shell

from censoapp.models import MaterialConstructionFamilyCard, FamilyCard

# Verificar registros de vivienda
total_viviendas = MaterialConstructionFamilyCard.objects.count()
total_fichas = FamilyCard.objects.filter(state=True).count()

print(f"Fichas familiares activas: {total_fichas}")
print(f"Registros de vivienda: {total_viviendas}")
print(f"Cobertura: {(total_viviendas/total_fichas*100):.2f}%")

# Verificar integridad OneToOneField
duplicados = MaterialConstructionFamilyCard.objects.values('family_card').annotate(
    count=Count('id')
).filter(count__gt=1)

if duplicados.exists():
    print(f"⚠️ ALERTA: {duplicados.count()} fichas con múltiples registros de vivienda")
else:
    print("✅ Integridad OneToOneField verificada")
```

---

## 📞 Soporte

### En Caso de Problemas:

1. **Revisar logs** (ver sección Monitoreo)
2. **Ejecutar tests**: `python manage.py test censoapp -v 2`
3. **Verificar permisos** de archivos y directorios
4. **Validar configuración** de base de datos
5. **Consultar documentación**:
   - `IMPLEMENTACION_DATOS_VIVIENDA.md`
   - `RESUMEN_EJECUTIVO_VIVIENDA.md`

### Comandos de Diagnóstico:
```bash
# Verificar versión de Django
python manage.py --version

# Verificar configuración
python manage.py check

# Verificar conexión a BD
python manage.py dbshell

# Listar migraciones pendientes
python manage.py showmigrations --plan
```

---

## ✅ Checklist Final

- [ ] Backup de base de datos realizado
- [ ] Código actualizado en servidor
- [ ] Migraciones ejecutadas correctamente
- [ ] Parámetro "Datos de Vivienda" configurado
- [ ] Datos de materiales cargados
- [ ] Archivos estáticos colectados
- [ ] Servidor reiniciado
- [ ] Tests ejecutados exitosamente
- [ ] Prueba manual completada
- [ ] Logs revisados (sin errores)
- [ ] Equipo notificado del despliegue
- [ ] Documentación actualizada

---

**Fecha:** 13 de Diciembre de 2025  
**Versión:** 1.0.0  
**Responsable:** Administrador del Sistema

