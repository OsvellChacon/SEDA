from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries.fields import countries
from django.http import HttpResponseForbidden

# Create your views here.
def estudiantes(request):
    # Obtener todos los estudiantes y contar el total
    Shinobu = Estudiantes.objects.all().order_by('-id')
    Mitsuri = Estudiantes.objects.count()

    # Contar documentos pendientes, aprobados y rechazados
    documentos_pendientes = DocumentosEstudiante.objects.filter(estado_inscripcion="En Revisión").count()
    documentos_aprobados = DocumentosEstudiante.objects.filter(estado_inscripcion="Aprobado").count()
    documentos_rechazados = DocumentosEstudiante.objects.filter(estado_inscripcion="Rechazado").count()

    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(Shinobu, 5)

    try:
        Shinobu = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Shinobu = paginator.page(paginator.num_pages)

    # Contexto para la plantilla
    context = {
        'page_title': 'SEDA | Estudiantes',
        'Culona': Shinobu,  # Lista de estudiantes paginada
        'estudiantes': Mitsuri,  # Total de estudiantes
        'pendientes': documentos_pendientes,  # Total de documentos pendientes
        'aprobados': documentos_aprobados,  # Total de documentos aprobados
        'rechazados': documentos_rechazados,  # Total de documentos rechazados
        'paginator': paginator
    }

    return render(request, "estudiantes.html", context)

def listaEstudiantes(request):
    query = request.GET.get('q', '').strip()

    if query:
        Gojo = Estudiantes.objects.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(dni__icontains=query) | 
            Q(nacionalidad__icontains=query)  # Aquí sigue filtrando por código de país
        ).order_by('dni')
    else:
        Gojo = Estudiantes.objects.filter(is_superuser=False).order_by('-id')

    # Convertir el código de país en nombre de país legible
    for estudiante in Gojo:
        estudiante.nacionalidad_nombre = countries.name(estudiante.nacionalidad)

    page = request.GET.get('page', 1)
    paginator = Paginator(Gojo, 5)

    try:
        Gojo = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Gojo = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'SEDA | Lista Estudiantes',
        'Gojo': Gojo,
        'paginator': paginator
    }

    return render(request, "estudiantes/estudiantes.html", context)

def agregarEstudiante(request): 
    if request.method == 'POST':
        Douma = EstudiantesRegistroForm(request.POST)
        if Douma.is_valid():
            Douma.save()
            messages.success(request, "Estudiante Agregado Exitosamente!")
            return redirect('lista_estudiantes')
        else:
            messages.error(request, 'Error al intentar guardar al estudiante')
    else:
        Douma = EstudiantesRegistroForm()
        
    context = {
        'page_title': 'SEDA | Agregar Estudiante',
        'Douma': Douma
    }
    
    return render(request, "estudiantes/agregarEstudiante.html", context)


def actualizarEstudiante(request, id): 
    
    Agatsuma = get_object_or_404(Estudiantes, id=id)
    
    if request.method == 'POST':
        Zenitsu = EstudiantesActualizacionForm(request.POST, instance=Agatsuma)
        if Zenitsu.is_valid():
            Zenitsu.save()
            messages.success(request, f"{Agatsuma.nombre} {Agatsuma.apellido} actualizado Exitosamente!")
            return redirect('lista_estudiantes')
        else:
            messages.error(request, 'Error al intentar guardar al estudiante')
    else:
        Zenitsu = EstudiantesActualizacionForm(instance=Agatsuma)
        
    context = {
        'page_title': f'SEDA | {Agatsuma.nombre} {Agatsuma.apellido}',
        'Agatsuma': Zenitsu,
        'Nezuko': Agatsuma
    }
    
    return render(request, "estudiantes/actualizarEstudiante.html", context)

def eliminarEstudiante(request, id): 
    Kanao = get_object_or_404(Estudiantes, id=id)
    Kanao.delete()
    messages.success(request, f"{Kanao.nombre} {Kanao.apellido} Eliminado Exitosamente")
    return redirect('lista_estudiantes')

def mostrarEstudiante(request, id):
    user = get_object_or_404(Estudiantes, pk=id)
    context = {
        'maki': user,
        'page_title': f'Oseed | {user.nombre} {user.apellido}',
    }

    return render(request, "estudiantes/tarjetaEstudiante.html", context)

@login_required
def subir_documentos(request):
    estudiante = request.user.estudiantes  # Obtener el estudiante autenticado
    documentos, created = DocumentosEstudiante.objects.get_or_create(estudiante=estudiante)

    if request.method == 'POST':
        form = DocumentosEstudianteForm(request.POST, request.FILES, instance=documentos)
        if form.is_valid():
            form.save()
            return redirect('estudiante_dashboard')  # Redirige al dashboard del estudiante tras la subida
    else:
        form = DocumentosEstudianteForm(instance=documentos)
        
    context = {
        'page_title': 'SEDA | Subir Documentos',
        'form': form
    }

    return render(request, 'documentos/subir_documentos.html', context)
@login_required
def actualizar_documentos(request, id):
    estudiante = request.user.estudiantes  # Obtener el estudiante autenticado
    
    # Asegurar que el estudiante solo pueda actualizar sus propios documentos
    documentos = get_object_or_404(DocumentosEstudiante, id=id, estudiante=estudiante)

    if request.method == 'POST':
        form = DocumentosEstudianteForm(request.POST, request.FILES, instance=documentos)
        if form.is_valid():
            form.save()
            messages.success(request, "Documentos actualizados exitosamente.")
            return redirect('estudiante_dashboard')  # Redirige al dashboard tras la actualización
        else:
            messages.error(request, "Hubo un error al actualizar los documentos.")
    else:
        form = DocumentosEstudianteForm(instance=documentos)
        
    context = {
        'page_title': 'SEDA | Actualizar Documentos',
        'form': form
    }

    return render(request, 'documentos/actualizar_documentos.html', context)

def documentos_pendientes(request):
    query = request.GET.get('q', '').strip()

    if query:
        Maki = DocumentosEstudiante.objects.filter(
            Q(estudiante__nombre__icontains=query) |
            Q(estudiante__apellido__icontains=query) |
            Q(codigo_inscripcion__icontains=query)
        ).filter(estado_inscripcion="En Revisión").order_by('-id')
    else:
        Maki = DocumentosEstudiante.objects.filter(estado_inscripcion="En Revisión").order_by('-id')

    context = {
        'page_title': 'SEDA | Documentos Pendientes',
        'Zenin': Maki
    }

    return render(request, "pendientes/documentos_pendientes.html", context)

def visualizarDocumentos(request, id):
    
    Geto = get_object_or_404(DocumentosEstudiante, id=id)
    
    context = {
        'page_title': f'SEDA | Documentos: {Geto.estudiante.nombre} {Geto.estudiante.apellido}',
        'Suguru': Geto
    }
    
    return render(request, "pendientes/visualizarEstudiante.html", context)

def documentos_aprobados(request):
    
    query = request.GET.get('q', '').strip()

    if query:
        Maki = DocumentosEstudiante.objects.filter(
            Q(estudiante__nombre__icontains=query) |
            Q(estudiante__apellido__icontains=query) |
            Q(codigo_inscripcion__icontains=query)
        ).filter(estado_inscripcion="Aprobado").order_by('-id')
    else:
        Maki = DocumentosEstudiante.objects.filter(estado_inscripcion="Aprobado").order_by('-id')
    
    context = {
        'page_title': 'SEDA | Procesos Aprobados',
        'Zenin': Maki
    }
    
    return render(request, "pendientes/procesos_aprobados.html", context)

def documentos_rechazados(request):
    
    query = request.GET.get('q', '').strip()

    if query:
        Maki = DocumentosEstudiante.objects.filter(
            Q(estudiante__nombre__icontains=query) |
            Q(estudiante__apellido__icontains=query) |
            Q(codigo_inscripcion__icontains=query)
        ).filter(estado_inscripcion="Rechazado").order_by('-id')
    else:
        Maki = DocumentosEstudiante.objects.filter(estado_inscripcion="Rechazado").order_by('-id')
    
    
    context = {
        'page_title': 'SEDA | Procesos Aprobados',
        'Zenin': Maki
    }
    
    return render(request, "pendientes/procesos_rechazados.html", context)

@login_required
def cambiar_estado_inscripcion(request, id):
    documentos = get_object_or_404(DocumentosEstudiante, id=id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_inscripcion')
        if nuevo_estado in dict(EstadoInscripcion.choices):
            documentos.estado_inscripcion = nuevo_estado
            documentos.save()
            messages.success(request, f"El estado de inscripción se cambió a {nuevo_estado}.")
        else:
            messages.error(request, "Estado de inscripción no válido.")
    
    return redirect('estudiantes')

@login_required
def actualizar_perfil_estudiante(request):
    # Obtener el usuario autenticado como instancia de Estudiantes
    estudiante = get_object_or_404(Estudiantes, id=request.user.id)

    if request.method == 'POST':
        form = EstudiantesActualizacionForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('estudiante_dashboard')  # Redirigir al dashboard o a otra página
        else:
            messages.error(request, "Hubo un error al actualizar el perfil.")
    else:
        form = EstudiantesActualizacionForm(instance=estudiante)

    context = {
        'page_title': f'SEDA | Actualizar Perfil',
        'form': form,
        'user': estudiante
    }

    return render(request, 'estudiantes/actualizarPerfil.html', context)