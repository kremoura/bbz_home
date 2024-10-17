from django.urls import path
from cadastro.views import cad_index, escolha_atualizacao, alterar_dados, alterar_proprietario, alterar_locatario, teste_km, cria_sessao_form_passo1

urlpatterns = [
    path('cadastro/', cad_index, name='cad_index'),
    path('cadastro/ujeFES/', escolha_atualizacao, name='escolha_atualizacao'),
    path('cadastro/ukeuOJOU/', alterar_dados, name='alterar_dados'),
    path('cadastro/ukeuOJuu/', alterar_proprietario, name='alterar_proprietario'),
    path('cadastro/ukeuOJoo/', alterar_locatario, name='alterar_locatario'),
    path('cadastro/teste/', teste_km, name='teste_km'),
    path('cadastro/passo1/', cria_sessao_form_passo1, name='cria_sessao_form_passo1'),
]