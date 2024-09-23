from django.db import models

class dados_cadastrais(models.Model):
    nome_proprietario = models.CharField(max_length=100, null=False, blank=False)