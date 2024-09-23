from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'atualizacao_cadastral/lgpd.html')

def escolha_atualizacao(request):
    return render(request, 'atualizacao_cadastral/escolha/index.html')
