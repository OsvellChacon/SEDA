from django import forms
from django.core.exceptions import ValidationError
from collections import OrderedDict
from datetime import date, datetime
from .models import CustomUser, Cargo

# Formulario para cargos
class CargosFrm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'


# Formulario para crear empleados
class EmpleadosFrm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = [
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'date_joined',
        ]
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'dni': {'unique': "Este DNI ya está registrado."},
            'email': {'invalid': "Introduce un correo electrónico válido."},
        }

    # Validación personalizada para DNI
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if CustomUser.objects.filter(dni=dni).exclude(id=self.instance.id).exists():
            raise ValidationError("Ya existe una persona con este DNI.")
        return dni

    # Validación personalizada para teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Permitir formato internacional como +584147080725
            if not telefono.startswith('+') or not telefono[1:].isdigit():
                raise ValidationError("El número de teléfono debe estar en formato internacional, como +584147080725.")
        return telefono


    # Validación personalizada para fecha de nacimiento
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if not fecha_nacimiento:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad < 18:
            raise ValidationError("El empleado debe tener al menos 18 años.")
        
        # Convertir la fecha a un formato adecuado si llega como cadena
        if isinstance(fecha_nacimiento, str):
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        
        return fecha_nacimiento

    # Sobrescribir el método save para manejar el hash de la contraseña
    def save(self, commit=True):
        user = super(EmpleadosFrm, self).save(commit=False)
        
        # Asignar contraseñas de manera segura
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        
        # Deshabilitar privilegios de superusuario y acceso al panel de administración
        user.is_superuser = False
        user.is_staff = False  # Cambiado a False si no deseas acceso al panel de administración
        user.is_active = self.cleaned_data.get('status', True)  # Usar el valor de 'status' para el estado de la cuenta
        
        if commit:
            user.save()
        return user

    # Ordenar los campos en el formulario
    def __init__(self, *args, **kwargs):
        super(EmpleadosFrm, self).__init__(*args, **kwargs)
        ordered_fields = OrderedDict([
            ('username', self.fields['username']),
            ('nombre', self.fields['nombre']),
            ('apellido', self.fields['apellido']),
            ('email', self.fields['email']),
            ('password', self.fields['password']),
            ('dni', self.fields['dni']),
            ('telefono', self.fields['telefono']),
            ('direccion', self.fields['direccion']),
            ('cargo', self.fields['cargo']),
            ('fecha_nacimiento', self.fields['fecha_nacimiento']),
            ('status', self.fields['status']),
            ('foto_perfil', self.fields['foto_perfil']),
        ])
        self.fields = ordered_fields


class actEmpleadosFrm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = [
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'date_joined',
            'password',
            'fecha_nacimiento',
        ]
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'dni': {'unique': "Este DNI ya está registrado."},
            'email': {'invalid': "Introduce un correo electrónico válido."},
        }

    # Validaciones personalizadas
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if not fecha_nacimiento:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad < 18:
            raise ValidationError("El empleado debe tener al menos 18 años.")
        return fecha_nacimiento

    def __init__(self, *args, **kwargs):
        super(actEmpleadosFrm, self).__init__(*args, **kwargs)
        ordered_fields = OrderedDict([
            ('username', self.fields['username']),
            ('nombre', self.fields['nombre']),
            ('apellido', self.fields['apellido']),
            ('email', self.fields['email']),
            ('dni', self.fields['dni']),
            ('telefono', self.fields['telefono']),
            ('direccion', self.fields['direccion']),
            ('cargo', self.fields['cargo']),
            ('status', self.fields['status']),
            ('foto_perfil', self.fields['foto_perfil']),
        ])
        self.fields = ordered_fields
