from backend.models.user import User
from backend.schemas.user import UserResponse, UserUpdater, PasswordUpdateRequest
from sqlalchemy.orm import Session
from backend.common.response import PageResponse


def get_user_info(user: User)->UserResponse:
    return UserResponse.model_validate(user)

def update_user_info(db: Session, user: User, update_data: UserUpdater):
    user_dict = update_data.model_dump(exclude_none=True)#pydatic 转换为字典
    for key, value in user_dict.items():
        setattr(user, key, value)
    db.commit()
    return UserResponse.model_validate(user)

def update_password(db: Session, user: User,data: PasswordUpdateRequest):
    if not verify_password(data.old_password, user.password):
        raise BusinessException("旧密码错误")
    if data.new_password == data.old_password:
        raise BusinessException("新密码不能与旧密码相同")
    user.password = hash_password(data.new_password)
    db.commit()

def get_user_page_list(db: Session, page: int, page_size: int,username:str|None=None)->PageResponse:
    """分页查询用户"""
    query = db.query(User)
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    total = query.count()
    item=(
        query.order_by(User.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all() 
        )
    return PageResponse(list=[UserResponse.model_validate(user) for user in item],total=total)
 