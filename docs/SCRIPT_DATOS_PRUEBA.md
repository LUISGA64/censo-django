# Script de Creación de Datos de Prueba - Censo Django

**Fecha:** 2025-12-15  
**Archivo:** `crear_datos_prueba.py`  
**Propósito:** Crear fichas familiares y personas de prueba para validar la funcionalidad del sistema

---

## Descripción General

Este script automatiza la creación de fichas familiares y personas de prueba con datos realistas que simulan el funcionamiento completo del sistema de censo. Los datos generados son completamente funcionales y cumplen con todas las validaciones del modelo.

---

## Características del Script

### ✅ Validaciones Implementadas

1. **Verificación de datos base**: Verifica que existan datos en todas las tablas relacionadas antes de crear registros
2. **Números de ficha únicos**: Usa `FamilyCard.get_next_family_card_number()` para evitar duplicados
3. **Documentos únicos**: Genera números de identificación únicos y valida que no existan previamente
4. **Emails válidos**: Genera direcciones de email válidas o las deja vacías
5. **Edades apropiadas**: 
   - Cabeza de familia: 18-65 años
   - Miembros: 0-25 años (según parentesco)
6. **Tipos de documento según edad**:
   - Menores de 7 años: Registro Civil (RC)
   - 7-17 años: Tarjeta de Identidad (TI)
   - Mayores de 18 años: Cédula de Ciudadanía (CC)

### 📊 Datos Generados

#### Fichas Familiares
- **Número de fichas**: 5 (configurable)
- **Campos poblados**:
  - Dirección de vivienda (complemento opcional)
  - Vereda (aleatorio de las existentes)
  - Zona (Rural o Urbana)
  - Organización (aleatorio de las existentes)
  - Coordenadas (valor por defecto "0")

#### Personas

**Cabeza de Familia:**
- Mayor de 18 años
- Cédula de Ciudadanía
- Parentesco: "Padre" o similar
- `family_head = True`
- Estado civil: aleatorio
- Todos los campos obligatorios completados

**Miembros de la Familia:**
- 1-4 miembros adicionales por familia
- Primer miembro puede ser cónyuge si el cabeza está casado
- Otros miembros son hijos/hijas
- Usan apellidos del cabeza de familia
- Edades y documentos coherentes

### 📁 Estructura de Datos

```
Familia #1
├── Cabeza de Familia (18-65 años)
│   ├── Juan Carlos García López - CC 12345678
│   └── Parentesco: Padre
└── Miembros
    ├── María Elena García Pérez - CC 87654321 (Cónyuge)
    ├── Pedro García - TI 1234567890 (Hijo, 12 años)
    └── Ana García - RC 9876543 (Hija, 5 años)
```

---

## Uso del Script

### Ejecución Básica

```bash
cd C:\Users\luisg\PycharmProjects\censo-django
python crear_datos_prueba.py
```

### Modificar Cantidad de Familias

Edita la línea 330 del script:

```python
# Cambiar de 5 a la cantidad deseada (máximo 20)
num_familias = 10
```

---

## Tablas Base Requeridas

El script verifica que existan datos en las siguientes tablas:

| Tabla | Descripción | Registros Mínimos |
|-------|-------------|-------------------|
| `Sidewalks` | Veredas | 1+ |
| `Organizations` | Resguardos/Organizaciones | 1+ |
| `IdentificationDocumentType` | Tipos de documento (RC, TI, CC) | 3 |
| `Gender` | Géneros (Masculino, Femenino) | 2 |
| `CivilState` | Estados civiles (Soltero, Casado) | 1+ |
| `EducationLevel` | Niveles educativos | 1+ |
| `Occupancy` | Ocupaciones | 1+ |
| `Kinship` | Parentescos (Padre, Hijo, etc.) | 1+ |
| `SecuritySocial` | Seguridad social | 1+ |
| `Eps` | EPS | 1+ |
| `Handicap` | Capacidades diversas | 1+ |

---

## Datos de Ejemplo Generados

### Nombres Utilizados

**Masculinos:** Juan, Carlos, Pedro, Luis, José, Miguel, Antonio, Francisco, Diego, Andrés

**Femeninos:** María, Ana, Rosa, Luz, Carmen, Elena, Sofia, Laura, Paula

**Apellidos:** García, Rodríguez, López, Martínez, González, Pérez, Sánchez, Torres

### Direcciones de Ejemplo

- "Casa amarilla al lado de la escuela"
- "Frente al parque principal"
- "Detrás de la iglesia"
- "Al lado del puesto de salud"
- "Cerca del río"
- "Primera casa entrada izquierda"
- "" (vacío, algunas fichas)
- "Casa de dos pisos esquina"

---

## Resultados del Script

### Salida Esperada

```
======================================================================
🏠 CREACIÓN DE FICHAS FAMILIARES Y PERSONAS DE PRUEBA
======================================================================
📋 Verificando datos base...
✅ sidewalks: 3 registros
✅ organizations: 2 registros
✅ document_types: 3 registros
✅ genders: 2 registros
✅ civil_states: 2 registros
✅ education_levels: 3 registros
✅ occupations: 4 registros
✅ kinships: 4 registros
✅ security_socials: 2 registros
✅ eps: 2 registros
✅ handicaps: 1 registros

✅ Se crearán 5 fichas familiares de prueba

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

---

## Validación de Datos Creados

### Verificar en la Interfaz Web

1. Acceder a `http://127.0.0.1:8000/family-card/`
2. Verificar que aparezcan las nuevas fichas familiares
3. Hacer clic en "Ver Detalle" de cada ficha
4. Verificar que cada ficha tenga:
   - Cabeza de familia correctamente marcado
   - Miembros de la familia listados
   - Todos los campos poblados

### Verificar en la Base de Datos

```bash
python manage.py shell
```

```python
from censoapp.models import FamilyCard, Person

# Ver todas las fichas
fichas = FamilyCard.objects.all()
print(f"Total fichas: {fichas.count()}")

# Ver última ficha creada
ultima_ficha = FamilyCard.objects.latest('created_at')
print(f"Ficha #{ultima_ficha.family_card_number}")

# Ver personas de esa ficha
personas = Person.objects.filter(family_card=ultima_ficha)
for p in personas:
    print(f"  - {p.full_name} ({p.kinship.description_kinship})")
```

---

## Manejo de Errores

### Errores Comunes

1. **UNIQUE constraint failed: censoapp_familycard.family_card_number**
   - ✅ **Solucionado**: Ahora usa `get_next_family_card_number()`

2. **Error al crear cabeza de familia: email inválido**
   - ✅ **Solucionado**: Genera emails sin caracteres especiales o los deja vacíos

3. **UNIQUE constraint failed: censoapp_person.identification_person**
   - ✅ **Solucionado**: Verifica documentos existentes y genera únicos

4. **Falta de datos base**
   - ✅ **Validado**: Script verifica que existan datos antes de crear

---

## Mejoras Futuras

### Posibles Extensiones

1. **Parámetros de línea de comandos**:
   ```bash
   python crear_datos_prueba.py --familias 10 --miembros-max 5
   ```

2. **Datos de vivienda**:
   - Crear registros en `MaterialConstructionFamilyCard`
   - Añadir datos de materiales de construcción

3. **Datos más realistas**:
   - Usar librería `Faker` para nombres y datos
   - Coordenadas GPS reales de la región

4. **Exportar a fixture**:
   - Guardar datos creados como fixture JSON
   - Permitir reproducir los mismos datos

5. **Modo interactivo**:
   - Permitir al usuario elegir vereda, organización
   - Personalizar cantidad de miembros por familia

---

## Troubleshooting

### El script no crea personas

**Problema:** Las fichas se crean pero las personas fallan

**Solución:** Verificar que existan datos en las tablas relacionadas:
- Kinship (debe tener "Padre", "Hijo", etc.)
- Eps (al menos 1 registro)
- SecuritySocial (al menos 1 registro)
- Handicap (al menos 1 registro)

### Números de documento duplicados

**Problema:** Error de documento único

**Solución:** El script ya verifica duplicados. Si ocurre, puede ser por:
- Ejecución múltiple muy rápida
- Números generados previamente en el sistema

### No se crean miembros de familia

**Problema:** Solo se crea el cabeza de familia

**Solución:** Verificar que existan parentescos adecuados en la tabla `Kinship`:
- Hijo/Hija
- Cónyuge/Esposa/Esposo

---

## Limpieza de Datos de Prueba

### Eliminar Datos Creados por el Script

```bash
python manage.py shell
```

```python
from censoapp.models import FamilyCard, Person
from datetime import datetime, timedelta

# Eliminar fichas creadas hoy
hoy = datetime.now().date()
fichas_hoy = FamilyCard.objects.filter(created_at__date=hoy)
print(f"Fichas a eliminar: {fichas_hoy.count()}")

# Eliminar (descomentar para ejecutar)
# fichas_hoy.delete()
```

---

## Conclusión

Este script es una herramienta útil para:
- ✅ Probar la funcionalidad del sistema
- ✅ Validar formularios y vistas
- ✅ Generar datos para demostraciones
- ✅ Realizar pruebas de carga
- ✅ Entrenar a nuevos usuarios

**Estado:** ✅ Funcional y probado  
**Última ejecución exitosa:** 2025-12-15  
**Fichas creadas en última ejecución:** 5  
**Personas creadas en última ejecución:** 15  

---

**Desarrollado por:** GitHub Copilot  
**Proyecto:** Censo Django - Sistema de Registro de Familias Indígenas

