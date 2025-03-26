from django.urls import path
from . import views

urlpatterns = [
    path('', views.estudiantes, name='estudiantes'),
    path('listadoEstudiantes/', views.listaEstudiantes, name='lista_estudiantes'),
    path('agregarEstudiante/', views.agregarEstudiante, name='addEstudiante'),
    path('actualizarEstudiante/<id>/', views.actualizarEstudiante, name='actEstudiante'),
    path('eliminarEstudiante/<id>/', views.eliminarEstudiante, name='dltEstudiante'),
    path('verEstudiante/<id>/', views.mostrarEstudiante, name='verEstudiante'),
    path('subir_documentos/', views.subir_documentos, name='subir_documentos'),
    path('actualizar_documentos/<id>/', views.actualizar_documentos, name='actualizar_documentos'),
]
