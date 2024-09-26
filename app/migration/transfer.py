import io
from typing import Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from googleapiclient.http import MediaIoBaseUpload


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=30))
def upload_file_resumable(drive_service, file_metadata: Dict, content_stream: io.BufferedReader, mimetype: Optional[str]) -> Dict:
    media = MediaIoBaseUpload(content_stream, mimetype=mimetype, chunksize=5 * 1024 * 1024, resumable=True)
    request = drive_service.files().create(body=file_metadata, media_body=media, fields="id, name, parents")
    response = None
    while response is None:
        status, response = request.next_chunk()
    return response


