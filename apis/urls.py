from django.urls import path
from apis.views import buscar_emails, ficha_cadastral_unidade

urlpatterns = [
    path('api/', buscar_emails, name='buscar_emails'),
    path('atualizar_form_proprietario/', ficha_cadastral_unidade, name='atualizar_form_proprietario'),
]