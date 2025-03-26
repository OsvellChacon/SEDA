from django.shortcuts import render
from usuarios.models import Empleado
from estudiantes.models import Estudiantes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from estudiantes.models import DocumentosEstudiante
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    Megumi = Empleado.objects.count()
    Itadori = Estudiantes.objects.count()
    
    # Ordenar el QuerySet explícitamente
    Maki = Estudiantes.objects.all().order_by('id')  # Ordenar por el campo 'id'
    
    page = request.GET.get('page', 1)

    paginator = Paginator(Maki, 5)

    try:
        Maki = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Maki = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': 'SEDA | Dashboard',
        'usuarios': Megumi,
        'estudiantes': Itadori,
        'Zenin': Maki,
        'paginator': paginator
    }
    
    return render(request, "dashboard.html", context)

@login_required
def estudiante_dashboard(request):
    # Obtener los documentos del estudiante logueado
    documentos = DocumentosEstudiante.objects.filter(estudiante=request.user).first()

    # Calcular el progreso de los documentos subidos
    progreso = documentos.calcular_progreso() if documentos else 0

    # Paginación de los documentos (si es necesario)
    Maki = [documentos] if documentos else []  # Convertir a lista para paginar
    page = request.GET.get('page', 1)
    paginator = Paginator(Maki, 5)

    try:
        Maki = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Maki = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'SEDA | Dashboard - Estudiantes',
        'Zenin': Maki,  # Paginador de documentos
        'progreso': progreso,  # Progreso de los documentos subidos
        'paginator': paginator,
        'documentos': documentos,  # Pasamos los documentos al contexto
    }

    return render(request, "dashboardEstudiantes.html", context)
