from django import forms
from .models import  sugerencia, historial, usuario_historial

class forms_sugerencia(forms.ModelForm):
    
    class Meta:
        model = sugerencia
        fields = [
            'nombre_completo',
            'correo_electronico',
            'telefono',
            'direccion',
            'mensaje',
        ]

class forms_historial(forms.ModelForm):

    class Meta:
        model=historial
        fields = {
            'busqueda',
            'usuario'
        }

class forms_usuario_historial(forms.ModelForm):

    class Meta:
        model = usuario_historial
        fields = {
            'usuario',
            'historial'
        }