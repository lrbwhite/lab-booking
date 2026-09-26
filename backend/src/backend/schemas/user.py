from pydantic import BaseModel,ConfigDict

class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str
    name: str
    email: str
    phone: str|None=None
    avatar: str|None=None
    
    model_config = ConfigDict(from_attributes=True)