# 🏠 Importación Masiva con Datos de Vivienda Opcionales

**Fecha:** 22 de Diciembre de 2024  
**Funcionalidad:** Columnas de Materiales de Vivienda Opcionales  
**Estado:** ✅ Implementado

---

## 🎯 Problema Resuelto

### Situación
No todos los cabildos registran información sobre **materiales de construcción de viviendas** en sus censos:

- ❌ Algunos cabildos NO tienen estos datos en sus Excel actuales
- ❌ Importación fallaba si faltaban las columnas
- ❌ Incompatible con censos existentes sin datos de vivienda

### Solución
Template Excel **dinámico** que se adapta según un parámetro del sistema.

---

## ⚙️ Cómo Funciona

### Parámetro del Sistema

**Ubicación:** Admin → System Parameters  
**Key:** `Datos de Vivienda`  
**Valores:**
- `S` = SÍ (Habilitado) - Incluye columnas de materiales
- `N` = NO (Deshabilitado) - NO incluye columnas de materiales

---

## 📊 Comportamiento Según Configuración

### Caso 1: Datos de Vivienda HABILITADOS (S)

**Template incluye:**
```
Hoja "Fichas":
├─ numero_ficha       (OBLIGATORIO)
├─ vereda            (OBLIGATORIO)
├─ zona              (OBLIGATORIO)
├─ direccion         (OBLIGATORIO)
├─ tipo_vivienda     (OBLIGATORIO)
├─ material_paredes  (OPCIONAL) ✅
├─ material_piso     (OPCIONAL) ✅
└─ material_techo    (OPCIONAL) ✅
```

**Ejemplo de datos:**
| numero_ficha | vereda | zona | direccion | tipo_vivienda | material_paredes | material_piso | material_techo |
|--------------|--------|------|-----------|---------------|------------------|---------------|----------------|
| 1 | El Rosal | R | Calle 123 | Propia | Ladrillo | Cemento | Zinc |

**Mensaje en UI:**
```
ℹ️ Datos de vivienda habilitados: El template incluirá 
   columnas para material_paredes, material_piso y material_techo.
```

---

### Caso 2: Datos de Vivienda DESHABILITADOS (N)

**Template incluye:**
```
Hoja "Fichas":
├─ numero_ficha       (OBLIGATORIO)
├─ vereda            (OBLIGATORIO)
├─ zona              (OBLIGATORIO)
├─ direccion         (OBLIGATORIO)
└─ tipo_vivienda     (OBLIGATORIO)

❌ NO incluye columnas de materiales
```

**Ejemplo de datos:**
| numero_ficha | vereda | zona | direccion | tipo_vivienda |
|--------------|--------|------|-----------|---------------|
| 1 | El Rosal | R | Calle 123 | Propia |

**Mensaje en UI:**
```
ℹ️ Datos de vivienda deshabilitados: El template NO incluirá 
   columnas de materiales de construcción. Solo se registrarán 
   datos básicos de la ficha familiar.
```

---

## 🔧 Implementación Técnica

### 1. Verificación del Parámetro

```python
def _check_housing_data_enabled(self):
    """Verifica si el parámetro de datos de vivienda está habilitado."""
    try:
        from censoapp.models import SystemParameters
        param = SystemParameters.objects.filter(key='Datos de Vivienda').first()
        return param and param.value == 'S'
    except Exception:
        return False  # Por defecto deshabilitado
```

### 2. Template Dinámico

```python
# Headers base (siempre presentes)
headers_fichas = [
    'numero_ficha', 'vereda', 'zona', 'direccion', 'tipo_vivienda'
]

# Agregar columnas de materiales solo si está habilitado
if housing_data_enabled:
    headers_fichas.extend([
        'material_paredes', 'material_piso', 'material_techo'
    ])
```

### 3. Validación Adaptativa

```python
# Columnas base siempre requeridas
columnas_fichas_requeridas = [
    'numero_ficha', 'vereda', 'zona', 'direccion', 'tipo_vivienda'
]

# Solo requerir columnas de materiales si el parámetro está habilitado
if self.housing_data_enabled:
    columnas_fichas_requeridas.extend([
        'material_paredes', 'material_piso', 'material_techo'
    ])
```

### 4. Instrucciones Dinámicas

```python
instrucciones = [
    "1. HOJA 'Fichas':",
    "   - numero_ficha: ... (OBLIGATORIO)",
    "   - vereda: ... (OBLIGATORIO)",
    # ...
]

if housing_data_enabled:
    instrucciones.extend([
        "   - material_paredes: ... (OPCIONAL)",
        "   - material_piso: ... (OPCIONAL)",
        "   - material_techo: ... (OPCIONAL)",
    ])
else:
    instrucciones.append(
        "   NOTA: Las columnas de materiales NO están habilitadas"
    )
```

---

## 📋 Flujo Completo

### Para Cabildo SIN Datos de Vivienda

```
1. Admin configura: Datos de Vivienda = N
   ↓
2. Usuario descarga template
   ↓
3. Template SIN columnas de materiales
   ↓
4. Usuario llena solo datos básicos
   ↓
5. Sube Excel
   ↓
6. Validación pasa (no requiere materiales)
   ↓
7. ✅ Importación exitosa
```

### Para Cabildo CON Datos de Vivienda

```
1. Admin configura: Datos de Vivienda = S
   ↓
2. Usuario descarga template
   ↓
3. Template CON columnas de materiales
   ↓
4. Usuario llena datos básicos + materiales
   ↓
5. Sube Excel
   ↓
6. Validación pasa (incluye materiales)
   ↓
7. ✅ Importación exitosa con materiales
```

---

## 🎯 Casos de Uso

### Caso 1: Migración de Excel Existente (Sin Materiales)

**Escenario:**
- Cabildo tiene censo en Excel hace 3 años
- NO registraron materiales de vivienda
- 500 familias censadas

**Proceso:**
```
1. Admin: Configurar "Datos de Vivienda" = N
2. Descargar template (sin columnas de materiales)
3. Copiar datos del Excel antiguo
4. Adaptar nombres de columnas al template
5. Importar
6. ✅ 500 familias importadas sin problemas
```

### Caso 2: Censo Nuevo (Con Materiales)

**Escenario:**
- Cabildo nuevo quiere incluir datos de vivienda
- Planean censar 1000 familias

**Proceso:**
```
1. Admin: Configurar "Datos de Vivienda" = S
2. Descargar template (con columnas de materiales)
3. Capacitar censadores
4. Llenar datos completos
5. Importar
6. ✅ 1000 familias con datos completos
```

### Caso 3: Cambio de Configuración

**Escenario:**
- Cabildo empezó sin datos de vivienda
- Después deciden agregarlos

**Proceso:**
```
1. Ya tienen 300 familias sin materiales
2. Admin: Cambiar "Datos de Vivienda" a S
3. Nuevas importaciones incluyen materiales
4. Familias antiguas quedan sin materiales (OK)
5. Se pueden completar manualmente si se desea
```

---

## ✅ Ventajas

### Flexibilidad
- ✅ Se adapta a necesidades de cada cabildo
- ✅ Compatible con Excel existentes
- ✅ No obliga a registrar datos innecesarios

### Compatibilidad
- ✅ No rompe importaciones actuales
- ✅ Excel antiguos siguen funcionando
- ✅ Migración suave entre configuraciones

### Claridad
- ✅ Mensaje visible en la UI
- ✅ Instrucciones adaptativas
- ✅ Usuario sabe qué esperar

### Mantenibilidad
- ✅ Un solo código para ambos casos
- ✅ Configuración centralizada
- ✅ Fácil de cambiar

---

## 🔍 Verificación

### Comprobar Estado Actual

**En Admin:**
```
1. Ir a Admin → System Parameters
2. Buscar key "Datos de Vivienda"
3. Ver value: S (habilitado) o N (deshabilitado)
```

**En la UI:**
```
1. Ir a Importación Masiva
2. Ver mensaje informativo azul
3. Leer estado actual del parámetro
```

**En el Template:**
```
1. Descargar template Excel
2. Abrir hoja "Fichas"
3. Ver columnas presentes
4. Leer hoja "Instrucciones"
```

---

## 📝 Configuración Recomendada

### Para Mayoría de Cabildos

**Recomendación:** `Datos de Vivienda = N` (Deshabilitado)

**Razones:**
- La mayoría NO registra materiales
- Simplifica el censo
- Reduce tiempo de llenado
- Compatible con Excel existentes

### Para Cabildos Avanzados

**Recomendación:** `Datos de Vivienda = S` (Habilitado)

**Razones:**
- Información más completa
- Análisis de condiciones de vivienda
- Programas de mejoramiento
- Estadísticas detalladas

---

## 🎓 Capacitación

### Para Administradores

```
1. Conocer el parámetro "Datos de Vivienda"
2. Decidir configuración según necesidades
3. Configurar en Admin antes de importar
4. Informar a operadores
```

### Para Operadores

```
1. Ver mensaje en página de importación
2. Descargar template correcto
3. Llenar solo columnas presentes
4. No agregar columnas manualmente
5. Importar normalmente
```

---

## ⚠️ Notas Importantes

### NO Mezclar Templates

```
❌ NO descargar template con parámetro S y llenar sin materiales
❌ NO descargar template con parámetro N y agregar columnas manualmente
✅ SÍ descargar template según configuración actual
✅ SÍ usar template tal como se descarga
```

### Consistencia

```
ℹ️ El parámetro debe configurarse ANTES de:
   - Descargar template
   - Importar datos
   
ℹ️ Si cambia el parámetro:
   - Descargar nuevo template
   - Adaptar datos si es necesario
```

---

## 🎉 Resultado Final

**El sistema ahora:**

✅ **Se adapta** a cada cabildo  
✅ **No obliga** a registrar datos innecesarios  
✅ **Compatible** con Excel existentes  
✅ **Flexible** según configuración  
✅ **Claro** en instrucciones  
✅ **Fácil** de usar  

**Beneficio Principal:**
```
Los cabildos pueden importar sus Excel actuales 
SIN necesidad de agregar columnas de materiales 
si no las tienen registradas.
```

---

**Funcionalidad:** Datos de Vivienda Opcionales  
**Estado:** ✅ Implementado  
**Configuración:** System Parameters → "Datos de Vivienda"  
**Valores:** S (Habilitado) / N (Deshabilitado)  
**GitHub:** ✅ Actualizado  

**¡Importación masiva ahora es compatible con todos los cabildos!** 🎊

