from django.db import models
from django.contrib.auth.models import User

class comprar(models.Model):
    nombre_completo= models.CharField(max_length=100)
    correo_electronico= models.CharField(max_length=100)
    telefono= models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    numero_de_tarjeta= models.CharField(max_length=100)
    fecha_de_expedicion= models.CharField(max_length=100)
    ccv= models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_completo

class sugerencia(models.Model):
    nombre_completo= models.CharField(max_length=100)
    correo_electronico= models.CharField(max_length=100)
    telefono= models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    mensaje = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_completo

class historial(models.Model):
    historial= models.CharField(max_length=400)
    fecha = models.DateField(max_length=20)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha