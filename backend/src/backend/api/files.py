from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import time
import os
import shutil
from backend.config import UPLOAD_DIR, MAX_UPLOAD_SIZE, ALL_ALLOWED_EXTENSIONS
from backend.common.exceptions import BusinessExceptionException
from backend.common.response import Response



router = APIRouter(prefix="/files",tags=["文件管理"])

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """文件上传接口"""
    if not file.filename:
        raise BusinessExceptionException(code=400, msg="文件名不能为空")
    #原始文件名 用户头像.jpg
    original_filename = os.path.basename(file.filename)
    #文件后缀 .jpg
    ext=Path(original_filename).suffix.lower()
    if ext not in ALL_ALLOWED_EXTENSIONS:
        raise BusinessExceptionException(code=400, msg=f"文件后缀 {ext} 不被允许")
    #文件大小
    if file.size and file.size > MAX_UPLOAD_SIZE:
        raise BusinessExceptionException(code=400, msg=f"文件大小不能超过 {MAX_UPLOAD_SIZE//1024//1024} MB")
    #设置唯一文件名
    disk_name=f"{int(time.time()*1000)}{ext}"
    #文件存储实际路径
    upload_path =UPLOAD_DIR / disk_name
    #流式写入文件到指定路径
    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return Response.success(data={
        "original_filename": original_filename,
        "disk_name": disk_name,
        "size": file.size,
        "url": f"/uploads/{disk_name}",
    })

