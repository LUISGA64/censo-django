from django import forms
from .models import FamilyCard, Person, DocumentType, Gender, SecuritySocial, Kinship, EducationLevel, CivilState, \
    Occupancy, Sidewalks, Organizations
from .choices import zone, handicap, ethnic_group

from django import forms


class FormFamilyCard(forms.Form):
    address_home = forms.CharField(max_length=100, label='Dirección de residencia',
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'})),
    sidewalk_home = forms.ModelChoiceField(
        queryset=Sidewalks.objects.all(),
        empty_label="Seleccione una vereda",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Vereda'})
    ),
    latitude = forms.CharField(max_length=15, label='Latitud',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitud'})),
    longitude = forms.CharField(max_length=15, label='Longitud',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Longitud'})),
    zone = forms.ChoiceField(choices=zone, label='Zona',
                             widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Zona',
                                                        'required': 'required', 'autofocus': 'autofocus',
                                                        'id': 'zone'})),
    organization_id = forms.ModelChoiceField(
        queryset=Organizations.objects.all(),
        empty_label="Seleccione una Organización",
        label='Resguardo Indígena',
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Organización'})
    )


class FormPerson(forms.Form):
    first_name = forms.CharField(max_length=50, label='Nombres', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombres'})),
    last_name = forms.CharField(max_length=50, label='Apellidos', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Apellidos'})),
    document_type_id = forms.ModelChoiceField(queryset=DocumentType.objects.all(),
                                              empty_label="Seleccione un tipo de documento",
                                              widget=forms.Select(attrs={'class': 'form-control'})),
    cell_phone = forms.CharField(max_length=10, label='Celular', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Celular'})),
    personal_email = forms.EmailField(max_length=50, label='Correo personal', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Correo personal'})),
    gender_id = forms.ModelChoiceField(
        queryset=Gender.objects.all(), empty_label="Seleccione un género", widget=forms.Select(
            attrs={'class': 'form-control'})),
    birth_date = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento'})),
    social_insurance = forms.ModelChoiceField(
        queryset=SecuritySocial.objects.all(), empty_label="Seleccione una EPS", widget=forms.Select(
            attrs={'class': 'form-control'})),
    kinship_id = forms.ModelChoiceField(
        queryset=Kinship.objects.all(), empty_label="Seleccione un parentesco", widget=forms.Select(
            attrs={'class': 'form-control'})),
    education_level_id = forms.ModelChoiceField(
        queryset=EducationLevel.objects.all(), empty_label="Seleccione un nivel de educación", widget=forms.Select(
            attrs={'class': 'form-control'})),
    civil_state_id = forms.ModelChoiceField(
        queryset=CivilState.objects.all(), empty_label="Seleccione un estado civil", widget=forms.Select(
            attrs={'class': 'form-control'})),
    occupation_id = forms.ModelChoiceField(
        queryset=Occupancy.objects.all(), empty_label="Seleccione una ocupación", widget=forms.Select(
            attrs={'class': 'form-control'})),
    handicap = forms.ChoiceField(choices=handicap, label='Discapacidad', widget=forms.Select(
        attrs={'class': 'form-control'}))
