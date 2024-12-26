from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class SellersSkillsSchema(BaseModel):
    id: UUID = Field(..., description="ID of skill")
    proficiency: Optional[str] = Field(None, description="The seller's proficiency level for this skill.")

    class Config:
        orm_mode = True


class SkillsSchema(BaseModel):
    id: UUID = Field(..., description="ID of skill")
    name: str = Field(..., description="The name of the skill.")
    description: Optional[str] = Field(None, description="An optional description of the skill.")

    class Config:
        orm_mode = True

class OrdersSchema(BaseModel):
    id: UUID
    status: str = Field(..., description="The current status of the order.")
    description: Optional[str] = Field(None, description="Details about the order.")
    total_price: float = Field(..., description="The total price of the order.")
    created_at: datetime = Field(..., description="The date and time when the order was created.")

    class Config:
        orm_mode = True

class JobApplicationsSchema(BaseModel):
    id: UUID
    cover_letter: Optional[str] = Field(None, description="The seller's explanation of their suitability for the job.")
    bid_amount: float = Field(..., description="The amount bid by the seller for the job.")
    created_at: datetime = Field(..., description="The date and time when the application was created.")
    status: str = Field(..., description="The current status of the application (e.g., 'Pending', 'Accepted').")

    class Config:
        orm_mode = True

class JobsSchema(BaseModel):
    id: UUID
    title: str = Field(..., description="The title of the job.")
    description: str = Field(..., description="A detailed description of the job.")
    budget: Optional[float] = Field(None, description="The budget allocated for the job.")
    deadline: Optional[datetime] = Field(None, description="The deadline for the job.")

    class Config:
        orm_mode = True

class CreateJobApplicationSchema(BaseModel):
    job_id: UUID = Field(..., description="The ID of the job being applied for.")
    seller_id: UUID = Field(..., description="The ID of the seller applying for the job.")
    cover_letter: Optional[str] = Field(None, description="An optional explanation of the seller's suitability for the job.")
    bid_amount: float = Field(..., description="The amount the seller is bidding for the job.")

    class Config:
        orm_mode = True

class CreateOrderSchema(BaseModel):
    buyer_id: UUID = Field(..., description="The ID of the buyer placing the order.")
    seller_id: UUID = Field(..., description="The ID of the seller fulfilling the order.")
    description: Optional[str] = Field(None, description="Details about the order.")
    total_price: float = Field(..., description="The total price of the order.")

    class Config:
        orm_mode = True

class SearchOrdersSchema(BaseModel):
    buyer_id: Optional[UUID] = Field(None, description="Filter by the buyer's ID.")
    seller_id: Optional[UUID] = Field(None, description="Filter by the seller's ID.")
    status: Optional[str] = Field(None, description="Filter by the order's status.")
    min_price: Optional[float] = Field(None, description="Filter orders with a minimum total price.")
    max_price: Optional[float] = Field(None, description="Filter orders with a maximum total price.")
    start_date: Optional[datetime] = Field(None, description="Filter orders created after this date.")
    end_date: Optional[datetime] = Field(None, description="Filter orders created before this date.")

    class Config:
        orm_mode = True