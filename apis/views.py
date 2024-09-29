from django.shortcuts import render

from zeep import Client

def buscar_emails_chatbot_json(senha, usuario, cnpj_cpf, chave_autenticacao):
    # URL do WSDL da API
    wsdl = "http://bbz.mine.nu:81/condominioweb/wsDocumentos.asmx?WSDL"
    
    # Criar um cliente SOAP
    client = Client(wsdl)

    # Definir os parâmetros para o método específico
    params = {
        'senha': senha,
        'usuario': usuario,
        'cnpj_cpf': cnpj_cpf,
        'chave': chave_autenticacao
    }
    
    # Chamar o método da API
    response = client.service.BuscaCPF_Todos_Emails_Chatbot_Json(**params)
    
    # Retornar a resposta do serviço
    return response

from django.http import JsonResponse

def buscar_emails(request):
    # Exemplo de parâmetros
    chave = "sua_chave_aqui"
    login = "seu_login_aqui"
    cpf_cnpj = "12345678900"
    chave_autenticacao = "sua_chave_autenticacao_aqui"
    
    # Chama a função que consome a API
    response = buscar_emails_chatbot_json(chave, login, cpf_cnpj, chave_autenticacao)
    
    # Retornar a resposta como JSON
    return render(request, 'buscar_emails.html', {'results': response})  # Renderiza a página HTML com a resposta({'result': response})
