from django.db.models.base import Model as Model
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from .forms import LoginForm, UsuarioForm, BoletoForm, ComprovanteForm, FilhoForm, NoticiaForm, AnotacoesForm, TurmaForm
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Boleto, Usuario, Noticia, Turma, Comprovante, Filho, Anotacoes
from django.utils import timezone
from datetime import date, datetime
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models.functions import ExtractMonth
from django.db.models import Count
import calendar
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from babel.dates import get_month_names
from django.utils.translation import activate
from calendar import month_abbr


class BoletoListStaff(LoginRequiredMixin,ListView):
    model = Boleto
    template_name = 'perfil_staff/financeiro.html'
    context_object_name = 'boletos'

    def get_queryset(self):
        txt_educando = self.request.GET.get('educando')
        status = self.request.GET.get('status')
        mes = self.request.GET.get('mes')

        queryset = Boleto.objects.all()

        if txt_educando:
            queryset = queryset.filter(educando__username__icontains=txt_educando)
        if status == 'Pago':
            queryset = queryset.filter(is_payed=True)
        elif status == 'Em análise':
            # Usamos o operador Q para combinar várias condições
            queryset = queryset.filter(Q(comprovante__isnull=False) & Q(is_payed=False))
        elif status == 'Atrasado':
            queryset = queryset.filter(Q(data_vencimento__lt= timezone.now().date()) & Q(comprovante__isnull=True) & Q(is_payed=False))
        elif status =='Em aberto':
            queryset = queryset.filter(Q(data_vencimento__gt= timezone.now().date()) & Q(comprovante__isnull=True) & Q(is_payed=False))
        if mes:
            queryset = queryset.filter(data_vencimento__month=mes.split('-')[1])
        return queryset


class BoletoList(LoginRequiredMixin,ListView):
    model = Boleto
    template_name = 'perfil/boletos.html'
    def get_queryset(self):
        return Boleto.objects.filter(educando=self.request.user)
    
class BoletoCreate(LoginRequiredMixin, CreateView):
    model = Boleto
    form_class = BoletoForm
    template_name = 'perfil_staff/envio_boleto.html'
    success_url = reverse_lazy('criar-boleto')
    context_object_name = 'mes_atual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes_atual1 = datetime.now().month
        mes_atual = datetime.now()
        context['mes_atual'] = mes_atual

        # Filtrando usuários não deletados e que são alunos
        context['total_de_clientes'] = Usuario.objects.filter(is_aluno=True, date_deleted__isnull=True).count()
        
        context['boletos_enviados'] = Boleto.objects.filter(data_vencimento__month=mes_atual1).count()
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        self.object = form.save()
        return response

    def get_queryset(self):
        mes_atual = datetime.now().month

        # Filtrando usuários não deletados e que são alunos
        return super().get_queryset().filter(educando__is_aluno=True, educando__date_deleted__isnull=True)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        self.object = form.save()
        return response

    def get_queryset(self):
        mes_atual = datetime.now().month
        return super().get_queryset().filter(educando__is_aluno=True)
    
    
class ComprovanteCreate(LoginRequiredMixin,CreateView):
    model = Comprovante
    form_class = ComprovanteForm
    template_name = 'perfil/comprovante.html'
    success_url = reverse_lazy('listar-boleto')
    def form_valid(self, form):
        # Obtém o Boleto com base no parâmetro pk da URL
        boleto = get_object_or_404(Boleto, pk=self.kwargs['pk'])

        # Salva o comprovante no banco de dados
        self.object = form.save()

        # Vincula o comprovante ao boleto específico
        boleto.comprovante = self.object
        boleto.save()

        return super().form_valid(form) 
    
def deletar_cliente(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    
    # Atualiza o campo date_deleted e salva o usuário
    usuario.date_deleted = date.today()
    usuario.save()
    
    # Define uma mensagem de sucesso
    messages.success(request, 'Cliente deletado com sucesso.')
    
    return redirect('listar-clientes')
    
class ClienteList(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'perfil_staff/clientes.html'
    context_object_name = 'turma'
    
    def get_queryset(self):
        return Usuario.objects.filter(is_aluno=True, date_deleted__isnull=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["turma"] = Turma.objects.all()
        context["num_alunos"] = Usuario.objects.filter(is_aluno=True, date_deleted__isnull=True).count()
        
        # Contando o número de clientes registrados por mês com is_aluno=True
        usuarios_por_mes = Usuario.objects.filter(is_aluno=True).annotate(
            mes_registro=ExtractMonth('date_joined')
        ).values('mes_registro').annotate(
            total=Count('id')
        ).order_by('mes_registro')
        
        # Contando o número de clientes deletados por mês com is_aluno=True
        deletados_por_mes = Usuario.objects.filter(is_aluno=True).annotate(
            mes_deletado=ExtractMonth('date_deleted')
        ).values('mes_deletado').annotate(
            total=Count('id')
        ).order_by('mes_deletado')

        # Configurando para português
        activate('pt_BR')
        
        # Criando listas para os resultados
        meses = []
        registros = []
        deletados = []

        month_names = get_month_names('abbreviated', locale='pt_BR')

        for i in range(1, 13):  # Garantir que todos os meses estejam representados
            nome_mes = month_names[i]
            meses.append(nome_mes)
            registros.append(next((item['total'] for item in usuarios_por_mes if item['mes_registro'] == i), 0))
            deletados.append(next((item['total'] for item in deletados_por_mes if item['mes_deletado'] == i), 0))

        context["meses"] = meses
        context["registros"] = registros
        context["deletados"] = deletados
        
        # Gerando o gráfico
        buffer = BytesIO()
        x = range(len(meses))
        width = 0.35
        
        plt.figure(figsize=(5, 3))
        plt.bar(x, registros, width, label='Registrados', color='skyblue')
        plt.bar([p + width for p in x], deletados, width, label='Deletados', color='red')
        
        plt.xlabel('Mês')
        plt.ylabel('Número de Usuários')
        plt.title('Número de Usuários Registrados e Deletados por Mês')
        plt.xticks([p + width / 2 for p in x], meses)
        plt.legend()

        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        buffer.close()
        
        context['grafico'] = graphic
        
        return context
        
    
class StaffList(LoginRequiredMixin,ListView):
    
    model = Usuario
    template_name = 'perfil_staff/staff.html'
    
    def get_queryset(self):
        return Usuario.objects.filter(is_staff=True)

    
class EducadoresList(LoginRequiredMixin,ListView):
    
    model = Usuario
    template_name = 'perfil_staff/educadores.html'
    context_object_name = 'turma'
    
    def get_queryset(self):
        return Usuario.objects.filter(is_professor=True)
    
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context["turma"] = Turma.objects.all()
        return context
    
def alterar_turma(request,pk):
    if request.method == 'POST':
        usuario_id = pk
        turma_id = request.POST.get('turma')  # Obter o ID da turma do formulário
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        turma = get_object_or_404(Turma, pk=turma_id)

        if turma.limite_de_usuarios_atingido():
            if turma.alunos.filter(pk=usuario_id).exists():
                # Se o usuário já estiver na turma, remova-o e adicione-o novamente
                turma.alunos.remove(usuario)
                messages.error(request, 'Usuário removido da turma com sucesso.')
            else:
                messages.error(request, 'A turma está cheia. Não é possível adicionar mais usuários.')
        else:
            if turma.alunos.filter(pk=usuario_id).exists():
                # Se o usuário já estiver na turma, remova-o e adicione-o novamente
                turma.alunos.remove(usuario)
                messages.error(request, 'Usuário removido da turma com sucesso.')
            else:
                # Adicione o usuário à turma
                turma.alunos.add(usuario)
                messages.success(request, 'Usuário adicionado à turma com sucesso.')
    return redirect('listar-clientes')

def editar_foto(request):
    if request.method == 'POST':
        usuario = request.user  # Obtenha o usuário atualmente logado
        nova_foto = request.FILES.get('foto')  # Obtenha o arquivo enviado pelo formulário
        if nova_foto:
            usuario.avatar = nova_foto  # Atribua a nova foto ao campo avatar do usuário
            usuario.save()
    return redirect('perfil')

def editar_foto_prof(request):
    if request.method == 'POST':
        usuario = request.user  # Obtenha o usuário atualmente logado
        nova_foto = request.FILES.get('foto_prof')  # Obtenha o arquivo enviado pelo formulário
        if nova_foto:
            usuario.avatar = nova_foto  # Atribua a nova foto ao campo avatar do usuário
            usuario.save()
    return redirect('perfil_prof')

def confirmar_boleto(request,pk):
    if request.method == 'POST':
        
        boleto = get_object_or_404(
            Boleto, pk=pk
        )
        if boleto.is_payed == False:
            boleto.is_payed = True
            boleto.save()
        
        return redirect ('financeiro')
    
def deletar_boleto(request,pk):
    if request.method == 'POST':
        
        boleto = get_object_or_404(
            Boleto, pk=pk
        )
        
        boleto.delete()
        
        return redirect ('financeiro')
    
def enviar_comprovante(request, pk):
    if request.method == 'POST':
        boleto = get_object_or_404(Boleto, pk=pk)
        comprovante_file = request.FILES.get('comprovante')

        if comprovante_file:
            # Salvar o arquivo enviado como uma instância do modelo Comprovante
            comprovante_instance = Comprovante.objects.create(arquivo=comprovante_file)

            # Associar o comprovante_instance ao campo comprovante do modelo Boleto
            boleto.comprovante = comprovante_instance
            boleto.save()

            # Redirecionar ou fazer qualquer outra coisa depois de salvar o comprovante
            return redirect('listar-boleto')
        
def alterar_senha(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        novasenha = request.POST.get('novasenha')

        user = Usuario.objects.get(username=username)
        user.set_password(novasenha)
        user.save()
        messages.success(request,'Senha alterada com sucesso!')
        try:
            user = Usuario.objects.get(username=username)
        except user.DoesNotExist:
            messages.success(request, 'Dados errados')
            return redirect('perfil')
        

    return render(request,'perfil/alterar_senha.html')
    
class AnotacoesCreate(LoginRequiredMixin, CreateView):
    model = Anotacoes
    form_class = AnotacoesForm
    template_name = 'perfil_prof/criar_anotacoes.html'
    success_url = reverse_lazy('perfil_prof')

    def form_valid(self, form):
        form.instance.remetente = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['remetente'] = self.request.user
        return kwargs
    

class TurmaCreate(LoginRequiredMixin,CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'perfil_staff/turma.html'
    success_url = reverse_lazy('perfil_staff')
    
class TurmaList(LoginRequiredMixin,ListView):
    model = Turma
    template_name = 'perfil_prof/perfil_prof.html'
    def get_queryset(self):
        return Turma.objects.filter(professor=self.request.user)
    

class NoticiaList(LoginRequiredMixin,ListView):
    model = Noticia
    template_name = 'perfil/perfil.html'
    def get_queryset(self):
        return Noticia.objects.all()
    
class AnotacoesList(LoginRequiredMixin,ListView):
    model = Anotacoes
    template_name = 'perfil/anotacoes.html'
    def get_queryset(self):
        return Anotacoes.objects.filter(destinatario=self.request.user)
    
class UsuarioCreate(LoginRequiredMixin, CreateView):
    model= Usuario
    template_name = 'perfil_staff/cadastro_usuario.html'
    form_class = UsuarioForm
    
    def form_valid(self, form):
        # Salva o formulário e obtém o objeto de usuário criado
        self.object = form.save()
        # Obtém o ID do usuário criado
        user_id = self.object.id
        
        # Redireciona para a página de criação de filho com o ID do usuário como parte da URL
        self.success_url = reverse_lazy('cadastrar-filho', kwargs={'pk': user_id})
        return super().form_valid(form)
    
class FilhoCreate(LoginRequiredMixin, CreateView):
    model = Filho
    template_name = 'perfil_staff/cadastro_filho.html'
    form_class = FilhoForm
    success_url = reverse_lazy('perfil_staff')
    
    def form_valid(self, form):
        # Obtém o Usuario com base no parâmetro pk da URL
        usuario = get_object_or_404(Usuario, pk=self.kwargs['pk'])

        # Salva o filho no banco de dados
        self.object = form.save()

        # Vincula o filho ao usuario específico
        usuario.filho = self.object
        usuario.save()

        return super().form_valid(form)
    
class NoticiaCreate(LoginRequiredMixin, CreateView):
    model= Noticia
    template_name = 'perfil_staff/criar_noticia.html'
    form_class = NoticiaForm
    
    def form_valid(self, form):
        # Salva o formulário e obtém o objeto de usuário criado
        self.object = form.save()
        
        # Redireciona para a página de criação de filho com o ID do usuário como parte da URL
        self.success_url = reverse_lazy('perfil_staff')
        return super().form_valid(form)
    
    
def Login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_professor:
                login_django(request, user)
                return redirect('perfil_prof')
            elif user is not None and user.is_aluno:
                login_django(request, user)
                return redirect('perfil')
            elif user is not None and user.is_staff:
                login_django(request,user)
                return redirect('perfil_staff')
            else:
                msg= "Usuário ou senha inválidos"
        else:
            msg = "Formulário invalido"   
    return render(request, 'login/login.html', {'form':form, 'msg':msg})


@login_required

def perfil_prof(request):
    return render(request, 'perfil_prof/perfil_prof.html')

def perfil(request):
    return render(request, 'perfil/perfil.html')

def perfil_staff(request):
    return render(request, 'perfil_staff/perfil_staff.html')

def escola(request):
    return render(request, 'perfil_staff/escola.html')

def usuarios(request):
    return render(request, 'perfil_staff/usuarios.html')

def financeiro(request):
    return render(request, 'perfil_staff/financeiro.html')
    
def logout_view(request):
    logout(request)
    return redirect('/usuario/login/login') 