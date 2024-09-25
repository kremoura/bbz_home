from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly'
]

def get_gdrive_service():
    creds = None
    token_path = os.path.join(settings.BASE_DIR, 'token.json')

    # Tente carregar o token salvo do usuário
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Se não tiver credenciais válidas, faça a autenticação OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_DRIVE_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salve as credenciais para uso futuro
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def list_drive_files(request):
    # Conecte-se ao Google Drive
    service = get_gdrive_service()

    # Liste os arquivos
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        return HttpResponse("No files found.")
    else:
        # Retorne os arquivos como uma lista HTML
        file_list = "<ul>"
        for item in items:
            file_list += f"<li>{item['name']} (ID: {item['id']})</li>"
        file_list += "</ul>"

    return HttpResponse(file_list)
    

                
