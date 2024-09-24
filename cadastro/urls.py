from django.urls import path
from cadastro.views import index, escolha_atualizacao, alterar_dados, alterar_proprietario, alterar_locatario

urlpatterns = [
    path('cadastro/', index, name='lgpd'),
    path('cadastro/ujeFES/', escolha_atualizacao, name='escolha_atualizacao'),
    path('cadastro/ukeuOJOU/', alterar_dados, name='alterar_dados')
]