import json
import re
from django.shortcuts import render
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
import base64
import requests


def buscar_emails_chatbot_json(cnpj_cpf, usuario, senha, chave):

    # Crie uma sessão com um tempo de espera de 30 segundos
    session = Session()
    session.timeout = 30

    # Crie um adaptador de transporte com a porta correta
    adapter = HTTPAdapter(max_retries=3)
    session.mount('http://bbz.mine.nu:81', adapter)

    # Crie um transporte com a sessão
    transport = Transport(session=session)

    # URL do WSDL
    wsdl_url = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"

    # Crie o cliente com o transporte
    client = Client(wsdl="http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL", transport=transport)

    # Substitua o endpoint do serviço SOAP para garantir que a conexão seja feita na porta correta
    client.service._binding_options['address'] = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx"

    # Dados de entrada
    cnpj_cpf = cnpj_cpf
    usuario = usuario
    senha = senha
    chave = chave

    # Chamar a operação
    try:
        # Chama a operação do serviço SOAP
        response = client.service.BuscaCPF_Todos_Emails_Chatbot_Json(cnpj_cpf, usuario, senha, chave)

        resultado_json =  json.loads(response)

        emails = set()

        for condominio in resultado_json['Condominio']:
            for email in condominio['email'].split(','):
                # Esconder partes do email
                local_part = email.split('@')[0]
                domain = email.split('@')[1]
                email_escondido = local_part[1] + '***' + '@' + domain.split('.')[0][0] + '***' + '.' + domain.split('.')[-1]
                emails.add(email_escondido)

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
    usuario = 'bucha' 
    senha = 'Lnq:0BG^57,R~DIoovAz`'
    chave = ";vM^t;+_;b0JbGJ+LiC-_0-^-;qW=T_o+dPN_;=+_^nYiV;_YEkg7BL+Ea^0;Q0Y-;W^ZZ"
    
    # Chama a função que consome a API
    response = buscar_emails_chatbot_json(cnpj_cpf, usuario, senha, chave)
    
    # Retornar a resposta como JSON
    return render(request, 'api/buscar_emails.html', {'results': response})  # Renderiza a página HTML com a resposta({'result': response})
