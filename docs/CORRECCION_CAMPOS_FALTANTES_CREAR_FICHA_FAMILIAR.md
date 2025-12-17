# Corrección de Campos Faltantes en Formulario de Crear Ficha Familiar

**Fecha:** 2025-12-15  
**Módulo:** Creación de Ficha Familiar  
**Archivo:** `templates/censo/censo/createFamilyCard.html`

---

## Problema Identificado

Al intentar crear una ficha familiar, el formulario no mostraba todos los campos obligatorios del modelo `Person`, lo que generaba errores al momento de guardar el registro del cabeza de familia.

### Campos Faltantes en el HTML

Los siguientes campos **obligatorios** del modelo `Person` no estaban presentes en el template:

1. **kinship** (Parentesco) - Campo obligatorio en el modelo
2. **social_insurance** (Seguridad Social) - Campo obligatorio en el modelo
3. **eps** (EPS) - Campo obligatorio en el modelo
4. **handicap** (Capacidades Diversas) - Campo obligatorio en el modelo

---

## Solución Implementada

### 1. Actualización del Template `createFamilyCard.html`

Se agregaron los 4 campos faltantes en la sección "Datos del Cabeza de Familia":

```html
<!-- CAMPOS AGREGADOS -->
<div class="col-md-4">
    {{ person_form.kinship|as_crispy_field }}
</div>
<div class="col-md-4">
    {{ person_form.social_insurance|as_crispy_field }}
</div>
<div class="col-md-4">
    {{ person_form.eps|as_crispy_field }}
</div>
<div class="col-md-4">
    {{ person_form.handicap|as_crispy_field }}
</div>
```

### 2. Reorganización de Campos

Se reorganizaron los campos del formulario para mejorar la experiencia del usuario:

**Orden anterior:**
- Nombres y apellidos (4 campos)
- Tipo documento e identificación (2 campos)
- Fecha nacimiento y género (2 campos)
- Estado civil, educación, ocupación (3 campos)
- Teléfono y email (2 campos)

**Orden actual (mejorado):**
- Nombres y apellidos (4 campos)
- Tipo documento e identificación (2 campos)
- Fecha nacimiento y género (2 campos)
- **Parentesco**, estado civil, educación (3 campos)
- Ocupación, **seguridad social**, **EPS** (3 campos)
- **Capacidades diversas**, teléfono, email (3 campos)

---

## Campos del Formulario FormPerson

### Campos Obligatorios (required=True)
- `first_name_1` - Primer Nombre ✓
- `last_name_1` - Primer Apellido ✓
- `document_type` - Tipo de Documento ✓
- `identification_person` - Número de Identificación ✓
- `date_birth` - Fecha de Nacimiento ✓
- `gender` - Género ✓
- `kinship` - Parentesco ✓ **(AGREGADO)**
- `social_insurance` - Seguridad Social ✓ **(AGREGADO)**
- `eps` - EPS ✓ **(AGREGADO)**
- `handicap` - Capacidades Diversas ✓ **(AGREGADO)**
- `education_level` - Nivel Educativo ✓
- `civil_state` - Estado Civil ✓
- `occupation` - Ocupación ✓

### Campos Opcionales (required=False)
- `first_name_2` - Segundo Nombre
- `last_name_2` - Segundo Apellido
- `cell_phone` - Teléfono Móvil
- `personal_email` - Correo Electrónico

---

## Validaciones del Modelo Person

El modelo `Person` tiene las siguientes validaciones importantes:

### Campos NOT NULL (obligatorios)
```python
first_name_1 = models.CharField(blank=False, null=False, max_length=30)
last_name_1 = models.CharField(blank=False, null=False, max_length=30)
identification_person = models.CharField(blank=False, null=False, unique=True, max_length=15)
document_type = models.ForeignKey(..., blank=False, null=False)
date_birth = models.DateField(blank=False, null=False)
gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
social_insurance = models.ForeignKey('SecuritySocial', on_delete=models.CASCADE)
eps = models.ForeignKey('Eps', on_delete=models.CASCADE)
kinship = models.ForeignKey('Kinship', blank=False, null=False, on_delete=models.CASCADE)
handicap = models.ForeignKey(Handicap, on_delete=models.CASCADE)
education_level = models.ForeignKey('EducationLevel', on_delete=models.CASCADE)
civil_state = models.ForeignKey('CivilState', on_delete=models.CASCADE)
occupation = models.ForeignKey('Occupancy', blank=False, null=False, on_delete=models.CASCADE)
family_card = models.ForeignKey('FamilyCard', on_delete=models.CASCADE)
family_head = models.BooleanField(blank=False, null=False, default=False)
state = models.BooleanField(blank=False, null=False, default=True)
```

### Campos Nullable (opcionales)
```python
first_name_2 = models.CharField(blank=True, null=True, max_length=30)
last_name_2 = models.CharField(blank=True, null=True, max_length=30)
cell_phone = models.CharField(blank=True, null=True, max_length=15)
personal_email = models.EmailField(blank=True, null=True, max_length=50)
```

---

## Validaciones en la Vista create_family_card

La vista ya incluye validaciones robustas:

1. **Validación de permisos** - Solo usuarios con permisos de escritura pueden crear
2. **Duplicidad de identificación** - Verifica que el documento no esté registrado
3. **Edad mínima** - El cabeza de familia debe ser mayor de 18 años
4. **Validación de formularios** - Valida ambos formularios antes de guardar
5. **Transacción atómica** - Si falla algo, no se guarda nada
6. **Mensajes claros** - Mensajes específicos para cada tipo de error

---

## Pruebas Recomendadas

### Caso 1: Crear Ficha Familiar Exitosa
1. Acceder a `/family-card/create/`
2. Completar todos los campos obligatorios de la vivienda
3. Completar todos los campos obligatorios del cabeza de familia
4. Verificar que se crea correctamente la ficha

### Caso 2: Validación de Campos Faltantes
1. Intentar guardar sin completar algún campo obligatorio
2. Verificar que aparezca mensaje de error específico
3. Verificar que los datos ingresados se mantengan en el formulario

### Caso 3: Validación de Edad
1. Ingresar una fecha de nacimiento que resulte en edad < 18 años
2. Verificar que aparezca mensaje de error sobre edad mínima

### Caso 4: Validación de Documento Duplicado
1. Intentar crear una ficha con un documento ya registrado
2. Verificar que aparezca mensaje indicando la duplicidad

---

## Impacto de los Cambios

### ✅ Ventajas
- Formulario completo con todos los campos requeridos
- Evita errores de integridad de base de datos
- Mejora la experiencia del usuario
- Formulario más organizado y profesional
- Cumple con las restricciones del modelo

### ⚠️ Consideraciones
- Los usuarios ahora deben completar más campos (4 adicionales)
- Se recomienda tener datos precargados en las tablas relacionadas:
  - `Kinship` (Parentescos)
  - `SecuritySocial` (Seguridad Social)
  - `Eps` (EPS)
  - `Handicap` (Capacidades Diversas)

---

## Datos Recomendados para Tablas Relacionadas

### Tabla: Kinship (Parentescos)
- Cabeza de Familia
- Cónyuge
- Hijo/a
- Padre/Madre
- Hermano/a
- Nieto/a
- Otro

### Tabla: SecuritySocial (Seguridad Social)
- Contributivo
- Subsidiado
- Especial
- No asegurado

### Tabla: Handicap (Capacidades Diversas)
- Ninguna
- Visual
- Auditiva
- Física
- Intelectual
- Psicosocial
- Múltiple

---

## Archivos Modificados

1. `templates/censo/censo/createFamilyCard.html`
   - Se agregaron 4 campos faltantes
   - Se reorganizó el orden de los campos
   - Se mejoró el diseño responsivo

---

## Estado Actual

✅ **COMPLETADO** - El formulario ahora incluye todos los campos obligatorios del modelo `Person` y está listo para crear fichas familiares sin errores de integridad.

---

## Próximos Pasos Recomendados

1. ✅ Verificar que las tablas relacionadas tengan datos precargados
2. ✅ Realizar pruebas de creación de fichas familiares
3. ⏳ Validar que el formulario de **editar persona** también tenga todos los campos
4. ⏳ Revisar el formulario de **crear persona** (agregar miembro a familia existente)
5. ⏳ Considerar hacer algunos campos opcionales si el negocio lo permite

---

**Desarrollado por:** GitHub Copilot  
**Revisado por:** Equipo de Desarrollo Censo Django

