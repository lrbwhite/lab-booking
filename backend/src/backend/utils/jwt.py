import datetime

import jwt

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
    解码JWT token
    """
    try:
        return jwt.decode(token, config.jwt_secret_key, algorithms=[config.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        return {"code": 401, "msg": "token过期"}
    except jwt.InvalidTokenError:
        return {"code": 401, "msg": "token无效"}