# Registro de 50 Fichas Familiares - Organización 1

**Fecha:** 2025-12-18  
**Estado:** ✅ COMPLETADO

## Objetivo

Crear 50 fichas familiares de prueba para la Organización 1 (Resguardo Indígena Prueba 1), con familias que tengan entre 3 y 5 integrantes cada una.

## Proceso de Creación

### Script Principal: `crear_50_fichas_familiares.py`

El script genera automáticamente:
- Fichas familiares con datos realistas
- Familias con 3-5 integrantes (jefe de familia + cónyuge + hijos)
- Datos demográficos variados (nombres, edades, documentos, etc.)
- Distribución geográfica entre las veredas disponibles
- Asignación automática de números de ficha

### Características de los Datos Generados

**Estructura Familiar:**
- **Jefe de familia:** Adulto de 25-60 años (puede ser hombre o mujer)
- **Cónyuge:** Adulto de 23-55 años (en familias de 4-5 integrantes)
- **Hijos:** Niños/jóvenes de 0-17 años

**Datos Personales:**
- Nombres y apellidos aleatorios de listas predefinidas
- Documentos de identidad únicos (8 dígitos)
- Números de teléfono celular
- Correos electrónicos (70% de los jefes de familia)
- Fechas de nacimiento coherentes con las edades
- Asignación aleatoria de EPS, nivel educativo, ocupación, etc.

**Datos de Ubicación:**
- Direcciones variadas con números de casa
- Distribución entre zona Rural y Urbana
- Asignación a diferentes veredas
- Coordenadas geográficas aleatorias (dentro de Colombia)

## Resultados

### Estadísticas Finales

```
📊 Total de fichas en organización 1: 83 fichas
📊 Total de personas registradas: 326 personas
📊 Total de jefes de familia: 83
📊 Promedio de integrantes por familia: 3.93
```

### Distribución por Número de Integrantes

```
1 integrante:    1 ficha  (  1.2%)  
3 integrantes:  30 fichas ( 36.1%) ██████████████████
4 integrantes:  25 fichas ( 30.1%) ███████████████
5 integrantes:  27 fichas ( 32.5%) ████████████████
```

**Nota:** La ficha con 1 integrante corresponde a una ejecución previa con errores. Las 50 fichas nuevas tienen entre 3-5 integrantes correctamente.

### Distribución por Zona

```
Rural:   45 fichas (54.2%)
Urbana:  38 fichas (45.8%)
```

### Distribución por Vereda

```
Tabo:        23 fichas (27.7%)
Purac:       21 fichas (25.3%)
Hispala:     14 fichas (16.9%)
Campamento:  14 fichas (16.9%)
Cuar:        11 fichas (13.3%)
```

### Distribución por Género

```
Femenino:  173 personas (53.1%)
Masculino: 153 personas (46.9%)
```

### Distribución por Parentesco

```
Hija/o:  191 personas (58.6%)
Padre:    83 personas (25.5%)
Madre:    52 personas (16.0%)
```

## Ejemplos de Fichas Creadas

### Ficha #83
- **Ubicación:** Vereda alta #37 - Hispala (Urbana)
- **Integrantes:** 4 personas
- **Jefe de familia:** Eduardo Díaz Vargas
  - Tel: 3198484985
  - Email: eduardo.diaz@example.com
- **Miembros:**
  - Eduardo Díaz (Jefe - Doc: 16835493)
  - Lucía Rodríguez (Madre - Doc: 59063343)
  - Roberto Díaz (Hijo - Doc: 90820578)
  - Patricia Díaz (Hija - Doc: 34938694)

### Ficha #82
- **Ubicación:** Sector norte #53 - Cuar (Urbana)
- **Integrantes:** 5 personas
- **Jefe de familia:** Natalia Paola Romero Pérez
  - Tel: 3183198602
  - Email: natalia.romero@example.com
- **Miembros:**
  - Natalia Romero (Jefa - Doc: 16113078)
  - Pedro Jiménez (Madre - Doc: 95423191)
  - Carolina Romero (Hija - Doc: 31366655)
  - Pedro Romero (Hijo - Doc: 73147161)
  - Antonio Romero (Hijo - Doc: 33562600)

### Ficha #81
- **Ubicación:** Vereda alta #42 - Purac (Rural)
- **Integrantes:** 4 personas
- **Jefe de familia:** Adriana Sánchez Castillo
  - Tel: 3149002085
  - Email: adriana.sanchez@example.com
- **Miembros:**
  - Adriana Sánchez (Jefa - Doc: 72399584)
  - Daniel Vega (Madre - Doc: 24157677)
  - Rafael Sánchez (Hijo - Doc: 13685089)
  - Gabriela Sánchez (Hija - Doc: 72601139)

## Archivos Creados

1. ✅ **crear_50_fichas_familiares.py** - Script de creación de fichas
2. ✅ **verificar_fichas_org1.py** - Script de verificación y estadísticas

## Cómo Usar los Scripts

### Crear más fichas familiares

```bash
python crear_50_fichas_familiares.py
```

Este script:
- Crea 50 nuevas fichas familiares
- Asigna números de ficha automáticamente
- Genera datos realistas para cada familia
- Muestra progreso cada 10 fichas

### Verificar estadísticas

```bash
python verificar_fichas_org1.py
```

Este script muestra:
- Estadísticas generales
- Distribución por número de integrantes
- Distribución por zona y vereda
- Estadísticas demográficas
- Últimas 10 fichas creadas con detalles

## Validaciones Implementadas

✅ **Documentos únicos:** Se verifica que no existan documentos duplicados  
✅ **Emails válidos:** Los caracteres especiales se normalizan (á→a, ñ→n, etc.)  
✅ **Edades coherentes:** Jefes de familia ≥18 años, hijos 0-17 años  
✅ **Transacciones atómicas:** Si hay error, no se guarda nada de esa ficha  
✅ **Números de ficha automáticos:** Usa el método `get_next_family_card_number()`  

## Correcciones Aplicadas

Durante el desarrollo se corrigieron:

1. **Filtro de veredas:** Se ajustó para usar todas las veredas disponibles
2. **Campos de modelo:** Se corrigió para usar `description_kinship` en lugar de `kinship`
3. **Emails con acentos:** Se agregó función `normalizar_texto()` para caracteres especiales
4. **Estadísticas de distribución:** Se corrigió el conteo de integrantes por ficha

## Beneficios

✅ **Datos de prueba realistas** para desarrollo y testing  
✅ **Diversidad demográfica** (edades, géneros, parentescos)  
✅ **Distribución geográfica** entre veredas  
✅ **Datos validados** (no duplicados, formatos correctos)  
✅ **Fácil de ejecutar** y repetir  
✅ **Estadísticas detalladas** disponibles  

## Notas Importantes

- Los datos generados son ficticios y solo para propósitos de prueba
- Los documentos de identidad son números aleatorios de 8 dígitos
- Los emails usan el dominio @example.com
- Las coordenadas geográficas son aleatorias dentro de rangos de Colombia
- El script puede ejecutarse múltiples veces para crear más fichas

---

**Estado Final:** ✅ 50 FICHAS FAMILIARES CREADAS EXITOSAMENTE

Total en Organización 1: **83 fichas** con **326 personas** registradas.

