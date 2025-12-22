# 📥 GUÍA: Importación Masiva de Datos

**Sistema de Censo - Importación Masiva desde Excel**  
**Versión:** 1.2  
**Fecha:** 22 de Diciembre de 2024

---

## 🎯 ¿Qué es la Importación Masiva?

La Importación Masiva permite cargar **cientos o miles de fichas familiares y personas** desde un archivo Excel en cuestión de minutos, en lugar de semanas de registro manual.

### ⚡ Comparación de Tiempos

| Cantidad de Personas | Registro Manual | Importación Masiva | Ahorro |
|---------------------|-----------------|-------------------|--------|
| 100 personas | ~8 horas | ~5 minutos | **96%** |
| 500 personas | ~42 horas (1 semana) | ~15 minutos | **99%** |
| 1000 personas | ~83 horas (2 semanas) | ~30 minutos | **99%** |
| 5000 personas | ~417 horas (2 meses) | ~2 horas | **99%** |

**¡100x más rápido!** ⚡

---

## 📋 PROCESO COMPLETO (4 Pasos)

```
1. Descargar Template
   ↓
2. Llenar Datos en Excel
   ↓
3. Subir y Validar Archivo
   ↓
4. Confirmar Importación
```

---

## 🔰 PASO 1: Descargar Template Excel

### ¿Cómo?

1. Ir al menú lateral → **"Importación Masiva"**
2. Click en el botón **"Descargar Template"**
3. Guardar el archivo `template_importacion_censo.xlsx`

### ¿Qué contiene el template?

El archivo tiene **3 hojas**:

#### 📄 Hoja 1: "Fichas"
```
Columnas:
- numero_ficha: Número único de la ficha (ej: 1, 2, 3...)
- vereda: Nombre de la vereda
- zona: U (Urbana) o R (Rural)
- direccion: Dirección de la vivienda
- tipo_vivienda: Propia, Arrendada, Familiar, etc.
- material_paredes: Ladrillo, Madera, etc.
- material_piso: Cemento, Tierra, etc.
- material_techo: Zinc, Teja, etc.
```

#### 👥 Hoja 2: "Personas"
```
Columnas OBLIGATORIAS:
- numero_ficha: Debe coincidir con una ficha
- primer_nombre: Obligatorio
- primer_apellido: Obligatorio
- identificacion: Única, no puede repetirse
- tipo_documento: CC, TI, RC, CE, PA
- fecha_nacimiento: Formato YYYY-MM-DD (ej: 1990-05-15)
- genero: Masculino o Femenino
- parentesco: Jefe de Hogar, Cónyuge, Hijo, etc.
- cabeza_familia: SI o NO

Columnas OPCIONALES:
- segundo_nombre
- segundo_apellido
- celular
- email
- nivel_educativo
- ocupacion
```

#### 📖 Hoja 3: "Instrucciones"
- Guía completa de llenado
- Valores permitidos
- Notas importantes

---

## ✏️ PASO 2: Llenar Datos en Excel

### Ejemplo Completo

#### Hoja "Fichas":
| numero_ficha | vereda | zona | direccion | tipo_vivienda | material_paredes | material_piso | material_techo |
|--------------|--------|------|-----------|---------------|------------------|---------------|----------------|
| 1 | Vereda El Rosal | R | Calle 123 | Propia | Ladrillo | Cemento | Zinc |
| 2 | Vereda La Esperanza | R | Carrera 45 | Arrendada | Madera | Tierra | Teja |

#### Hoja "Personas":
| numero_ficha | primer_nombre | segundo_nombre | primer_apellido | segundo_apellido | identificacion | tipo_documento | fecha_nacimiento | genero | parentesco | cabeza_familia |
|--------------|--------------|----------------|-----------------|------------------|----------------|----------------|------------------|--------|------------|----------------|
| 1 | Juan | Carlos | García | López | 123456789 | CC | 1980-05-15 | Masculino | Jefe de Hogar | SI |
| 1 | María | Elena | García | Pérez | 987654321 | CC | 1985-08-20 | Femenino | Cónyuge | NO |
| 1 | Pedro | | García | García | 456789123 | TI | 2010-03-10 | Masculino | Hijo | NO |
| 2 | Ana | María | Rodríguez | Sánchez | 111222333 | CC | 1990-01-01 | Femenino | Jefe de Hogar | SI |

### ⚠️ REGLAS IMPORTANTES

#### ✅ HACER:
- Usar números de ficha únicos (1, 2, 3, 4...)
- Escribir fechas como `YYYY-MM-DD` (ej: `1990-05-15`)
- Usar identificaciones únicas (sin repetir)
- Poner "SI" o "NO" en cabeza_familia
- Usar "U" o "R" para zona
- Cada ficha debe tener al menos UNA persona
- Solo UNA persona puede ser cabeza de familia por ficha

#### ❌ EVITAR:
- Identificaciones duplicadas
- Fechas en formato incorrecto (15/05/1990 NO)
- Fichas sin personas
- Más de un cabeza de familia por ficha
- Campos obligatorios vacíos
- Números de ficha repetidos

---

## 📤 PASO 3: Subir y Validar Archivo

### ¿Cómo?

1. Ir a **Importación Masiva**
2. **Click en el área de carga** o **arrastrar el archivo**
3. Seleccionar archivo `.xlsx` o `.xls`
4. Click en **"Validar y Continuar"**

### ¿Qué pasa durante la validación?

El sistema verifica:
- ✅ Estructura correcta del archivo
- ✅ Todas las columnas necesarias existen
- ✅ Datos obligatorios completos
- ✅ Fechas válidas
- ✅ Identificaciones únicas
- ✅ Relaciones correctas (ficha-persona)
- ✅ Valores permitidos

### Resultados Posibles

#### 🟢 ARCHIVO VÁLIDO
```
✅ ¡Archivo válido!
Se importarán 50 fichas familiares y 230 personas

Preview:
- Ficha #1: Vereda El Rosal, 5 integrantes
- Ficha #2: Vereda La Esperanza, 3 integrantes
...

[Botón: Confirmar Importación]
```

#### 🔴 ARCHIVO CON ERRORES
```
❌ El archivo tiene errores

Errores encontrados (3):
- Fila 10: Identificación duplicada: 123456789
- Fila 15: Fecha de nacimiento inválida (formato: YYYY-MM-DD)
- Fila 20: Cabeza de familia debe ser SI/NO

[Botón: Volver e Intentar de Nuevo]
```

---

## ✅ PASO 4: Confirmar Importación

### Preview

Antes de importar, el sistema muestra:
- **Total de fichas** a crear
- **Total de personas** a crear
- **Preview de primeras 10 fichas**
- **Preview de primeras 10 personas**
- **Advertencias** (si las hay)

### Confirmar

1. Revisar el preview cuidadosamente
2. Click en **"Confirmar Importación"**
3. Confirmar la acción (no se puede deshacer)
4. Esperar (puede tomar varios minutos)

### Resultado

```
✅ Importación completada exitosamente:
50 fichas y 230 personas creadas

Serás redirigido a la lista de fichas familiares
```

---

## 🎓 CASOS DE USO

### Caso 1: Censo Nuevo Completo
```
Situación: Nuevo cabildo sin datos previos
Personas: 1000
Tiempo: ~1 hora total

Proceso:
1. Recopilar datos en papel/formularios
2. Transcribir a Excel (puede ser por varios operadores)
3. Importar todo de una vez
4. Listo!
```

### Caso 2: Migración de Otro Sistema
```
Situación: Tienen datos en otro software
Personas: 500
Tiempo: ~30 minutos

Proceso:
1. Exportar datos del sistema antiguo a Excel
2. Adaptar columnas al template
3. Importar
4. Verificar
```

### Caso 3: Actualización Parcial
```
Situación: Agregar nuevas familias
Personas: 100
Tiempo: ~10 minutos

Proceso:
1. Descargar template
2. Llenar solo las nuevas familias
3. Importar
4. Se agregan a las existentes
```

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### Error: "Identificación duplicada"

**Causa:** Ya existe una persona con esa identificación

**Solución:**
```
1. Buscar el número de identificación en el Excel
2. Verificar si está duplicado en el archivo
3. Si ya existe en la base de datos:
   - Cambiar el número
   - O eliminar del Excel si ya está registrado
```

### Error: "Fecha de nacimiento inválida"

**Causa:** Formato incorrecto de fecha

**Solución:**
```
❌ Incorrecto: 15/05/1990, 15-05-1990, 1990/05/15
✅ Correcto: 1990-05-15

En Excel:
1. Seleccionar columna fecha_nacimiento
2. Formato de celdas → Personalizado
3. Tipo: yyyy-mm-dd
```

### Error: "Falta la columna X"

**Causa:** Se eliminó o renombró una columna obligatoria

**Solución:**
```
1. Descargar el template de nuevo
2. Copiar tus datos al template nuevo
3. NO eliminar ni renombrar columnas
```

### Error: "Ficha X no tiene personas"

**Causa:** Hay una ficha sin integrantes

**Solución:**
```
Opción 1: Agregar al menos una persona a esa ficha
Opción 2: Eliminar la ficha si no se va a usar
```

### Error: "Más de un cabeza de familia en ficha X"

**Causa:** Hay 2 o más personas con cabeza_familia = "SI"

**Solución:**
```
1. Buscar la ficha X en Excel
2. Dejar solo UNA persona con "SI"
3. Las demás cambiar a "NO"
```

---

## 💡 TIPS Y MEJORES PRÁCTICAS

### 1. Trabajo en Equipo
```
✅ Distribuir el trabajo:
- Persona A: Fichas 1-100
- Persona B: Fichas 101-200
- Persona C: Fichas 201-300

Luego: Combinar todo en un solo archivo
```

### 2. Validar Antes de Importar
```
✅ Revisar:
- Identificaciones únicas
- Fechas correctas
- Un cabeza por ficha
- Todos los campos obligatorios
```

### 3. Empezar Pequeño
```
✅ Primera vez:
1. Importar 10-20 fichas de prueba
2. Verificar que todo está correcto
3. Luego importar el resto
```

### 4. Backup
```
✅ Antes de importar:
1. Hacer backup de la base de datos
2. Tener copia del Excel
3. Importar en horario de baja actividad
```

### 5. Nombres Consistentes
```
✅ Usar siempre el mismo formato:
- Veredas: "Vereda El Rosal" (no "el rosal" o "EL ROSAL")
- Géneros: "Masculino" / "Femenino" (no "M" / "F")
- Documentos: "CC", "TI", "RC" (mayúsculas)
```

---

## 📊 VALIDACIONES QUE HACE EL SISTEMA

### Estructura
- ✅ Archivo Excel válido (.xlsx o .xls)
- ✅ Hojas "Fichas" y "Personas" existen
- ✅ Todas las columnas necesarias presentes

### Datos de Fichas
- ✅ Número de ficha presente
- ✅ Vereda presente
- ✅ Zona es U o R
- ✅ No hay fichas duplicadas

### Datos de Personas
- ✅ Primer nombre presente
- ✅ Primer apellido presente
- ✅ Identificación presente y única
- ✅ Fecha de nacimiento válida
- ✅ Género válido
- ✅ Cabeza de familia SI/NO
- ✅ Ficha existe

### Relaciones
- ✅ Cada ficha tiene al menos una persona
- ✅ Solo un cabeza de familia por ficha
- ✅ Todas las personas tienen ficha asignada
- ✅ No hay identificaciones duplicadas

---

## 🎯 BENEFICIOS

### Velocidad
- ⚡ **100x más rápido** que registro manual
- ⏱️ 1000 personas en 30 minutos

### Precisión
- ✅ Validación automática
- ✅ Detecta errores antes de guardar
- ✅ No se pierde información

### Seguridad
- 🔒 Transacción atómica (todo o nada)
- 🔙 Rollback automático si hay error
- 📋 Preview antes de confirmar

### Facilidad
- 👥 Trabajo en equipo posible
- 📊 Formato familiar (Excel)
- 📖 Instrucciones incluidas

---

## 📞 SOPORTE

### Si tienes problemas:

1. **Revisar esta guía completa**
2. **Ver el archivo de instrucciones del template**
3. **Contactar al administrador del sistema**

### Información Útil al Reportar:
- Qué error aparece
- En qué fila del Excel
- Captura de pantalla
- Archivo Excel (si es posible)

---

## 📝 CHECKLIST PRE-IMPORTACIÓN

Antes de importar, verificar:

- [ ] Descargué el template oficial
- [ ] Llené todas las columnas obligatorias
- [ ] Las fechas están en formato YYYY-MM-DD
- [ ] Las identificaciones son únicas
- [ ] Cada ficha tiene al menos una persona
- [ ] Solo hay un cabeza de familia por ficha
- [ ] Los números de ficha son únicos
- [ ] Revisé los datos de ejemplo
- [ ] Guardé el archivo
- [ ] Tengo backup de mis datos

---

## 🎉 ¡Listo para Importar!

**Con esta guía, puedes importar censos completos de forma:**
- ⚡ Rápida
- ✅ Segura
- 🎯 Precisa
- 😊 Fácil

**¡Ahorra semanas de trabajo manual!** 🚀

---

**Ubicación:** Menú → Importación Masiva  
**URL:** `/importacion/`  
**Soporte:** Administrador del sistema  
**Versión de la guía:** 1.0  
**Última actualización:** 22 de Diciembre de 2024

