import pysimplesoap as pysoap

# URL do serviço SOAP
url = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"
# Crie um cliente SOAP
client = pysoap.Client(url)

# Autentique no serviço SOAP
client.setCredentials('usuario', 'senha', 'chave', 'cnpj_cpf')

# Chame o método do serviço SOAP
resultado = client.BuscaCPF_Todos_Emails_Chatbot_Json(
    _soapheaders={
        'usuario': 'bucha',
        'senha': 'Lnq:0BG^57,R~DIoovAz',
        'chave': ';vM^t;+_;b0JbGJ+LiC-_0-^-;qW=T_o+dPN_;=+_^nYiV;_YEkg7BL+Ea^0;Q0Y-;W^ZZ',
        'cnpj_cpf': 34212563819  # substitua pelo CPF que você deseja utilizar
    }
)

print(resultado)