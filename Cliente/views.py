from .forms import UsuarioForm, LoginForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Usuario

def CadastroUsuario(request):
    msg=None
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            
            user = form.save()

            msg = "Usuario criado"
            return redirect('../../Cliente/Login/')
        else:
            msg = "Formulario invalido"
    else:        
        form = UsuarioForm()
    return render(request, 'CadastroUsuario/CadastroUsuario.html', {'form':form, 'msg':msg})
    
    
def Login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None and user.is_professor:
                login_django(request, user)
                return redirect('PerfilProf')
            elif user is not None and user.is_aluno:
                login_django(request, user)
                return redirect('Perfil')
            else:
                msg= "Usuário ou senha inválidos"
        else:
            msg = "Formulário invalido"   
    return render(request, 'Login/Login.html', {'form':form, 'msg':msg})


@login_required

def Perfil(request):
    return render(request, 'Perfil/Perfil.html')

def PerfilProf(request):
    return render(request, 'PerfilProf/PerfilProf.html')
    
def logout_view(request):
    logout(request)
    return redirect('/Cliente/Login/Login')    