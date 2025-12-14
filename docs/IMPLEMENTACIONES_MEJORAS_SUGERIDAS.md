# 🚀 IMPLEMENTACIONES CONCRETAS - MEJORAS PRIORITARIAS

**Proyecto:** censo-django  
**Fecha:** 14 de Diciembre de 2025

---

## 1️⃣ AUDITORÍA CON DJANGO-SIMPLE-HISTORY

### Instalación
```bash
pip install django-simple-history
```

### Configuración en settings.py
```python
INSTALLED_APPS = [
    # ...apps existentes...
    'simple_history',
]

MIDDLEWARE = [
    # ...middleware existentes...
    'simple_history.middleware.HistoryRequestMiddleware',
]
```

### Actualizar models.py
```python
from simple_history.models import HistoricalRecords

class FamilyCard(models.Model):
    # ...campos existentes...
    history = HistoricalRecords()
    
class Person(models.Model):
    # ...campos existentes...
    history = HistoricalRecords()
    
class MaterialConstructionFamilyCard(models.Model):
    # ...campos existentes...
    history = HistoricalRecords()
```

### Migrar
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ver historial en templates
```django
<!-- En detail_family_card.html -->
<h4>Historial de Cambios</h4>
<ul>
{% for change in family_card.history.all %}
    <li>
        {{ change.history_date }} - 
        {{ change.history_type }} - 
        por {{ change.history_user }}
    </li>
{% endfor %}
</ul>
```

---

## 2️⃣ CACHE DE PARÁMETROS DEL SISTEMA

### Crear archivo utils.py en censoapp/
```python
# censoapp/utils.py
from django.core.cache import cache
from .models import SystemParameters

def get_system_parameters_cached(timeout=3600):
    """
    Obtiene parámetros del sistema con cache.
    Por defecto cachea por 1 hora (3600 segundos).
    """
    cache_key = 'system_parameters'
    params = cache.get(cache_key)
    
    if params is None:
        params_qs = SystemParameters.objects.all().values('key', 'value')
        params = {p['key']: p['value'] for p in params_qs}
        cache.set(cache_key, params, timeout)
    
    return params

def invalidate_system_parameters_cache():
    """Invalida el cache cuando se actualizan parámetros"""
    cache.delete('system_parameters')
```

### Usar en views.py
```python
from .utils import get_system_parameters_cached

class UpdateFamily(LoginRequiredMixin, UpdateView):
    # ...código existente...
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Usar versión cacheada
        system_params = get_system_parameters_cached()
        
        context['segment'] = 'family_card'
        context['system_params'] = system_params
        context['datos_vivienda'] = system_params.get('Datos de Vivienda', 'N')
        
        # ...resto del código...
        return context
```

### Actualizar admin.py para invalidar cache
```python
# censoapp/admin.py
from django.contrib import admin
from .models import SystemParameters
from .utils import invalidate_system_parameters_cache

class SystemParametersAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        invalidate_system_parameters_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        invalidate_system_parameters_cache()

admin.site.register(SystemParameters, SystemParametersAdmin)
```

---

## 3️⃣ EXPORTACIÓN A EXCEL

### Instalación
```bash
pip install openpyxl
```

### Crear archivo exports.py
```python
# censoapp/exports.py
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from django.http import HttpResponse
from .models import Person, FamilyCard
from django.db.models import Count

def export_family_cards_to_excel():
    """Exportar fichas familiares a Excel"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Fichas Familiares"
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2196F3", end_color="2196F3", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Headers
    headers = [
        'N° Ficha', 'Cabeza de Familia', 'Documento', 
        'Vereda', 'Zona', 'Resguardo', 
        'Total Miembros', 'Dirección'
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Datos
    families = (Person.objects
                .filter(family_head=True, state=True)
                .select_related('family_card', 'family_card__sidewalk_home', 
                              'family_card__organization', 'document_type')
                .annotate(member_count=Count('family_card__person', 
                                            filter=Q(family_card__person__state=True)))
                .order_by('family_card__family_card_number'))
    
    for row_num, person in enumerate(families, 2):
        ws.cell(row=row_num, column=1, value=person.family_card.family_card_number)
        ws.cell(row=row_num, column=2, value=person.full_name)
        ws.cell(row=row_num, column=3, value=person.identification_person)
        ws.cell(row=row_num, column=4, value=person.family_card.sidewalk_home.sidewalk_name)
        ws.cell(row=row_num, column=5, value=person.family_card.zone)
        ws.cell(row=row_num, column=6, value=person.family_card.organization.organization_name)
        ws.cell(row=row_num, column=7, value=person.member_count)
        ws.cell(row=row_num, column=8, value=person.family_card.address_home or '')
    
    # Ajustar anchos de columna
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width
    
    return wb


def export_persons_to_excel():
    """Exportar personas a Excel"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Personas"
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2196F3", end_color="2196F3", fill_type="solid")
    
    # Headers
    headers = [
        'N° Ficha', 'Nombres', 'Apellidos', 'Documento', 
        'Género', 'Fecha Nacimiento', 'Edad', 'Parentesco',
        'Nivel Educativo', 'Ocupación', 'EPS'
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
    
    # Datos
    from datetime import date
    personas = (Person.objects
                .filter(state=True)
                .select_related('family_card', 'gender', 'kinship', 
                              'education_level', 'occupation', 'eps', 'document_type')
                .order_by('family_card__family_card_number', '-family_head'))
    
    for row_num, person in enumerate(personas, 2):
        today = date.today()
        age = today.year - person.date_birth.year - (
            (today.month, today.day) < (person.date_birth.month, person.date_birth.day)
        )
        
        ws.cell(row=row_num, column=1, value=person.family_card.family_card_number)
        ws.cell(row=row_num, column=2, value=f"{person.first_name_1} {person.first_name_2 or ''}")
        ws.cell(row=row_num, column=3, value=f"{person.last_name_1} {person.last_name_2 or ''}")
        ws.cell(row=row_num, column=4, value=person.identification_person)
        ws.cell(row=row_num, column=5, value=person.gender.gender)
        ws.cell(row=row_num, column=6, value=person.date_birth.strftime('%Y-%m-%d'))
        ws.cell(row=row_num, column=7, value=age)
        ws.cell(row=row_num, column=8, value=person.kinship.description_kinship)
        ws.cell(row=row_num, column=9, value=person.education_level.education_level)
        ws.cell(row=row_num, column=10, value=person.occupation.description_occupancy)
        ws.cell(row=row_num, column=11, value=person.eps.name_eps)
    
    # Ajustar anchos
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width
    
    return wb
```

### Agregar vistas en views.py
```python
from .exports import export_family_cards_to_excel, export_persons_to_excel

@login_required
def export_family_cards_excel(request):
    """Vista para exportar fichas familiares a Excel"""
    wb = export_family_cards_to_excel()
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fichas_familiares.xlsx'
    wb.save(response)
    return response


@login_required
def export_persons_excel(request):
    """Vista para exportar personas a Excel"""
    wb = export_persons_to_excel()
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=personas.xlsx'
    wb.save(response)
    return response
```

### Agregar URLs
```python
# censoapp/urls.py
urlpatterns = [
    # ...urls existentes...
    
    # Exportaciones
    path('export/family-cards/', login_required(export_family_cards_excel), name='export-family-cards'),
    path('export/persons/', login_required(export_persons_excel), name='export-persons'),
]
```

### Agregar botones en templates
```django
<!-- En familyCardIndex.html -->
<div class="mb-3">
    <a href="{% url 'export-family-cards' %}" class="btn btn-success">
        <i class="fas fa-file-excel"></i> Exportar a Excel
    </a>
</div>

<!-- En listado_personas.html -->
<div class="mb-3">
    <a href="{% url 'export-persons' %}" class="btn btn-success">
        <i class="fas fa-file-excel"></i> Exportar a Excel
    </a>
</div>
```

---

## 4️⃣ TESTS UNITARIOS COMPLETOS

### Crear archivo test_family_flow.py
```python
# censoapp/tests/test_family_flow.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from censoapp.models import (
    FamilyCard, Person, Sidewalks, Organizations, Association,
    DocumentType, Gender, Kinship, EducationLevel, CivilState,
    Occupancy, SecuritySocial, Eps, Handicap
)
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile


class FamilyCardFlowTestCase(TestCase):
    def setUp(self):
        """Configuración inicial para todos los tests"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Crear datos requeridos
        self.association = Association.objects.create(
            association_name='Test Association',
            association_identification='123456789',
            association_type_document='NIT',
            association_phone_mobile='3001234567',
            association_phone='6012345678',
            association_address='Calle 123',
            association_departament='Test Dept',
            association_email='test@association.com',
            association_logo=SimpleUploadedFile('logo.jpg', b'content', content_type='image/jpeg')
        )
        
        self.organization = Organizations.objects.create(
            organization_name='Test Org',
            organization_identification='987654321',
            organization_territory='Test Territory',
            organization_email='test@org.com',
            organization_mobile_phone='3009876543',
            organization_phone='6019876543',
            organization_address='Carrera 45',
            organization_logo=SimpleUploadedFile('org.jpg', b'content', content_type='image/jpeg'),
            association_id=self.association
        )
        
        self.sidewalk = Sidewalks.objects.create(
            sidewalk_name='Test Vereda',
            organization_id=self.organization
        )
        
        # Datos para persona
        self.document_type = DocumentType.objects.create(code_document_type='CC', document_type='Cédula')
        self.gender = Gender.objects.create(gender_code='M', gender='Masculino')
        self.kinship = Kinship.objects.create(code_kinship='1', description_kinship='Cabeza')
        self.education = EducationLevel.objects.create(code_education_level='1', education_level='Primaria')
        self.civil_state = CivilState.objects.create(code_state_civil='S', state_civil='Soltero')
        self.occupation = Occupancy.objects.create(description_occupancy='Agricultor')
        self.social_security = SecuritySocial.objects.create(code_security_social='01', affiliation='Contributivo')
        self.eps = Eps.objects.create(code_eps='EPS001', name_eps='Test EPS')
        self.handicap = Handicap.objects.create(code_handicap='0', handicap='Ninguna')
    
    def test_create_family_card_with_adult_head_success(self):
        """Test: Crear ficha con cabeza de familia mayor de 18 años - ÉXITO"""
        self.client.login(username='testuser', password='testpass123')
        
        birth_date = date.today() - timedelta(days=365*25)  # 25 años
        
        data = {
            # Datos de familia
            'address_home': 'Casa de prueba',
            'sidewalk_home': self.sidewalk.id,
            'latitude': '4.123456',
            'longitude': '-74.123456',
            'zone': 'R',
            'organization': self.organization.id,
            
            # Datos de persona
            'first_name_1': 'Juan',
            'first_name_2': 'Carlos',
            'last_name_1': 'Pérez',
            'last_name_2': 'García',
            'identification_person': '1234567890',
            'document_type': self.document_type.id,
            'date_birth': birth_date.strftime('%Y-%m-%d'),
            'cell_phone': '3001234567',
            'personal_email': 'juan@test.com',
            'gender': self.gender.id,
            'kinship': self.kinship.id,
            'education_level': self.education.id,
            'civil_state': self.civil_state.id,
            'occupation': self.occupation.id,
            'social_insurance': self.social_security.id,
            'eps': self.eps.id,
            'handicap': self.handicap.id,
        }
        
        response = self.client.post(reverse('createFamilyCard'), data)
        
        # Verificaciones
        self.assertEqual(FamilyCard.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)
        
        family = FamilyCard.objects.first()
        person = Person.objects.first()
        
        self.assertTrue(person.family_head)
        self.assertEqual(person.family_card, family)
        self.assertEqual(family.family_card_number, 1)
    
    def test_create_family_card_with_underage_head_fails(self):
        """Test: Crear ficha con cabeza menor de 18 años - FALLA"""
        self.client.login(username='testuser', password='testpass123')
        
        birth_date = date.today() - timedelta(days=365*15)  # 15 años
        
        data = {
            'address_home': 'Casa de prueba',
            'sidewalk_home': self.sidewalk.id,
            'latitude': '4.123456',
            'longitude': '-74.123456',
            'zone': 'R',
            'organization': self.organization.id,
            'first_name_1': 'Pedro',
            'last_name_1': 'López',
            'identification_person': '9876543210',
            'document_type': self.document_type.id,
            'date_birth': birth_date.strftime('%Y-%m-%d'),
            'gender': self.gender.id,
            'kinship': self.kinship.id,
            'education_level': self.education.id,
            'civil_state': self.civil_state.id,
            'occupation': self.occupation.id,
            'social_insurance': self.social_security.id,
            'eps': self.eps.id,
            'handicap': self.handicap.id,
        }
        
        response = self.client.post(reverse('createFamilyCard'), data)
        
        # No debe crear registros
        self.assertEqual(FamilyCard.objects.count(), 0)
        self.assertEqual(Person.objects.count(), 0)
        
        # Debe mostrar mensaje de error
        messages = list(response.context['messages'])
        self.assertTrue(any('18 años' in str(m) for m in messages))
    
    def test_create_family_with_duplicate_document_fails(self):
        """Test: Crear ficha con documento duplicado - FALLA"""
        self.client.login(username='testuser', password='testpass123')
        
        # Crear persona existente
        birth_date = date.today() - timedelta(days=365*30)
        existing_family = FamilyCard.objects.create(
            sidewalk_home=self.sidewalk,
            zone='R',
            organization=self.organization,
            family_card_number=1
        )
        Person.objects.create(
            first_name_1='Existing',
            last_name_1='Person',
            identification_person='1111111111',
            document_type=self.document_type,
            date_birth=birth_date,
            gender=self.gender,
            kinship=self.kinship,
            education_level=self.education,
            civil_state=self.civil_state,
            occupation=self.occupation,
            social_insurance=self.social_security,
            eps=self.eps,
            handicap=self.handicap,
            family_card=existing_family,
            family_head=True
        )
        
        # Intentar crear nueva con mismo documento
        data = {
            'address_home': 'Nueva casa',
            'sidewalk_home': self.sidewalk.id,
            'zone': 'U',
            'organization': self.organization.id,
            'first_name_1': 'Nueva',
            'last_name_1': 'Persona',
            'identification_person': '1111111111',  # Duplicado
            'document_type': self.document_type.id,
            'date_birth': birth_date.strftime('%Y-%m-%d'),
            'gender': self.gender.id,
            'kinship': self.kinship.id,
            'education_level': self.education.id,
            'civil_state': self.civil_state.id,
            'occupation': self.occupation.id,
            'social_insurance': self.social_security.id,
            'eps': self.eps.id,
            'handicap': self.handicap.id,
        }
        
        response = self.client.post(reverse('createFamilyCard'), data)
        
        # Solo debe existir la ficha y persona original
        self.assertEqual(FamilyCard.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)
        
        # Mensaje de error
        messages = list(response.context['messages'])
        self.assertTrue(any('ya está registrado' in str(m) for m in messages))


class PersonFlowTestCase(TestCase):
    def setUp(self):
        """Configuración para tests de personas"""
        # Reutilizar setup similar al anterior
        # ... (mismo código de setUp de FamilyCardFlowTestCase)
        pass
    
    def test_add_person_to_existing_family_success(self):
        """Test: Agregar persona a familia existente - ÉXITO"""
        # Implementar
        pass
    
    def test_change_family_head_success(self):
        """Test: Cambiar cabeza de familia - ÉXITO"""
        # Implementar
        pass
    
    def test_cannot_have_two_family_heads(self):
        """Test: No puede haber dos cabezas de familia - FALLA"""
        # Implementar
        pass
```

### Ejecutar tests
```bash
python manage.py test censoapp.tests.test_family_flow
```

---

## 5️⃣ ÍNDICES DE BASE DE DATOS

### Actualizar models.py
```python
class Person(models.Model):
    # ...campos existentes...
    
    class Meta:
        indexes = [
            models.Index(fields=['identification_person'], name='idx_person_ident'),
            models.Index(fields=['family_card', 'state'], name='idx_person_family_state'),
            models.Index(fields=['family_head', 'state'], name='idx_person_head_state'),
            models.Index(fields=['date_birth'], name='idx_person_birth'),
        ]
        ordering = ['family_card', '-family_head']


class FamilyCard(models.Model):
    # ...campos existentes...
    
    class Meta:
        indexes = [
            models.Index(fields=['family_card_number'], name='idx_family_number'),
            models.Index(fields=['sidewalk_home', 'state'], name='idx_family_sidewalk'),
            models.Index(fields=['state'], name='idx_family_state'),
        ]
        ordering = ['family_card_number']
```

### Crear migración
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Prioridad 1 (Esta semana)
- [ ] Instalar y configurar django-simple-history
- [ ] Implementar cache de parámetros del sistema
- [ ] Agregar índices a modelos Person y FamilyCard
- [ ] Ejecutar migraciones

### Prioridad 2 (Próxima semana)
- [ ] Implementar exportación a Excel (fichas y personas)
- [ ] Crear suite de tests unitarios completa
- [ ] Agregar botones de exportación en templates
- [ ] Validar coverage de tests (>70%)

### Prioridad 3 (Mes siguiente)
- [ ] Implementar búsqueda avanzada con filtros
- [ ] Agregar dashboard con más estadísticas
- [ ] Implementar notificaciones por email
- [ ] Documentar API endpoints

---

**Última actualización:** 2025-12-14  
**Mantenedor:** Equipo censo-django

