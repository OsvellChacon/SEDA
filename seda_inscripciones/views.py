from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from usuarios.models import *

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from usuarios.models import CustomUser

def login_view(request):
    login_error = False
    inactive_error = False 

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        try:
            user = CustomUser.objects.get(username=username)
            if not user.status:  
                inactive_error = True
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    login_error = True
        except CustomUser.DoesNotExist:
            login_error = True

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {
        'form': form,
        'login_error': login_error,
        'inactive_error': inactive_error,
        'page_title': 'SEDA | Login'
    })


def cerrar_sesion(request):
    logout(request)
    return redirect('login')