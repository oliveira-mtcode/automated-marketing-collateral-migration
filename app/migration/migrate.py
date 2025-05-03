import io
from typing import Dict, List
from app.clients.box_client import get_box_client
from app.clients.drive_client import get_drive_service
from app.config.settings import settings
from app.migration.permissions import map_box_identity
from app.migration.transfer import upload_file_resumable


def ensure_drive_folder(drive_service, parent_id: str, name: str) -> str:
    q = f"name = '{name.replace("'", "\\'")}' and '{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    res = drive_service.files().list(q=q, fields="files(id, name)").execute()
    items = res.get("files", [])
    if items:
        return items[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    folder = drive_service.files().create(body=meta, fields="id").execute()
    return folder["id"]


def set_drive_permissions(drive_service, file_id: str, box_permissions: List[Dict]):
    for perm in box_permissions:
        target_email = map_box_identity(perm.get("box_user_id"), perm.get("box_group_id"))
        if not target_email:
            continue
        role = perm.get("role", settings.default_permission_role)
        body = {"type": "user", "role": role, "emailAddress": target_email}
        try:
            drive_service.permissions().create(fileId=file_id, body=body, sendNotificationEmail=False).execute()
        except Exception:
            continue


def migrate_folder_recursive(box_client, drive_service, box_folder, drive_parent_id: str):
    drive_folder_id = ensure_drive_folder(drive_service, drive_parent_id, box_folder.name)

    # Apply folder permissions mapping (simplified placeholder; actual Box permission extraction needed)
    # set_drive_permissions(drive_service, drive_folder_id, box_folder_permissions)

    items = box_folder.get_items(limit=1000)
    for item in items:
        if item.type == "folder":
            migrate_folder_recursive(box_client, drive_service, item, drive_folder_id)
        else:
            stream = io.BytesIO()
            item.download_to(stream)
            stream.seek(0)
            mimetype = item.content_created_at and item.get().get("content_type") or None
            metadata = {"name": item.name, "parents": [drive_folder_id]}
            created = upload_file_resumable(drive_service, metadata, stream, mimetype)
            # TODO: capture permissions per file and map


def main():
    box = get_box_client()
    drive = get_drive_service()
    root_folder = box.folder(folder_id=settings.box_root_folder_id).get()
    drive_root = settings.drive_root_folder_id
    if not drive_root:
        # fallback to Drive root of impersonated user
        about = drive.about().get(fields="rootFolderId").execute()
        drive_root = about["rootFolderId"]
    migrate_folder_recursive(box, drive, root_folder, drive_root)


if __name__ == "__main__":
    main()



# tweak 15 at 2025-09-26 19:57:42

# tweak 15 at 2025-09-26 20:00:03
