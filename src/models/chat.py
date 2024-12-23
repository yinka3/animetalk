import roles
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, Boolean, DateTime
from datetime import datetime
from uuid import uuid4
from database import Base



class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    sender_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    sender: Mapped["roles.Users"] = relationship("Users", foreign_keys=[sender_id], back_populates="sent_messages")
    chat: Mapped["Chats"] = relationship("Chats", back_populates="messages")

class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    members: Mapped[list["ChatMembers"]] = relationship("ChatMembers", back_populates="chat")
    messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="chat")

class ChatMembers(Base):
    __tablename__ = "chat_members"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    chat: Mapped["Chats"] = relationship("Chats", back_populates="members")
    user: Mapped["roles.Users"] = relationship("Users", back_populates="chats")