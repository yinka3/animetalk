from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  ForeignKey, Enum, UUID, Float, Text, String, DateTime, Integer
from datetime import datetime
from uuid import uuid4
from src.database import Base
import src.models.roles as roles
from src.utils import Proficiency, OrderStatus, JobStatus

class SellersSkills(Base):
    __tablename__ = "sellers_skills"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    seller_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sellers.id"), nullable=False)
    skill_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    proficiency: Mapped[Proficiency] = mapped_column(Enum(Proficiency), nullable=True)

    seller: Mapped["roles.Sellers"] = relationship("Sellers", back_populates="skills")
    skill: Mapped["Skills"] = relationship("Skills", back_populates="sellers")

class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)  # E.g., "3D Modeling", "2D Animation"
    description: Mapped[str] = mapped_column(Text, nullable=True)  # Optional description of the skill

    sellers: Mapped[list["SellersSkills"]] = relationship("SellerSkills", back_populates="skill")


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

    buyer: Mapped["roles.Buyers"] = relationship("Buyers", back_populates="orders")
    seller: Mapped["roles.Sellers"] = relationship("Sellers", back_populates="orders")


class JobApplications(Base):
    __tablename__ = "job_applications"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    job_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    seller_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sellers.id"), nullable=False)
    cover_letter: Mapped[str] = mapped_column(Text, nullable=True)  # Seller's explanation of their suitability
    bid_amount: Mapped[float] = mapped_column(Float, nullable=False)  # Proposed price
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    status: Mapped[JobStatus] = mapped_column(String(50), default=JobStatus.PENDING)  # "Accepted", "Rejected", etc.

    job: Mapped["Jobs"] = relationship("Jobs", back_populates="applications")
    seller: Mapped["roles.Sellers"] = relationship("Sellers", back_populates="applications")


class Jobs(Base):
    __tablename__ = "jobs"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    buyer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("buyers.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)  # Detailed text specification
    budget: Mapped[float] = mapped_column(Float, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Optional deadline
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    buyer: Mapped["roles.Buyers"] = relationship("Buyers", back_populates="jobs")
    applications: Mapped[list["JobApplications"]] = relationship("JobApplications", back_populates="job", cascade="all, delete-orphan")