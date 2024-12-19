from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import Table, ForeignKey, Index, Enum, UUID, LargeBinary, Float, JSON, Text, String, Boolean, DateTime, \
    Integer, Column
from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4
from database import Base


class UserRole(PyEnum):
    BUYER = "buyer"
    SELLER = "seller"
    BOTH = "both"
    NONE = "none"

class ContentType(PyEnum):
    POST = "post"
    FANART = "fanart"
    COMMENT = "comment"

class OrderStatus(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INPROGRESS = "inprogress"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

buyer_seller = Table(
    "buyer_seller",
    Base.metadata,
    Column("buyer_id", UUID(as_uuid=True), ForeignKey("buyers.id"), primary_key=True),
    Column("seller_id", UUID(as_uuid=True), ForeignKey("sellers.id"), primary_key=True),
)

class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hashed: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    buyer_profile: Mapped["Buyers"] = relationship("Buyers", back_populates="user", uselist=False)
    seller_profile: Mapped["Sellers"] = relationship("Sellers", back_populates="user", uselist=False)
    reviews_given: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="reviewer")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="user_comments")
    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="user")
    arts: Mapped[list["FanArts"]] = relationship("FanArts", back_populates="user")
    tags_received: Mapped[list["Tags"]] = relationship("Tags", back_populates="tagged_user", cascade="all, delete-orphan")
    teams: Mapped[list["TeamMembers"]] = relationship("TeamMembers", back_populates="user")
    sent_messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="sender")
    received_messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="receiver")
    chat: Mapped[list["ChatMembers"]] = relationship("ChatMembers", back_populates="user")

class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tagged_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType), nullable=False)
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index("idx_content_type_content_id", "content_type", "content_id"),
    )

    tagged_user: Mapped["User"] = relationship(back_populates="tags_received")

class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    buyer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("buyers.id"), nullable=False)
    seller_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sellers.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    description: Mapped[str] = mapped_column(Text, nullable=True)  # Details about the order
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    buyer: Mapped["Buyer"] = relationship("Buyer", back_populates="orders")
    seller: Mapped["Seller"] = relationship("Seller", back_populates="orders")

class Buyers(Base):
    __tablename__ = "buyers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=True)

    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="buyer")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="seller_review")
    user: Mapped["Users"] = relationship("Users", back_populates="buyer_profile")
    sellers: Mapped[list["Sellers"]] = relationship("Sellers", back_populates="clients", secondary=buyer_seller)

class Sellers(Base):
    __tablename__ = "sellers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    skills: Mapped[dict] = mapped_column(JSON, nullable=False)
    portfolio_url: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    order_status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)

    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="seller")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="buyer_review")
    clients: Mapped[list["Buyers"]] = relationship("Buyers", back_populates="sellers", secondary=buyer_seller)
    user: Mapped["Users"] = relationship("Users", back_populates="seller_profile")

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["Users"] = relationship(back_populates="posts")
    comments: Mapped[list["Comments"]] = relationship(back_populates="post", cascade="all, delete-orphan")

class FanArts(Base):
    __tablename__ = "fanArts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user: Mapped["Users"] = relationship("User", back_populates="arts")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="fanArt", cascade="all, delete-orphan")


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    parent_comment_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
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
    user_comments: Mapped["Users"] = relationship("Users", back_populates="comments")
    post: Mapped["Posts"] = relationship("Posts", back_populates="comments")
    fanArt: Mapped["FanArts"] = relationship("FanArts", back_populates="comments")

class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey("sellers.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("buyers.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    seller_review: Mapped["Sellers"] = relationship("Sellers", back_populates="reviews")
    buyer_review: Mapped["Buyers"] = relationship("Buyers", back_populates="reviews")
    reviewer: Mapped["Users"] = relationship("Users", back_populates="reviews_given")

class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    members: Mapped[list["TeamMembers"]] = relationship("TeamMembers", back_populates="team", cascade="all, delete-orphan")

class TeamMembers(Base):

    __tablename__ = "team_members"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    team: Mapped["Teams"] = relationship("Teams", back_populates="members")
    user: Mapped["Users"] = relationship("Users", back_populates="teams")

class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    sender_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    sender: Mapped["Users"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    chat: Mapped["Chats"] = relationship("Chat", back_populates="messages")

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
    user: Mapped["Users"] = relationship("Users", back_populates="chats")


#TODO : Work more on the saved favorites part and start testing with the database