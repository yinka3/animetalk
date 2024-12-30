from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, Enum, UUID, LargeBinary, Text, String, Boolean, DateTime, Integer
from datetime import datetime
from uuid import uuid4
from database import Base
from src.utils import ContentType
import roles

class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    parent_comment_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    user_id: Mapped[UUID] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    post_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=True)
    fanArt_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fanArts.id"), nullable=True)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType), nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index("idx_content_id", "content_id"),
        Index("idx_parent_comment_id", "parent_comment_id"),
    )

    parent_comment: Mapped["Comments"] = relationship("Comments", remote_side=[id], backref="replies")
    user_comments: Mapped["roles.Users"] = relationship("Users", back_populates="comments")
    post: Mapped["Posts"] = relationship("Posts", back_populates="comments")
    fanArt: Mapped["FanArts"] = relationship("FanArts", back_populates="comments")

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["roles.Users"] = relationship("Users", back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="post", cascade="all, delete-orphan")

class FanArts(Base):
    __tablename__ = "fanArts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user: Mapped["roles.Users"] = relationship("User", back_populates="arts")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="fanArt", cascade="all, delete-orphan")


class SavedContents(Base):
    __tablename__ = "saved_contents"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)  # ID of the saved content
    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    user: Mapped["roles.Users"] = relationship("Users", back_populates="saved_contents")

class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    tagged_user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)  # Reference to Post or FanArt ID
    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType), nullable=False)  # Use ContentType Enum
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    tagged_user: Mapped["roles.Users"] = relationship("User", back_populates="tags_received")

    # @property
    # def content(self):
    #     """Dynamically fetch the related content (Post or FanArt) based on content_type."""
    #     if self.content_type == ContentType.POST:
    #         return session.query(Posts).filter_by(id=self.content_id).first()
    #     elif self.content_type == ContentType.FANART:
    #         return session.query(FanArts).filter_by(id=self.content_id).first()
    #     return None

class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey("sellers.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("buyers.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    seller_review: Mapped["roles.Sellers"] = relationship("Sellers", back_populates="reviews")
    buyer_review: Mapped["roles.Buyers"] = relationship("Buyers", back_populates="reviews")
    reviewer: Mapped["roles.Users"] = relationship("Users", back_populates="reviews_given")