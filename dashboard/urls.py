from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('error404/', views.error404, name='E404'), 
    path('buscar/', views.buscar, name='buscar'),   
    path('estudiantesDashboard/', views.estudiante_dashboard ,name='estudiante_dashboard')
]