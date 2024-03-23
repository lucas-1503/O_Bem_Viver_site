from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('Login/', views.Login, name="Login"),
    path('CadastroUsuario/', views.CadastroUsuario, name="CadastroUsuario"),
    path('Perfil/', views.Perfil, name="Perfil"),
    path('PerfilProf/', views.PerfilProf, name="PerfilProf"),
    path('Login/', LogoutView.as_view(), name="logout"),
]