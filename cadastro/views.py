from django.shortcuts import render
from django.http import HttpResponse

def cad_index(request):
    return render(request, 'cadastro/lgpd.html')

def escolha_atualizacao(request):
    return render(request, 'cadastro/escolha.html')

def alterar_proprietario(request):
    return render(request, 'cadastro/alterar_proprietario.html')

def alterar_locatario(request):
    return render(request, 'cadastro/alterar_locatario.html')

def alterar_dados(request):
    return render(request, 'cadastro/alterar_dados.html')

def get_dados_atualizacao(request):
    owner_check = request.POST.get("owner_check")
    tenant_check = request.POST.get("tenant_check")
    name = request.POST.get("name")
    email = request.POST.get("email")
    cep = request.POST.get("cep")
    state = request.POST.get("state")
    city = request.POST.get("city")
    neighborhood = request.POST.get("neighborhood")
    address = request.POST.get("address")
    number = request.POST.get("number")
    complement = request.POST.get("complement")
    nome_do_condominio = request.POST.get("nome_do_condominio")
    block = request.POST.get("block")
    unid = request.POST.get("unid")
    phone = request.POST.get("phone")
    new_owner = request.POST.get("new_owner")
    type_owner = request.POST.get("type_owner")
    new_cpf_cnpj = request.POST.get("new_cpf_cnpj")
    new_phone = request.POST.get("new_phone")
    new_email = request.POST.get("new_email")
    tax = request.POST.get("tax")
    spoils = request.POST.get("spoils")
    new_cep = request.POST.get("new_cep")
    new_state = request.POST.get("new_state")
    new_city = request.POST.get("new_city")
    new_neighborhood = request.POST.get("new_neighborhood")
    new_address = request.POST.get("new_address")
    new_number = request.POST.get("new_number")
    new_complement = request.POST.get("new_complement")
    additional = request.POST.get("additional")

    return f"Nome: {name}"

def teste_km(request):
    retorno = get_dados_atualizacao(request)

    return HttpResponse(retorno)
