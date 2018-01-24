from django import forms
from django.core.validators import RegexValidator

class TomarAsistencia_form(forms.Form):
    Correo=forms.EmailField(max_length=254)
    Nombre = forms.CharField(max_length=40,required=False,validators=[RegexValidator(r'^[A-Z]{1}[a-z]{1,30}[- ]{0,1}$',message='Ingresa un nombre valido')])
    Escuela=forms.CharField(max_length=40,required=False,validators=[RegexValidator(r'^[A-Z]{1}[a-z]{1,30}[- ]{0,1}$',message='Ingresa una escuela valido')])