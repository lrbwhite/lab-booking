from pydantic import BaseModel
from backend.schemas.user import UserResponse

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: UserResponse