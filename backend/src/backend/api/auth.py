from fastapi import APIRouter,Depends
from backend.schemas.auth import LoginRequest
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user import UserResponse



router = APIRouter(prefix="/api/auth",tags=["权限验证"])

@router.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # 从数据库查询用户
    user = db.query(User).filter(User.username == login_request.username).first()
    if not user or user.password != login_request.password:
        return {"code":404,"msg":"用户不存在或密码错误"}

    # 登录成功，返回用户信息
    return {"code":200,"msg":"登录成功","data":UserResponse.model_validate(user)}
