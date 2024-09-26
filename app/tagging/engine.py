from typing import Dict, List
import base64
from google.cloud.vision import types as vision_types  # type: ignore
from app.clients.gcp_clients import get_vision_client, get_video_intel_client
from app.config.settings import settings
import yaml


def _load_campaign_keywords() -> List[str]:
    with open(settings.campaign_keywords_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return list(data.get("campaign_keywords", []))


def tag_image_bytes(content: bytes) -> Dict:
    vision = get_vision_client()
    image = {"content": content}

    responses = {}
    label_resp = vision.label_detection(request={"image": image})
    logo_resp = vision.logo_detection(request={"image": image})
    text_resp = vision.text_detection(request={"image": image})

    responses["labels"] = [l.description for l in label_resp.label_annotations or []]
    responses["logos"] = [l.description for l in logo_resp.logo_annotations or []]
    responses["text"] = (text_resp.full_text_annotation.text if text_resp.full_text_annotation else "")

    # Campaign keyword extraction
    keywords = _load_campaign_keywords()
    text_lower = responses.get("text", "").lower()
    responses["campaign"] = [k for k in keywords if k.replace("_", " ") in text_lower]
    return responses


def tag_video_gcs_uri(gcs_uri: str) -> Dict:
    video_client = get_video_intel_client()
    features = [
        1,  # LABEL_DETECTION
        3,  # LOGO_RECOGNITION
        9,  # EXPLICIT_CONTENT_DETECTION
    ]
    op = video_client.annotate_video(input_uri=gcs_uri, features=features)
    result = op.result(timeout=600)
    labels = []
    logos = []
    for a in result.annotation_results:
        labels.extend([l.entity.description for l in a.segment_label_annotations])
        logos.extend([l.entity.description for l in getattr(a, "logo_recognition_annotations", [])])
    return {"labels": list(set(labels)), "logos": list(set(logos))}


