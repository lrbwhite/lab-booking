from backend.models.user import User
from backend.schemas.user import UserResponse

def get_user_info(user: User)->UserResponse:
    return UserResponse.model_validate(user)