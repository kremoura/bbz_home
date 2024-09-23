from django.urls import path
from cadastro.views import index, escolha_atualizacao

urlpatterns = [
    path('cadastro/', index, name='lgpd'),
    path('escolha/', escolha_atualizacao, name='escolha_atualizacao')
]