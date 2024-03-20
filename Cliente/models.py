
from django.db import models

class Educando(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.IntegerField()

    def __str__(self): 
        return self.nome

class Educador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=100)
    educandos = models.ManyToManyField(Educando, related_name='educador')

    def __str__(self):
        return self.nome

    
class Mensagem(models.Model):
    titulo = models.CharField(max_length=50)
    remetente = models.ForeignKey(Educador, on_delete=models.CASCADE)
    conteudo = models.TextField(max_length=300)
    destinatario = models.ForeignKey(Educando, on_delete=models.CASCADE)

    def __str__(self) :
        return self.conteudo

class Boleto(models.Model):
    data = models.CharField(max_length=50)
    arquivo = models.FileField(unique=True)
    destinatario = models.ForeignKey(Educando, on_delete=models.CASCADE)

    def __str__(self) :
        return self.arquivo