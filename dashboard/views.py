from django.shortcuts import render
from usuarios.models import Empleado
from estudiantes.models import Estudiantes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def dashboard(request):
    
    Megumi = Empleado.objects.count()
    Itadori = Estudiantes.objects.count()
    
    Maki = Estudiantes.objects.all()
    
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

def estudiante_dashboard(request):
    
    Megumi = Empleado.objects.count()
    Itadori = Estudiantes.objects.count()
    
    Maki = Estudiantes.objects.all()
    
    page = request.GET.get('page', 1)

    paginator = Paginator(Maki, 5)

    try:
        Maki = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        Maki = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': 'SEDA | Dashboard - Estudiantes',
        'usuarios': Megumi,
        'estudiantes': Itadori,
        'Zenin': Maki,
        'paginator': paginator
    }
    
    return render(request, "dashboardEstudiantes.html", context)