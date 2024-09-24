from django.shortcuts import render

def index(request):
    return render(request, 'cadastro/lgpd.html')

def escolha_atualizacao(request):
    return render(request, 'cadastro/escolha.html')

def alterar_proprietario(request):
    return render(request, 'cadastro/alterar_proprietario.html')

def alterar_locatario(request):
    return render(request, 'cadastro/alterar_locatario.html')

def alterar_dados(request):
    return render(request, 'cadastro/alterar_dados.html')
