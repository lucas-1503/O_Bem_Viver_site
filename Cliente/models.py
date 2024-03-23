from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    is_aluno = models.BooleanField("Aluno",default=False)
    is_professor = models.BooleanField("Professor",default=False)

    def __str__(self):
        return self.username


class Mensagem(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(default=True)
    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_enviadas', null=True)
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_recebidas', null=True)

    def __str__(self):
        return self.titulo

class Boleto(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField(null=True)
    pdf = models.FileField(upload_to='boletos/', null=True)
    educando = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='boletos', null=True)

    def __str__(self):
        return f"Boleto - {self.valor}"
