import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status, Response, APIRouter
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Buyers, Users, Orders, Jobs, Sellers, Reviews
from src.models.orders import Skills, SellersSkills
from src.routes.users import get_current_user
from src.schemas.job import JobsSchema, SearchFilter
from src.utils import UserRole, hash_password, verify_password, OrderStatus


router = APIRouter(
    tags=['Buyer']
)


@router.post("/buyer/register")
def create_buyer(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.buyer_profile:
        raise HTTPException(status_code=400, detail="Buyer already registered")

    new_buyer = Buyers()
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    logging.info(f"New buyer registered: {new_buyer.id}")
    current_user.buyer_profile = new_buyer
    if current_user.role == UserRole.USER:
        current_user.role = UserRole.USERBUYER
    else:
        current_user.role = UserRole.ALL
    db.commit()
    db.refresh(new_buyer)
    return {"message": "Buyer profile created!",
            "username": current_user.username}

def buyer_access(current_user: Users = Depends(get_current_user)):
    if not current_user.buyer_profile:
        raise HTTPException(
            status_code=403,
            detail="You must have a buyer profile to access this resource."
        )
    return current_user

@router.get("/buyer/me")
def get_buyer_account(current_user: Users = Depends(buyer_access)):
    return current_user

@router.get("/buyer/{current_user.username}/orders")
def view_buyer_orders(current_user: Users = Depends(buyer_access)):
    buyer = current_user.buyer_profile
    return buyer.orders

@router.post("buyer/orders/{order_id}")
def cancel_order(order_id: UUID, current_user: Users = Depends(buyer_access), db: Session = Depends(get_db)):

    buyer = current_user.buyer_profile

    if not buyer:
        raise HTTPException(status_code=403, detail="You must have a buyer profile to access this resource.")

    target_order = db.query(Orders).filter(Orders.id == order_id).first()
    if target_order in buyer.orders:
        if target_order.status == OrderStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Buyer already cancelled")

        if target_order.status == OrderStatus.PENDING or target_order.status == OrderStatus.INPROGRESS:
            target_order.status = OrderStatus.CANCELLED.value
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Order not found")

@router.get("/buyer/{current_user.username}/orders/{order_id}")
def view_an_order(order_id: UUID, current_user: Users = Depends(buyer_access), db: Session = Depends(get_db)):
    buyer = current_user.buyer_profile
    if not buyer:
        raise HTTPException(status_code=403, detail="You must have a buyer profile to access this resource.")

    target_order = db.query(Orders).filter(Orders.id == order_id).first()
    seller = db.query(Sellers).filter(Sellers.id == target_order.seller_id).first()

    if not seller:
        raise HTTPException(status_code=400, detail="Figure out an error code for this")
    if target_order in buyer.orders:
        if target_order.status == OrderStatus.CANCELLED or target_order.status == OrderStatus.COMPLETED:
            # want to give it a limited view if cancelled
            return {"buyer": current_user.username,
                    "seller":  {
                    "username": seller.user.username,
                    "email": seller.user.email,
                }
            }

        if target_order.status in [OrderStatus.PENDING, OrderStatus.ACCEPTED, OrderStatus.INPROGRESS]:
            return {
                "buyer": current_user.username,
                "seller": {
                    "username": seller.user.username,
                    "email": seller.user.email,  # Include email for detailed view
                },
                "order_details": {
                    "id": str(target_order.id),
                    "status": target_order.status,
                    "description": target_order.description,
                    "price": target_order.total_price,
                    "created_at": target_order.created_at,
                },
                "seller_feedback": "Add something here",
                "buyer_feedback": "Add something here",
            }
    else:
        raise HTTPException(status_code=400, detail="Order not found")


@router.post("/buyer/create")
def post_job(new_job: JobsSchema, current_buyer: Users = Depends(buyer_access), db: Session = Depends(get_db)):
    buyer = current_buyer.buyer_profile
    deadline = datetime.strptime(new_job.deadline, "%m/%d/%Y")

    post_job: Jobs = Jobs(
        buyer_id = buyer.id,
        title = new_job.title,
        description = new_job.description,
        budget = new_job.budget,
        deadline = deadline
    )


    db.add(post_job)
    db.commit()
    db.refresh(post_job)

    return {
        "message": "Job created!",
        "details": {
            "buyer": current_buyer.username,
            "title": post_job.title,
            "created_at": post_job.created_at,
        }
    }

@router.get("/buyer/search")
def search(search_filter: SearchFilter, db: Session = Depends(get_db)):

    query = db.query(Sellers)\
            .join(SellersSkills, Sellers.id == SellersSkills.seller_id)\
            .join(Skills, SellersSkills.skill_id == Skills.id)\
            .outerjoin(Reviews, Sellers.id == Reviews.seller_id)\
            .group_by(Sellers.id)

    if search_filter.skill and not search_filter.rating:
        query = query.filter(Skills.name.ilike(f"%{search_filter.skill}%"))


    if search_filter.rating and not search_filter.skill:
        query = query.having(func.coalesce(func.avg(Reviews.rating), 0) >= search_filter.rating)

    sellers = query.all()

    return [
        {
            "username": seller.user.username,
            "portfolio_url": seller.portfolio_url,
            "reviews": seller.reviews,
            "skills": seller.skills
        }
        for seller in sellers
    ]









