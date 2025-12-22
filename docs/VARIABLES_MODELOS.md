# Variables Disponibles de los Modelos del Sistema

Este documento contiene todas las variables/campos disponibles en los modelos principales del sistema de censo.

---

## 1. ASOCIACIÓN (Association)

**Modelo:** `Association`  
**Descripción:** Representa la asociación que agrupa varias organizaciones indígenas.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único de la asociación | Automático |
| `association_name` | CharField(50) | Nombre de la asociación | Sí |
| `association_identification` | CharField(15) | Número de identificación (NIT) | Sí |
| `association_type_document` | CharField(3) | Tipo de documento (defecto: 'NIT') | Sí |
| `association_phone_mobile` | CharField(15) | Número de celular | No |
| `association_phone` | CharField(15) | Número de teléfono fijo | No |
| `association_address` | CharField(50) | Dirección física | Sí |
| `association_departament` | CharField(15) | Departamento donde se ubica | Sí |
| `association_email` | EmailField | Correo electrónico | Sí |
| `association_logo` | ImageField | Logo de la asociación | No |

**Ejemplo de uso en template:**
```django
{{ asociacion.association_name }}
{{ asociacion.association_identification }}
{{ asociacion.association_email }}
{{ asociacion.association_logo.url }}
```

---

## 2. ORGANIZACIÓN (Organizations)

**Modelo:** `Organizations`  
**Descripción:** Representa un resguardo o comunidad indígena perteneciente a una asociación.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único de la organización | Automático |
| `organization_name` | CharField(50) | Nombre del resguardo | Sí |
| `organization_identification` | CharField(15) | NIT único de la organización | Sí |
| `organization_type_identification` | CharField(3) | Tipo documento (defecto: 'NIT') | Sí |
| `organization_territory` | CharField(50) | Territorio que ocupa | Sí |
| `organization_email` | EmailField | Correo electrónico | Sí |
| `organization_mobile_phone` | CharField(15) | Celular de contacto | No |
| `organization_phone` | CharField(15) | Teléfono fijo | No |
| `organization_address` | CharField(50) | Dirección física | Sí |
| `organization_logo` | ImageField | Logo de la organización | Sí |
| `association_id` | ForeignKey | Asociación a la que pertenece | Sí |

**Relaciones:**
- `association_id`: Asociación padre
- `sidewalks_set`: Veredas de la organización
- `familycard_set`: Fichas familiares de la organización
- `board_positions`: Cargos de junta directiva

**Ejemplo de uso en template:**
```django
{{ organization.organization_name }}
{{ organization.organization_identification }}
{{ organization.organization_territory }}
{{ organization.association_id.association_name }}
```

---

## 3. PERFIL DE USUARIO (UserProfile)

**Modelo:** `UserProfile`  
**Descripción:** Perfil extendido del usuario vinculado a una organización (multi-tenancy).

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `user` | OneToOneField | Usuario de Django | Sí |
| `organization` | ForeignKey | Organización del usuario | Sí |
| `role` | CharField(50) | Rol: ADMIN, OPERATOR, VIEWER | Sí |
| `can_view_all_organizations` | BooleanField | Acceso a todas las organizaciones | No (default: False) |
| `is_active` | BooleanField | Perfil activo | Sí (default: True) |
| `created_at` | DateTimeField | Fecha de creación | Automático |
| `updated_at` | DateTimeField | Última actualización | Automático |

**Roles disponibles:**
- `ADMIN`: Administrador de Organización
- `OPERATOR`: Operador
- `VIEWER`: Solo Consulta

**Ejemplo de uso:**
```python
# En vista
user_profile = request.user.profile
organization = user_profile.organization
can_edit = user_profile.role in ['ADMIN', 'OPERATOR']
```

---

## 4. FICHA FAMILIAR (FamilyCard)

**Modelo:** `FamilyCard`  
**Descripción:** Representa una familia registrada en el censo.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `family_card_number` | IntegerField | Número de ficha (único) | Automático |
| `address_home` | CharField(50) | Dirección de la vivienda | No |
| `sidewalk_home` | ForeignKey | Vereda donde vive | Sí |
| `latitude` | CharField(15) | Coordenada latitud | No (default: '0') |
| `longitude` | CharField(15) | Coordenada longitud | No (default: '0') |
| `zone` | CharField(10) | Zona: Urbana o Rural | Sí |
| `organization` | ForeignKey | Resguardo al que pertenece | Sí |
| `state` | BooleanField | Estado activo/inactivo | Sí (default: True) |
| `created_at` | DateTimeField | Fecha de creación | Automático |
| `updated_at` | DateTimeField | Última actualización | Automático |

**Relaciones:**
- `sidewalk_home`: Vereda
- `organization`: Organización/Resguardo
- `person_set`: Personas de la familia
- `material_construction`: Datos de vivienda (OneToOne)
- `publicservices_set`: Servicios públicos

**Métodos útiles:**
```python
family_card.get_next_family_card_number()  # Obtener siguiente número
family_card.get_count_members(family_card_id)  # Contar miembros
```

**Ejemplo de uso en template:**
```django
{{ family_card.family_card_number }}
{{ family_card.address_home }}
{{ family_card.sidewalk_home.sidewalk_name }}
{{ family_card.organization.organization_name }}
{{ family_card.zone }}
{{ family_card.created_at|date:"d/m/Y" }}
```

---

## 5. PERSONA (Person)

**Modelo:** `Person`  
**Descripción:** Representa un individuo registrado en el censo, asociado a una ficha familiar.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `first_name_1` | CharField(30) | Primer nombre | Sí |
| `first_name_2` | CharField(30) | Segundo nombre | No |
| `last_name_1` | CharField(30) | Primer apellido | Sí |
| `last_name_2` | CharField(30) | Segundo apellido | No |
| `identification_person` | CharField(15) | Número de identificación (único) | Sí |
| `document_type` | ForeignKey | Tipo de documento (CC, TI, etc.) | Sí |
| `cell_phone` | CharField(15) | Teléfono celular | No |
| `personal_email` | EmailField(50) | Correo electrónico | No |
| `gender` | ForeignKey | Género de la persona | Sí |
| `date_birth` | DateField | Fecha de nacimiento | Sí |
| `social_insurance` | ForeignKey | Tipo de seguridad social | Sí |
| `eps` | ForeignKey | EPS a la que pertenece | Sí |
| `kinship` | ForeignKey | Parentesco en la familia | Sí |
| `handicap` | ForeignKey | Capacidades diversas | Sí |
| `education_level` | ForeignKey | Nivel educativo | Sí |
| `civil_state` | ForeignKey | Estado civil | Sí |
| `occupation` | ForeignKey | Ocupación | Sí |
| `family_card` | ForeignKey | Ficha familiar a la que pertenece | Sí |
| `family_head` | BooleanField | Es cabeza de familia | Sí (default: False) |
| `state` | BooleanField | Estado vivo/fallecido | Sí (default: True) |

**Propiedades calculadas:**
- `full_name`: Nombre completo concatenado
- `calcular_anios`: Edad en años o meses

**Relaciones:**
- `family_card`: Ficha familiar
- `document_type`: Tipo de documento
- `gender`: Género
- `social_insurance`: Seguridad social
- `eps`: EPS
- `kinship`: Parentesco
- `handicap`: Discapacidad
- `education_level`: Nivel educativo
- `civil_state`: Estado civil
- `occupation`: Ocupación
- `board_position_holder`: Cargos como titular
- `board_position_alternate`: Cargos como suplente

**Ejemplo de uso en template:**
```django
{{ person.full_name }}
{{ person.identification_person }}
{{ person.document_type.document_type }}
{{ person.date_birth|date:"d/m/Y" }}
{{ person.calcular_anios }}
{{ person.gender.gender }}
{{ person.eps.name_eps }}
{{ person.kinship.description_kinship }}
{{ person.education_level.education_level }}
{{ person.civil_state.state_civil }}
{{ person.occupation.description_occupancy }}
{{ person.family_card.family_card_number }}
{% if person.family_head %}JEFE DE FAMILIA{% endif %}
```

---

## 6. VEREDA (Sidewalks)

**Modelo:** `Sidewalks`  
**Descripción:** Veredas o sectores de una organización.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `sidewalk_name` | CharField(40) | Nombre de la vereda | Sí |
| `organization_id` | ForeignKey | Organización a la que pertenece | Sí |

**Ejemplo de uso:**
```django
{{ sidewalk.sidewalk_name }}
{{ sidewalk.organization_id.organization_name }}
```

---

## 7. MATERIAL DE CONSTRUCCIÓN DE VIVIENDA (MaterialConstructionFamilyCard)

**Modelo:** `MaterialConstructionFamilyCard`  
**Descripción:** Características de construcción y vivienda de una familia (relación OneToOne con FamilyCard).

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `family_card` | OneToOneField | Ficha familiar (única) | Sí |
| `material_roof` | ForeignKey | Material del techo | Sí |
| `material_wall` | ForeignKey | Material de la pared | Sí |
| `material_floor` | ForeignKey | Material del piso | Sí |
| `number_families` | IntegerField | Número de familias | Sí (default: 1) |
| `number_people_bedrooms` | IntegerField | Personas por habitación | Sí (default: 1) |
| `condition_roof` | CharField(50) | Estado del techo | Sí |
| `condition_wall` | CharField(50) | Estado de la pared | Sí |
| `condition_floor` | CharField(50) | Estado del piso | Sí |
| `home_ownership` | ForeignKey | Tipo de propiedad | Sí |
| `kitchen_location` | IntegerField | Ubicación cocina (1:Interior, 2:Exterior) | Sí (default: 1) |
| `cooking_fuel` | ForeignKey | Combustible de cocina | Sí |
| `home_smoke` | BooleanField | Problemas de humo | Sí (default: False) |
| `number_bedrooms` | IntegerField | Número de habitaciones | Sí (default: 1) |
| `ventilation` | BooleanField | Ventilación adecuada | Sí (default: False) |
| `lighting` | BooleanField | Iluminación adecuada | Sí (default: False) |

**Ejemplo de uso:**
```django
{{ vivienda.material_roof.material_name }}
{{ vivienda.material_wall.material_name }}
{{ vivienda.material_floor.material_name }}
{{ vivienda.condition_roof }}
{{ vivienda.number_bedrooms }}
{{ vivienda.home_ownership.ownership_type }}
{{ vivienda.cooking_fuel.fuel_type }}
{% if vivienda.ventilation %}Tiene ventilación{% endif %}
{% if vivienda.lighting %}Tiene iluminación{% endif %}
```

---

## 8. SERVICIOS PÚBLICOS (PublicServices)

**Modelo:** `PublicServices`  
**Descripción:** Servicios públicos y saneamiento de una vivienda.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `family_card` | ForeignKey | Ficha familiar | Sí |
| `water_service` | BooleanField | Servicio de agua | Sí (default: False) |
| `water_source` | ForeignKey | Fuente de agua | Sí |
| `water_treatment` | ForeignKey | Tratamiento del agua | Sí |
| `electricity_service` | BooleanField | Servicio de electricidad | Sí (default: False) |
| `sewage_service` | BooleanField | Servicio de alcantarillado | Sí (default: False) |
| `internet_service` | BooleanField | Servicio de internet | Sí (default: False) |
| `biodegradable_waste` | ForeignKey | Manejo residuos biodegradables | Sí |
| `recyclable_waste` | ForeignKey | Manejo residuos reciclables | Sí |
| `non_recyclable_waste` | ForeignKey | Manejo residuos no reciclables | Sí |
| `hazardous_waste` | ForeignKey | Manejo residuos peligrosos | Sí |
| `excreta_waste` | ForeignKey | Manejo de excreta | Sí |
| `waste_water` | ForeignKey | Manejo de aguas residuales | Sí |

**Ejemplo de uso:**
```django
{% if services.water_service %}Tiene agua{% endif %}
{{ services.water_source.source_type }}
{{ services.water_treatment.treatment_type }}
{% if services.electricity_service %}Tiene electricidad{% endif %}
{% if services.internet_service %}Tiene internet{% endif %}
```

---

## 9. CARGO DE JUNTA DIRECTIVA (BoardPosition)

**Modelo:** `BoardPosition`  
**Descripción:** Cargos directivos de la organización con titular y suplente.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `organization` | ForeignKey | Organización | Sí |
| `position_name` | CharField(50) | Cargo (GOBERNADOR, ALCALDE, etc.) | Sí |
| `holder_person` | ForeignKey | Persona titular del cargo | Sí |
| `alternate_person` | ForeignKey | Persona suplente del cargo | No |
| `can_sign_documents` | BooleanField | Autorizado para firmar | Sí (default: False) |
| `start_date` | DateField | Fecha de inicio | Sí |
| `end_date` | DateField | Fecha de finalización | No |
| `is_active` | BooleanField | Cargo activo | Sí (default: True) |
| `observations` | TextField | Observaciones | No |
| `created_at` | DateTimeField | Fecha de creación | Automático |
| `updated_at` | DateTimeField | Última actualización | Automático |

**Cargos disponibles:**
- `GOBERNADOR`
- `ALCALDE`
- `CAPITAN`
- `ALGUACIL`
- `COMISARIO`
- `TESORERO`
- `SECRETARIO`

**Métodos útiles:**
```python
board_position.is_valid_on_date(fecha)  # Verifica vigencia
BoardPosition.get_valid_positions_on_date(org, fecha)  # Obtiene cargos vigentes
```

**Ejemplo de uso:**
```django
{{ cargo.get_position_name_display }}
{{ cargo.holder_person.full_name }}
{{ cargo.alternate_person.full_name }}
{{ cargo.start_date|date:"d/m/Y" }}
{{ cargo.end_date|date:"d/m/Y" }}
{% if cargo.can_sign_documents %}Autorizado para firmar{% endif %}
```

---

## 10. TIPO DE DOCUMENTO (DocumentType)

**Modelo:** `DocumentType`  
**Descripción:** Tipos de documentos que genera la organización (Aval, Constancia, etc.).

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `document_type_name` | CharField(100) | Nombre del tipo de documento | Sí |
| `description` | TextField | Descripción del tipo | No |
| `requires_expiration` | BooleanField | Requiere fecha de vencimiento | Sí (default: True) |
| `template_content` | TextField | Plantilla del contenido | No |
| `is_active` | BooleanField | Tipo activo | Sí (default: True) |
| `created_at` | DateTimeField | Fecha de creación | Automático |
| `updated_at` | DateTimeField | Última actualización | Automático |

**Ejemplo de uso:**
```django
{{ doc_type.document_type_name }}
{{ doc_type.description }}
{% if doc_type.requires_expiration %}Tiene vencimiento{% endif %}
```

---

## 11. PARÁMETROS DEL SISTEMA (SystemParameters)

**Modelo:** `SystemParameters`  
**Descripción:** Configuraciones globales del sistema para habilitar/deshabilitar funcionalidades.

### Variables Disponibles:

| Campo | Tipo | Descripción | Obligatorio |
|-------|------|-------------|-------------|
| `id` | Integer | Identificador único | Automático |
| `key` | CharField(100) | Clave del parámetro (única) | Sí |
| `value` | CharField(250) | Valor del parámetro | Sí |

**Parámetros comunes:**
- `Datos de Vivienda`: S/N (Habilita formulario de vivienda)

**Ejemplo de uso:**
```python
# En vista
params = SystemParameters.objects.all()
params_dict = {p.key: p.value for p in params}
context['datos_vivienda'] = params_dict.get('Datos de Vivienda', 'N')
```

```django
{% if datos_vivienda == 'S' %}
    <!-- Mostrar formulario de vivienda -->
{% endif %}
```

---

## MODELOS AUXILIARES (Catálogos)

### Estado Civil (CivilState)
- `code_state_civil`: CharField(1)
- `state_civil`: CharField(25)

### Nivel Educativo (EducationLevel)
- `code_education_level`: CharField(1)
- `education_level`: CharField(50)

### EPS (Eps)
- `code_eps`: CharField(6)
- `name_eps`: CharField(50)

### Parentesco (Kinship)
- `code_kinship`: CharField(1)
- `description_kinship`: CharField(25)

### Ocupación (Occupancy)
- `description_occupancy`: CharField(35)

### Tipo de Documento de Identidad (IdentificationDocumentType)
- `code_document_type`: CharField(3)
- `document_type`: CharField(25)

### Género (Gender)
- `gender_code`: CharField(1)
- `gender`: CharField(15)

### Discapacidad (Handicap)
- `code_handicap`: CharField(1)
- `handicap`: CharField(50)

### Seguridad Social (SecuritySocial)
- `code_security_social`: CharField(5)
- `affiliation`: CharField(30)

### Material de Construcción (MaterialConstruction)
- `material_name`: CharField(50)
- `roof`: BooleanField (uso en techos)
- `wall`: BooleanField (uso en paredes)
- `floor`: BooleanField (uso en pisos)

### Tipo de Propiedad (HomeOwnership)
- `ownership_type`: CharField(50)

### Tipo de Combustible (CookingFuel)
- `fuel_type`: CharField(50)

### Fuente de Agua (WaterSource)
- `source_type`: CharField(50)

### Tratamiento de Agua (WaterTreatment)
- `treatment_type`: CharField(50)

### Manejo de Residuos (WasteManagement)
- `management_type`: CharField(50)
- `biodegradable`: BooleanField
- `recyclable`: BooleanField
- `non_recyclable`: BooleanField
- `hazardous`: BooleanField
- `excreta`: BooleanField
- `wastewater`: BooleanField

---

## EJEMPLOS DE USO AVANZADO

### 1. Obtener todas las personas de una organización
```python
organization = request.user.profile.organization
personas = Person.objects.filter(
    family_card__organization=organization,
    state=True
).select_related('family_card', 'gender', 'kinship', 'eps')
```

### 2. Obtener fichas familiares con contador de miembros
```python
from django.db.models import Count

fichas = FamilyCard.objects.filter(
    organization=organization,
    state=True
).annotate(
    total_members=Count('person', filter=Q(person__state=True))
).select_related('sidewalk_home', 'organization')
```

### 3. Obtener jefes de familia de una organización
```python
jefes = Person.objects.filter(
    family_card__organization=organization,
    family_head=True,
    state=True
).select_related('family_card')
```

### 4. Validar permisos de usuario
```python
user_profile = request.user.profile
can_edit = user_profile.role in ['ADMIN', 'OPERATOR']
can_view_all = user_profile.can_view_all_organizations
```

### 5. Obtener junta directiva vigente
```python
from datetime import date

junta = BoardPosition.objects.filter(
    organization=organization,
    is_active=True,
    start_date__lte=date.today()
).filter(
    Q(end_date__isnull=True) | Q(end_date__gte=date.today())
).select_related('holder_person', 'alternate_person')
```

---

## NOTAS IMPORTANTES

1. **Auditoría**: Los modelos `FamilyCard`, `Person`, `MaterialConstructionFamilyCard` y `BoardPosition` tienen historial de cambios activado mediante `django-simple-history`.

2. **Multi-tenancy**: El sistema implementa multi-tenancy a nivel de aplicación mediante `UserProfile`, permitiendo que múltiples organizaciones convivan de forma independiente.

3. **Validaciones**: Muchos modelos implementan validaciones personalizadas en el método `clean()` que se ejecutan antes de guardar.

4. **Normalización**: Los campos de texto se normalizan automáticamente (capitalización) en el método `save()`.

5. **Relaciones**: Usar `select_related()` y `prefetch_related()` para optimizar consultas con relaciones ForeignKey y ManyToMany.

---

**Fecha de creación:** 20 de diciembre de 2024  
**Versión del sistema:** 1.0  
**Última actualización:** 20/12/2024

