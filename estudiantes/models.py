from django.db import models
from django_countries.fields import CountryField
from usuarios.models import CustomUser

class Estudiantes(CustomUser): 
    rol = models.CharField(max_length=20, default='Estudiante')
    nacionalidad = CountryField(blank=True, null=True)  # Campo de país

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nacionalidad})"
