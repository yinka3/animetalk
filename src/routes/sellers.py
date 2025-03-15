from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas.job import CreateJobApplicationSchema
from src.utils import UserRole
from src.models import Users, Sellers
from src.routes.users import get_current_user
from src.database import get_db

router = APIRouter(
    tags=["sellers"],
)


def seller_access(current_user: Users = Depends(get_current_user)):
    if not current_user.seller_profile:
        raise HTTPException(
            status_code=403,
            detail="You must have a seller profile to access this resource."
        )
    return current_user

@router.post("/register")
def create_seller(user: Users = Depends(get_current_user), db = Depends(get_db)):

    if user.seller_profile:
        raise HTTPException(
            status_code=400,
            detail="You are a seller already."
        )

    seller = Sellers()
    db.add(seller)
    db.commit()
    db.refresh(seller)
    if user.role == UserRole.USER:
        user.role = UserRole.USERSELLER
    else:
        user.role = UserRole.ALL
    db.commit()
    db.refresh(user)
    return {"message": "Seller profile created!",
            "username": user.username}

@router.get("/me")
def get_seller_account(current_user: Users = Depends(seller_access)):
    return current_user

@router.post("/seller/job_applications")
def create_application(application: CreateJobApplicationSchema, db: Session = Depends(get_db), current_user: Users = Depends(seller_access)):


@router.get("/seller/orders")