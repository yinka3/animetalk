from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from sqlalchemy import UUID
from src.models import ChatMembers
from src.utils import ChatType, MessageType


class CreateChat(BaseModel):
    chat_id: UUID
    creator_id: UUID
    creator_username: str
    name: Optional[str] = None
    chat_type: Optional[ChatType]

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    name: str
    members: List[ChatMembers]

    class Config:
        from_attributes = True


class CreateMessage(BaseModel):
    id: UUID
    chat_id: UUID
    user_id: UUID
    content: str
    sent_at: datetime
    type: MessageType = MessageType.NEW_MESSAGE

    class Config:
        from_attributes = True


class AddChatMember(BaseModel):
    chat_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class RemoveChatMember(AddChatMember):
    pass


class ChatMemberResponse(BaseModel):
    chat_id: UUID
    user_id: UUID
    username: str

    class Config:
        from_attributes = True


class RemoveChatMemberResponse(BaseModel):
    chat_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
