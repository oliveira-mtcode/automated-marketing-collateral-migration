import json
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud import videointelligence_v1 as videointelligence
from app.config.settings import settings


def get_gcp_credentials():
    with open(settings.google_service_account_json, "r", encoding="utf-8") as f:
        info = json.load(f)
    return service_account.Credentials.from_service_account_info(info)


def get_vision_client() -> vision.ImageAnnotatorClient:
    creds = get_gcp_credentials()
    return vision.ImageAnnotatorClient(credentials=creds)


def get_video_intel_client() -> videointelligence.VideoIntelligenceServiceClient:
    creds = get_gcp_credentials()
    return videointelligence.VideoIntelligenceServiceClient(credentials=creds)


