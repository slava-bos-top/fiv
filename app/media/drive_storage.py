import json
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from oauth2client.service_account import ServiceAccountCredentials
from config import Config

def get_drive_service():
    scope = ["https://www.googleapis.com/auth/drive"]
    cred_dict = json.loads(Config.GOOGLE_CREDENTIALS)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    return build("drive", "v3", credentials=creds)

def download_json(file_id: str) -> list | dict:
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buffer.seek(0)
    return json.loads(buffer.read().decode("utf-8"))

def upload_json(file_id: str, data: list | dict):
    service = get_drive_service()
    buffer = io.BytesIO(
        json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8")
    )
    media = MediaIoBaseUpload(buffer, mimetype="application/json")
    service.files().update(fileId=file_id, media_body=media).execute()
