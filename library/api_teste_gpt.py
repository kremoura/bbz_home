from zeep import Client
from requests.adapters import HTTPAdapter
import requests
from django.http import JsonResponse
from zeep.transports import Transport
from requests import Session


from zeep import Client, Settings
from zeep.transports import Transport
from requests import Session

def buscar_emails_chatbot_json(senha, usuario, cpf, chave):
    # URL do WSDL com a porta correta
    wsdl = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"

    # Configurar a sessão com maior timeout
    session = Session()
    session.trust_env = False  # Desativar proxies automáticos do sistema
    transport = Transport(session=session, timeout=60)  # Timeout de 60 segundos

    # Criar o cliente SOAP
    settings = Settings(strict=False)
    client = Client(wsdl=wsdl, transport=transport, settings=settings)

    # Substituir o endpoint diretamente para garantir o uso da porta 81
    client.service._binding_options['address'] = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx"

    # Definir os parâmetros para o método específico
    params = {
        'senha': senha,
        'usuario': usuario,
        'cnpj_cpf': cpf,
        'chave': chave
    }

    # Chamar o método da API
    response = client.service.BuscaCPF_Todos_Emails_Chatbot_Json(**params)

    return response


def buscar_emails(request):

   # Configurações da API
    usuario = 'bucha'
    senha = 'Lnq:0BG^57,R~DIoovAz'
    chave = ';vM^t;+_;b0JbGJ+LiC-_0-^-;qW=T_o+dPN_;=+_^nYiV;_YEkg7BL+Ea^0;Q0Y-;W^ZZ'
    cpf = 34212563819  # substitua pelo CPF que você deseja utilizar
    
    # Chama a função que consome a API
    response = buscar_emails_chatbot_json(senha, usuario, cpf, chave)
    
    # Retornar a resposta como JSON
    return JsonResponse({'result': response})

buscar_emails(request="")