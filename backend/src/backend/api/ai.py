from fastapi import APIRouter,Depends
from backend.services import ai_service
from backend.common.response import Response
from backend.dependencies.auth import get_current_user
from backend.schemas.aichat import ChatRequest,ChatMessage
from backend.models.user import User


router = APIRouter(prefix="/ai",tags=["LLM对话"])

@router.post("/chat")
def chat(request: ChatRequest,current_user: User = Depends(get_current_user)):
    """LLM对话"""
    message = ai_service.chat(request)
    return Response.success(data=ChatMessage(role="assistant",content=message))
