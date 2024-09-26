from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from django.conf import settings
import os

gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('bin/jfueojFESF/uioe9j3mej/credentials.json', scope)
drive = GoogleDrive(gauth)
arquivos = drive.ListFile({'q': "'0By6djoRj_4OYN1RMVloyRmttNEU' in parents and trashed=false"}).GetList()
for arquivo in arquivos:
    # print(url_base)
    print(f"nome: {arquivo['title']}, id: {arquivo['id']}")