from uuid import uuid4
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, UUID, Enum, Float, JSON
from sqlalchemy.orm import relationship
from database import Base


class UserRole(Enum):
    BUYER = "buyer"
    SELLER = "seller"
    BOTH = "both"
    NONE = "none"


# first lets create User
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hashed = Column(String, nullable=False)
    role = Column(UserRole, nullable=True)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    buyer_profile = relationship("Buyer", back_populates="users", uselist=False)
    seller_profile = relationship("Seller", back_populates="users", uselist=False)


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    budget = Column(Float, nullable=True)

    reviews_written = relationship("Review", back_populates="seller_review")
    user = relationship("User", back_populates="buyer_profile")


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    skills = Column(JSON, nullable=False)
    portfolio_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)

    user = relationship("User", back_populates="seller_profile")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    seller_review = relationship("Seller", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews_written")
