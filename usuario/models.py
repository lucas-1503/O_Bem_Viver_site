from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, datetime
from django.core.exceptions import ValidationError




    
class Filho(models.Model):
    GENDER_CHOICES ={
        'Masculino':'Masculino',
        'Feminino':'Feminino',
        'Outros':'Outros',
    }
    primeiro_nome_filho = models.CharField(max_length=30, null=True)
    segundo_nome_filho = models.CharField(max_length=50, null=True)
    genero_filho = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Masculino')
    data_nascimento_filho = models.DateField('data_nascimento_filho', null=True)
    
    
    def __str__(self):
        return self.primeiro_nome_filho
    
class Usuario(AbstractUser):
    GENDER_CHOICES ={
        'Masculino':'Masculino',
        'Feminino':'Feminino',
        'Outros':'Outros',
    }
    is_aluno = models.BooleanField("aluno",default=False)
    is_professor = models.BooleanField("professor", default=False) 
    is_staff = models.BooleanField("staff", default=False)
    cpf = models.CharField(max_length=14, null=True)
    genero_usuario = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Masculino')
    data_nascimento= models.DateField('data_nascimento', null=True)
    avatar = models.ImageField(upload_to='img/', null=True, blank=True)
    filho = models.OneToOneField(Filho, on_delete=models.CASCADE, null=True, unique=True)
    date_deleted = models.DateField('date_deleted', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    def delete(self, *args, **kwargs):
        self.date_deleted = date.today()
        self.save()
        super().delete(*args, **kwargs)
        
    def clean(self):
        if self.date_deleted is not None:
            raise ("This user has been deleted and cannot log in.")
    
    @property
    
    def status(self):
        if self.is_aluno == True:
            return 'Aluno'
        elif self.is_professor == True:
            return 'Professor'
        else:
            return 'Administração'
        
        
class Turma(models.Model):
    modalidade = models.CharField(max_length=30, null=False, default='Musicalização infantil')
    professor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='turmas_ministradas', null=True, blank=True)
    dia = models.CharField(max_length=30, null=False, default=timezone.now)
    horario = models.TimeField(null=False, default=timezone.now)
    alunos = models.ManyToManyField(Usuario, related_name='alunos_da_turma', blank=True)
    quantidade_maxima_alunos = models.IntegerField(default=8)  # Defina o limite máximo de usuários por turma

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

    def __str__(self):
        return f'{self.professor}/{self.modalidade}'

    def numero_de_usuarios(self):
        return self.alunos.count()  # Retorna o número atual de usuários associados a esta turma

    def limite_de_usuarios_atingido(self):
        return self.numero_de_usuarios() >= self.quantidade_maxima_alunos

    
class Noticia(models.Model):
    COLOR_CHOICES ={
        'verde':'verde',
        'laranja':'laranja',
        'vermelho':'vermelho',
    }
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to="img/")
    conteudo = models.TextField()
    cor_de_fundo = models.CharField(max_length=10, choices=COLOR_CHOICES, default='verde')
    data_de_publicacao = models.DateField('data_de_publicacao', null=False, blank=False, default=timezone.now)
    
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
    
    def save(self, *args, **kwargs):
        if not self.data_de_publicacao:
            self.data_de_publicacao = timezone.now().date()
        super().save(*args,**kwargs)
    
class Anotacoes(models.Model):
    OPCOES_CHOICES = {
        "Ruim":"Ruim",
        "Regular":"Regular",
        "Bom":"Bom",
        "Excelente":"Excelente",
    }
    data_de_publicacao = models.DateField('data_de_publicacao', null=False, blank=False, default=timezone.now)
    concentracao = models.CharField(max_length=15, choices=OPCOES_CHOICES, default="Excelente")
    engajamento = models.CharField(max_length=15, choices=OPCOES_CHOICES, default="Excelente")
    competencias_tecnicas = models.CharField(max_length=15, choices=OPCOES_CHOICES, default="Excelente")
    competencias_socio_emocionais = models.CharField(max_length=15, choices=OPCOES_CHOICES, default="Excelente")
    observacoes = models.TextField()
    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='professor', null=True)
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destinatario', null=True)
    
    class Meta:
        ordering = ('-data_de_publicacao',)
        verbose_name = 'Anotação'
        verbose_name_plural = 'Anotações'
    
    def __str__(self):
        return self.data_de_publicacao
    
    def save(self, *args, **kwargs):
        if not self.data_de_publicacao:
            self.data_de_publicacao = timezone.now().date()
        super().save(*args,**kwargs)
        
class Comprovante(models.Model):
    arquivo = models.FileField(upload_to='pdf/', null=True)
    
    def __str__(self):
        return f"Boleto - {self.arquivo}"
    
class Boleto(models.Model):
    
    valor = models.IntegerField(null=False, blank=False)
    data_vencimento = models.DateField('data_vencimento')
    pdf = models.FileField(upload_to='pdf/', null=True)
    comprovante = models.OneToOneField(Comprovante, on_delete=models.CASCADE, null=True, unique=True)
    educando = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='boletos', null=True)
    is_payed = models.BooleanField('payed', default=False)
    
    @property
    
    def status(self):
        if self.data_vencimento < timezone.now().date() and self.comprovante is not None and self.is_payed == False:
            return 'Em análise'
        elif self.data_vencimento < timezone.now().date() and self.comprovante is None and self.is_payed == False:
            return 'Atrasado'
        elif self.data_vencimento > timezone.now().date() and self.comprovante is not None and self.is_payed == False:
            return 'Em análise'
        elif self.is_payed == True:
            return 'Pago'
        else:
            return 'Em aberto'
        

    def __str__(self):
        return f"Boleto - {self.valor}"
    
    def save(self, *args, **kwargs):
        if not self.data_vencimento:
            self.data_vencimento = datetime.now()
        super().save(*args,**kwargs)
    
    



