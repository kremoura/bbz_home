from django.db import models

class Condominio(models.Model):
    nome = models.CharField(max_length=250, null=False, blank=False)
    cid = models.IntegerField(null=False, Blank=False)
    pasta_nuvem = models.CharField(max_length=100, null=False, blank=False)
    pasta_prestacao_contas = models.CharField(max_length=100, null=False, blank=False)
    gerente = models.CharField(max_length=100, null=False, blank=False)
    gerente_id = models.IntegerField(null=False, Blank=False)
