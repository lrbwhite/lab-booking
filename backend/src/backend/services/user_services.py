from backend.models.user import User
from backend.schemas.user import UserResponse, UserUpdater, PasswordUpdateRequest
from sqlalchemy.orm import Session
from backend.common.response import PageResponse
from backend.common.exceptions import BusinessException
from backend.utils.password import hash_password, verify_password


def get_user_info(user: User)->UserResponse:
    return UserResponse.model_validate(user)

def update_user_info(db: Session, user: User, update_data: UserUpdater):
    user_dict = update_data.model_dump(exclude_none=True,exclude=["role","status"])#pydatic 转换为字典
    for key, value in user_dict.items():
        setattr(user, key, value)
    db.commit()
    return UserResponse.model_validate(user)

def update_password(db: Session, user: User,data: PasswordUpdateRequest):
    if not verify_password(data.old_password, user.password):
        raise BusinessException(code=400, msg="旧密码错误")
    if data.new_password == data.old_password:
        raise BusinessException(code=400, msg="新密码不能与旧密码相同")
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
 

def create_user(db: Session, data: UserCreateRequest):
    """创建用户"""
    exist_user = db.query(User).filter(User.username == data.username).first()
    if exist_user:
        raise BusinessException(code=400, msg="用户名已存在")

    user=User(
        username=data.username,
        password=hash_password(data.password),
        role=data.role,
        name=data.name,
        email=data.email,
        phone=data.phone,
        avatar=data.avatar,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

def update_user(db: Session, user_id: int, data: UserUpdater):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(code=404, msg="用户不存在")
    payload = data.model_dump(exclude_none=True)
    for field,value in payload.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

def delete_user(db: Session, user_id: int,current_user: User):
    """删除用户"""
    if user_id == current_user.id:
        raise BusinessException(code=400, msg="不能删除当前登录用户")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(code=404, msg="用户不存在")
    db.delete(user)
    db.commit()
