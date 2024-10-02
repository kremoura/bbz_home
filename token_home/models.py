from django.db import models

class TokenHome(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    cnpj_cpf = models.CharField(max_length=14)
    data_criacao = models.DateTimeField(auto_now_add=True)
    validade = models.DateTimeField()
    data_uso = models.DateTimeField(null=True, blank=True)
    usado = models.BooleanField(default=False)

    def __str__(self):
        return self.token