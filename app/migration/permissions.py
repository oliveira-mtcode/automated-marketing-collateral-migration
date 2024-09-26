from typing import Dict, Optional
import yaml
from app.config.settings import settings


def load_identity_mappings() -> Dict[str, Dict[str, str]]:
    with open(settings.campaign_keywords_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    identities = data.get("identities", {})
    return {
        "users": identities.get("users", {}),
        "groups": identities.get("groups", {}),
    }


def map_box_identity(box_user_id: Optional[str], box_group_id: Optional[str]) -> Optional[str]:
    mappings = load_identity_mappings()
    if box_user_id and box_user_id in mappings["users"]:
        return mappings["users"][box_user_id]
    if box_group_id and box_group_id in mappings["groups"]:
        return mappings["groups"][box_group_id]
    policy = settings.unmapped_identity_policy
    if policy == "default" and settings.default_target_group_email:
        return settings.default_target_group_email
    return None


