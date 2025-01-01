from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, Boolean, DateTime
from datetime import datetime
from uuid import uuid4
from src.database import Base

if TYPE_CHECKING:
    from src.models.roles import Users

class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    members: Mapped[list["ChatMembers"]] = relationship("ChatMembers", back_populates="chat")
    messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="chat")

class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Single FK to Users
    content: Mapped[str] = mapped_column(String, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    is_sender: Mapped[bool] = mapped_column(Boolean, nullable=False)  # True if sender, False if receiver
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["Users"] = relationship("Users", back_populates="messages")
    chat: Mapped["Chats"] = relationship("Chats", back_populates="messages")

class ChatMembers(Base):
    __tablename__ = "chat_members"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    chat: Mapped["Chats"] = relationship("Chats", back_populates="members")
    user: Mapped["Users"] = relationship("Users", back_populates="chats")