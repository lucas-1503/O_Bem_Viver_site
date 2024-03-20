from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def Cadastro(request):
    if request.method =="GET":
        return render(request, 'Cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = User.objects.filter(username=username, email=email).first()

        if user:
            return HttpResponse('Este usuário já existe')
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        
        return HttpResponse("usuário cadastrado com sucesso")
    
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