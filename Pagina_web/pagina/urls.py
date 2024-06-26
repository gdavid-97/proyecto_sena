from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name="home"),
    path('contacto', views.acerca, name="contacto"),
    path('crear_cuenta', views.crear_cuenta, name="crear_cuenta"),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('sugerencias', views.sugerencia, name="sugerencias"),
    path('logout', views.cerrar_sesion, name="logout"),
    path('check/<str:nombre_usuario>/<int:clave>', views.verificar_usuario, name="check"),
    path('historial/<str:nombre_usuario>/<int:clave>/<str:informacion>', views.agregar_historial, name="agregar_historial"),
    path('crud/', views.crud, name="crud"),
    path('usuario/', views.usuario, name="usuario"),
    path('chat', views.chat, name="chat")
]
