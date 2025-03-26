import os
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django_countries.fields import CountryField
from usuarios.models import CustomUser
from auditlog.registry import auditlog

# Función para validar formato y tamaño de archivo
def validar_archivo(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError("Formato de archivo no válido. Solo se permiten PDF, JPG y PNG.")
    if value.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("El archivo no debe superar los 5MB.")

# Función para generar un código único de inscripción
def generar_codigo_inscripcion(dni):
    unique_part = uuid.uuid4().hex[:5].upper()  # 5 caracteres aleatorios
    return f"{dni}-{unique_part}"

class Estudiantes(CustomUser): 
    rol = models.CharField(max_length=20, default='Estudiante')
    nacionalidad = CountryField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nacionalidad})"
    
class EstadoInscripcion(models.TextChoices):
    EN_REVISION = "En Revisión", "En Revisión"
    APROBADO = "Aprobado", "Aprobado"
    RECHAZADO = "Rechazado", "Rechazado"

class DocumentosEstudiante(models.Model):
    estudiante = models.OneToOneField(Estudiantes, on_delete=models.CASCADE, related_name="documentos")
    codigo_inscripcion = models.CharField(max_length=15, unique=True, blank=True, editable=False)

    # Documentos requeridos
    pasaporte = models.FileField(upload_to='documentos_estudiantes/pasaporte/', blank=True, null=True, validators=[validar_archivo])
    documento_identidad = models.FileField(upload_to='documentos_estudiantes/identidad/', blank=True, null=True, validators=[validar_archivo])
    antecedentes_penales = models.FileField(upload_to='documentos_estudiantes/antecedentes/', blank=True, null=True, validators=[validar_archivo])
    seguro_medico = models.FileField(upload_to='documentos_estudiantes/seguro/', blank=True, null=True, validators=[validar_archivo])
    carta_inscripcion = models.FileField(upload_to='documentos_estudiantes/carta_inscripcion/', blank=True, null=True, validators=[validar_archivo])
    recibo_pago = models.FileField(upload_to='documentos_estudiantes/pago/', blank=True, null=True, validators=[validar_archivo])
    diploma_traducido = models.FileField(upload_to='documentos_estudiantes/diploma/', blank=True, null=True, validators=[validar_archivo])
    transcripcion_traducida = models.FileField(upload_to='documentos_estudiantes/transcripcion/', blank=True, null=True, validators=[validar_archivo])
    carta_intencion = models.FileField(upload_to='documentos_estudiantes/carta_intencion/', blank=True, null=True, validators=[validar_archivo])
    resumen_financiero = models.FileField(upload_to='documentos_estudiantes/resumen_financiero/', blank=True, null=True, validators=[validar_archivo])
    extracto_bancario = models.FileField(upload_to='documentos_estudiantes/extracto_bancario/', blank=True, null=True, validators=[validar_archivo])

    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    estado_inscripcion = models.CharField(
        max_length=20, 
        choices=EstadoInscripcion.choices, 
        default=EstadoInscripcion.EN_REVISION
    )

    def save(self, *args, **kwargs):
        if not self.codigo_inscripcion:
            self.codigo_inscripcion = generar_codigo_inscripcion(self.estudiante.dni)
        super().save(*args, **kwargs)

    def calcular_progreso(self):
        """
        Calcula el porcentaje de documentos subidos.
        """
        total_documentos = 11  # Número total de documentos requeridos
        documentos_subidos = sum([
            bool(self.pasaporte),
            bool(self.documento_identidad),
            bool(self.antecedentes_penales),
            bool(self.seguro_medico),
            bool(self.carta_inscripcion),
            bool(self.recibo_pago),
            bool(self.diploma_traducido),
            bool(self.transcripcion_traducida),
            bool(self.carta_intencion),
            bool(self.resumen_financiero),
            bool(self.extracto_bancario),
        ])
        return int((documentos_subidos / total_documentos) * 100)

    def __str__(self):
        return f"Documentos de {self.estudiante.nombre} {self.estudiante.apellido}"

auditlog.register(Estudiantes)
auditlog.register(DocumentosEstudiante)