from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *

def CadastroUsuario(request):
    if request.method =="GET":
        return render(request, 'CadastroUsuario.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tipo = request.POST.get('tipo')
        
        user = Usuario.objects.filter(username=username, email=email).first()

        if user:
            return HttpResponse('Este usuário já existe')
        
        user = Usuario.objects.create(username=username, email=email, password=senha, tipo=tipo)
        user.save()
        
        return HttpResponse("Educando cadastrado com sucesso")
    
    
def Login(request):
    if request.method == "GET":
        return render(request, 'Login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return redirect('/Cliente/Perfil')
        else:
            return HttpResponse("usuário ou senha invalidos")

@login_required

def Perfil(request):
    return render(request, 'Perfil.html')
    
def logout_view(request):
    logout(request)
    return redirect('/Cliente/Login')    