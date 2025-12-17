# 🏠 Crear Datos de Prueba - Censo Django

Script automatizado para crear fichas familiares y personas de prueba con datos realistas.

## 🚀 Uso Rápido

```bash
python crear_datos_prueba.py
```

Esto creará **5 fichas familiares** con **15-20 personas** aproximadamente.

## ⚙️ Configuración

### Cambiar la cantidad de familias

Edita la línea 330 en `crear_datos_prueba.py`:

```python
num_familias = 10  # Cambiar el número (máximo 20)
```

## ✅ Prerequisitos

Antes de ejecutar el script, asegúrate de tener datos en estas tablas:

- ✅ Sidewalks (Veredas)
- ✅ Organizations (Resguardos)
- ✅ IdentificationDocumentType (Tipos de documento)
- ✅ Gender (Géneros)
- ✅ CivilState (Estados civiles)
- ✅ EducationLevel (Niveles educativos)
- ✅ Occupancy (Ocupaciones)
- ✅ Kinship (Parentescos)
- ✅ SecuritySocial (Seguridad social)
- ✅ Eps (EPS)
- ✅ Handicap (Capacidades diversas)

## 📊 ¿Qué crea el script?

### Por cada familia:
- 1 Ficha familiar con datos de ubicación
- 1 Cabeza de familia (mayor de 18 años)
- 1-4 Miembros adicionales (cónyuge, hijos)

### Datos generados:
- ✅ Nombres y apellidos realistas
- ✅ Documentos únicos (CC, TI, RC según edad)
- ✅ Edades coherentes
- ✅ Parentescos apropiados
- ✅ Todos los campos obligatorios

## 📝 Ejemplo de salida

```
======================================================================
🏠 CREACIÓN DE FICHAS FAMILIARES Y PERSONAS DE PRUEBA
======================================================================
📋 Verificando datos base...
✅ sidewalks: 3 registros
✅ organizations: 2 registros
...

🏠 Creando 5 fichas familiares de prueba...
✅ Ficha #7 - Campamento (Urbana)
✅ Ficha #8 - Puracé (Rural)
...

👨‍👩‍👧‍👦 Creando personas para cada familia...

📋 Ficha #7 - Campamento
  👤 Cabeza: Luz Elena Rodríguez Sánchez - 48422827
    👥 Andrés Miguel Rodríguez Sánchez - Cónyuge - 60649307
    👥 Luis Rodríguez - Hijo/a - 86397370

======================================================================
📊 RESUMEN DE CREACIÓN
======================================================================
✅ Fichas familiares creadas: 5
✅ Personas creadas: 15
✅ Promedio de miembros por familia: 3.0

🎉 ¡Datos de prueba creados exitosamente!
======================================================================
```

## 🔍 Verificar datos creados

### En la interfaz web:
1. Accede a `http://127.0.0.1:8000/family-card/`
2. Verifica las nuevas fichas
3. Revisa los detalles de cada familia

### En la consola de Django:
```bash
python manage.py shell
```

```python
from censoapp.models import FamilyCard, Person

# Ver total de fichas
print(f"Total fichas: {FamilyCard.objects.count()}")

# Ver total de personas
print(f"Total personas: {Person.objects.count()}")

# Ver última ficha creada
ficha = FamilyCard.objects.latest('created_at')
print(f"Ficha #{ficha.family_card_number}")
personas = Person.objects.filter(family_card=ficha)
for p in personas:
    print(f"  - {p.full_name} ({p.kinship.description_kinship})")
```

## 🗑️ Limpiar datos de prueba

```bash
python manage.py shell
```

```python
from censoapp.models import FamilyCard
from datetime import datetime

# Ver fichas creadas hoy
hoy = datetime.now().date()
fichas = FamilyCard.objects.filter(created_at__date=hoy)
print(f"Fichas a eliminar: {fichas.count()}")

# Eliminar (¡cuidado!)
# fichas.delete()
```

## 📚 Documentación completa

Ver: `docs/SCRIPT_DATOS_PRUEBA.md`

## ⚠️ Notas importantes

- Los números de ficha son secuenciales y únicos
- Los documentos de identidad son únicos
- El script valida que existan datos base antes de crear
- Se pueden ejecutar múltiples veces sin problemas

## 🐛 Problemas comunes

### "No hay datos en kinships"
**Solución:** Carga datos en la tabla Kinship con valores como "Padre", "Hijo", "Cónyuge"

### "UNIQUE constraint failed"
**Solución:** Ya está solucionado. Si ocurre, reporta el error.

### "Error al crear cabeza de familia"
**Solución:** Verifica que todas las tablas relacionadas tengan al menos 1 registro.

---

**¿Necesitas ayuda?** Revisa la documentación completa en `docs/SCRIPT_DATOS_PRUEBA.md`

