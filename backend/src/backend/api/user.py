from fastapi import APIRouter,Depends
from backend.dependencies.auth import get_current_user
from backend.models.user import User
from backend.schemas.user import UserResponse

router = APIRouter(prefix="/user",tags=["用户信息"])

@router.get("/info")
def get_user_info(current_user: User = Depends(get_current_user)):
    return {
        "code":200,
        "msg":"获取用户信息成功",
        "user":UserResponse.model_validate(current_user)}
