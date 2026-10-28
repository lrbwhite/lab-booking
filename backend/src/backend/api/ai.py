from fastapi import APIRouter,Depends
from backend.services import ai_service
from backend.common.response import Response
from backend.dependencies.auth import get_current_user
from backend.schemas.aichat import ChatRequest,ChatMessage
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services import async_ai_service
from fastapi.responses import StreamingResponse
import json


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

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest,current_user:User = Depends(get_current_user)):
    """LLM流式对话"""
    generator=async_ai_service.chat_stream(current_user,request)
    async def event_stream():
        async for event in generator:
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )



    