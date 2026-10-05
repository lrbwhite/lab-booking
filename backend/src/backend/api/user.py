from fastapi import APIRouter, Depends

from backend.common.response import Response
from backend.dependencies.auth import get_current_user
from backend.models.user import User
from backend.services import user_services
from backend.schemas.user import UserUpdater, PasswordUpdateRequest
from backend.database import get_db
from sqlalchemy.orm import Session



router = APIRouter(prefix="/user", tags=["用户信息"])


@router.get("/me")
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取用户信息"""
    return Response.success(data=user_services.get_user_info(current_user))

@router.put("/me")
def update_user_info(
    data: UserUpdater,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新用户信息"""
    res=user_services.update_user_info(db, current_user, data)
    return Response.success(data=res)

@router.put("/password")
def update_password(
    data: PasswordUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新用户密码"""
    user_services.update_password(db, current_user, data)
    return Response.success()
