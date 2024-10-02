import json
from django.shortcuts import render
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.adapters import HTTPAdapter
import os
import requests

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
    usuario = str(os.getenv('USUARIO'))
    senha = str(os.getenv('SENHA'))
    chave = str(os.getenv('CHAVE'))

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
