from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    title: Optional[str] = None
    ai_role: Optional[str] = None
    ai_personality: Optional[str] = None
    ai_region: Optional[str] = None

class ConversationUpdate(BaseModel):
    ai_role: Optional[str] = None
    ai_personality: Optional[str] = None
    ai_region: Optional[str] = None

class Conversation(BaseModel):
    id: int
    title: str
    ai_role: str = "小美"
    ai_personality: str = "温柔体贴的妹子"
    ai_region: str = "广西"
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True

class ConversationListItem(BaseModel):
    id: int
    title: str
    ai_role: str = "小美"
    ai_personality: str = "温柔体贴的妹子"
    ai_region: str = "广西"
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    content: str

class ChatResponse(BaseModel):
    reply: str
    user_message: Message
    assistant_message: Message

class StopResponse(BaseModel):
    message: str