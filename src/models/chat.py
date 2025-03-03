from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, Boolean, DateTime, func, Enum
from datetime import datetime
from uuid import uuid4
from src.database import Base
from src.utils import ChatType, MessageType

if TYPE_CHECKING:
    from src.models.roles import Users


class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(),
                                                 onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    chat_type: Mapped[ChatType] = mapped_column(Enum(ChatType), nullable=False, default=ChatType.PRIVATE)

    owner: Mapped["Users"] = relationship("Users", back_populates="created_chats")
    members: Mapped[list["ChatMembers"]] = relationship("ChatMembers", back_populates="chat")
    messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="chat")


class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"),
                                          nullable=False)  # Single FK to Users
    content: Mapped[str] = mapped_column(String, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    type: Mapped[MessageType] = mapped_column(MessageType, default=MessageType.NEW_MESSAGE)

    user: Mapped["Users"] = relationship("Users", back_populates="messages")
    chat: Mapped["Chats"] = relationship("Chats", back_populates="messages")


class ChatMembers(Base):
    __tablename__ = "chat_members"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    chat: Mapped["Chats"] = relationship("Chats", back_populates="members")
    user: Mapped["Users"] = relationship("Users", back_populates="chats")
