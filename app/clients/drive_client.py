from typing import Optional
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config.settings import settings


SCOPES = [
    "https://www.googleapis.com/auth/drive",
]


def get_drive_service():
    with open(settings.google_service_account_json, "r", encoding="utf-8") as f:
        info = json.load(f)
    credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    if settings.google_impersonate_user:
        credentials = credentials.with_subject(settings.google_impersonate_user)
    service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    return service


