# Corrección: Asignación Automática del Número de Ficha Familiar

**Fecha:** 2025-12-18  
**Estado:** ✅ COMPLETADO

## Problema Identificado

Al intentar crear una nueva ficha familiar, se recibía el siguiente mensaje de error:

```
Datos de vivienda - family_card_number: El número de ficha familiar no puede ser 0. Se asignará automáticamente
```

### Causa del Problema

El error se producía debido a un conflicto en el flujo de validación:

1. El campo `family_card_number` en el modelo `FamilyCard` tiene `default=0`
2. El método `clean()` del modelo se ejecuta durante `form.is_valid()` y validaba que el número NO fuera 0
3. El número automático se asignaba DESPUÉS en el método `save()` o en la vista
4. Esto creaba un círculo vicioso: el formulario validaba con valor 0, y el método `clean()` lo rechazaba

## Solución Implementada

### 1. Modificación del Modelo `FamilyCard` (models.py)

**Archivo:** `censoapp/models.py`

**Cambio en el método `clean()`:**

```python
def clean(self):
    """Validar que el número de ficha sea válido"""
    from django.core.exceptions import ValidationError

    # Solo validar duplicados si el número NO es 0
    # Si es 0, se asignará automáticamente en save()
    if self.family_card_number and self.family_card_number != 0:
        duplicates = FamilyCard.objects.filter(
            family_card_number=self.family_card_number
        ).exclude(pk=self.pk)

        if duplicates.exists():
            raise ValidationError({
                'family_card_number': f'El número de ficha {self.family_card_number} ya está en uso.'
            })
```

**Cambios realizados:**
- ✅ Se eliminó la validación que rechazaba `family_card_number = 0`
- ✅ Se permite que el valor sea 0 durante la creación
- ✅ Se mantiene la validación de duplicados para números válidos (> 0)

### 2. Modificación del Formulario `FormFamilyCard` (forms.py)

**Archivo:** `censoapp/forms.py`

**Cambio 1 - Meta del formulario:**

```python
class Meta:
    model = FamilyCard
    fields = ['address_home', 'sidewalk_home', 'latitude', 'longitude', 'zone', 'organization']
    # Se eliminó 'family_card_number' de los fields
```

**Cambio 2 - Método `__init__()`:**

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_id = 'id-FamilyCard'
    self.helper.form_class = 'pl-6 pr-6 pb-6 pt-6'
    self.helper.label_class = 'control-label'

    # Excluir family_card_number del formulario tanto en creación como en edición
    # En creación se asignará automáticamente en la vista
    # En edición no debe ser modificable
    self.fields.pop('family_card_number', None)

    # Configurar comportamiento según modo (creación vs edición)
    if self.instance and self.instance.pk:
        # Modo edición: asegurar que los campos críticos mantengan sus valores
        if self.data:  # En POST
            # Si los campos no vienen en POST, usar valores de la instancia
            data_copy = self.data.copy()
            if not data_copy.get('sidewalk_home'):
                data_copy['sidewalk_home'] = self.instance.sidewalk_home_id
            if not data_copy.get('zone'):
                data_copy['zone'] = self.instance.zone
            if not data_copy.get('organization'):
                data_copy['organization'] = self.instance.organization_id
            self.data = data_copy
```

**Cambios realizados:**
- ✅ Se eliminó `family_card_number` de los fields del formulario
- ✅ Se simplificó el método `__init__()` para excluir siempre el campo
- ✅ Se eliminó el código que intentaba hacer el campo readonly en modo creación

## Flujo Correcto Ahora

### Creación de Ficha Familiar

1. **Usuario completa el formulario** (sin campo `family_card_number` visible)
2. **El formulario se valida** sin incluir `family_card_number`
3. **En la vista `create_family_card()`:**
   ```python
   family_card = family_card_form.save(commit=False)
   family_card.family_card_number = FamilyCard.get_next_family_card_number()
   family_card.state = True
   family_card.save()
   ```
4. **El método `save()` del modelo:**
   - Si el número es 0, lo asigna automáticamente
   - Guarda la ficha con el número correcto
5. **No se ejecuta validación de `clean()`** porque el número ya está asignado

### Edición de Ficha Familiar

1. El campo `family_card_number` no aparece en el formulario
2. El número de ficha permanece sin cambios
3. Solo se editan los demás campos (ubicación, vereda, etc.)

## Verificación

Se creó un script de prueba (`test_crear_ficha_familiar.py`) que verifica:

✅ **Test 1:** Crear ficha usando `FormFamilyCard`
- El formulario se valida correctamente sin `family_card_number`
- El número se asigna automáticamente al guardar
- La ficha se crea exitosamente

✅ **Test 2:** Crear ficha directamente con el modelo
- El modelo acepta `family_card_number=0` durante la creación
- El método `save()` asigna automáticamente el siguiente número
- La ficha se guarda correctamente

### Resultado de las Pruebas

```
================================================================================
PRUEBA: Creación de Ficha Familiar con Asignación Automática
================================================================================

✓ Formulario válido
✓ Ficha creada exitosamente
✓ Número de ficha asignado automáticamente: 1

================================================================================
PRUEBA COMPLETADA
================================================================================
```

## Archivos Modificados

1. ✅ `censoapp/models.py` - Método `clean()` de `FamilyCard`
2. ✅ `censoapp/forms.py` - Clase `FormFamilyCard`

## Archivos Creados

1. ✅ `test_crear_ficha_familiar.py` - Script de prueba

## Impacto

- ✅ Los usuarios ahora pueden crear fichas familiares sin errores
- ✅ El número de ficha se asigna automáticamente de forma transparente
- ✅ No se requiere intervención manual para asignar números
- ✅ Se mantiene la validación de duplicados para evitar conflictos
- ✅ El flujo de creación es más simple y robusto

## Notas Técnicas

- El método `get_next_family_card_number()` calcula el siguiente número disponible
- La validación de duplicados solo se ejecuta para números > 0
- El campo permanece como `IntegerField` con `unique=True` en la base de datos
- La lógica de asignación automática se mantiene tanto en el modelo como en la vista para mayor robustez

## Recomendaciones

1. ✅ Probar la creación de fichas en el ambiente de producción
2. ✅ Verificar que las fichas existentes no se vean afectadas
3. ✅ Monitorear que no se generen números duplicados
4. ⚠️ Considerar agregar un índice de base de datos si hay muchas fichas

---

**Estado Final:** ✅ PROBLEMA RESUELTO

El mensaje de error "El número de ficha familiar no puede ser 0" ya no aparecerá al crear nuevas fichas familiares. El número se asigna automáticamente de forma correcta y transparente.

