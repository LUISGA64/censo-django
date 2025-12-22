# Manual de Usuario - Sistema de Censo
## Versión 1.0

---

## 📖 Índice

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Panel Principal](#panel-principal)
4. [Gestión de Fichas Familiares](#gestión-de-fichas-familiares)
5. [Gestión de Personas](#gestión-de-personas)
6. [Datos de Vivienda](#datos-de-vivienda)
7. [Generación de Documentos](#generación-de-documentos)
8. [Reportes y Estadísticas](#reportes-y-estadísticas)
9. [Administración](#administración)
10. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📌 Introducción

El Sistema de Censo es una aplicación diseñada para el registro y gestión de información de comunidades indígenas, permitiendo:

✅ Registro de familias y sus miembros  
✅ Gestión de datos de vivienda y saneamiento  
✅ Generación de documentos oficiales  
✅ Reportes y estadísticas demográficas  
✅ Gestión multi-organización  

---

## 🔐 Acceso al Sistema

### Primera Vez

1. Abrir navegador web (Chrome, Firefox o Edge)
2. Ingresar la dirección: `http://localhost:8000` o la IP del servidor
3. Ingresar credenciales proporcionadas por el administrador
4. **Cambiar contraseña** en el primer acceso

### Recuperación de Contraseña

Si olvida su contraseña:
1. Contactar al administrador del sistema
2. El administrador puede restablecer la contraseña desde el panel administrativo

---

## 🏠 Panel Principal

Al iniciar sesión, verá el panel principal con:

### Estadísticas Generales
- Total de fichas familiares
- Total de personas registradas
- Personas por vereda
- Gráficos demográficos

### Menú de Navegación (Sidebar)

**Gestión:**
- 📋 Fichas Familiares
- 👥 Personas
- 📄 Documentos
- 📊 Estadísticas

**Administración:**
- 🏢 Asociación
- 🏛️ Organizaciones
- ⚙️ Configuración

---

## 📋 Gestión de Fichas Familiares

### Crear Nueva Ficha Familiar

1. Click en **"Fichas Familiares"** en el menú
2. Click en botón **"+ Nueva Ficha"**
3. Completar **Paso 1: Datos de Ubicación**
   - Seleccionar Resguardo
   - Seleccionar Vereda
   - Seleccionar Zona (Urbana/Rural)
   - Dirección (opcional)
   - Coordenadas GPS (opcional)

4. Click en **"Siguiente"**

5. Completar **Paso 2: Datos del Cabeza de Familia**
   - Nombres y apellidos
   - Tipo y número de documento
   - Fecha de nacimiento
   - Género
   - Estado civil
   - Nivel educativo
   - Ocupación
   - EPS
   - Teléfono (opcional)
   - Email (opcional)

6. Click en **"Guardar"**

**⚠️ Importante:** El primer registro siempre debe ser el cabeza de familia (mayor de 18 años).

### Listar Fichas Familiares

1. Click en **"Fichas Familiares"**
2. Visualizar tabla con todas las fichas
3. Usar **filtros** para buscar:
   - Por número de ficha
   - Por vereda
   - Por zona

### Ver Detalle de Ficha

1. En la lista de fichas, click en el ícono 👁️ (Ver)
2. Se muestra:
   - Datos de ubicación
   - Lista de miembros de la familia
   - Datos de vivienda (si están registrados)

### Editar Ficha Familiar

1. En la lista, click en el ícono ✏️ (Editar)
2. Modificar datos necesarios
3. Click en **"Actualizar Datos"**

**Nota:** Los campos Vereda, Zona y Resguardo se mantienen automáticamente.

### Exportar Fichas a Excel

1. En la lista de fichas, click en botón **"Excel"**
2. Se descargará archivo con todas las fichas y sus miembros

---

## 👥 Gestión de Personas

### Agregar Miembro a Familia

1. Desde el detalle de una ficha, click en **"+ Agregar Miembro"**
   
   O bien:
   
2. Ir a **"Personas"** → **"+ Nueva Persona"**
3. Completar formulario:
   - Datos personales
   - Datos de salud
   - Datos socioeconómicos
   - Seleccionar ficha familiar existente
   - **NO marcar** como cabeza de familia

4. Click en **"Guardar"**

### Listar Personas

1. Click en **"Personas"** en el menú
2. Visualizar tabla con todas las personas
3. Filtros disponibles:
   - **Todos:** Muestra todas las personas
   - **Jefes de Familia:** Solo cabezas de familia

### Ver Detalle de Persona

1. En la lista, click en el ícono 👁️ (Ver)
2. Se muestra:
   - Información personal completa
   - Datos de salud
   - Datos educativos
   - Datos laborales
   - Ficha familiar a la que pertenece
   - Opciones para generar documentos (si aplica)

### Editar Persona

1. En la lista o detalle, click en ✏️ (Editar)
2. Modificar datos en las pestañas:
   - Datos Personales
   - Datos de Salud
   - Datos Socioeconómicos
3. Click en **"Actualizar"**

### Exportar Personas a Excel

1. En la lista de personas, click en **"Excel"**
2. Se descarga archivo con:
   - Número de ficha
   - Datos personales
   - Datos de salud
   - Datos socioeconómicos

---

## 🏘️ Datos de Vivienda

### Registrar Datos de Vivienda

**Opción 1: Al crear ficha**
1. Si el parámetro "Datos de Vivienda" está habilitado
2. Aparecerá pestaña **"Vivienda"** en edición de ficha
3. Completar datos de construcción

**Opción 2: Editar ficha existente**
1. Editar ficha familiar
2. Click en pestaña **"Vivienda"**
3. Completar:
   - Materiales de construcción (techo, pared, piso)
   - Condiciones (bueno, regular, malo)
   - Número de habitaciones
   - Tipo de propiedad
   - Ubicación de cocina
   - Tipo de combustible
   - Ventilación e iluminación

4. Click en **"Guardar Datos de Vivienda"**

---

## 📄 Generación de Documentos

### Tipos de Documentos

1. **Constancia de Pertenencia:** Certifica que una persona pertenece a la comunidad
2. **Aval:** Documento de respaldo para trámites

### Generar Documento

**Desde detalle de persona:**
1. Ir al detalle de la persona
2. Click en **"Generar Documento"**
3. Seleccionar tipo de documento
4. El sistema genera automáticamente:
   - PDF con formato oficial
   - Código QR para validación
   - Hash de seguridad

### Previsualizar Documento

1. Ir a **"Documentos"** → **"Estadísticas"**
2. En la tabla, click en 👁️ (Vista Previa)
3. Se abre modal con el PDF
4. Opciones:
   - Ver en pantalla
   - Descargar PDF
   - Imprimir

### Validar Documento (QR)

1. Escanear código QR del documento
2. Se abre página de validación
3. Muestra:
   - ✅ Documento válido/inválido
   - Datos del titular
   - Fecha de emisión
   - Organización emisora
   - Junta directiva firmante

---

## 📊 Reportes y Estadísticas

### Estadísticas Generales

1. Ir a **"Panel Principal"** o **"Estadísticas"**
2. Visualizar:
   - Total de fichas
   - Total de personas
   - Gráficos por género
   - Gráficos por grupo etario
   - Distribución por vereda

### Estadísticas de Documentos

1. Ir a **"Documentos"** → **"Estadísticas"**
2. Visualizar:
   - Total de documentos generados
   - Documentos por tipo
   - Documentos por organización
   - Tabla con todos los documentos

### Exportar Datos

**Fichas Familiares:**
- Click en botón **"Excel"** en lista de fichas
- Incluye datos de todas las personas

**Personas:**
- Click en botón **"Excel"** en lista de personas
- Incluye datos completos

---

## ⚙️ Administración

### Gestión de Asociación

**Solo para administradores**

1. Ir a **"Asociación"**
2. Editar datos:
   - Nombre
   - NIT
   - Dirección y contacto
   - Logo

### Gestión de Organizaciones

1. Ir a **"Organizaciones"**
2. Crear/editar resguardos:
   - Datos básicos
   - Información de contacto
   - Logo

### Gestión de Junta Directiva

1. Ir a **"Organizaciones"** → Seleccionar organización
2. Ver junta directiva vigente
3. Agregar/editar cargos:
   - Gobernador
   - Alcalde
   - Capitán
   - Alguacil
   - Comisario
   - Tesorero
   - Secretario
4. Asignar titular y suplente
5. Definir periodo de vigencia
6. Marcar si puede firmar documentos

### Gestión de Usuarios

**Solo para administradores**

1. Ir a **"Admin"** → **"Usuarios"**
2. Crear nuevo usuario:
   - Datos de acceso
   - Asignar organización
   - Asignar rol:
     - **Admin:** Gestión completa
     - **Operador:** Crear y editar datos
     - **Consulta:** Solo visualización

### Configuración de Parámetros

1. Ir a **"Admin"** → **"System Parameters"**
2. Editar parámetros:
   - `Datos de Vivienda`: S/N

---

## ❓ Preguntas Frecuentes

### ¿Cómo cambio mi contraseña?

1. Click en su nombre (esquina superior derecha)
2. Seleccionar **"Cambiar Contraseña"**
3. Ingresar contraseña actual y nueva contraseña

### ¿Puedo tener más de un jefe de familia por ficha?

No, solo puede haber un cabeza de familia por ficha familiar.

### ¿Cómo registro menores de edad?

Los menores se registran como miembros de familia (no como cabeza de familia).  
Use tipo de documento TI (Tarjeta de Identidad) o RC (Registro Civil).

### ¿Qué hago si me equivoco al registrar datos?

Use la opción **"Editar"** para corregir la información. El sistema guarda un historial de cambios.

### ¿Cómo exporto todos los datos?

Use los botones **"Excel"** en las listas de fichas y personas para exportar los datos.

### ¿Los documentos generados son válidos legalmente?

Los documentos tienen validez interna de la organización. Incluyen código QR para verificación de autenticidad.

### ¿Puedo eliminar una ficha familiar?

Por seguridad, las fichas no se eliminan sino que se **inactivan**. Contacte al administrador.

### ¿Cómo sé qué permisos tengo?

Sus permisos dependen del rol asignado:
- **Admin:** Acceso completo a su organización
- **Operador:** Crear y editar datos
- **Consulta:** Solo visualización

### ¿El sistema funciona sin internet?

Sí, el sistema funciona en red local sin necesidad de internet una vez instalado.

---

## 📞 Soporte Técnico

**Email:** soporte@censo-indigena.com  
**Teléfono:** +57 XXX XXX XXXX  
**Horario:** Lunes a Viernes, 8:00 AM - 6:00 PM

---

## 📝 Notas Importantes

⚠️ **Seguridad de Datos**
- No comparta su contraseña
- Cierre sesión al terminar
- Los datos son confidenciales

⚠️ **Respaldos**
- El administrador debe realizar respaldos periódicos
- Contacte al administrador si necesita recuperar datos

⚠️ **Actualizaciones**
- El sistema puede recibir actualizaciones
- Será notificado de cambios importantes

---

**Versión del Manual:** 1.0  
**Fecha:** 20 de Diciembre de 2024  
**Última Actualización:** 20/12/2024

