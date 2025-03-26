from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estudiantesDashboard/', views.estudiante_dashboard ,name='estudiante_dashboard')
]