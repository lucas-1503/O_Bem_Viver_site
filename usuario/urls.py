from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', views.Login, name='Login'),
    path('login/', LogoutView.as_view(), name="logout"),

    path('perfil/', NoticiaList.as_view(), name='perfil'),
    path('perfil_prof/', TurmaList.as_view(), name='perfil_prof'),
    path('perfil_staff/', views.perfil_staff, name='perfil_staff'),
    
    path('perfil/comprovante/<int:pk>/', views.enviar_comprovante, name='criar-comprovante'),
    path('perfil/alterar_senha/', views.alterar_senha, name='alterar-senha'),
    path('perfil/boletos/', BoletoList.as_view(), name='listar-boleto'),
    path('editar-perfil/', views.editar_foto, name='editar-perfil'),
    path('perfil/anotacoes', AnotacoesList.as_view(), name='listar-anotacoes'),
    
    path('perfil_prof/anotacoes/', AnotacoesCreate.as_view(), name='criar-anotacoes'),
    path('editar-perfil-prof/', views.editar_foto_prof, name='editar-perfil-prof'),
    
    path('perfil_staff/cadastro_usuario/', UsuarioCreate.as_view(), name='cadastro-usuario'),
    path('perfil_staff/envio_boleto/', BoletoCreate.as_view(), name='criar-boleto'),
    path('deletar-boleto/<int:pk>/', views.deletar_boleto, name='deletar-boleto'),
    path('perfil_staff/turma/', TurmaCreate.as_view(), name='criar-turma'),
    path('perfil_staff/usuarios', views.usuarios, name='usuarios'),
    path('perfil_staff/clientes', ClienteList.as_view(), name='listar-clientes'),
    path('perfil_staff/staff', StaffList.as_view(), name='listar-staff'),
    path('perfil_staff/educadores', EducadoresList.as_view(), name='listar-educadores'),
    path('perfil_staff/update_boleto/<int:pk>/', views.confirmar_boleto, name='editar-boleto'),
    path('perfil_staff/cadastro_filho/<int:pk>/', FilhoCreate.as_view(), name='cadastrar-filho'),
    path('perfil_staff/criar_noticia', NoticiaCreate.as_view(), name='criar-noticia'),
    path('deletar-usuario/<int:pk>/', views.deletar_cliente, name='deletar-cliente'),
    path('alterar-turma/<int:pk>/', views.alterar_turma, name='alterar-turma'),
    path('perfil_staff/escola/', views.escola, name='escola'),
    path('perfil_staff/financeiro/', BoletoListStaff.as_view(), name='financeiro'),
]