import os
from datetime import datetime, timedelta
from typing import Optional, List

import fastapi
import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Buyers, Users
from src.schemas.user import CreateBuyerSchema

app = FastAPI()

app.post("/buyer/register")
def create_buyer(buyer: CreateBuyerSchema, db: Session = Depends(get_db())):
    if buyer.user_id:
        user = db.query(Users).filter(Users.id == buyer.user_id).first()

        if user:
            if user.buyer_profile:
                raise HTTPException(status_code=400, detail="Buyer already registered")

            new_buyer = Buyers(user_id=user.id, name=buyer.name, email=user.email)
            db.add(new_buyer)
            db.commit()
            db.refresh(new_buyer)
            user.buyer_profile = new_buyer
            db.commit()
            return {
                "buyer" : {
                    "username": user.username,
                    "name": new_buyer.name,
                    "email": new_buyer.email,
                }
            }
        else:
            existing_buyer = db.query(Buyers).filter(Buyers.email == buyer.email).first()
            if existing_buyer:
                raise HTTPException(status_code=400, detail="Email already registered as a standalone buyer")

            if not buyer.email or not buyer.name:
                raise HTTPException(status_code=400, detail="Need more credentials")

            new_buyer = Buyers(name=buyer.name, email=buyer.email)
            db.add(new_buyer)
            db.commit()
            db.refresh(new_buyer)
            return {
                "buyer": {
                    "name": new_buyer.name,
                    "email": new_buyer.email,
                }
            }

