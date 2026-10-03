from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.common.response import Response
from backend.database import get_db
from backend.schemas.auth import LoginRequest, LoginResponse
from backend.services import auth_service

router = APIRouter(prefix="/auth", tags=["权限验证"])


@router.post("/login", response_model=Response[LoginResponse])
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """登录接口"""
    result = auth_service.login(login_request, db)
    return Response(code=200, msg="登录成功", data=result)