from django.db import models

class WhiteList(models.Model):
    id = models.AutoField(primary_key=True)
    email_agente = models.EmailField(max_length=255)
    nome_agente = models.CharField(max_length=255)
    cid_condominio = models.IntegerField()
    id_servico = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.email_agente} - {self.nome_agente}"