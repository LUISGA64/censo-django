from django import forms


zone = {1: 'Rural', 2: 'Urbana'}


class FormFamilyCard(forms.Form):
    address = forms.CharField(label='Dirección', max_length=100, required=True)
    sidewalk = forms.CharField(label='Vereda', max_length=100, required=True)
    latitude = forms.CharField(label='Latitud', max_length=100, required=False)
    longitude = forms.CharField(label='Longitud', max_length=100, required=False)
    zone = forms.ChoiceField(label='Zona', choices=zone.items(), required=True)