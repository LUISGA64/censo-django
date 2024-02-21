from django import forms
from .models import FamilyCard, Person, DocumentType, Gender, SecuritySocial, Kinship, EducationLevel, CivilState, \
    Occupancy, Sidewalks, Organizations, Eps
from .choices import zone, handicap, ethnic_group
from crispy_forms.helper import FormHelper

from django import forms


class FormFamilyCard(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-FamilyCard'
        self.helper.form_class = 'pl-6 pr-6 pb-6 pt-6'
        self.helper.label_class = 'control-label'

    address_home = forms.CharField(label='Dirección Vivienda', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Dirección Vivienda'}))
    sidewalk_home = forms.ModelChoiceField(queryset=Sidewalks.objects.all(),
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

    organization_id = forms.ModelChoiceField(queryset=Organizations.objects.all(),
                                             empty_label="Seleccione el Resguardo",
                                             widget=forms.Select(attrs={'class': 'form-control',
                                                                        'placeholder': 'Resguardo'}),
                                             label="Resguardo Indígena")


class FormPerson(forms.Form):

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
                                     attrs={'class': 'form-control', 'placeholder': 'Teléfono Móvil'}))

    # Correo Personal
    personal_email = forms.EmailField(label='Correo Personal', max_length=50, required=False,
                                      widget=forms.EmailInput(
                                          attrs={'class': 'form-control', 'placeholder': 'Correo Personal'}))

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
    gender_id = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Seleccione el Género",
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
    kinship_id = forms.ModelChoiceField(queryset=Kinship.objects.all(), empty_label="Seleccione Parentesco",
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Parentesco'}),
                                        label="Parentesco")

    # Tipo de Discapacidad
    handicap = forms.ChoiceField(choices=handicap,
                                 widget=forms.Select(
                                     attrs={'class': 'form-control', 'placeholder': 'Discapacidad'}),
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



