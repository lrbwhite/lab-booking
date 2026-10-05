from pydantic import BaseModel,ConfigDict

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    name: str
    email: str
    phone: str|None=None
    avatar: str|None=None
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdater(BaseModel):
    name: str|None=None
    email: str|None=None
    phone: str|None=None
    avatar: str|None=None


class PasswordUpdateRequest(BaseModel):
    """修改密码的请求参数"""
    old_password: str
    new_password: str