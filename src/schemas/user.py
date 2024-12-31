import re
from src.schemas import team
from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.utils import UserRole


class BuyersBaseSchema(BaseModel):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

class BuyersSchema(BuyersBaseSchema):
    pass


class CreateBuyerSchema(BuyersBaseSchema):
    user_id: UUID = Field(..., description="The buyer's unique ID.")


class SellersBaseSchema(BaseModel):
    skills: dict = Field(..., description="Skills of the seller.")
    portfolio_url: Optional[str] = Field(None, description="URL to the seller's portfolio.")
    rating: float = Field(0.0, description="Seller's rating.")

    class Config:
        from_attributes = True


class SellersSchema(SellersBaseSchema):
    id: UUID
    user_id: UUID


class CreateSellerSchema(SellersBaseSchema):
    user_id: UUID = Field(..., description="The seller's unique ID.")



class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The user's unique username.")
    email: EmailStr = Field(..., description="The user's email address.")
    role: UserRole = Field(UserRole.USER, description="The user's role in the system.")
    is_active: bool = Field(True, description="Indicates whether the user is active.")
    created_at: Optional[datetime] = Field(..., description="The date and time when the user account was created.")

    class Config:
        from_attributes = True

class UserProfileSchema(UserBaseSchema):
    id: UUID = Field(..., description="The unique identifier of the user.")
    teams: Optional[team.TeamSchema] = Field(None, description="The user's teams.")
    buyer_profile: Optional[BuyersSchema] = Field(None, description="The user's buyer profile.")
    seller_profile: Optional[SellersSchema] = Field(None, description="The user's seller profile.")


class UserSchema(UserProfileSchema):
    pass

class UpdateUserSchema(UserBaseSchema):
    pass

class DisplayUserSummarySchema(UserBaseSchema):
    id: UUID = Field(..., description="The unique identifier of the user.")



class CreateUserSchema(UserBaseSchema):
    password: str = Field(
        ...,
        min_length=10,
        description=(
            "The user's password. Must be at least 10 characters long, "
            "contain at least 1 digit, 1 symbol (!@#$%^&*()), and 1 uppercase letter."
        ),
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.now,
                                           description="The date and time when the user account was created.")

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r'[!@#$%^&*()]', value):
            raise ValueError("Password must contain at least one symbol: !@#$%^&*()")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        return value

class CreateUserResponseSchema(UserBaseSchema):
    id: UUID = Field(..., description="The user's unique ID.")


class DeleteUserSchema(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the user.")
    reason: Optional[str] = Field(None, description="Reason for deleting the user account.")

    class Config:
        from_attributes = True


