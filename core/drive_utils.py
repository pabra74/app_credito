import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def autenticar_drive():
    creds_path = os.getenv("GOOGLE_CREDS_JSON_PATH", "credentials.json")
    creds = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

def upload_para_drive(file_path, nome_arquivo=None, pasta_id=None):
    service = autenticar_drive()
    nome = nome_arquivo if nome_arquivo else os.path.basename(file_path)

    file_metadata = {
        "name": nome,
        "parents": [pasta_id] if pasta_id else []
    }

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return file.get("id")
