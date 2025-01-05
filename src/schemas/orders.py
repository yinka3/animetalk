from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class OrderBaseSchema(BaseModel):
    description: Optional[str] = Field(None, description="Details about the order.")
    total_price: float = Field(..., description="The total price of the order.")

    class Config:
        from_attributes = True


class OrdersSchema(OrderBaseSchema):
    id: UUID = Field(..., description="The unique ID of the order.")
    status: str = Field(..., description="The current status of the order.")
    created_at: datetime = Field(..., description="The date and time when the order was created.")


class CreateOrderSchema(OrderBaseSchema):
    buyer_id: UUID = Field(..., description="The ID of the buyer placing the order.")
    seller_id: UUID = Field(..., description="The ID of the seller fulfilling the order.")


class SearchOrdersSchema(BaseModel):
    buyer_id: Optional[UUID] = Field(None, description="Filter by the buyer's ID.")
    seller_id: Optional[UUID] = Field(None, description="Filter by the seller's ID.")
    status: Optional[str] = Field(None, description="Filter by the order's status.")
    min_price: Optional[float] = Field(None, description="Filter orders with a minimum total price.")
    max_price: Optional[float] = Field(None, description="Filter orders with a maximum total price.")
    start_date: Optional[datetime] = Field(None, description="Filter orders created after this date.")
    end_date: Optional[datetime] = Field(None, description="Filter orders created before this date.")

    class Config:
        from_attributes = True