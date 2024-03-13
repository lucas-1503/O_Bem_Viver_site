from django.urls import path
from . import views

urlpatterns = [
    path('Login/', views.Login, name="Login"),
    path('Cadastro/', views.Cadastro, name="Cadastro"),
    path('Perfil/', views.Perfil, name="Perfil")
]