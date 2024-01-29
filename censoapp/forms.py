from django import forms
from .models import FamilyCard, Person, DocumentType, Gender, SecuritySocial, Kinship, EducationLevel, CivilState, \
    Occupancy, Sidewalks, Organizations
from .choices import zone, handicap, ethnic_group

from django import forms


class FormFamilyCard(forms.ModelForm):
    class Meta:
        model = FamilyCard
        fields = ['address_home', 'sidewalk_home', 'latitude', 'longitude', 'zone', 'organization_id']
        widgets = {
            'address_home': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección Vivienda'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitud'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Longitud'}),
            'zone': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Zona'}),

        }


class FormPerson(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name_1', 'first_name_2', 'last_name_1', 'last_name_2', 'identification_person',
                  'document_type', 'cell_phone', 'personal_email', 'gender_id', 'date_birth', 'social_insurance',
                  'kinship_id', 'handicap', 'education_level', 'civil_state', 'occupation']

        widgets = {'date_birth': forms.DateInput(format='%d-%m-%Y',
                                                 attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                        'type': 'date'}),
                   'personal_email': forms.EmailInput(
                       attrs={'class': 'form-control', 'placeholder': 'Correo Personal', 'type': 'email'}),
                   'social_insurance': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo Afiliación'}),
                   }
