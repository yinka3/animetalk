from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, ForeignKey, Enum, UUID, String, Boolean, DateTime, Integer, Column
from datetime import datetime
from uuid import uuid4
from database import Base
from chat import Messages, ChatMembers
from content import SavedContents, Comments, Posts, FanArts, Tags, Reviews
from orders import Orders, Jobs, JobApplications, SellersSkills
from utils import UserRole

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

    buyer_profile: Mapped[Optional["Buyers"]] = relationship("Buyers", back_populates="user", uselist=False)
    seller_profile: Mapped[Optional["Sellers"]] = relationship("Sellers", back_populates="user", uselist=False)
    reviews_given: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="reviewer")
    comments: Mapped[list["Comments"]] = relationship("Comments", back_populates="user_comments")
    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="user")
    arts: Mapped[list["FanArts"]] = relationship("FanArts", back_populates="user")
    tags_received: Mapped[list["Tags"]] = relationship("Tags", back_populates="tagged_user", cascade="all, delete-orphan")
    teams: Mapped[list["TeamMembers"]] = relationship("TeamMembers", back_populates="user")
    sent_messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="sender")
    received_messages: Mapped[list["Messages"]] = relationship("Messages", back_populates="receiver")
    chat: Mapped[list["ChatMembers"]] = relationship("ChatMembers", back_populates="user")
    saved_contents: Mapped[list["SavedContents"]] = relationship("SavedContents", back_populates="user")

class Buyers(Base):
    __tablename__ = "buyers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    jobs: Mapped[list["Jobs"]] = relationship("Jobs", back_populates="buyer")
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="buyer")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="seller_review")
    user: Mapped["Users"] = relationship("Users", back_populates="buyer_profile")
    sellers: Mapped[list["Sellers"]] = relationship("Sellers", back_populates="clients", secondary=buyer_seller)

class Sellers(Base):
    __tablename__ = "sellers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    portfolio_url: Mapped[str] = mapped_column(String, nullable=True)

    applications: Mapped[list["JobApplications"]] = relationship("JobApplication", back_populates="seller")
    skills: Mapped[list["SellersSkills"]] = relationship("SellerSkills", back_populates="seller")
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="seller")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="buyer_review")
    clients: Mapped[list["Buyers"]] = relationship("Buyers", back_populates="sellers", secondary=buyer_seller)
    user: Mapped["Users"] = relationship("Users", back_populates="seller_profile")

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
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"),nullable=False, unique=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    team: Mapped["Teams"] = relationship("Teams", back_populates="members")
    user: Mapped["Users"] = relationship("Users", back_populates="teams")


