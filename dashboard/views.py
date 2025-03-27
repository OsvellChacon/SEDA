from django.shortcuts import render
from usuarios.models import Empleado
from estudiantes.models import Estudiantes, DocumentosEstudiante
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from estudiantes.models import DocumentosEstudiante
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    # Contar usuarios y estudiantes
    Megumi = Empleado.objects.count()
    Itadori = Estudiantes.objects.count()
    
    # Contar documentos pendientes, aprobados y rechazados
    documentos_pendientes = DocumentosEstudiante.objects.filter(estado_inscripcion="En Revisión").count()
    documentos_aprobados = DocumentosEstudiante.objects.filter(estado_inscripcion="Aprobado").count()
    documentos_rechazados = DocumentosEstudiante.objects.filter(estado_inscripcion="Rechazado").count()
    
    # Obtener los documentos pendientes para mostrarlos en el dashboard
    documentos_pendientes_lista = DocumentosEstudiante.objects.filter(estado_inscripcion="En Revisión").order_by('-fecha_subida')[:5]  # Mostrar los 5 más recientes
    
    # Paginación de estudiantes
    Maki = Estudiantes.objects.all().order_by('id')  # Ordenar por el campo 'id'
    page = request.GET.get('page', 1)
    paginator = Paginator(Maki, 5)

    try:
        Maki = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Maki = paginator.page(paginator.num_pages)
    
    # Contexto para la plantilla
    context = {
        'page_title': 'SEDA | Dashboard',
        'usuarios': Megumi,  # Total de empleados
        'estudiantes': Itadori,  # Total de estudiantes
        'Zenin': Maki,  # Lista de estudiantes paginada
        'paginator': paginator,  # Paginador
        'pendientes': documentos_pendientes,  # Total de documentos pendientes
        'aprobados': documentos_aprobados,  # Total de documentos aprobados
        'rechazados': documentos_rechazados,  # Total de documentos rechazados
        'documentos_pendientes_lista': documentos_pendientes_lista,  # Lista de documentos pendientes
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
