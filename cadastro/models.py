from django.db import models

class dados_cadastrais(models.Model):
    id = models.AutoField(primary_key=True)
    flag = models.CharField(max_length=1, choices=[
        ('P', 'Proprietário'),
        ('I', 'Inquilino')
    ])
    nome_completo = models.CharField(max_length=250)
    email = models.EmailField()
    cep = models.CharField(max_length=9)
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=250)
    bairro = models.CharField(max_length=250)
    endereco = models.CharField(max_length=250)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=250, blank=True)
    nome_condominio = models.CharField(max_length=250)
    bloco = models.CharField(max_length=250)
    unidade = models.CharField(max_length=250)
    telefone = models.CharField(max_length=11)
    
    # dados que o usuario pode alterar
    nome = models.CharField(max_length=250, blank=True)
    pessoa_fj = models.CharField(max_length=1, choices=[
        ('F', 'Física'),
        ('J', 'Jurídica')
    ], blank=True)
    cpf_cnpj = models.CharField(max_length=14, blank=True)
    telefone_alteravel = models.CharField(max_length=11, blank=True)
    email_alteravel = models.EmailField(blank=True)
    cep_alteravel = models.CharField(max_length=9, blank=True)
    uf_alteravel = models.CharField(max_length=2, blank=True)
    cidade_alteravel = models.CharField(max_length=250, blank=True)
    bairro_alteravel = models.CharField(max_length=250, blank=True)
    endereco_alteravel = models.CharField(max_length=250, blank=True)
    numero_alteravel = models.CharField(max_length=5, blank=True)
    complemento_alteravel = models.CharField(max_length=250, blank=True)
    arquivos = models.FileField(upload_to='arquivos/', blank=True)
    informacoes_adicionais = models.TextField(blank=True)
    alterado_em = models.DateTimeField(auto_now=True)
    alteracao_por = models.CharField(max_length=250, blank=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    