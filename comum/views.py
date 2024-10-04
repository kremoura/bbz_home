from django.shortcuts import render
from apis.views import buscar_emails_chatbot_json, get_unidades_api
from django import template
from log.views import criar_log, adicionar_descricao_log
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from token_home.models import TokenHome
from datetime import datetime, timedelta
from white_list.models import WhiteList

import random
import re


register = template.Library()

def index(request):
    """
    Mostra a tela de login do sistema.

    Esta view  chamada quando o usurio acessa a raiz do sistema.
    Ela apenas renderiza a template de login.
    """
    return render(request, 'comum/sign-in/signin.html')

def bbz_home(request):
    cnpj_cpf = request.session.get('cnpj_cpf')
    email_informado = request.session.get('email_informado')
    log_id = request.session.get('log_id')

    if not cnpj_cpf:
        return error(request, 'Para acessar essa página, por favor faça o login clicando no link abaixo.')
    
    try:
        token_gerado = TokenHome.objects.get(token=request.POST.get('numero_token'))

        #atualiza o Log
        descricao2 = ''
        token_validado = False

        if timezone.now() > token_gerado.validade:
            # a data e hora atual é posterior ao campo validade
            descricao2 = 'Token já expirado.'
            return error(request, descricao2)
        elif token_gerado.usado:
            #verifica se o TOKEN já foi usado.
            descricao2 = 'Token já usado.'
            return error(request, descricao2)
        elif token_gerado.email != email_informado:
             #verifica se o email é o mesmo que foi enviado o TOKEN.
            descricao2 = f'O TOKEN foi enviado para outro E-Mail. No banco: {token_gerado.email} - na sessao: {email_informado} '
            return error(request, descricao2)
        else:
            #valida o TOKEN corretamente
            token_gerado.usado = True
            token_gerado.data_uso = timezone.now()
            token_gerado.save()
            token_validado = True
            descricao2 = 'Token validado com sucesso.'

        descricao = f' Validação do Token: {token_gerado} - enviado para o E-Mail: {email_informado} - {descricao2}'

        if token_validado:   
            adicionar_descricao_log(log_id, descricao)
            return render(request, 'comum/bbz_home/bbz_home.html')
        else:
            return error(request, 'O TOKEN não pode ser validade, por favor, tente novamente mais tarde.')
        
    except TokenHome.DoesNotExist:
        descricao2 = 'Token é diferente do que foi passado. Por favor, informe o token correto.'
        descricao = f' Validação do Token: {token_gerado} - enviado para o E-Mail: {email_informado} - {descricao2}'
        adicionar_descricao_log(log_id, descricao)
        return error(request, descricao2)

def valida_email(request):
    pass    

def error(request, error):
    return render(request, 'error/error.html', {'error': error})

def cria_sessao(request, indice, valor):
    if isinstance(valor, list):
        for v in valor:
            request.session[indice] = v
    else:
        request.session[indice] = valor

def valida_documento(documento):
    """
    Valida um documento, seja CPF ou CNPJ.

    :param str documento: CPF ou CNPJ a ser validado.
    :return: True se o documento for valido, False caso contrario.
    """
    if len(documento) == 11:
        # Valida CPF
        cpf = documento.replace('.', '').replace('-', '')
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        if cpf in ['00000000000', '11111111111', '22222222222', '33333333333', '44444444444', '55555555555', '66666666666', '77777777777', '88888888888', '99999999999']:
            return False
        soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        dv1 = (soma1 * 10) % 11
        dv2 = (soma2 * 10) % 11
        if dv1 != int(cpf[9]) or dv2 != int(cpf[10]):
            return False
        return True
    elif len(documento) == 14:
        # Valida CNPJ
        cnpj = documento.replace('.', '').replace('-', '').replace('/', '')
        if len(cnpj) != 14 or not cnpj.isdigit():
            return False
        if cnpj in ['00000000000000', '11111111111111', '22222222222222', '33333333333333', '44444444444444', '55555555555555', '66666666666666', '77777777777777', '88888888888888', '99999999999999']:
            return False
        soma1 = sum(int(cnpj[i]) * (5 - i % 8) for i in range(12))
        soma2 = sum(int(cnpj[i]) * (6 - i % 8) for i in range(13))
        dv1 = (soma1 * 10) % 11
        dv2 = (soma2 * 10) % 11
        if dv1 != int(cnpj[12]) or dv2 != int(cnpj[13]):
            return False
        return True
    else:
        return False

def gera_token(request):

    cnpj_cpf = request.session.get('cnpj_cpf')
    email_informado = request.POST.get('email').strip()
    log_id = request.session.get('log_id')

    email_e_bbz = re.match(r"^.*@bbz\.com\.br$", email_informado)
    email_agente = WhiteList.objects.filter(email_agente=email_informado)

    response_emails = buscar_emails_chatbot_json(cnpj_cpf, False)

    for email in response_emails:
        if email.strip() == email_informado or email_e_bbz or email_agente:
            cria_sessao(request, 'email_informado', email_informado)
            break

    if request.session.has_key('email_informado'):
        token_gerado = criar_token()
        data_validade = datetime.now() + timedelta(minutes=15)
        envio_email = enviar_email_token(token_gerado, 'token@bbz.com.br', 'kre.moura@gmail.com', data_validade)
        if envio_email:
            token = TokenHome(
                token = token_gerado,
                email = request.session.get('email_informado'),
                cnpj_cpf = cnpj_cpf,
                validade = data_validade,
            )

            token.save()

            if token.id:
                #verifica se é um email da BBZ
                descricao2 = ''
                if email_e_bbz:
                    descricao2 = f' - é um Email da BBZ'

                #verifica se é um email de agente
                if email_agente:
                    descricao2 = f' - é um E-mail de agente: {email_informado}'

                #atualiza o Log
                descricao = f' Foi gerado o TOKEN de acesso: {token_gerado} - enviado para o E-Mail: {email_informado} - {descricao2}'
                adicionar_descricao_log(log_id, descricao)

                #renderiza a página
                return render(request, 'comum/valida_token.html')
            else:
                return error(request, 'Erro ao salvar o token.')
        else:
            return error(request, 'E-Mail não foi enviado. Por favor, verifique e tente novamente.')
    else:
        return error(request, 'E-Mail não foi encontrado no sistema. Por favor, verifique e tente novamente.')
    
def valida_token(request):
    pass

def listar_emails_escondidos(request): 
    
    if request.POST.get('cpf') is None:
        return error(request, 'CPF - Campo não pode estar vazio.')

    # Dados de entrada
    cnpj_cpf = request.POST.get('cpf')
    termo = request.POST.get('termo')
    termo2 = request.POST.get('termo2')

    if not valida_documento(cnpj_cpf):
        return error(request, 'CPF - O campo está em um formato errado ou campo está vazio')
    
    cria_sessao(request, 'cnpj_cpf', cnpj_cpf)

    response_emails = buscar_emails_chatbot_json(cnpj_cpf)

    descricao_log = 'CNPJ/CPF: ' + cnpj_cpf + ' entrou no sistema com um cpf ou cnpj válido. ' + ', '.join(response_emails) + ', termo: ' + str(termo) + ', termo2: ' + str(termo2)

    dados = {
        'cpf': cnpj_cpf,
        'email': '-',
        'descricao': descricao_log
    }

    try:
        log_id = criar_log(request, dados)
        if log_id is not None:
            cria_sessao(request, 'log_id', log_id)
        else:
            return error(request, 'Erro ao criar log Inicial')
        return render(request, 'comum/emails_para_enviar_token.html', {'emails': response_emails})
    except Exception as e:
        return error(request, str(e))

def criar_token():
    token = str(random.randint(100000, 999999))
    return token

def enviar_email_token(token, email_remetente, email_destinatario, data_validade):
    subject = "Seu Token de Acesso"
    body = render_to_string("comum/corpo_email_enviar_token.html", {"token": token, "data_validade": data_validade})
    return send_mail(subject, body, email_remetente, [email_destinatario], html_message=body)

def lista_condominio_unidades_por_cpf(request):
    cnpj_cpf = request.session.get('cnpj_cpf')
    email_informado = request.session.get('email_informado')
    log_id = request.session.get('log_id')

    if not cnpj_cpf:
        return error(request, 'Para acessar essa página, por favor faça o login clicando no link abaixo.')
    
    try:
        lista_unidades = get_unidades_api(cnpj_cpf)
        
        return render(request, 'comum/lists/lista_unidades_por_cpf.html', {'lista_unidades': lista_unidades})
    except Exception as e:
        return error(request, f'.Erro ao buscar unidades: {str(e)}')
    