from django.db import models

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11)
    email = models.EmailField()
    descricao = models.TextField()
    criacao = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    hardware = models.CharField(max_length=100)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
