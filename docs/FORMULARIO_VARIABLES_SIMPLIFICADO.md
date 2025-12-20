# ✅ FORMULARIO SIMPLIFICADO - Variables Personalizadas

## Fecha: 19 de diciembre de 2025

---

## 🎯 CAMBIO SOLICITADO

**Usuario solicita:**
> "En el formulario de Nueva Variable personalizada los campos a utilizar deben ser los campos de cada modelo (persona, fichas familiares, asociación, organización) de tal forma que los campos del formulario deberían ser:
> - NOMBRE VARIABLE
> - TIPO VARIABLE
> - VALOR (dependiendo del tipo mostrar los campos disponibles validando que no pueden haber variables repetidas)
> - DESCRIPCIÓN"

---

## ✨ FORMULARIO SIMPLIFICADO

### ANTES (5 campos con complejidad) ❌

```
┌────────────────────────────────────────┐
│ Nueva Variable Personalizada     [X]  │
├────────────────────────────────────────┤
│ Nombre de la Variable *               │
│ [territorio___________________]       │
│                                        │
│ Tipo de Variable *                    │
│ [Valor Estático (texto fijo)   ▼]     │
│ [Dato de Organización          ▼]     │
│ [Dato de Persona               ▼]     │
│ [Dato de Ficha Familiar        ▼]     │
│                                        │
│ Valor * (cambia según tipo)           │
│ • Si es estático: textarea            │
│ • Si es dinámico: selector + input    │
│                                        │
│ Descripción                            │
│ [____________________________]         │
│                                        │
│                [Cancelar] [Guardar]   │
└────────────────────────────────────────┘

Problemas:
❌ Complejo (modo estático vs dinámico)
❌ Dos inputs diferentes según tipo
❌ No valida duplicados
❌ Interfaz confusa
```

### DESPUÉS (4 campos simples) ✅

```
┌────────────────────────────────────────┐
│ Nueva Variable Personalizada     [X]  │
├────────────────────────────────────────┤
│ 📛 Nombre de la Variable *            │
│ [territorio___________________]       │
│ Nombre único sin llaves {}            │
│                                        │
│ 🏷️ Tipo de Variable *                │
│ [Dato de Organización          ▼]     │
│   • Dato de Persona                   │
│   • Dato de Ficha Familiar            │
│   • Dato de Asociación                │
│   • Dato de Organización              │
│ Selecciona de qué modelo proviene     │
│                                        │
│ 💾 Campo del Modelo *                 │
│ [Territorio (organization_territory) ▼]│
│ ✓ Campo de texto                      │
│                                        │
│ 📝 Descripción                        │
│ [Territorio del resguardo_____]       │
│                                        │
│                [Cancelar] [Guardar]   │
└────────────────────────────────────────┘

Ventajas:
✅ Solo 4 campos claros
✅ Todas las variables son dinámicas
✅ Valida duplicados
✅ Interfaz intuitiva
✅ Iconos descriptivos
```

---

## 📋 LOS 4 CAMPOS DEL FORMULARIO

### 1. NOMBRE VARIABLE

```
Campo: input text
Requerido: Sí
Validación: Único por organización
Ejemplo: "territorio", "nombre_completo", "edad"

Características:
• Nombre sin llaves {}
• Se valida que no exista en la organización
• Solo letras, números y guiones bajos
• Mensaje de error si ya existe
```

### 2. TIPO VARIABLE

```
Campo: select
Requerido: Sí
Opciones:
  • person           → Dato de Persona
  • family_card      → Dato de Ficha Familiar
  • association      → Dato de Asociación
  • organization     → Dato de Organización

Comportamiento:
• Al cambiar, carga los campos disponibles
• Muestra selector de campos dinámicamente
```

### 3. VALOR (Campo del Modelo)

```
Campo: select dinámico
Requerido: Sí
Contenido: Depende del tipo seleccionado

Si tipo = "organization":
  • Nombre de la organización (organization_name)
  • Territorio (organization_territory)
  • NIT/Identificación (organization_identification)
  • ... 11 campos en total

Si tipo = "person":
  • Nombre completo (full_name)
  • Identificación (identification_person)
  • Edad en años (calcular_anios)
  • ... 16 campos en total

Si tipo = "family_card":
  • Número de ficha (family_card_number)
  • Vereda (sidewalk_home.sidewalk_name)
  • Dirección (address_home)
  • ... 10 campos en total

Si tipo = "association":
  • Nombre de asociación (association_name)
  • Código (association_code)
  • Presidente (president_name)
  • ... 6 campos disponibles
```

### 4. DESCRIPCIÓN

```
Campo: textarea
Requerido: No
Ejemplo: "Territorio del resguardo indígena"

Uso:
• Ayuda contextual para el usuario
• Documenta el propósito de la variable
• Se muestra en la lista de variables
```

---

## 🔧 CAMBIOS TÉCNICOS REALIZADOS

### 1. Modelo TemplateVariable Actualizado

**Archivo:** `censoapp/template_models.py`

**Cambios:**
```python
class TemplateVariable(models.Model):
    # NUEVO CAMPO
    variable_type = models.CharField(
        max_length=20,
        choices=[
            ('person', 'Dato de Persona'),
            ('family_card', 'Dato de Ficha Familiar'),
            ('association', 'Dato de Asociación'),
            ('organization', 'Dato de Organización'),
        ],
        verbose_name="Tipo de Variable"
    )
    
    # CAMPO MODIFICADO
    variable_value = models.CharField(  # Era TextField
        max_length=200,
        verbose_name="Campo del Modelo",
        help_text="Nombre del campo del modelo"
    )
    
    # NUEVO ORDERING
    class Meta:
        ordering = ['organization', 'variable_type', 'variable_name']
        unique_together = [['organization', 'variable_name']]
```

### 2. Vista variable_create con Validación

**Archivo:** `censoapp/template_views.py`

**Nuevas validaciones:**
```python
def variable_create(request):
    # 1. Validar nombre no vacío
    if not variable_name:
        return JsonResponse({'error': 'El nombre es obligatorio'})
    
    # 2. Validar que no exista duplicado
    if TemplateVariable.objects.filter(
        organization=organization,
        variable_name=variable_name
    ).exists():
        return JsonResponse({
            'error': f'Ya existe una variable "{variable_name}"'
        })
    
    # 3. Crear variable
    variable = TemplateVariable.objects.create(
        variable_name=variable_name,
        variable_type=variable_type,    # NUEVO
        variable_value=variable_value,
        ...
    )
```

### 3. Vista variable_update con Validación

**Cambios:**
```python
def variable_update(request, pk):
    # Validar duplicados excluyendo la variable actual
    if TemplateVariable.objects.filter(
        organization=variable.organization,
        variable_name=variable_name
    ).exclude(pk=pk).exists():
        return JsonResponse({'error': 'Ya existe otra variable'})
    
    # Actualizar con nuevo campo
    variable.variable_type = request.POST.get('variable_type')
    variable.save()
```

### 4. Endpoint get_model_fields Mejorado

**Agregado soporte para asociaciones:**
```python
def get_model_fields(request):
    variable_type = request.GET.get('type', '')
    
    if variable_type == 'association':
        fields = [
            {'value': 'association_name', 'label': 'Nombre', 'type': 'text'},
            {'value': 'president_name', 'label': 'Presidente', 'type': 'text'},
            {'value': 'total_members', 'label': 'Total miembros', 'type': 'number'},
            ...
        ]
    
    return JsonResponse({'fields': fields})
```

### 5. Template HTML Simplificado

**Archivo:** `templates/templates/variables.html`

**Modal de Creación:**
```html
<form id="createVariableForm">
    <!-- 1. NOMBRE -->
    <input type="text" name="variable_name" required>
    
    <!-- 2. TIPO -->
    <select name="variable_type" onchange="loadFieldOptions()">
        <option value="person">Dato de Persona</option>
        <option value="family_card">Dato de Ficha Familiar</option>
        <option value="association">Dato de Asociación</option>
        <option value="organization">Dato de Organización</option>
    </select>
    
    <!-- 3. VALOR (dinámico) -->
    <select name="variable_value" required>
        <!-- Se llena automáticamente vía AJAX -->
    </select>
    
    <!-- 4. DESCRIPCIÓN -->
    <textarea name="description"></textarea>
</form>
```

**Modal de Edición:**
```html
<form id="editVariableForm">
    <input type="text" name="variable_name" required>
    <select name="variable_type" onchange="loadEditFieldOptions()">...</select>
    <select name="variable_value" required>...</select>
    <textarea name="description"></textarea>
    <input type="checkbox" name="is_active">
</form>
```

### 6. JavaScript Refactorizado

**Funciones clave:**

```javascript
// Cargar campos según tipo seleccionado
function loadFieldOptions() {
    const type = document.getElementById('create_variable_type').value;
    
    fetch(`/variables/campos-modelo/?type=${type}`)
        .then(response => response.json())
        .then(data => {
            // Llenar selector con campos del modelo
            data.fields.forEach(field => {
                option.textContent = `${field.label} (${field.value})`;
            });
        });
}

// Crear variable con validación
function createVariable() {
    // Validar campos requeridos
    if (!variableName || !variableType || !variableValue) {
        alert('Completa todos los campos obligatorios');
        return;
    }
    
    // Enviar al servidor
    fetch('/variables/crear/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            // Mostrar error (ej: variable duplicada)
            alert('Error: ' + data.error);
        }
    });
}
```

---

## 📊 CAMPOS DISPONIBLES POR TIPO

### Organización (11 campos)

```
✅ organization_name              - Nombre de la organización
✅ organization_identification    - NIT/Identificación
✅ organization_type_document     - Tipo de documento
✅ organization_mobile_phone      - Teléfono móvil
✅ organization_phone             - Teléfono fijo
✅ organization_address           - Dirección
✅ organization_departament       - Departamento
✅ organization_municipality      - Municipio
✅ organization_territory         - Territorio
✅ organization_email             - Email
✅ organization_web               - Sitio web
```

### Persona (16 campos)

```
✅ full_name                      - Nombre completo
✅ first_name_1                   - Primer nombre
✅ first_name_2                   - Segundo nombre
✅ last_name_1                    - Primer apellido
✅ last_name_2                    - Segundo apellido
✅ identification_person          - Número de identificación
✅ document_type.document_type    - Tipo de documento
✅ date_birth                     - Fecha de nacimiento
✅ calcular_anios                 - Edad en años (método)
✅ gender.gender                  - Género
✅ civil_state.civil_state        - Estado civil
✅ eps.eps                        - EPS
✅ education_level.education_level - Nivel educativo
✅ occupancy.occupancy            - Ocupación
✅ mobile_phone                   - Teléfono celular
✅ email                          - Email
```

### Ficha Familiar (10 campos)

```
✅ family_card_number             - Número de ficha familiar
✅ sidewalk_home.sidewalk_name    - Vereda (relación)
✅ zone                           - Zona (Rural/Urbana)
✅ address_home                   - Dirección de residencia
✅ homeownership.homeownership    - Tipo de vivienda
✅ water_source.water_source      - Fuente de agua
✅ water_treatment.water_treatment - Tratamiento del agua
✅ lighting_type.lighting_type    - Tipo de alumbrado
✅ cooking_fuel.cooking_fuel      - Combustible para cocinar
✅ number_occupants               - Número de ocupantes
```

### Asociación (6 campos)

```
✅ association_name               - Nombre de la asociación
✅ association_code               - Código de asociación
✅ president_name                 - Nombre del presidente
✅ secretary_name                 - Nombre del secretario
✅ creation_date                  - Fecha de creación
✅ total_members                  - Total de miembros
```

**Total: 43 campos disponibles**

---

## ✅ VALIDACIONES IMPLEMENTADAS

### 1. Validación de Nombre Único

```python
# En variable_create
if TemplateVariable.objects.filter(
    organization=organization,
    variable_name=variable_name
).exists():
    return JsonResponse({
        'success': False,
        'error': f'Ya existe una variable con el nombre "{variable_name}"'
    }, status=400)
```

**Mensaje al usuario:**
```
❌ Error
Ya existe una variable con el nombre "territorio" 
en esta organización
```

### 2. Validación en Edición

```python
# En variable_update
if TemplateVariable.objects.filter(
    organization=variable.organization,
    variable_name=variable_name
).exclude(pk=pk).exists():  # Excluye la variable actual
    return JsonResponse({
        'error': 'Ya existe otra variable con ese nombre'
    })
```

### 3. Validación de Campos Requeridos (JavaScript)

```javascript
function createVariable() {
    const variableName = formData.get('variable_name').trim();
    const variableType = formData.get('variable_type');
    const variableValue = formData.get('variable_value');

    if (!variableName) {
        alert('El nombre de la variable es obligatorio');
        return;
    }

    if (!variableType) {
        alert('Selecciona el tipo de variable');
        return;
    }

    if (!variableValue) {
        alert('Selecciona un campo del modelo');
        return;
    }
    
    // Continuar con la creación...
}
```

---

## 🎨 MEJORAS EN LA INTERFAZ

### Lista de Variables Mejorada

**Ahora muestra:**
```
┌─────────────────────────────────────────────────┐
│ {territorio}  🏷️ Dato de Organización  ✓ Activa │
│                                                 │
│ Campo del Modelo: organization_territory        │
│ ℹ️ Territorio del resguardo indígena           │
│                                    [✏️] [🗑️]    │
└─────────────────────────────────────────────────┘
```

**Características:**
- ✅ Badge con el tipo de variable (color azul)
- ✅ Estado (Activa/Inactiva)
- ✅ Campo del modelo en formato código
- ✅ Descripción opcional
- ✅ Botones de editar/eliminar

### Iconos Descriptivos

```
📛 Nombre de la Variable
🏷️ Tipo de Variable
💾 Campo del Modelo
📝 Descripción
✏️ Editar
🗑️ Eliminar
✓ Activa
```

---

## 🎯 FLUJO DE USO

### Crear Nueva Variable

```
1. Click "Nueva Variable"
   ↓
2. Ingresar nombre: "territorio"
   ↓
3. Seleccionar tipo: "Dato de Organización"
   ↓
   Sistema carga automáticamente 11 campos de Organizations
   ↓
4. Seleccionar campo: "Territorio (organization_territory)"
   ↓
   Ayuda muestra: "✓ Campo de texto"
   ↓
5. Agregar descripción: "Territorio del resguardo"
   ↓
6. Click "Guardar Variable"
   ↓
   Sistema valida:
   • ¿Nombre vacío? → Error
   • ¿Ya existe? → Error "Ya existe una variable 'territorio'"
   • ¿Tipo seleccionado? → Error
   • ¿Campo seleccionado? → Error
   ↓
   ✅ Variable creada exitosamente
   ✅ Disponible como {territorio} en plantillas
   ✅ Se muestra en la lista
```

### Editar Variable Existente

```
1. Click botón "✏️" en la variable
   ↓
2. Modal se abre con datos precargados:
   • Nombre: "territorio"
   • Tipo: "Dato de Organización"
   • Valor: "organization_territory" (preseleccionado)
   • Descripción: "Territorio del resguardo"
   • Estado: ✓ Activa
   ↓
3. Modificar cualquier campo
   ↓
4. Click "Actualizar"
   ↓
   Sistema valida:
   • Si se cambió el nombre, verifica que no exista otra variable
   • Si se cambió el tipo, valida que el valor sea compatible
   ↓
   ✅ Variable actualizada
   ✅ Cambios reflejados inmediatamente
```

---

## 🗃️ MIGRACIÓN DE BASE DE DATOS

### Migración Creada

**Archivo:** `censoapp/migrations/0028_update_templatevariable_type_choices.py`

**Cambios aplicados:**

1. **Agregar campo variable_type**
   ```python
   field=models.CharField(
       choices=[
           ('person', 'Dato de Persona'),
           ('family_card', 'Dato de Ficha Familiar'),
           ('association', 'Dato de Asociación'),
           ('organization', 'Dato de Organización'),
       ],
       default='person',
       max_length=20,
       verbose_name='Tipo de Variable'
   )
   ```

2. **Cambiar variable_value de TextField a CharField**
   ```python
   field=models.CharField(
       max_length=200,
       verbose_name='Campo del Modelo'
   )
   ```

3. **Actualizar ordering del modelo**
   ```python
   options={
       'ordering': ['organization', 'variable_type', 'variable_name'],
       'verbose_name': 'Variable Personalizada',
       'verbose_name_plural': 'Variables Personalizadas'
   }
   ```

**Comando ejecutado:**
```bash
python manage.py migrate
```

**Resultado:**
```
✅ Applying censoapp.0028_update_templatevariable_type_choices... OK
```

---

## 📈 COMPARACIÓN

### Antes vs Después

| Aspecto | ANTES | DESPUÉS |
|---------|-------|---------|
| **Número de campos** | 5 campos | 4 campos |
| **Modos de entrada** | 2 (estático/dinámico) | 1 (solo dinámico) |
| **Validación duplicados** | ❌ No | ✅ Sí |
| **Campos disponibles** | 37 (solo 3 tipos) | 43 (4 tipos) |
| **Interfaz** | Confusa (cambia según tipo) | Clara (siempre igual) |
| **Iconos** | ❌ No | ✅ Sí |
| **Tipo de variable visible** | ❌ No | ✅ Sí (badge) |
| **Ayuda contextual** | Básica | Detallada |
| **Errores claros** | Genéricos | Específicos |
| **Edición** | Perdía tipo | Mantiene tipo |

---

## 🎉 VENTAJAS DEL NUEVO SISTEMA

### Para el Usuario

```
✅ Formulario más simple (4 campos)
✅ Sin confusión entre estático/dinámico
✅ Ve todos los campos disponibles
✅ Validación inmediata de duplicados
✅ Mensajes de error claros
✅ Iconos intuitivos
✅ Ayuda contextual por tipo de campo
✅ Edición preserva el tipo
✅ Interfaz consistente
```

### Para el Administrador

```
✅ Menos errores de configuración
✅ Todas las variables son trazables al modelo
✅ Fácil auditoría (tipo visible)
✅ Ordenamiento lógico (por tipo y nombre)
✅ Validación a nivel de base de datos
✅ Migraciones aplicadas correctamente
```

### Para el Sistema

```
✅ Datos más consistentes
✅ Validación a nivel de modelo
✅ Menos excepciones en runtime
✅ Mejor rendimiento (CharField vs TextField)
✅ Integridad referencial
✅ Escalable (fácil agregar nuevos tipos)
```

---

## 📝 ARCHIVOS MODIFICADOS

```
✅ censoapp/template_models.py
   • Actualizado modelo TemplateVariable
   • Agregado campo variable_type
   • Cambiado variable_value a CharField
   • Agregado ordering

✅ censoapp/template_views.py
   • Actualizado variable_create con validación
   • Actualizado variable_update con validación
   • Agregado soporte para associations en get_model_fields

✅ templates/templates/variables.html
   • Simplificado modal de creación (4 campos)
   • Actualizado modal de edición
   • Agregados iconos descriptivos
   • Mejorada visualización de lista
   • Refactorizado JavaScript

✅ censoapp/migrations/0028_update_templatevariable_type_choices.py
   • Nueva migración aplicada
```

---

## ✅ ESTADO FINAL

**Formulario simplificado:** ✅ IMPLEMENTADO  
**4 campos definidos:** ✅ COMPLETADO  
**Validación de duplicados:** ✅ FUNCIONAL  
**Soporte para 4 tipos:** ✅ LISTO  
**43 campos disponibles:** ✅ CONFIGURADO  
**Migración aplicada:** ✅ OK  
**Sin errores:** ✅ VERIFICADO  

---

## 🚀 PRÓXIMOS PASOS SUGERIDOS

### Mejoras Futuras (Opcionales)

```
⏳ Importar/Exportar variables entre organizaciones
⏳ Variables globales (compartidas por todas las orgs)
⏳ Preview en tiempo real del valor
⏳ Historial de cambios por variable
⏳ Búsqueda avanzada con filtros por tipo
⏳ Agrupación visual por tipo en la lista
⏳ Validación de campos al momento de usar en plantillas
⏳ Sugerencias de variables frecuentes
```

---

**Implementado por:** GitHub Copilot  
**Fecha:** 19 de diciembre de 2025  
**Archivos modificados:** 4 archivos  
**Migración:** 1 nueva migración  
**Estado:** ✅ COMPLETAMENTE FUNCIONAL  
**Mejora UX:** 🚀 Significativa

---

## 📖 DOCUMENTACIÓN DE USO

### Para crear una variable:

1. Ir a **Variables Personalizadas**
2. Click en **"Nueva Variable"**
3. Completar:
   - **Nombre:** Sin llaves, único (ej: "territorio")
   - **Tipo:** Seleccionar modelo (Persona, Ficha, Asociación, Organización)
   - **Valor:** Elegir campo de la lista
   - **Descripción:** Opcional, para documentar
4. Click en **"Guardar Variable"**

### Para usar en plantillas:

```html
La persona {nombre_completo} vive en {territorio}
```

### Tipos de campos disponibles:

- **text** → Texto simple
- **relation** → Campo relacionado (usa punto: `sidewalk_home.sidewalk_name`)
- **date** → Fecha
- **number** → Número
- **method** → Método calculado (ej: `calcular_anios`)

---

**✅ SISTEMA SIMPLIFICADO Y LISTO PARA USAR**

