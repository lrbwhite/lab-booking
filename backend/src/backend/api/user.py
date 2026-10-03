from fastapi import APIRouter, Depends

from backend.common.response import Response
from backend.dependencies.auth import get_current_user
from backend.models.user import User
from backend.schemas.user import UserResponse
from backend.services.user_services import get_user_info

router = APIRouter(prefix="/user", tags=["用户信息"])


@router.get("/info")
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取用户信息"""
    return Response.success(data=get_user_info(current_user))