from django.shortcuts import render
from comum.views import error
from apis.views import buscar_boletos_unidade, buscar_segunda_via_boleto_xml_por_recibo

# Create your views here.
def boleto_pagamento(request):
    cnpj_cpf = request.session.get('cnpj_cpf')
    email_informado = request.session.get('email_informado')
    log_id = request.session.get('log_id')

    # if not cnpj_cpf:
    #     return error(request, 'Para acessar essa página, por favor faça o login clicando no link abaixo.')
    
    lista_boletos = buscar_boletos_unidade(request)
    
    lista_segunda_via_boleto = []

    for recibo in lista_boletos:
        recibo_pesquisa = recibo['recibo']
        lista_segunda_via = buscar_segunda_via_boleto_xml_por_recibo(recibo_pesquisa)
        lista_segunda_via_boleto.append(lista_segunda_via)

    print(lista_segunda_via_boleto)

    return render(request, 'boleto/boleto_pagamento.html', {'lista_boletos': lista_boletos, 'lista_segunda_via_boleto': lista_segunda_via_boleto})