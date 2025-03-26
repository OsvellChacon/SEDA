from django.shortcuts import render
from .models import *

# Create your views here.
def estudiantes(request):
    
    Gara = Estudiantes.objects.count()
    
    context = {
        'page_title': 'SEDA | Estudiantes',
        'estudiantes': Gara 
    }
    
    return render(request, "estudiantes.html", context)