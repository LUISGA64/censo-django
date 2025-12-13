from django import forms

from .models import FamilyCard, Person, DocumentType, Gender, SecuritySocial, Kinship, EducationLevel, CivilState, \
    Occupancy, Sidewalks, Organizations, Eps, Handicap, MaterialConstruction, MaterialConstructionFamilyCard, \
    HomeOwnership, CookingFuel
from .choices import zone
from crispy_forms.helper import FormHelper


class FormFamilyCard(forms.ModelForm):
    """Formulario para crear/editar fichas familiares con validaciones mejoradas"""

    class Meta:
        model = FamilyCard
        fields = ['sidewalk_home', 'latitude', 'longitude', 'zone', 'organization', 'family_card_number']

    sidewalk_home = forms.ModelChoiceField(
        queryset=Sidewalks.objects.all(),
        label="Vereda",
        empty_label="Seleccione la vereda donde vive",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Vereda',
            'required': True
        }),
        error_messages={
            'required': 'Debe seleccionar una vereda.',
            'invalid_choice': 'Seleccione una vereda válida.'
        }
    )

    latitude = forms.CharField(
        label='Latitud',
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 4.6097100 (opcional)'
        }),
        help_text='Coordenada de latitud (opcional)'
    )

    longitude = forms.CharField(
        label='Longitud',
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: -74.0817500 (opcional)'
        }),
        help_text='Coordenada de longitud (opcional)'
    )

    zone = forms.ChoiceField(
        choices=zone,
        label="Zona",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Zona',
            'required': True
        }),
        error_messages={
            'required': 'Debe seleccionar una zona.',
            'invalid_choice': 'Seleccione una zona válida.'
        }
    )

    organization = forms.ModelChoiceField(
        queryset=Organizations.objects.all(),
        label="Resguardo Indígena",
        empty_label="Seleccione el Resguardo",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Resguardo'
        }),
        error_messages={
            'required': 'Debe seleccionar un resguardo.',
            'invalid_choice': 'Seleccione un resguardo válido.'
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-FamilyCard'
        self.helper.form_class = 'pl-6 pr-6 pb-6 pt-6'
        self.helper.label_class = 'control-label'

        # Configurar family_card_number como readonly
        self.fields['family_card_number'].required = False
        self.fields['family_card_number'].widget.attrs.update({
            'readonly': True,
            'class': 'form-control bg-light',
            'placeholder': 'Se asignará automáticamente'
        })

    def clean_latitude(self):
        """Validar formato de latitud"""
        latitude = self.cleaned_data.get('latitude')
        if latitude:
            try:
                lat_float = float(latitude)
                if not -90 <= lat_float <= 90:
                    raise forms.ValidationError('La latitud debe estar entre -90 y 90 grados.')
            except ValueError:
                raise forms.ValidationError('Formato de latitud inválido.')
        return latitude

    def clean_longitude(self):
        """Validar formato de longitud"""
        longitude = self.cleaned_data.get('longitude')
        if longitude:
            try:
                lon_float = float(longitude)
                if not -180 <= lon_float <= 180:
                    raise forms.ValidationError('La longitud debe estar entre -180 y 180 grados.')
            except ValueError:
                raise forms.ValidationError('Formato de longitud inválido.')
        return longitude

    def clean(self):
        """Validaciones cruzadas del formulario"""
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        # Si se proporciona una coordenada, la otra también debe proporcionarse
        if (latitude and not longitude) or (longitude and not latitude):
            raise forms.ValidationError(
                'Debe proporcionar tanto la latitud como la longitud, o dejar ambas en blanco.'
            )

        return cleaned_data



class FormPerson(forms.ModelForm):
    """Formulario para crear/editar personas con validaciones mejoradas"""

    class Meta:
        model = Person
        fields = ['first_name_1', 'first_name_2', 'last_name_1', 'last_name_2', 'document_type',
                  'identification_person', 'gender', 'date_birth', 'kinship', 'social_insurance',
                  'eps', 'handicap', 'education_level', 'civil_state', 'occupation', 'cell_phone',
                  'personal_email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-Person'
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'control-label'

    # Primer Nombre
    first_name_1 = forms.CharField(
        label='Primer Nombre',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primer Nombre',
            'required': True,
            'pattern': r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+',
            'title': 'Solo se permiten letras'
        }),
        error_messages={
            'required': 'El primer nombre es obligatorio.',
            'max_length': 'El primer nombre no puede tener más de 30 caracteres.'
        }
    )

    # Segundo Nombre
    first_name_2 = forms.CharField(
        label='Segundo Nombre',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Segundo Nombre (opcional)',
            'pattern': r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+',
            'title': 'Solo se permiten letras'
        })
    )

    # Primer Apellido
    last_name_1 = forms.CharField(
        label='Primer Apellido',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primer Apellido',
            'required': True,
            'pattern': r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+',
            'title': 'Solo se permiten letras'
        }),
        error_messages={
            'required': 'El primer apellido es obligatorio.',
            'max_length': 'El primer apellido no puede tener más de 30 caracteres.'
        }
    )

    # Segundo Apellido
    last_name_2 = forms.CharField(
        label='Segundo Apellido',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Segundo Apellido (opcional)',
            'pattern': r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+',
            'title': 'Solo se permiten letras'
        })
    )

    # Número Teléfonico
    cell_phone = forms.CharField(
        label='Teléfono Móvil',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3001234567',
            'pattern': '[0-9]{10,15}',
            'title': 'Ingrese un número de teléfono válido (10-15 dígitos)'
        }),
        help_text='10-15 dígitos numéricos'
    )

    # Correo Personal
    personal_email = forms.EmailField(
        label='Correo Electrónico',
        max_length=50,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'type': 'email'
        }),
        error_messages={
            'invalid': 'Ingrese una dirección de correo electrónico válida.'
        }
    )

    # Identificación de la persona
    identification_person = forms.CharField(
        label='Número de Identificación',
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de documento',
            'required': True,
            'pattern': '[0-9A-Za-z-]+',
            'title': 'Ingrese un número de documento válido'
        }),
        error_messages={
            'required': 'El número de identificación es obligatorio.',
            'max_length': 'El número de identificación no puede tener más de 15 caracteres.'
        }
    )

    # Fecha de nacimiento
    date_birth = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True,
            'max': '9999-12-31'
        }),
        error_messages={
            'required': 'La fecha de nacimiento es obligatoria.',
            'invalid': 'Ingrese una fecha válida.'
        }
    )

    def clean_identification_person(self):
        """Validar que la identificación no contenga caracteres especiales peligrosos"""
        identification = self.cleaned_data.get('identification_person')
        if identification:
            identification = identification.strip()
            if len(identification) < 5:
                raise forms.ValidationError(
                    'El número de identificación debe tener al menos 5 caracteres.'
                )
        return identification

    def clean_first_name_1(self):
        """Validar y limpiar el primer nombre"""
        name = self.cleaned_data.get('first_name_1')
        if name:
            name = name.strip().title()
            if len(name) < 2:
                raise forms.ValidationError('El primer nombre debe tener al menos 2 caracteres.')
        return name

    def clean_last_name_1(self):
        """Validar y limpiar el primer apellido"""
        lastname = self.cleaned_data.get('last_name_1')
        if lastname:
            lastname = lastname.strip().title()
            if len(lastname) < 2:
                raise forms.ValidationError('El primer apellido debe tener al menos 2 caracteres.')
        return lastname

    def clean_date_birth(self):
        """Validar que la fecha de nacimiento sea coherente"""
        from datetime import date, timedelta
        date_birth = self.cleaned_data.get('date_birth')

        if date_birth:
            today = date.today()
            min_date = today - timedelta(days=365 * 120)  # Máximo 120 años
            max_date = today  # No puede ser fecha futura

            if date_birth > max_date:
                raise forms.ValidationError('La fecha de nacimiento no puede ser una fecha futura.')

            if date_birth < min_date:
                raise forms.ValidationError('La fecha de nacimiento no puede ser anterior a 120 años.')

        return date_birth

    def clean_cell_phone(self):
        """Validar formato de teléfono"""
        phone = self.cleaned_data.get('cell_phone')
        if phone:
            # Eliminar espacios y guiones
            phone = phone.replace(' ', '').replace('-', '')
            if not phone.isdigit():
                raise forms.ValidationError('El teléfono debe contener solo números.')
            if len(phone) < 10:
                raise forms.ValidationError('El teléfono debe tener al menos 10 dígitos.')
        return phone



class MaterialConstructionFamilyForm(forms.ModelForm):
    class Meta:
        model = MaterialConstructionFamilyCard
        fields = ['material_roof', 'material_floor', 'material_wall', 'number_families', 'condition_roof',
                  'condition_floor', 'condition_wall', 'number_families', 'number_people_bedrooms',
                  'home_ownership', 'kitchen_location', 'cooking_fuel', 'home_smoke', 'number_bedrooms',
                  'ventilation', 'lighting']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-MaterialConstruction'
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'control-label'

    material_roof = forms.ModelChoiceField(queryset=MaterialConstruction.objects.filter(roof=True),
                                           empty_label="Seleccione el Material del Techo",
                                           widget=forms.Select(attrs={'class': 'form-control'}),
                                           label="Material del Techo")

    material_floor = forms.ModelChoiceField(queryset=MaterialConstruction.objects.filter(floor=True),
                                            empty_label="Seleccione el Material del Piso",
                                            widget=forms.Select(attrs={'class': 'form-control text-'}),
                                            label="Material del Piso")

    material_wall = forms.ModelChoiceField(queryset=MaterialConstruction.objects.filter(wall=True),
                                           empty_label="Seleccione el Material de la Pared",
                                           widget=forms.Select(attrs={'class': 'form-control'}),
                                           label="Material de la Pared")

    number_families = forms.ChoiceField(label='Número de Familias',
                                         choices=[(1, '1'), (2, '2'), (3, '3 o más')],
                                         widget=forms.Select(attrs={'class': 'form-control',
                                                                  'placeholder': 'Número de Familias'}),)

    number_people_bedrooms = forms.ChoiceField(label='Número de Personas por Habitación',
                                               choices=[(1, '1'), (2, '2'), (3, '3 o más')],
                                               widget=forms.Select(attrs={'class': 'form-control',
                                                                        'placeholder': 'Número de Personas por Habitación'}),)

    condition_roof = forms.BooleanField(label="¿Techo Adecuado?", required=True,
                                        widget=forms.CheckboxInput(
                                            attrs={'class': 'form-check-input checkbox-vertical', 'placeholder': 'Estado del Techo'}),)

    condition_floor = forms.BooleanField(label="¿Piso Adecuado?", required=True,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-vertical', 'placeholder': 'Estado del Piso'}),)

    condition_wall = forms.BooleanField(label="¿Paredes Adecuadas?", required=True,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-vertical', 'placeholder': 'Estado de la Pared'}),)

    home_ownership = forms.ModelChoiceField(queryset=HomeOwnership.objects.all(),
                                            empty_label="Seleccione el Tipo de Propiedad",
                                            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de Propiedad'}),
                                            label="Tipo de Propiedad")

    kitchen_location = forms.ChoiceField(label='Ubicación de la Cocina',
                                         choices=[(1, 'Interior'), (2, 'Exterior')],
                                         widget=forms.Select(attrs={'class': 'form-control',
                                                                    'placeholder': 'Ubicación de la Cocina'}))

    cooking_fuel = forms.ModelChoiceField(queryset=CookingFuel.objects.all(),
                                           empty_label="Cocina con",
                                           widget=forms.Select(attrs={'class': 'form-control',
                                                                      'placeholder': 'Combustible de Cocina'}),
                                           label="Combustible de Cocina")

    home_smoke = forms.BooleanField(label="Humo en el Hogar", required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-vertical', 'placeholder': 'Humo en el Hogar'}),)

    number_bedrooms = forms.IntegerField(label='Número de Habitaciones', required=False, min_value=1, max_value=5,
                                         widget=forms.NumberInput(
                                             attrs={'class': 'form-control text-muted', 'placeholder': 'Número de Habitaciones'}),)

    ventilation = forms.BooleanField(label="Ventilación Adecuada?", required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-vertical', 'placeholder': 'Ventilación Adecuada?'}),)

    lighting = forms.BooleanField(label="Iluminación Adecuada?", required=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-vertical', 'placeholder': 'Iluminación Adecuada?'}),)



