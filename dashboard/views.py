from django.shortcuts import render
from usuarios.models import CustomUser

# Create your views here.
def dashboard(request):
    
    Megumi = CustomUser.objects.count()
    
    context = {
        'page_title': 'SEDA | Dashboard',
        'usuarios': Megumi
    }
    
    return render(request, "dashboard.html", context)