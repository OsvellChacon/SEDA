from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def estudiantes(request):
    
    Shinobu = Estudiantes.objects.all().order_by('-id')
    Mitsuri = Estudiantes.objects.count()
    
    page = request.GET.get('page', 1)

    paginator = Paginator(Shinobu, 5)

    try:
        Shinobu = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Shinobu = paginator.page(paginator.num_pages)
    
    
    context = {
        'page_title': 'SEDA | Estudiantes',
        'Culona': Shinobu,
        'estudiantes': Mitsuri,
        'paginator': paginator
    }
    
    return render(request, "estudiantes.html", context)

def listaEstudiantes(request):
    
    query = request.GET.get('q', '').strip()

    # Filtrar los usuarios si se proporciona una búsqueda
    if query:
        Gojo = Estudiantes.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(dni__icontains=query) | Q(nacionalidad__icontains=query)
        ).order_by('dni')
    else:
        # Si no se pasa un término de búsqueda, se muestran todos
        Gojo = Estudiantes.objects.filter(is_superuser=False).order_by('dni')
        
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