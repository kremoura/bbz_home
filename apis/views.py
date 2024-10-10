from django.shortcuts import render
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from io import BytesIO

import os
import requests
import json
import xmltodict


def verificar_intranet_ou_internet():

    url = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
        else:
            return "http://192.168.0.203/condominioweb/wsDocumentos.asmx?WSDL"
    except requests.exceptions.RequestException:
        return "http://192.168.0.203/condominioweb/wsDocumentos.asmx?WSDL"

def verificar_intranet_ou_internet_adm():

    url = "http://bbz.mine.nu:81/administracaoweb/wsDocumentos.asmx?WSDL"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
        else:
            return "http://192.168.0.203/administracaoweb/wsDocumentos.asmx?WSDL"
    except requests.exceptions.RequestException:
        return "http://192.168.0.203/administracaoweb/wsDocumentos.asmx?WSDL"

def verificar_intranet_ou_internet_reduzido():

    url = "http://bbz.mine.nu:81"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return url
        else:
            return "http://192.168.0.203"
    except requests.exceptions.RequestException:
        return "http://192.168.0.203"

def valida_apis():
    usuario = 'bucha'
    senha = 'Lnq:0BG^57,R~DIoovAz`'
    chave = ';vM^t;+_;b0JbGJ+LiC-_0-^-;qW=T_o+dPN_;=+_^nYiV;_YEkg7BL+Ea^0;Q0Y-;W^ZZ'

    lista_campos_validadores = {'usuario': usuario, 'senha': senha, 'chave': chave}

    return lista_campos_validadores

def buscar_emails_chatbot_json(cnpj_cpf, esconder_email = True):

    # URL do WSDL
    wsdl_url = verificar_intranet_ou_internet()
    wsdl_url_reduzido = verificar_intranet_ou_internet_reduzido()

    # Crie uma sessão com um tempo de espera de 30 segundos
    session = Session()
    session.timeout = 30

    # Crie um adaptador de transporte com a porta correta
    adapter = HTTPAdapter(max_retries=3)
    session.mount(wsdl_url_reduzido, adapter)

    # Crie um transporte com a sessão
    transport = Transport(session=session)

    # Crie o cliente com o transporte
    client = Client(wsdl=wsdl_url, transport=transport)

    # Substitua o endpoint do serviço SOAP para garantir que a conexão seja feita na porta correta
    client.service._binding_options['address'] = wsdl_url

    lista_campos_validadores = valida_apis()

    # Dados de entrada
    cnpj_cpf = cnpj_cpf
    usuario = lista_campos_validadores.get('usuario')  # Substitua pelo seu valor de usuario
    senha = lista_campos_validadores.get('senha')  # Substitua pelo seu valor de senha
    chave = lista_campos_validadores.get('chave')  # Substitua pelo seu valor de chave

    # Chamar a operação
    try:
        # Chama a operação do serviço SOAP
        response = client.service.BuscaCPF_Todos_Emails_Chatbot_Json(cnpj_cpf, usuario, senha, chave)

        resultado_json =  json.loads(response)

        emails = set()

        for condominio in resultado_json['Condominio']:
            for email in condominio['email'].split(','):
                if esconder_email:
                    # Esconder partes do email
                    local_part = email.split('@')[0]
                    domain = email.split('@')[1]
                    email_escondido = local_part[1] + '***' + '@' + domain.split('.')[0][0] + '***' + '.' + domain.split('.')[-1]
                    emails.add(email_escondido)
                else:
                    emails.add(email)

        return emails
    except Exception as e:
        return "Erro ao chamar o serviço:", str(e)

def buscar_emails(request):
    """
    Função que renderiza a página HTML com a resposta da API
    
    :param request: Requisição HTTP do cliente
    :type request: django.http.HttpRequest
    
    :return: Renderiza a página HTML com a resposta da API
    :rtype: django.http.HttpResponse
    """
    # Dados de entrada
    cnpj_cpf = '34212563819'
    
    # Chama a função que consome a API
    response = buscar_emails_chatbot_json(cnpj_cpf)
    
    # Retornar a resposta como JSON
    return render(request, 'api/buscar_emails.html', {'results': response})  # Renderiza a página HTML com a resposta({'result': response})

def cria_client_soap(link='condoweb'):

    # URL do WSDL
    if link == 'condoweb':
        wsdl_url = verificar_intranet_ou_internet()
    else:
        wsdl_url = verificar_intranet_ou_internet_adm()

    wsdl_url_reduzido = verificar_intranet_ou_internet_reduzido()

    # Crie uma sessão com um tempo de espera de 30 segundos
    session = Session()
    session.timeout = 30

    # Crie um adaptador de transporte com a porta correta
    adapter = HTTPAdapter(max_retries=3)
    session.mount(wsdl_url_reduzido, adapter)

    # Crie um transporte com a sessão
    transport = Transport(session=session)

    # Crie o cliente com o transporte
    client = Client(wsdl=wsdl_url, transport=transport)

    # Substitua o endpoint do serviço SOAP para garantir que a conexão seja feita na porta correta
    client.service._binding_options['address'] = wsdl_url

    return client

def get_unidades_api(cnpj_cpf):

    #client SOAP
    client = cria_client_soap()

    lista_campos_validadores = valida_apis()

    # Dados de entrada
    cnpj_cpf = cnpj_cpf
    usuario = lista_campos_validadores.get('usuario')  # Substitua pelo seu valor de usuario
    senha = lista_campos_validadores.get('senha')  # Substitua pelo seu valor de senha
    chave = lista_campos_validadores.get('chave')  # Substitua pelo seu valor de chave

    # Chamar a operação
    try:
        # Chama a operação do serviço SOAP
        response = client.service. BuscaCPF_Chatbot_Json(cnpj_cpf, usuario, senha, chave)

        resultado_json =  json.loads(response)

        lista_unidades = []

        situacao = 1

        for condominio in resultado_json['Condominio']:
            if situacao  == 1:
                situacao = 'adimplente'
            elif situacao == 0:
                situacao = 'inadimplente'

            if condominio['tipo'] == 'L':
                tipo = 'Locatário'
            elif condominio['tipo'] == 'P':
                tipo = 'Proprietário'

            api_lista_unidades = {
                'nome_condominio': condominio['nome'],
                'bloco': condominio['bloco'],
                'unidade': condominio['unidade'],
                'tipo': tipo,
                'condominio': condominio['condominio'],
            }

            lista_unidades.append(api_lista_unidades)
            
        return lista_unidades
    except Exception as e:
        return f"Erro ao chamar o serviço: {str(e)}"

def buscar_segunda_via_boleto_xml_por_recibo(recibo):
    #client SOAP
    client = cria_client_soap('adminweb')

    lista_campos_validadores = valida_apis()

    # Dados de entrada
    usuario = lista_campos_validadores.get('usuario')  # Substitua pelo seu valor de usuario
    senha = lista_campos_validadores.get('senha')      # Substitua pelo seu valor de senha
    chave = lista_campos_validadores.get('chave')      # Substitua pelo seu valor de chave

    data_pagamento = None

    try:
        # Chama a operação do serviço SOAP
        response = client.service.SegundaViaBoletos_XML(recibo, data_pagamento, usuario, senha, chave)

        response_dict = xmltodict.parse(response)

        lista_segunda_via = []

        for item in response_dict.values():
            lista_segunda_via.append(item)

        return lista_segunda_via
    except Exception as e:
        return f"(DEF: buscar_segunda_via_boleto_xml_por_recibo)Erro ao chamar o serviço: {str(e)}"

def boleto_pdf(request, recibo):
    #client SOAP
    client = cria_client_soap()

    lista_campos_validadores = valida_apis()

    # Dados de entrada
    recibo = recibo
    usuario = lista_campos_validadores.get('usuario')  # Substitua pelo seu valor de usuario
    senha = lista_campos_validadores.get('senha')      # Substitua pelo seu valor de senha
    chave = lista_campos_validadores.get('chave')      # Substitua pelo seu valor de chave

    try:
        # Chama a operação do serviço SOAP
        response = client.service.SegundaViaBoletos_PDF(recibo, usuario, senha, chave)
        return response
    except Exception as e:
        return f"(DEF:boleto_pdf)Erro ao chamar o serviço: {str(e)}"

def buscar_boletos_unidade(request):
    #client SOAP
    client = cria_client_soap('adminweb')

    lista_campos_validadores = valida_apis()

    # Dados de entrada
    cnpj_cpf = request.session.get('cnpj_cpf')
    usuario = lista_campos_validadores.get('usuario')  # Substitua pelo seu valor de usuario
    senha = lista_campos_validadores.get('senha')      # Substitua pelo seu valor de senha
    chave = lista_campos_validadores.get('chave')      # Substitua pelo seu valor de chave

    condominio = request.GET.get('condominio')
    bloco = request.GET.get('bloco')
    unidade = request.GET.get('unidade')

    # Define os intervalos de dias
    add_dias = timedelta(days=60)
    sub_dias = timedelta(days=90)

    # Cria objetos datetime para a data inicial e final
    datainicial = datetime.now()
    datafinal = datetime.now()

    datainicial -= sub_dias
    datafinal += add_dias

    try:
        # Chama a operação do serviço SOAP
        response = client.service.ExtratoUnidade_XML(condominio, bloco, unidade, datainicial, datafinal, usuario, senha, chave)

        # Assume que a variável 'response' contém o XML retornado pelo SOAP
        response_dict = xmltodict.parse(response)

        lista_recibos = []

        for item in response_dict['ExtratoUnidade']['ExtratoUnidade']:
            lista = {
                'recibo': item['recibo'],
                'valor': item['valor'],
                'vencto_original': item['vencto_original'],
                'vencto': item['vencto'],
                'data_limite': item['data_limite'],
                'juridico': item['juridico'],
                'emissao': item['emissao'],
            }

            if 'data_pagamento' not in item:
                lista_recibos.append(lista)
                
        return lista_recibos
    except Exception as e:
        return f"Erro ao chamar o serviço: {str(e)}" 