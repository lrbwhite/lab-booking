from backend.models.user import User
from backend.schemas.user import UserResponse, UserUpdater
from sqlalchemy.orm import Session

def get_user_info(user: User)->UserResponse:
    return UserResponse.model_validate(user)

def update_user_info(db: Session, user: User, update_data: UserUpdater):
    user_dict = update_data.model_dump(exclude_none=True)#pydatic 转换为字典
    for key, value in user_dict.items():
        setattr(user, key, value)
    db.commit()
    return UserResponse.model_validate(user)
