from django.urls import path
from comum.views import index, gera_token, valida_token, building_list

urlpatterns = [
    path('', index, name='login'),
    path('gerar_token/', gera_token, name='gera_token'),
    path('valida_token/', valida_token, name='valida_token'),
    path('bulding_list/', building_list, name='building_list')
]