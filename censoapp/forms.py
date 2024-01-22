from django import forms
from .models import FamilyCard, Person
from .choices import zone, handicap, ethnic_group


class FormFamilyCard(forms.ModelForm):
    # address = forms.CharField(label='Dirección', max_length=100, required=True)
    # sidewalk = forms.CharField(label='Vereda', max_length=100, required=True)
    # latitude = forms.CharField(label='Latitud', max_length=100, required=False)
    # longitude = forms.CharField(label='Longitud', max_length=100, required=False)
    # zone = forms.ChoiceField(label='Zona', choices=zone.items(), required=True)
    # organization = forms.CharField(label='Organización', max_length=100, required=True)
    class Meta:
        model = FamilyCard
        fields = ['address', 'sidewalk', 'latitude', 'longitude', 'zone', 'organization']
        labels = {
            'address': 'Dirección',
            'sidewalk': 'Vereda',
            'latitude': 'Latitud',
            'longitude': 'Longitud',
            'zone': 'Zona',
            'organization': 'Organización'
        }
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'sidewalk': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.ChoiceField(choices=zone.items(), attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'})
        }


class FormPerson(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name_1', 'first_name_2', 'last_name_1', 'last_name_2', 'document_type',
                  'identification_person', 'cell_phone', 'personal_email', 'gender_id', 'date_birth',
                  'social_insurance', 'kinship_id', 'handicap', 'education_level', 'civil_state', 'occupation']
        labels = {
            'first_name_1': 'Primer Nombre',
            'first_name_2': 'Segundo Nombre',
            'last_name_1': 'Primer Apellido',
            'last_name_2': 'Segundo Apellido',
            'document_type': 'Tipo de Documento',
            'identification_person': 'Número de Documento',
            'cell_phone': 'Celular',
            'personal_email': 'Correo Personal',
            'gender_id': 'Género',
            'date_birth': 'Fecha de Nacimiento',
            'social_insurance': 'Seguridad Social',
            'kinship_id': 'Parentesco',
            'handicap': 'Capacidades Diversas',
            'education_level': 'Nivel Educativo',
            'civil_state': 'Estado Civil',
            'occupation': 'Ocupación'
        }
        widgets = {
            'first_name_1': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name_2': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_1': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_2': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'identification_person': forms.TextInput(attrs={'class': 'form-control'}),
            'cell_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'personal_email': forms.TextInput(attrs={'class': 'form-control'}),
            'gender_id': forms.Select(attrs={'class': 'form-control'}),
            'date_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'social_insurance': forms.Select(attrs={'class': 'form-control'}),
            'kinship_id': forms.Select(attrs={'class': 'form-control'}),
            'handicap': forms.ChoiceField(choices=handicap, attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'civil_state': forms.Select(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'})
        }

