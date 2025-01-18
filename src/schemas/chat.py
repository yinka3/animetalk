from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from sqlalchemy import UUID
from src.models import ChatMembers
from src.utils import ChatType


class CreateChat(BaseModel):
    chat_id: UUID
    creator_id: UUID
    creator_username: str
    name: Optional[str] = None
    chat_type: Optional[ChatType]

    class Config:
        orm_mode = True

class ChatResponse(BaseModel):
    name: str
    members: List[ChatMembers]

    class Config:
        orm_mode = True

class CreateMessage(BaseModel):
    chat_id: UUID
    user_id: UUID
    content: str
    sent_at: datetime

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    chat_id: UUID
    user_id: UUID
    content: str
    is_read: bool

    class Config:
        orm_mode = True

class UpdateMessage(BaseModel):
    chat_id: UUID
    user_id: UUID
    content: str
    updated_at: datetime

    class Config:
        orm_mode = True

class AddChatMember(BaseModel):
    chat_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True

class ChatMemberResponse(BaseModel):
    chat_id: UUID
    user_id: UUID
    username: str

    class Config:
        orm_mode = True

class RemoveChatMemberResponse(BaseModel):
    chat_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


