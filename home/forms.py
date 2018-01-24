from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario, Evento, Imagenes
from django.contrib.admin import widgets
from datetime import date
from django.core.validators import RegexValidator

class SignUpForm_Alumno(UserCreationForm):
    Apellido_Materno = forms.CharField(max_length=30, required=False, help_text='Optional.',validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$')])
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    Direccion = forms.CharField(max_length=40,required=False,validators=[RegexValidator(r'^.*$',message='Ingresa una direccion valida')])
    NumControl = forms.CharField(required=False,max_length=8, validators=[RegexValidator(r'^\d{8}$',message='Ingresa un numero de control valido')])
    Telefono =  forms.CharField(required=False,max_length=10, validators=[RegexValidator(r'^[2-9]{2}\d{8}$',message='Ingresa un numero telefonico valido')])

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','Apellido_Materno',  'NumControl', 'Direccion', 'Telefono', 'email', 'password1', 'password2' )

class SignUpForm_Externo(UserCreationForm):
	Apellido_Materno = forms.CharField(max_length=30, required=False, help_text='Optional.',validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa un apellido valido')])
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	Direccion = forms.CharField(max_length=40,required=False,validators=[RegexValidator(r'^.*$',message='Ingresa una direccion valida')])
	Telefono = forms.CharField( required=False,max_length=10, validators=[RegexValidator(r'^[2-9]{2}\d{8}$',message='Ingresa un numero telefonico valido')])
	class Meta:
		model = User
		fields = ('username', 'first_name','last_name','Apellido_Materno', 'Direccion', 'Telefono', 'email', 'password1', 'password2' )

class SignUpForm_Staff(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2' )

class Crear_Evento_Form(forms.ModelForm):
    class Meta:
        model=Evento
        fields={'Titulo','DescripcionL','DescripcionC','Categorias','Tipos','Fecha','Hora'}
        widgets = {
            'Fecha': forms.DateInput(attrs={'type':'date'}),
        }

class SignUpForm_Usuario(UserCreationForm):
	Apellido_Materno = forms.CharField(max_length=30, required=False, help_text='Optional.',validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa un apellido valido')])
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	Direccion = forms.CharField(max_length=40,required=False,validators=[RegexValidator(r'^.*$',message='Ingresa una direccion valida')])
	NumControl = forms.CharField(required=False,max_length=8, validators=[RegexValidator(r'^\d{8}$',message='Ingresa un numero de control valido')])
	Telefono = forms.CharField( required=False,max_length=10, validators=[RegexValidator(r'^[2-9]{2}\d{8}$',message='Ingresa un numero telefonico valido')])
	tipo_opciones=(('A','Alumno'),('B','Admin'),('C','Externo'),('D','Interno'))
	Tipo = forms.ChoiceField(choices=tipo_opciones, required=True)
	class Meta:
		model = User
		fields = ('Tipo','username', 'first_name','last_name','Apellido_Materno',  'NumControl', 'Direccion', 'Telefono', 'email', 'password1', 'password2' )



class Imagen_Form(forms.ModelForm):
    class Meta:
        model=Imagenes
        fields={'Imagen'}