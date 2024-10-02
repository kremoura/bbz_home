from django.utils import timezone
from log.models import Log
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.db import models
from django.utils import timezone

import requests

def adicionar_descricao_log(log_id, descricao):
    Log.objects.filter(id=log_id).update(
        descricao=Concat(F('descricao'), Value(' | '), Value(descricao), output_field=models.TextField()),
        ultima_atualizacao=timezone.now()
    )

def criar_log(request, dados):
    if 'ip' not in dados:
        ip = requests.get('https://api.ipify.org').text

    if 'hardware' not in dados:
        hardware = request.headers.get('User-Agent')

    try:
        log = Log(
            cpf=dados.get('cpf'),
            email=dados.get('email'),
            descricao=dados.get('descricao'),
            ip=ip,
            hardware=hardware,
            criacao=timezone.now(),
            ultima_atualizacao=timezone.now()
        )

        log.save()

        if log.id is not None and log.id != '':
            return log.id
        else:
            return None
    except Exception as e:
        print(f'Erro ao salvar log...: {e}')