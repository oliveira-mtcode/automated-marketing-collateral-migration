import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    box_client_id: Optional[str] = os.getenv("BOX_CLIENT_ID")
    box_client_secret: Optional[str] = os.getenv("BOX_CLIENT_SECRET")
    box_enterprise_id: Optional[str] = os.getenv("BOX_ENTERPRISE_ID")
    box_jwt_private_key: Optional[str] = os.getenv("BOX_JWT_PRIVATE_KEY")
    box_jwt_private_key_id: Optional[str] = os.getenv("BOX_JWT_PRIVATE_KEY_ID")
    box_jwt_passphrase: Optional[str] = os.getenv("BOX_JWT_PASSPHRASE")

    google_service_account_json: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "./secrets/service_account.json")
    google_impersonate_user: Optional[str] = os.getenv("GOOGLE_IMPERSONATE_USER")
    gcp_project_id: Optional[str] = os.getenv("GCP_PROJECT_ID")

    box_root_folder_id: str = os.getenv("BOX_ROOT_FOLDER_ID", "0")
    drive_root_folder_id: Optional[str] = os.getenv("DRIVE_ROOT_FOLDER_ID")

    default_permission_role: str = os.getenv("DEFAULT_PERMISSION_ROLE", "reader")
    unmapped_identity_policy: str = os.getenv("UNMAPPED_IDENTITY_POLICY", "skip")
    default_target_group_email: Optional[str] = os.getenv("DEFAULT_TARGET_GROUP_EMAIL")

    tagging_max_concurrency: int = int(os.getenv("TAGGING_MAX_CONCURRENCY", "4"))
    campaign_keywords_file: str = os.getenv("CAMPAIGN_KEYWORDS_FILE", "app/config/mappings.yaml")

    search_bind_host: str = os.getenv("SEARCH_BIND_HOST", "0.0.0.0")
    search_bind_port: int = int(os.getenv("SEARCH_BIND_PORT", "8080"))

    tagging_bind_host: str = os.getenv("TAGGING_BIND_HOST", "0.0.0.0")
    tagging_bind_port: int = int(os.getenv("TAGGING_BIND_PORT", "8081"))

    admin_emails: Optional[str] = os.getenv("ADMIN_EMAILS")
    slack_webhook_url: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")


settings = Settings()


