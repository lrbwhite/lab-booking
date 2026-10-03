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
