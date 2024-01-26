from django import forms
from .models import FamilyCard, Person, DocumentType, Gender, SecuritySocial, Kinship, EducationLevel, CivilState, \
    Occupancy, Sidewalks, Organizations
from .choices import zone, handicap, ethnic_group

from django import forms


# class FormFamilyCard(forms.Form):
#     address_home = forms.CharField(max_length=100, label='Dirección',
#                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#     sidewalk_home = forms.ModelChoiceField(queryset=Sidewalks.objects.all(), label='Vereda',
#                                            empty_label="Seleccione...",
#                                            widget=forms.Select(attrs={'class': 'form-control'}))
#
#     latitude = forms.CharField(max_length=15, label='Latitud',
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.123456'}))
#
#     longitude = forms.CharField(max_length=15, label='Longitud',
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '-12.123456'}))
#
#     zone = forms.ChoiceField(choices=zone, label='Zona', widget=forms.Select(attrs={'class': 'form-control'}))
#
#     organization_id = forms.ModelChoiceField(queryset=Organizations.objects.all(), label='Resguardo Indígena',
#                                              empty_label="Seleccione...",
#                                              widget=forms.Select(attrs={'class': 'form-control'}))

    # formulario de persona
    # first_name_1 = forms.CharField(max_length=50, label='Primer Nombre',
    #                                widget=forms.TextInput(
    #                                    attrs={'class': 'form-control', 'placeholder': 'Primer Nombre'}))
    #
    # first_name_2 = forms.CharField(max_length=50, label='Segundo Nombre', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Segundo Nombre'}))
    #
    # last_name_1 = forms.CharField(max_length=50, label='Primer Apellido', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Primer Apellido'}))
    #
    # last_name_2 = forms.CharField(max_length=50, label='Segundo Apellido', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Segundo Apellido'}))
    #
    # identification_person = forms.CharField(max_length=15, label='Número de identificación', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}))
    #
    # document_type_id = forms.ModelChoiceField(queryset=DocumentType.objects.all(), label='Tipo de documento',
    #                                           empty_label="Seleccione...", widget=forms.Select(
    #         attrs={'class': 'form-control'}))
    #
    # cell_phone = forms.CharField(max_length=10, label='Celular', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Celular'}))
    #
    # personal_email = forms.EmailField(max_length=50, label='Correo personal', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Correo personal'}))
    #
    # gender_id = forms.ModelChoiceField(queryset=Gender.objects.all(), label='Género', empty_label="Seleccione...",
    #                                    widget=forms.Select(attrs={'class': 'form-control'}))
    #
    # birth_date = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento'}))
    #
    # social_insurance = forms.ModelChoiceField(queryset=SecuritySocial.objects.all(), label='Eps',
    #                                           empty_label="Seleccione...", widget=forms.Select(
    #         attrs={'class': 'form-control'}))
    #
    # kinship_id = forms.ModelChoiceField(queryset=Kinship.objects.all(), label='Parentesco',
    #                                     empty_label="Seleccione...", widget=forms.Select(
    #         attrs={'class': 'form-control'}))
    #
    # education_level_id = forms.ModelChoiceField(queryset=EducationLevel.objects.all(), widget=forms.Select(
    #     attrs={'class': 'form-control'}), label='Nivel educativo', empty_label="Seleccione...")
    #
    # civil_state_id = forms.ModelChoiceField(queryset=CivilState.objects.all(), label='Estado civil',
    #                                         empty_label="Seleccione...", widget=forms.Select(
    #         attrs={'class': 'form-control'}))
    #
    # occupation_id = forms.ModelChoiceField(queryset=Occupancy.objects.all(), label='Ocupación',
    #                                        empty_label="Seleccione...", widget=forms.Select(
    #         attrs={'class': 'form-control'}))
    #
    # handicap = forms.ChoiceField(choices=handicap, label='Discapacidad', widget=forms.Select(
    #     attrs={'class': 'form-control'}))


# class FormPerson(forms.Form):
#     first_name_1 = forms.CharField(max_length=50, label='Primer Nombre',
#                                    widget=forms.TextInput(
#                                        attrs={'class': 'form-control', 'placeholder': 'Primer Nombre'}))
#
#     first_name_2 = forms.CharField(max_length=50, label='Segundo Nombre', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Segundo Nombre'}))
#
#     last_name_1 = forms.CharField(max_length=50, label='Primer Apellido', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Primer Apellido'}))
#
#     last_name_2 = forms.CharField(max_length=50, label='Segundo Apellido', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Segundo Apellido'}))
#
#     identification_person = forms.CharField(max_length=15, label='Número de identificación', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Número de identificación'}))
#
#     document_type_id = forms.ModelChoiceField(queryset=DocumentType.objects.all(), label='Tipo de documento',
#                                               empty_label="Seleccione...", widget=forms.Select(
#             attrs={'class': 'form-control'}))
#
#     cell_phone = forms.CharField(max_length=10, label='Celular', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Celular'}))
#
#     personal_email = forms.EmailField(max_length=50, label='Correo personal', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Correo personal'}))
#
#     gender_id = forms.ModelChoiceField(queryset=Gender.objects.all(), label='Género', empty_label="Seleccione...",
#                                        widget=forms.Select(attrs={'class': 'form-control'}))
#
#     birth_date = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(
#         attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento'}))
#
#     social_insurance = forms.ModelChoiceField(queryset=SecuritySocial.objects.all(), label='Eps',
#                                               empty_label="Seleccione...", widget=forms.Select(
#             attrs={'class': 'form-control'}))
#
#     kinship_id = forms.ModelChoiceField(queryset=Kinship.objects.all(), label='Parentesco',
#                                         empty_label="Seleccione...", widget=forms.Select(
#             attrs={'class': 'form-control'}))
#
#     education_level_id = forms.ModelChoiceField(queryset=EducationLevel.objects.all(), widget=forms.Select(
#         attrs={'class': 'form-control'}), label='Nivel educativo', empty_label="Seleccione...")
#
#     civil_state_id = forms.ModelChoiceField(queryset=CivilState.objects.all(), label='Estado civil',
#                                             empty_label="Seleccione...", widget=forms.Select(
#             attrs={'class': 'form-control'}))
#
#     occupation_id = forms.ModelChoiceField(queryset=Occupancy.objects.all(), label='Ocupación',
#                                            empty_label="Seleccione...", widget=forms.Select(
#             attrs={'class': 'form-control'}))
#
#     handicap = forms.ChoiceField(choices=handicap, label='Discapacidad', widget=forms.Select(
#         attrs={'class': 'form-control'}))

class FormFamilyCard(forms.ModelForm):
    class Meta:
        model = FamilyCard
        fields = '__all__'


class FormPerson(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
