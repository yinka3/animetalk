from uuid import uuid4

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, UUID, Enum, Float, JSON, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


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

    buyer_profile = relationship("Buyer", back_populates="user", uselist=False)
    seller_profile = relationship("Seller", back_populates="user", uselist=False)
    reviews_given = relationship("Review", back_populates="reviewer")
    comments = relationship("Comments", back_populates="user_comments")


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    budget = Column(Float, nullable=True)

    reviews = relationship("Review", back_populates="seller_review")
    user = relationship("User", back_populates="buyer_profile")


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    skills = Column(JSON, nullable=False)
    portfolio_url = Column(String, nullable=True)
    rating = Column(Float, default=0.0)

    reviews = relationship("Review", back_populates="buyer_review")
    user = relationship("User", back_populates="seller_profile")

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    username = Column(String, ForeignKey("users.username"),nullable=False, unique=True)
    

class Comments(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    username = Column(String, ForeignKey("users.username"), nullable=False, unique=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=True)
    content_id = Column(Integer, nullable=False)  # ID of the content being commented on
    content_type = Column(String, nullable=False)  # E.g., "post", "fanart"
    status = Column(String, default="approved")
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)
    ip_address = Column(String, nullable=True)
    #metadata = Column(JSON, nullable=True) done know yet if all models should have this

    __table_args__ = (
        Index('idx_content_id', 'content_id'),
        Index('idx_parent_comment_id', 'parent_comment_id')
    )

    user_comments = relationship("User", back_populates="comments", foreign_keys="Comments.user_id")
    parent_comment = relationship("Comments", remote_side=[id], backref="replies")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4())
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    seller_review = relationship("Seller", back_populates="reviews", foreign_keys="Review.seller_id")
    buyer_review = relationship("Buyer", back_populates="reviews", foreign_keys="Review.buyer_id")
    reviewer = relationship("User", back_populates="reviews_given", foreign_keys="Review.reviewer_id")


