from django.urls import path,include
from core.formulario.views import *
urlpatterns = [
    path('',formulario,name='formulario'),
    path('reportar/',respuesta,name='reportar_seleccion'),
    path('solicitud/',obtener_resultados),
    path('procesar_solicitud/',procesar_solicitud,name='procesar_solicitud'),
    path('resultados/',resultados,name='resultados'),
    path('delete_results',delete_results,name='delete_results')
]
