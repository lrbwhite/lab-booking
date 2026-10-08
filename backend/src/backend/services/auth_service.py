from sqlalchemy.orm import Session

from backend.common.exceptions import BusinessException
from backend.models.user import User
from backend.schemas.auth import LoginRequest, LoginResponse
from backend.schemas.user import UserResponse
from backend.utils.jwt import create_jwt_token
from backend.utils.password import verify_password


def login(login_request: LoginRequest, db: Session) -> LoginResponse:
    # 从数据库查询用户
    user = db.query(User).filter(User.username == login_request.username).first()
    # 校验密码
    if not user or not verify_password(login_request.password, user.password):
        raise BusinessException(code=404, msg="用户不存在或密码错误")
    # 生成JWT
    token = create_jwt_token(user.id)
    return LoginResponse(token=token, user=UserResponse.model_validate(user))