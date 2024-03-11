from django.contrib import admin
from .models import comprar, sugerencia, historial, usuario_historial

# Register your models here.

admin.site.register(comprar)
admin.site.register(sugerencia)
admin.site.register(historial)
admin.site.register(usuario_historial)