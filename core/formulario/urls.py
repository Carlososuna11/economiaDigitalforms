from django.urls import path,include
from core.formulario.views import *
urlpatterns = [
    path('',formulario,name='formulario'),
    path('reportar/',respuesta,name='reportar_seleccion')   
]
