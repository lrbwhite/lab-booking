from fastapi import APIRouter,Depends
from backend.services import ai_service
from backend.common.response import Response
from backend.dependencies.auth import get_current_user
from backend.schemas.aichat import ChatRequest,ChatMessage
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.database import get_db


router = APIRouter(prefix="/ai",tags=["LLM对话"])

@router.post("/chat")
def chat(
        request: ChatRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        ):
    """LLM对话"""
    message = ai_service.chat(db,current_user,request)
    return Response.success(data=ChatMessage(role="assistant",content=message))
