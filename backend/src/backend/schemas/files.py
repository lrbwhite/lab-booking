from pydantic import BaseModel


class FileResponse(BaseModel):
    original_filename: str
    disk_name: str
    size: int
    url: str