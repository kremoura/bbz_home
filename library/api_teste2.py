import zeep
from django.conf import settings
from zeep.transports import Transport
from requests import Session

def buscar_emails_chatbot_json(senha, usuario, cpf, chave):
    # URL do WSDL com a porta correta
    wsdl = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"

    # Configurar a sessão com maior timeout
    session = Session()
    session.trust_env = False  # Desativar proxies específicos do sistema
    transport = Transport(session=session, timeout=60)  # Timeout de 60 segundos

    # Criar o cliente SOAP
    settings = zeep.Settings(strict=False)
    client = zeep.Client(wsdl=wsdl, transport=transport, settings=settings)

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
    session = Session()
    transport = Transport(session=session)

    # Configurações da API
    url = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"
    usuario = 'bucha'
    senha = 'Lnq:0BG^57,R~DIoovAz'
    chave = ';vM^t;+_;b0JbGJ+LiC-_0-^-;qW=T_o+dPN_;=+_^nYiV;_YEkg7BL+Ea^0;Q0Y-;W^ZZ'
    cpf = 34212563819  # substitua pelo CPF que você deseja utilizar

    # Criar um objeto de autenticação
    auth = zeep.xsd.Element(
        "autenticacao",
        zeep.xsd.ComplexType([
            zeep.xsd.Element("usuario", zeep.xsd.String()),
            zeep.xsd.Element("senha", zeep.xsd.String()),
            zeep.xsd.Element("chave", zeep.xsd.String()),
            zeep.xsd.Element("cnpj_cpf", zeep.xsd.String()),
        ])
    )
    auth.usuario = usuario
    auth.senha = senha
    auth.chave = chave
    auth.cpf_cnpj = cpf

    # Criar um cliente Zeep
    cliente = zeep.Client(url, transport=transport)

    # Chamar o método BuscaCPF_Todos_Emails_Chatbot_JSON
    resultado = cliente.service.BuscaCPF_Todos_Emails_Chatbot_Json(
        cnpj_cpf=cpf,
        usuario=usuario,
        senha=senha,
        chave=chave
    )

    # Imprimir o resultado
    