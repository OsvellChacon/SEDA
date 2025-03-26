from django.db import models
from usuarios.models import CustomUser

# Create your models here.
class Estudiantes(CustomUser): 
    rol = models.CharField(max_length=20, default='Estudiante')  # Agregamos max_length

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
