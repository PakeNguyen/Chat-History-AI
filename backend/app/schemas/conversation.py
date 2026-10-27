import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.message import MessageRead

class ConversationCreate(BaseModel):
    title: str = Field(default="Cuộc trò chuyện mới", min_length=1, max_length=200)

class ConversationRead(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatResponse(BaseModel):
    conversation_id: str
    user_message: MessageRead
    assistant_message: MessageRead