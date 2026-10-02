import datetime

import jwt
from fastapi import HTTPException, status

from backend.config import config


def create_jwt_token(user_id: int) -> str:
    """
    创建JWT token
    """
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=config.jwt_expire_time
    )
    payload = {"exp": expire, "user_id": user_id}
    return jwt.encode(payload, config.jwt_secret_key, algorithm=config.jwt_algorithm)


def decode_jwt_token(token: str) -> dict:
    """
    解码JWT token，失败时抛出 401 异常
    """
    try:
        return jwt.decode(token, config.jwt_secret_key, algorithms=[config.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token无效",
            headers={"WWW-Authenticate": "Bearer"},
        )