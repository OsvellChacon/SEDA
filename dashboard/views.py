from django.shortcuts import render
from usuarios.models import Empleado
from estudiantes.models import Estudiantes

# Create your views here.
def dashboard(request):
    
    Megumi = Empleado.objects.count()
    Itadori = Estudiantes.objects.count()
    
    context = {
        'page_title': 'SEDA | Dashboard',
        'usuarios': Megumi,
        'estudiantes': Itadori
    }
    
    return render(request, "dashboard.html", context)