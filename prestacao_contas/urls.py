from django.urls import path
from prestacao_contas.views import get_gdrive_service, list_drive_files

urlpatterns = [
    path('arquivos/ojfwjIJHU', list_drive_files, name='list_drive_files')
]