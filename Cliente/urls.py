from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('Login/', views.Login, name="Login"),
    path('Cadastro/', views.Cadastro, name="Cadastro"),
    path('Perfil/', views.Perfil, name="Perfil"),
    path('Login/', LogoutView.as_view(), name="logout")
]