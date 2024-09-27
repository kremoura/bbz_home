from django.shortcuts import render

def index(request):
    return render(request, 'comum/sign-in/signin.html')

def gera_token(request):
    return render(request, 'comum/emails_para_enviar_token.html')

def valida_token(request):
    return render(request, 'comum/valida_token.html')

def building_list(request):
    lista_unidades = get_unidades_api(request)
    return render(request, 'comum/lists/building_lists.html', {'lista_unidades': lista_unidades})

def get_unidades_api(request):
    nome_condominio = "000395 - Edificio Fascino"
    bloco = " 0  "
    unidade = "000091"
    situacao = 1
    cid = 395

    if situacao  == 1:
        situacao = 'adimplente'
    elif situacao == 0:
        situacao = 'inadimplente'

    lista_unidades = []

    api_lista_unidades = {
        'nome_condominio': nome_condominio,
        'nome_condominio': nome_condominio,
        'bloco': bloco,
        'unidade': unidade,
        'situacao': situacao,
        'cid': cid,
    }

    lista_unidades.append(api_lista_unidades)
        

    return lista_unidades



