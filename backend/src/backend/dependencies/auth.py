from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from backend.utils.jwt import decode_jwt_token
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> User:
    
    payload = decode_jwt_token(token)
    if "user_id" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=payload.get("msg","token无效"))
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="用户不存在") 
    return user
