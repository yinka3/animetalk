import re

from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

from src.models.chat import ChatMembers


## TODO: decide if I want to keep a limit to the password or not and where

class UserRoleEnum(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    BOTH = "both"
    NONE = "none"
    USER = "user"

class BuyersBaseSchema(BaseModel):
    id: UUID
    user_id: UUID


    class Config:
        orm_mode = True


class BuyersSchema(BuyersBaseSchema):
    pass

    class Config:
        orm_mode = True

class SellersBaseSchema(BaseModel):
    skills: dict = Field(..., description="Skills of the seller.")
    portfolio_url: Optional[str] = Field(None, description="URL to the seller's portfolio.")
    rating: float = Field(0.0, description="Seller's rating.")

    class Config:
        orm_mode = True


class SellersSchema(SellersBaseSchema):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True

class CreateTeamMemberSchema(BaseModel):
    user_id: UUID = Field(..., description="The unique identifier of the user to be added as a team member.")
    username: str = Field(..., min_length=3, max_length=50, description="The username of the team member.")

    class Config:
        orm_mode = True


class CreateTeamSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="The name of the team.")
    members: Optional[List[CreateTeamMemberSchema]] = Field(
        None, description="A list of user IDs and usernames to be added as initial members of the team."
    )

    class Config:
        orm_mode = True


class TeamSchema(CreateTeamSchema):
    pass

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the user.")
    username: str = Field(..., description="The user's unique username.")
    email: EmailStr = Field(..., description="The user's email address.")
    role: Optional[UserRoleEnum] = Field(None, description="The user's role in the system.")
    buyer_profile: Optional[BuyersSchema] = None
    seller_profile: Optional[SellersSchema] = None
    is_active: bool = Field(..., description="Indicates whether the user account is active.")
    created_at: datetime = Field(..., description="The date and time when the user account was created.")
    teams: Optional[TeamSchema] = Field(None, description="The user's teams.")
    class Config:
        orm_mode = True



class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The user's unique username.")
    email: EmailStr = Field(..., description="The user's email address.")
    role: Optional[UserRoleEnum] = Field(None, description="The user's role in the system.")
    is_active: bool = Field(..., description="Indicates whether the user is active.")
    teams: Optional[TeamSchema] = Field(None, description="The user's teams.")

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: str = Field(
        ...,
        min_length=10,
        description=(
            "The user's password. Must be at least 10 characters long, "
            "contain at least 1 digit, 1 symbol (!@#$%^&*()), and 1 uppercase letter."
        ),
    )

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r'[!@#$%^&*()]', value):
            raise ValueError("Password must contain at least one symbol: !@#$%^&*()")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        return value

    class Config:
        orm_mode = True



class CreateBuyerSchema(BuyersBaseSchema):
    user_id: UUID = Field(..., description="The buyer's unique ID.")

    class Config:
        orm_mode = True



