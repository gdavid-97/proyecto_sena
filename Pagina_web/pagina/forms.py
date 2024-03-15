from django import forms
from .models import  sugerencia, historial

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
            'historial',
            'fecha',
            'usuario'
        }

class forms_usuario_historial(forms.ModelForm):

    class Meta:
        fields = {
            'usuario',
            'historial'
        }