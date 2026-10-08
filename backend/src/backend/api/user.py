from fastapi import APIRouter, Depends

from backend.common.response import Response
from backend.dependencies.auth import get_current_user,get_current_admin
from backend.models.user import User
from backend.services import user_services
from backend.schemas.user import UserCreateRequest, UserUpdater,PasswordUpdateRequest
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

@router.get("/list")
def get_user_list(
        page: int = 1,
        page_size: int = 10,
        username: str | None = None,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        res=user_services.get_user_page_list(db, page, page_size, username)
        return Response.success(data=res)

@router.post("")
def create_user(
    data:UserCreateRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    res=user_services.create_user(db, data)
    return Response.success(data=res)

@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdater,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    res=user_services.update_user(db, user_id, data)
    return Response.success(data=res)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user_services.delete_user(db, user_id, current_user)
    return Response.success()
