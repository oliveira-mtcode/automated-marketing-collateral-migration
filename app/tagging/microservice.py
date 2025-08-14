from fastapi import FastAPI
from pydantic import BaseModel
from app.clients.drive_client import get_drive_service
from app.tagging.engine import tag_image_bytes
from app.config.settings import settings
import base64


app = FastAPI(title="Tagging Microservice")


class TagRequest(BaseModel):
    file_id: str


@app.post("/tag")
def tag_file(req: TagRequest):
    drive = get_drive_service()
    file = drive.files().get(fileId=req.file_id, fields="id, name, mimeType").execute()
    mime = file["mimeType"]
    if mime.startswith("image/"):
        data = drive.files().get_media(fileId=req.file_id).execute()
        tags = tag_image_bytes(data)
        # Store in appProperties
        props = {"tags": ",".join(sorted(set(tags.get("labels", []) + tags.get("logos", []) + tags.get("campaign", []))))}
        drive.files().update(fileId=req.file_id, body={"appProperties": props}).execute()
        return {"status": "tagged", "tags": props}
    return {"status": "skipped", "reason": "unsupported mime"}



# tweak 22 at 2025-09-26 19:57:45

# tweak 22 at 2025-09-26 20:00:06
