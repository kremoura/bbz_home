from django.http import HttpResponse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import render


def pasta_prest_conta(request):
    service = get_service_account_drive_service()

    is_search = 0

    if request.method == 'POST':
        is_search = request.POST.get('is_search')

    if is_search:
        partial_name = request.POST.get('search')
        folder_id = request.POST.get('folder_id')

        items = search_partial_name(service, partial_name, folder_id)
    else:
        # Defina o ID da pasta específica do Google Drive
        #folder_id = '0By6djoRj_4OYN1RMVloyRmttNEU'  # Substitua este valor pelo ID da pasta desejada
        folder_id = request.GET.get('folder_id')

        items = list_drive_files(request, service, folder_id)

    folder_name_item = get_folder_name(service, folder_id)

    folders_tree = []
    folders = []
    files = []

    #lista a pasta mãe( Pasta Nuvem )
    folder_id_mother = '0By6djoRj_4OYN1RMVloyRmttNEU'
    folders_tree = get_folder_hierarchy_until_target(service, folder_id, folder_id_mother)

    qtd = 0
    
    if not items:
        return "Deu ruim"
    else:
        for item in items:
            permissions = item.get("permissions", [])
            is_public = False

            for permission in permissions:
                if permission['type'] == 'anyone':
                    qtd = qtd + 1

                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        folders.append(item)
                    else:
                        files.append(item)
       
    return render(request, 'prestacao_contas/folders.html', {'folders': folders, 'files': files, 'qtd_registros': qtd, 'folder_name': folder_name_item, 'folders_tree': folders_tree})

# Escopo necessário para acessar os arquivos do Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_folder_name(service, folder_id):
    try:
        folder = service.files().get(
            fileId=folder_id, fields='name, size, id'
        ).execute
        return folder
    except:
        return "deu errado"
    
def get_just_folder_name(service, folder_id):

        results = service.files().get(
            fileId=folder_id, fields='name, id, parents'
        ).execute

        return results()
    
def get_folder_hierarchy_until_target(service, file_id, stop_folder_id):
    
    folder_id_name_hierarchy = []

    try:
        current_folder_id = file_id

        while current_folder_id:
            # Obter a pasta atual e seu pai
            file = service.files().get(
                fileId=current_folder_id,
                fields="id, name, parents"
            ).execute()

            # Adicionar o nome da pasta à lista
            final = {'name': file['name'], 'id': file['id']}
            folder_id_name_hierarchy.append(final)

            # Verificar se a pasta atual é a pasta de parada
            if current_folder_id == stop_folder_id:
                break

            # Verificar se a pasta tem um pai
            if 'parents' in file:
                # Atualizar o ID para o próximo pai
                current_folder_id = file['parents'][0]
            else:
                # Se não houver pais, estamos na pasta raiz
                current_folder_id = None

        # Inverter a lista para começar da pasta de parada até a pasta atual
        folder_id_name_hierarchy.reverse()

        return folder_id_name_hierarchy

    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"


def get_service_account_drive_service():
    # Autentica usando a conta de serviço
    creds = Credentials.from_service_account_file(
        settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # Conecta ao serviço do Google Drive
    service = build('drive', 'v3', credentials=creds)
    return service

# Função recursiva para listar arquivos dentro de uma pasta e suas subpastas
def list_files_in_folder(service, folder_id):
    # Lista todos os arquivos e subpastas da pasta atual
    query = f"'{folder_id}' in parents"
    results = service.files().list(
        q=query, fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, webViewLink, webContentLink)"
    ).execute()
    
    items = results.get('files', [])
    file_list = []

    for item in items:
        # Se o item for uma pasta, busca recursivamente
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            file_list.append(
                f"<a href='{item['webViewLink']}'><li>📁 {item['name']} (Folder ID: {item['id']} Criado em: {item['createdTime']} Modificado em: {item['modifiedTime']}  )</li></a>"
                )
            subfolder_files = list_files_in_folder(service, item['id'])
            if subfolder_files:
                file_list.append("<ul>")
                file_list.extend(subfolder_files)
                file_list.append("</ul>")
        else:
            # Se for um arquivo, apenas adiciona à lista
            file_list.append(f"<a href='{item['webViewLink']}'><<li>{item['name']} (File ID: {item['id']} Criado em: {item['createdTime']} Modificado em: {item['modifiedTime']}  )</li></a>")
    
    return file_list

def list_drive_files_recursive(request):
    service = get_service_account_drive_service()

    # Defina o ID da pasta específica do Google Drive
    folder_id = '0By6djoRj_4OYN1RMVloyRmttNEU'  # Substitua este valor pelo ID da pasta desejada

    try:
        
        # Lista arquivos e subpastas da pasta raiz especificada
        file_list = list_files_in_folder(service, folder_id)

        

        if not file_list:
            return HttpResponse("No files found in the specified folder...")
        
        # Retorna os arquivos e pastas como uma lista HTML recursiva
        html_output = "<ul>" + "".join(file_list) + "</ul>"
        return HttpResponse(html_output)
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
    
def list_drive_files(request, service, folder_id):

    # Faz a listagem dos arquivos dentro da pasta especificada
    query = f"'{folder_id}' in parents and visibility != 'limited'"

    # Liste os arquivos
    results = service.files().list(
        q=query, fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, webViewLink, size, permissions, parents, webContentLink)"
    ).execute()

    items = results.get('files', [])

    if not items:
        return False
    else:
        return items
    
def search_partial_name(service, partial_name, folder_id):
   
    query = f"name contains '{partial_name}' and '{folder_id}' in parents and visibility != 'limited'"
        
    results = service.files().list(
        q=query, fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, webViewLink, size, permissions, parents, webContentLink)"
    ).execute()

    items = results.get('files', [])

    if not items:
        return False
    else:
        return items


        
        
