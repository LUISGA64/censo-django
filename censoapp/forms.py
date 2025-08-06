#from django.forms import ModelForm
#from django.forms import Field
from django import forms

from .models import FamilyCard, Person, DocumentType, Gender, SecuritySocial, Kinship, EducationLevel, CivilState, \
    Occupancy, Sidewalks, Organizations, Eps, Handicap, MaterialConstruction, MaterialConstructionFamilyCard, \
    HomeOwnership, CookingFuel
from .choices import zone
from crispy_forms.helper import FormHelper


class FormFamilyCard(forms.ModelForm):
    class Meta:
        model = FamilyCard
        fields = '__all__'
    # address_home = forms.CharField(label='Dirección Vivienda',  max_length=50, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Dirección Vivienda'}))

    sidewalk_home = forms.ModelChoiceField(queryset=Sidewalks.objects.all(), label_suffix=":",
                                           empty_label="Seleccione la vereda donde vive",
                                           widget=forms.Select(attrs={'class': 'form-control',
                                                                      'placeholder': 'Vereda'}),
                                           label="Vereda")
    latitude = forms.CharField(label='Latitud', required=False, max_length=15,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Latitud'}))

    longitude = forms.CharField(label='Longitud', required=False, max_length=15,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Longitud'}))

    zone = forms.ChoiceField(choices=zone, label="Zona",
                             widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Zona'}))

    organization = forms.ModelChoiceField(queryset=Organizations.objects.all(),
                                             empty_label="Seleccione el Resguardo",
                                             widget=forms.Select(attrs={'class': 'form-control',
                                                                        'placeholder': 'Resguardo'}),
                                             label="Resguardo Indígena")
    # family_card_number = forms.IntegerField(label='Número de Familia', disabled=True,
    #                                         widget=forms.NumberInput(attrs={
    #                                             'readonly': True,
    #                                         }),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-FamilyCard'
        self.helper.form_class = 'pl-6 pr-6 pb-6 pt-6'
        self.helper.label_class = 'control-label'
        # deshabilitar field family_card_number
        self.fields['family_card_number'].required = False
        self.fields['family_card_number'].widget.attrs['readonly'] = True



class FormPerson(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name_1', 'first_name_2', 'last_name_1', 'last_name_2', 'document_type', 'identification_person',
                  'gender', 'date_birth', 'kinship', 'social_insurance', 'eps', 'handicap',
                  'education_level', 'civil_state', 'occupation', 'cell_phone', 'personal_email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-Person'
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'control-label'

    # Primer Nombre
    first_name_1 = forms.CharField(label='Primer Nombre', max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control input-group', 'placeholder': 'Primer Nombre'}))

    # Segundo Nombre
    first_name_2 = forms.CharField(label='Segundo Nombre', max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'col-md-3', 'placeholder': 'Segundo Nombre'}))

    # Primer Apellido
    last_name_1 = forms.CharField(label='Primer Apellido', max_length=30,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Primer Apellido'}))

    # Segundo Apellido
    last_name_2 = forms.CharField(label='Segundo Apellido', max_length=30, required=False,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Segundo Apellido'}))

    # Número Teléfonico
    cell_phone = forms.CharField(label='Teléfono Móvil', max_length=15, required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': '000-000-0000'}))

    # Correo Personal
    personal_email = forms.EmailField(label='Correo Personal', max_length=50, required=False,
                                      widget=forms.EmailInput(
                                          attrs={'class': 'form-control', 'placeholder': 'mi_correo@censoweb.com'}))

    # Identificación de la persona
    identification_person = forms.CharField(label='Identificación', max_length=15,
                                            widget=forms.TextInput(
                                                attrs={'class': 'form-control', 'placeholder': 'Identificación'}))

    # Tipo de Documento
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(),
                                           empty_label="Seleccione el Tipo de Documento",
                                           widget=forms.Select(attrs={'class': 'form-control',
                                                                      'placeholder': 'Tipo de Documento'}),
                                           label="Tipo de Documento")
    # Género
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Seleccione el Género",
                                       widget=forms.Select(
                                           attrs={'class': 'form-control', 'placeholder': 'Género'}),
                                       label="Género")

    # Fecha de Nacimiento
    date_birth = forms.DateField(label='Fecha de Nacimiento',
                                 widget=forms.DateInput(format='%d-%m-%Y',
                                                        attrs={'class': 'form-control',
                                                               'placeholder': 'Fecha de Nacimiento',
                                                               'type': 'date'}))

    # Tipo de Afiliación
    social_insurance = forms.ModelChoiceField(queryset=SecuritySocial.objects.all(),
                                              empty_label="Seleccione Afiliación",
                                              widget=forms.Select(attrs={'class': 'form-control',
                                                                         'placeholder': 'Tipo Afiliación'}),
                                              label="Tipo Afiliación")

    # Empresa de Afiliación
    eps = forms.ModelChoiceField(queryset=Eps.objects.all(),
                                 empty_label="Seleccione EPS",
                                 widget=forms.Select(
                                     attrs={'class': 'form-control', 'placeholder': 'EPS'}),
                                 label="EPS")

    # Parentesco
    kinship = forms.ModelChoiceField(queryset=Kinship.objects.all(), empty_label="Seleccione Parentesco",
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Parentesco'}),
                                        label="Parentesco")

    # Tipo de Discapacidad
    # handicap = forms.ChoiceField(choices=handicap,
    #                              widget=forms.Select(
    #                                  attrs={'class': 'form-control', 'placeholder': 'Discapacidad'}),
    #                              label="Discapacidad")
    handicap = forms.ModelChoiceField(queryset=Handicap.objects.all(), empty_label="Seleccione Discapacidad",
                                      widget=forms.Select(attrs={'class': 'form-control',
                                                          'placeholder': 'Discapacidad'},
                                                          ),
                                        label="Discapacidad")

    # Nivel Educativo
    education_level = forms.ModelChoiceField(queryset=EducationLevel.objects.all(),
                                             empty_label="Seleccione Nivel de Educación",
                                             widget=forms.Select(attrs={'class': 'form-control',
                                                                        'placeholder': 'Nivel de Educación'}),
                                             label="Nivel de Educación")

    # Estado Civil
    civil_state = forms.ModelChoiceField(queryset=CivilState.objects.all(),
                                         empty_label="Seleccione Estado Civil",
                                         widget=forms.Select(attrs={'class': 'form-control',
                                                                    'placeholder': 'Estado Civil'}),
                                         label="Estado Civil")

    # Ocupación
    occupation = forms.ModelChoiceField(queryset=Occupancy.objects.all(), empty_label="Seleccione Ocupación",
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Ocupación'}),
                                        label="Ocupación")




class MaterialConstructionFamilyForm(forms.ModelForm):
    class Meta:
        model = MaterialConstructionFamilyCard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-MaterialConstruction'
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'control-label'

    material_roof = forms.ModelChoiceField(queryset=MaterialConstruction.objects.filter(roof=True),
                                           empty_label="Seleccione el Material del Techo",
                                           widget=forms.Select(attrs={'class': 'form-control'}))

    material_floor = forms.ModelChoiceField(queryset=MaterialConstruction.objects.filter(floor=True),
                                            empty_label="Seleccione el Material del Piso",
                                            widget=forms.Select(attrs={'class': 'form-control'}),
                                            label="Material del Piso")

    material_wall = forms.ModelChoiceField(queryset=MaterialConstruction.objects.filter(wall=True),
                                           empty_label="Seleccione el Material de la Pared",
                                           widget=forms.Select(attrs={'class': 'form-control'}),
                                           label="Material de la Pared")

    number_families = forms.ChoiceField(label='Número de Familias',
                                         choices=[(1, '1'), (2, '2'), (3, '3')],
                                         widget=forms.Select(attrs={'class': 'form-control',
                                                                  'placeholder': 'Número de Familias'}),)

    condition_roof = forms.BooleanField(label="Estado del Techo", required=True,
                                        widget=forms.Select(attrs={'class': 'form-control form-check-input', 'placeholder': 'Estado del Techo'}),)

    condition_floor = forms.BooleanField(label="Estado del Piso", required=True,
                                         widget=forms.Select(attrs={'class': 'form-control form-check-input', 'placeholder': 'Estado del Piso'}),)

    condition_wall = forms.BooleanField(label="Estado de la Pared", required=True,
                                        widget=forms.Select(attrs={'class': 'form-control form-check-input', 'placeholder': 'Estado de la Pared'}),)

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
                                    widget=forms.Select(attrs={'class': 'form-control form-check-input', 'placeholder': 'Humo en el Hogar'}),)

    number_bedrooms = forms.IntegerField(label='Número de Habitaciones', required=False,
                                         widget=forms.NumberInput(
                                             attrs={'class': 'form-control', 'placeholder': 'Número de Habitaciones'}),)

    ventilation = forms.BooleanField(label="Ventilación Adecuada?", required=False,
                                     widget=forms.Select(attrs={'class': 'form-control form-check-input', 'placeholder': 'Ventilación Adecuada?'}),)

    lighting = forms.BooleanField(label="Iluminación Adecuada?", required=False,
                                  widget=forms.Select(attrs={'class': 'form-control form-check-input', 'placeholder': 'Iluminación Adecuada?'}),)



