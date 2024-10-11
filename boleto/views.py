import json
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from django.core.files import File
from comum.views import error
from apis.views import buscar_boletos_unidade, buscar_segunda_via_boleto_xml_por_recibo, boleto_pdf
from comum.views import enviar_email_boleto, verificar_sessao_home
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from log.models import Log
from django import template

def boleto_pagamento(request):
    cnpj_cpf = request.session.get('cnpj_cpf')
    email_informado = request.session.get('email_informado')
    log_id = request.session.get('log_id')

    # Verifica se o usuário está logado
    verificar_sessao_home(request)

    # Busca os boletos
    lista_boletos = buscar_boletos_unidade(request)

    # lista para armazenar os boletos
    lista_segunda_via_boleto = []
    # lista para armazenar os boletos que o usuário ja enviou um e-mail
    lista_ja_enviou_email_boleto = ''

    # looping para inserir os boletos na lista
    for recibo in lista_boletos:
        recibo_pesquisa = recibo['recibo']
        lista_segunda_via = buscar_segunda_via_boleto_xml_por_recibo(recibo_pesquisa)

        # Verifica se o usuário não enviou um e-mail recentemente
        ja_enviou_email_boleto = verifica_se_ja_enviou_boleto_email(request, recibo_pesquisa)
        # Verifica se o usuário ja enviou um e-mail
        if ja_enviou_email_boleto.get('retorno') != False:
            print(f'1 - {ja_enviou_email_boleto.get('retorno')}')
            lista_ja_enviou_email_boleto = ja_enviou_email_boleto.get('retorno')
            print(f'Ja enviou email: {lista_ja_enviou_email_boleto}')

        # adiciona os boletos na lista
        lista_segunda_via_boleto.append(lista_segunda_via)

    # Renderiza o template
    # @lista_boletos: lista dos boletos
    # @lista_segunda_via_boleto: lista dos boletos da segunda via
    # @cookie_ja_enviou: indica se o usuário ja enviou um e-mail
    return render(request, 'boleto/boleto_pagamento.html', {'lista_boletos': lista_boletos, 'lista_segunda_via_boleto': lista_segunda_via_boleto, 'lista_cookie_ja_enviou': lista_ja_enviou_email_boleto})

def envia_email_boleto(request):
    cnpj_cpf = request.session.get('cnpj_cpf')
    email_informado = request.session.get('email_informado')
    log_id = request.session.get('log_id')

    print('Sess o atual:')
    for chave, conteudo in request.session.items():
        print(f'{chave}: {conteudo}')

    if not verificar_sessao_home(request):
        return error(request, 'Para acessar essa página, por favor faça o login clicando no link abaixo.')

    print('inicio')
    if request.method == 'POST':
        email = request.POST.get('email')
        recibo = request.POST.get('recibo')
        vencto_original = request.POST.get('vencto_original')

        nome_chave_sessao_ja_enviou_email = f'ultimo_envio_boleto_{recibo}'
        print('pos if POST')
        # Verifica se o usuário já enviou um e-mail recentemente
        print(request.session.get(nome_chave_sessao_ja_enviou_email))
        if nome_chave_sessao_ja_enviou_email in request.session:
            print('pos if JÁ ENVIOU EMAIL')
            ultimo_envio = datetime.fromisoformat(request.session[nome_chave_sessao_ja_enviou_email])
            tempo_limite = 30 * 60  # 30 minutos em segundos
            tempo_decorrido = (datetime.now() - ultimo_envio).total_seconds()

            if tempo_decorrido < tempo_limite:
                print('pos if TEMPO DECORRIDO')
                tempo_restante = tempo_limite - tempo_decorrido
                data = datetime.now().isoformat()
                response_data = {'retorno': 'Por favor, aguarde {:.0f} minuto(s).'.format(tempo_restante / 60), 'data': data}
        
                return JsonResponse(response_data)
            else:
                request.session.pop(nome_chave_sessao_ja_enviou_email)
            
        print('apos verificar se email foi enviado ')

        if log_id:
            # Atualiza o log com o envio do boleto
            log_atual = Log.objects.get(id=log_id)
            log_atual.descricao += f' | Envio de boleto por E-Mail - Recibo: {recibo} - Vencto: {vencto_original} - E-Mail: {email} - CNPJ/CPF: {cnpj_cpf}'
            log_atual.save()
        else:
            response_data = {'retorno': 'Você precisa fazer o login novamente'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        print('apos log atualizado')

        # bytes_pdf = base64.b64decode
        bytes_pdf = boleto_pdf(request, recibo)

        boleto_bytes = bytes_pdf['_value_1']['_value_1'][0]['SegundaViaBoletos_PDF']['SegundaViaBoletos_PDF']
      
        #attachment = File(bytes_pdf, name=f'Boleto_{recibo}_{vencto_original}.pdf')
        nome_pdf = f'Boleto_{recibo}_{vencto_original}.pdf'

        pdf_file = open(nome_pdf, 'wb')
        pdf_file.write(boleto_bytes)
        pdf_file.close()

        pdf_file = open(nome_pdf, 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()

        pdf_mime = MIMEBase('application', 'pdf', Name=nome_pdf)
        pdf_mime.set_payload(pdf_data)
        encoders.encode_base64(pdf_mime)

        subject = 'Boleto por Email'
        body = render_to_string("boleto/corpo_email_enviar_boleto.html", {"recibo": recibo})
        email_remetente = 'bode@bbz.com.br'
        email_destinatario = 'kre.moura@gmail.com' #request.session.get('email_informado')

        email = EmailMultiAlternatives(subject, body, email_remetente, [email_destinatario])
        email.attach(pdf_mime)
        email.send()

        # Exclui o arquivo PDF
        os.remove(nome_pdf)

        # Atualiza a sessão com o tempo do último envio
        request.session[nome_chave_sessao_ja_enviou_email] = datetime.now().isoformat()
        request.session.set_expiry(30 * 60)  # Expira a sessão em 30 minutos

        return JsonResponse({'retorno': 'sim'})
    else:
        return JsonResponse({'retorno': 'nao'})
    
def verifica_se_ja_enviou_boleto_email(request, recibo):

    # nome da chave de sessao que irá conter o tempo do envio
    nome_chave_sessao_ja_enviou_email = f'ultimo_envio_boleto_{recibo}'
    # Verifica se o usuário não enviou um e-mail recentemente
    if nome_chave_sessao_ja_enviou_email in request.session and request.session[nome_chave_sessao_ja_enviou_email] is not None:
        try:
            ultimo_envio = datetime.fromisoformat(request.session[nome_chave_sessao_ja_enviou_email])
            tempo_limite = 30 * 60  # 30 minutos em segundos
            tempo_decorrido = (datetime.now() - ultimo_envio).total_seconds()
            if tempo_decorrido < tempo_limite:
                tempo_restante = tempo_limite - tempo_decorrido
                response_data = {'retorno': 'Por favor, aguarde {:.0f} minutos.'.format(tempo_restante / 60)}
                return JsonResponse(response_data)
            else:
                request.session.pop(nome_chave_sessao_ja_enviou_email)
                return JsonResponse({'retorno': False})
        except ValueError:
            request.session.pop(nome_chave_sessao_ja_enviou_email)
            return JsonResponse({'retorno': False})
    else:
        return JsonResponse({'retorno': False})
    