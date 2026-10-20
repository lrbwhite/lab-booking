from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message:list[ChatMessage]