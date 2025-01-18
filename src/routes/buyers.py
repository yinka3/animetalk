import os
from datetime import datetime, timedelta
from typing import Optional, List

import fastapi
import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Response
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Buyers, Users, Orders, Jobs, Sellers
from src.aouth import get_current_user
from src.schemas.job import JobsSchema
from src.schemas.user import CreateUserSchema
from src.utils import UserRole, hash_password, verify_password, OrderStatus

app = FastAPI()

# TODO: See if needing to do authentication for buyers and sellers is needed (probably)

@app.post("/buyer/register")
def create_buyer(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db())):
    if current_user.buyer_profile:
        raise HTTPException(status_code=400, detail="Buyer already registered")

    new_buyer = Buyers()
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    current_user.buyer_profile = new_buyer
    if UserRole.BUYER.value not in current_user.role:
        current_user.role.append(UserRole.BUYER.value)
    db.commit()
    return {"message": "Buyer profile created!",
            "username": current_user.username}

def buyer_access(current_user: Users = Depends(get_current_user)):
    if not current_user.buyer_profile:
        raise HTTPException(
            status_code=403,
            detail="You must have a buyer profile to access this resource."
        )
    return current_user

@app.get("/buyer/me")
def get_buyer_account(current_user: Users = Depends(buyer_access)):
    return current_user

@app.get("/buyer/{current_user.username}/orders")
def view_buyer_orders(current_user: Users = Depends(buyer_access)):
    buyer = current_user.buyer_profile
    return buyer.orders

@app.post("buyer/orders/{order_id}")
def cancel_order(order_id: UUID, current_user: Users = Depends(buyer_access), db: Session = Depends(get_db())):

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

@app.get("/buyer/{current_user.username}/orders/{order_id}")
def view_an_order(order_id: UUID, current_user: Users = Depends(buyer_access), db: Session = Depends(get_db())):
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


@app.post("/buyer/{current_user.username}/create")
def post_job(new_job: JobsSchema, current_user: Users = Depends(buyer_access), db: Session = Depends(get_db)):
    buyer = current_user.buyer_profile

    job = db.query(Jobs).filter(Jobs.id == new_job.id)

    if job in buyer.jobs:
        raise HTTPException(status_code=400, detail="Job already exists")

    new_job = Jobs(
        title = new_job.title,
        description = new_job.description,
        budget = new_job.budget,
        deadline = new_job.deadline
    )

    # recommend jobs ( whole other thing to work on later )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job created!",
        "details": {
            "title": new_job.title,
            "created_at": new_job.created_at,
        }
    }

# viewing job applications









