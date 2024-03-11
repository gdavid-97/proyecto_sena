from django import forms
from .models import comprar, sugerencia

class forms_compra(forms.ModelForm):
    
    class Meta:
        model = comprar
        fields = [
            'nombre_completo',
            'correo_electronico',
            'telefono',
            'direccion',
            'numero_de_tarjeta',
            'fecha_de_expedicion',
            'ccv',
        ]

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