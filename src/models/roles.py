from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, Enum, UUID, String, Boolean, DateTime, Column, ARRAY
from datetime import datetime
from uuid import uuid4
from src.database import Base
from src.utils import UserRole


if TYPE_CHECKING:  # Imports used only for type checking
    from src.models.content import Reviews, Comments, Posts, FanArts, Tags, SavedContents
    from src.models.chat import Messages, ChatMembers
    from src.models.orders import Jobs, Orders, JobApplications, SellersSkills

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
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[list[UserRole]] = mapped_column(ARRAY(Enum(UserRole)), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    team_names: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    buyer_profile: Mapped[Optional["Buyers"]] = relationship("Buyers", back_populates="user", uselist=False)
    seller_profile: Mapped[Optional["Sellers"]] = relationship("Sellers", back_populates="user", uselist=False)
    reviews_given: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="reviewer")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="user_comments", foreign_keys="[Comments.user_id]")
    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="user", foreign_keys="[Posts.user_id]")
    arts: Mapped[list["FanArts"]] = relationship("FanArts", back_populates="user", foreign_keys="[FanArts.user_id]")
    tags_received: Mapped[list["Tags"]] = relationship("Tags", back_populates="tagged_user", cascade="all, delete-orphan")
    teams: Mapped[list["TeamMembers"]] = relationship("TeamMembers", back_populates="user")
    messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="user")
    chats: Mapped[list["ChatMembers"]] = relationship("ChatMembers", back_populates="user")
    saved_contents: Mapped[list["SavedContents"]] = relationship("SavedContents", back_populates="user")

class Buyers(Base):
    __tablename__ = "buyers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=True)

    jobs: Mapped[list["Jobs"]] = relationship("Jobs", back_populates="buyer")
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="buyer")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="buyer_review", foreign_keys="[Reviews.buyer_id]")
    user: Mapped["Users"] = relationship("Users", back_populates="buyer_profile")
    sellers: Mapped[list["Sellers"]] = relationship("Sellers", back_populates="clients", secondary=buyer_seller)

class Sellers(Base):
    __tablename__ = "sellers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=True)
    portfolio_url: Mapped[str] = mapped_column(String, nullable=True)

    applications: Mapped[list["JobApplications"]] = relationship("JobApplications", back_populates="seller")
    skills: Mapped[list["SellersSkills"]] = relationship("SellersSkills", back_populates="seller", foreign_keys="[SellersSkills.seller_id]")
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="seller", foreign_keys="[Orders.seller_id]")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="seller_review", foreign_keys="[Reviews.seller_id]")
    clients: Mapped[list["Buyers"]] = relationship("Buyers", back_populates="sellers", secondary=buyer_seller)
    user: Mapped["Users"] = relationship(Users, back_populates="seller_profile")

class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    members: Mapped[list["TeamMembers"]] = relationship("TeamMembers", back_populates="team", cascade="all, delete-orphan", foreign_keys="[TeamMembers.team_id]")

class TeamMembers(Base):

    __tablename__ = "team_members"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    team: Mapped["Teams"] = relationship("Teams", back_populates="members", foreign_keys=[team_id])
    user: Mapped["Users"] = relationship("Users", back_populates="teams", foreign_keys=[user_id])


