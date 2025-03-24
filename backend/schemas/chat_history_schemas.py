from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatHistoryBase(BaseModel):
    session_id: str
    role: str
    content: str


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistory(ChatHistoryBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(
        from_attributes=True
    )  # Enable ORM conversion and validation
