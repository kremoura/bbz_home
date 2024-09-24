from django.db import models

class BuscaCPF_Todos_Emails_Chatbot_JSON(models.Model):
    condominio = models.CharField(max_length=200)
    nome = models.CharField(max_length=20)
    bloco = models.CharField(max_length=4)
    unidade = models.CharField(max_length=6)
    tipo = models.CharField(max_length=1)
    gerente = models.CharField(max_length=20)
    nome_gerente = models.CharField(max_length=50)
    email = models.CharField(max_length=8000)