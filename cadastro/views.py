from django.shortcuts import render

def index(request):
    return render(request, 'cadastro/lgpd.html')

def escolha_atualizacao(request):
    return render(request, 'cadastro/escolha.html')