from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date
from .models import *
from django_countries.widgets import CountrySelectWidget

class EstudiantesRegistroForm(UserCreationForm):
    class Meta:
        model = Estudiantes
        fields = ['nombre', 'apellido', 'email', 'dni', 'telefono', 'direccion', 'fecha_nacimiento', 'foto_perfil', 'nacionalidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nacionalidad': CountrySelectWidget(attrs={'class': 'form-control'})  # No es necesario agregarlo como CharField
        }

    # Validación para la fecha de nacimiento (debe ser mayor de 16 años)
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if not fecha_nacimiento:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad < 16:
            raise ValidationError("El estudiante debe tener al menos 16 años.")
        return fecha_nacimiento

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    # Validación personalizada para el DNI
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Estudiantes.objects.filter(dni=dni).exists():
            raise ValidationError("Ya existe un estudiante con este DNI.")
        return dni

    # Validación personalizada para el teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and (not telefono.startswith('+') or not telefono[1:].isdigit()):
            raise ValidationError("El número de teléfono debe estar en formato internacional, como +584147080725.")
        return telefono

    # Guardar usuario con contraseña encriptada
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.rol = 'Estudiante'  # Asegurar que el rol se mantenga como estudiante
        if commit:
            user.save()
        return user

class EstudiantesActualizacionForm(forms.ModelForm):
    class Meta:
        model = Estudiantes
        fields = ['nombre', 'apellido', 'email', 'dni', 'telefono', 'direccion', 'status' ,'foto_perfil', 'nacionalidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nacionalidad': CountrySelectWidget(attrs={'class': 'form-control'})
        }

    # Validación personalizada para el DNI
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Estudiantes.objects.filter(dni=dni).exclude(id=self.instance.id).exists():
            raise ValidationError("Ya existe un estudiante con este DNI.")
        return dni

    # Validación personalizada para el teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and (not telefono.startswith('+') or not telefono[1:].isdigit()):
            raise ValidationError("El número de teléfono debe estar en formato internacional, como +584147080725.")
        return telefono

    def save(self, commit=True):
        # Guardamos el objeto sin modificar la contraseña
        estudiante = super().save(commit=False)
        if commit:
            estudiante.save()
        return estudiante
    
class DocumentosEstudianteForm(forms.ModelForm):
    class Meta:
        model = DocumentosEstudiante
        fields = [
            'pasaporte', 'documento_identidad', 'antecedentes_penales', 'seguro_medico',
            'carta_inscripcion', 'recibo_pago', 'diploma_traducido', 'transcripcion_traducida',
            'carta_intencion', 'resumen_financiero', 'extracto_bancario'
        ]
        widgets = {
            'pasaporte': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'documento_identidad': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'antecedentes_penales': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'seguro_medico': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'carta_inscripcion': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'recibo_pago': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'diploma_traducido': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'transcripcion_traducida': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'carta_intencion': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'resumen_financiero': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
            'extracto_bancario': forms.ClearableFileInput(attrs={'class': 'form-control file-input'}),
        }