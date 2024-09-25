from django.urls import path
from cadastro.views import cad_index, escolha_atualizacao, alterar_dados, alterar_proprietario, alterar_locatario

urlpatterns = [
    path('cadastro/', cad_index, name='cad_index'),
    path('cadastro/ujeFES/', escolha_atualizacao, name='escolha_atualizacao'),
    path('cadastro/ukeuOJOU/', alterar_dados, name='alterar_dados')
]