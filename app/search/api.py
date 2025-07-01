from fastapi import FastAPI, Query
from typing import List, Optional
from app.clients.drive_client import get_drive_service
from app.config.settings import settings


app = FastAPI(title="Collateral Search API")


def _build_query(q: Optional[str], labels: Optional[List[str]], mime: Optional[str], text: Optional[str]) -> str:
    parts = ["trashed = false"]
    if labels:
        # appProperties tags contain CSV
        for l in labels:
            parts.append(f"appProperties has {{ key='tags' and value contains '{l}' }}")
    if mime:
        parts.append(f"mimeType contains '{mime}'")
    if text:
        parts.append(f"fullText contains '{text}'")
    if q:
        parts.append(q)
    return " and ".join(parts)


@app.get("/search")
def search(q: Optional[str] = None, labels: Optional[str] = Query(None), mime: Optional[str] = None, text: Optional[str] = None):
    drive = get_drive_service()
    labels_list = labels.split(",") if labels else None
    query = _build_query(q, labels_list, mime, text)
    res = drive.files().list(q=query, fields="files(id, name, mimeType, appProperties)").execute()
    return res.get("files", [])



# tweak 19 at 2025-09-26 19:57:43

# tweak 19 at 2025-09-26 20:00:05
