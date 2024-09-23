from django.urls import path
from atualizacao_cadastral.views import index, escolha_atualizacao

urlpatterns = [
    path('', index, name='lgpd'),
    path('escolha/', escolha_atualizacao, name='escolha_atualizacao')
]