import requests
import json
from pprint import pprint

metodo = 'BuscaCPF_Todos_Emails_Chatbot_JSON'
url = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"

params = {
    'BuscaCPF_Todos_Emails_Chatbot_JSON': {
        'usuario':  'bucha',
        'senha': 'Lnq:0BG^57,R~DIoovAz',
        'cnpj_cpf': '34212563819',
        'chave': ';vM^t;+_;b0JbGJ+LiC-_0-^-;qW=T_o+dPN_;=+_^nYiV;_YEkg7BL+Ea^0;Q0Y-;W^ZZ'
    }
}

pprint(params)

response = requests.get(url=url, params=params)

print(response.status_code)

if response.status_code == 200:
    pprint(response)
else:
    print(f'Erro ao acessar a API {response.status_code}')
