from typing import List
import os
import requests
from app.clients.drive_client import get_drive_service
from app.config.settings import settings


def notify(msg: str):
    if settings.slack_webhook_url:
        try:
            requests.post(settings.slack_webhook_url, json={"text": msg}, timeout=5)
        except Exception:
            pass


def audit_missing_tags() -> List[str]:
    drive = get_drive_service()
    q = "trashed = false and mimeType != 'application/vnd.google-apps.folder'"
    res = drive.files().list(q=q, fields="files(id, name, appProperties)").execute()
    issues = []
    for f in res.get("files", []):
        props = f.get("appProperties", {})
        if not props.get("tags"):
            issues.append(f"Missing tags: {f['name']} ({f['id']})")
    return issues


def main():
    issues = audit_missing_tags()
    if issues:
        message = "Tagging audit: Found files without tags\n" + "\n".join(issues[:50])
        notify(message)
        print(message)
    else:
        print("Tagging audit: OK")


if __name__ == "__main__":
    main()


