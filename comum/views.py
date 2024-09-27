from django.shortcuts import render

def index(request):
    return render(request, 'comum/sign-in/signin.html')

def gera_token(request):
    return render(request, 'comum/emails_para_enviar_token.html')

def valida_token(request):
    return render(request, 'comum/valida_token.html')

def building_list(request):
    return render(request, 'comum/lists/building_lists.html')