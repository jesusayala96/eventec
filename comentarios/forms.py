from django import forms

class comentario_form(forms.Form):
    Comentario=forms.CharField(widget=forms.Textarea)