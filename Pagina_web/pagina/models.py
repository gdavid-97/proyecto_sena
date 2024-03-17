from django.db import models
from django.contrib.auth.models import User

class sugerencia(models.Model):
    nombre_completo= models.CharField(max_length=100)
    correo_electronico= models.CharField(max_length=100)
    telefono= models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    mensaje = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_completo

class historial(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    busqueda = models.CharField(max_length=255, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
class usuario_historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    historial = models.ForeignKey(historial, on_delete=models.CASCADE)