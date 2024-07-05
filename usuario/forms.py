from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Usuario,Boleto, Turma, Comprovante, Filho, Noticia, Anotacoes
from django.forms import ModelForm
from datetime import datetime

class UsuarioForm(UserCreationForm):
    username = forms.CharField(
        label='Nome ao logar',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    first_name = forms.CharField(
        label='Primeiro nome',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
        
    )
    last_name = forms.CharField(
        label='Segundo nome',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    data_nascimento = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password2 = forms.CharField(
        label='Repetir senha',
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    cpf = forms.CharField(
        label='Cpf',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    genero_usuario = forms.ChoiceField(
        label='Gênero do usuário',
        choices=Usuario.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "class":"form-control"
            }
        )
    )
    
    class Meta:
        model = Usuario
        fields = ('username','first_name','last_name','data_nascimento', 'email', 'password1', 'password2', 'is_aluno','is_professor', 'is_staff','cpf','genero_usuario')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)  
        
        self.fields['cpf'].widget.attrs.update({'class':'mask-cpf form-control'})
        
class FilhoForm(ModelForm):
    primeiro_nome_filho = forms.CharField(
        label='Primeiro nome',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    segundo_nome_filho = forms.CharField(
        label='Primeiro nome',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    genero_filho = forms.ChoiceField(
        label='Gênero do filho',
        choices=Filho.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "class":"form-control"
            }
        )
    )
    data_nascimento_filho = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    
    class Meta:
        model = Filho
        fields = ('primeiro_nome_filho','segundo_nome_filho','genero_filho','data_nascimento_filho')

class NoticiaForm(ModelForm):
    titulo = forms.CharField(
        label='Titulo',
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    imagem = forms.FileField(
        label='Imagem',
        widget=forms.FileInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    conteudo = forms.CharField(
        label='Conteudo',
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class":"form-control"
            }
        )
    )
    cor_de_fundo = forms.ChoiceField(
        label='Cor de fundo',
        choices=Noticia.COLOR_CHOICES,
        widget=forms.Select(
            attrs={
                "class":"form-control"
            }
        )
    )
    
    class Meta:
        model = Noticia
        fields = ('titulo','imagem','conteudo','cor_de_fundo')
        


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    

class BoletoForm(forms.ModelForm):
    valor = forms.IntegerField()
    data_vencimento = forms.DateField()
    pdf = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control"}))
    educando = forms.ModelChoiceField(label='Destinatário', queryset=None)

    class Meta:
        model = Boleto
        fields = ['valor', 'data_vencimento', 'pdf', 'educando']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mes_atual1 = datetime.now().month
        alunos_sem_boletos = Usuario.objects.filter(
            is_aluno=True,
            date_deleted__isnull=True
        ).exclude(boletos__data_vencimento__month=mes_atual1)
        self.fields['educando'].queryset = alunos_sem_boletos
        self.fields['data_vencimento'].widget.attrs.update({'class': 'mask-data_vencimento form-control'})
        self.fields['valor'].widget.attrs.update({'class': ' form-control'})  
        
        
class TurmaForm(ModelForm):
    DIAS_SEMANA_CHOICES = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    modalidade= forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        ))

    professor = forms.ModelChoiceField(
        label='Professor',
        queryset=Usuario.objects.filter(is_professor=True)
    )
    dia = forms.ChoiceField(
        label='Dia',
        choices=DIAS_SEMANA_CHOICES,
    )
    horario = forms.CharField(
        label='Horário',
        widget=forms.TextInput(attrs={'type': 'time'}),
    )


    class Meta:
        model = Turma
        fields = ['modalidade','professor', 'dia', 'horario']

    
    
        
        
        
class ComprovanteForm(ModelForm):
    
    class Meta:
        model = Comprovante
        fields = ['arquivo']
        
class AnotacoesForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(
        label='Para qual aluno seria essa anotação?',
        queryset=None,
    )
    
    class Meta:
        model = Anotacoes
        fields = ['destinatario', 'concentracao', 'engajamento', 'competencias_tecnicas', 'competencias_socio_emocionais', 'observacoes']
        
    def __init__(self, remetente, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra os alunos da turma do professor remetente
        self.fields['destinatario'].queryset = Usuario.objects.filter(
            is_aluno=True,
            alunos_da_turma__professor=remetente,
            date_deleted__isnull=True  # Filtra apenas os usuários que não foram deletados
        ).exclude(id=remetente.id)

        
        
