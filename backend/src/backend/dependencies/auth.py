from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from backend.utils.jwt import decode_jwt_token
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> User:
    
    try:
        payload = decode_jwt_token(token)

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token无效")
    user_id = payload["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_UNAUTHORIZED,detail="用户不存在") 
    return user
