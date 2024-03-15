from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name="home"),
    path('contacto', views.acerca, name="contacto"),
    path('crear_cuenta', views.crear_cuenta, name="crear_cuenta"),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('sugerencias', views.sugerencia, name="sugerencias"),
    path('logout', views.cerrar_sesion, name="logout"),
    path('check/<str:username>/<int:password>', views.verificar_usuario, name="check"),
    path('historial/<str:data>', views.add_history, name="add_historial"),
    path('crud/', views.crud, name="crud")
]
