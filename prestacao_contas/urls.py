from django.urls import path
from prestacao_contas.views import list_drive_files, pasta_prest_conta, pasta_vazia

urlpatterns = [
    path('arquivos/ojfwjIJHU/', list_drive_files, name='list_drive_files'),
    path('arquivos/pasta_prest_conta/', pasta_prest_conta, name='pasta_prest_conta'),
    path('arquivos/pasta_vazia/', pasta_vazia, name='pasta_vazia'),
]