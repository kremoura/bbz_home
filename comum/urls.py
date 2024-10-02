from django.urls import path
from comum.views import index, gera_token, listar_emails_escondidos, valida_email, error, bbz_home

urlpatterns = [
    path('', index, name='login'),
    path('valida_email/', valida_email, name='valida_email'),
    path('bbzhome/', bbz_home, name='bbz_home'),
    path('lista_emails_cadastrados/', listar_emails_escondidos, name='listar_emails_escondidos'),
    path('enviar_token/', gera_token, name='gera_token'), 
    path('error/', error, name='error'),
]