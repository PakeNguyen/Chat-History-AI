import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UserMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=20000)

class MessageRead(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
