import os
from datetime import datetime, timedelta
from typing import Optional, List

import jwt
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session, InstrumentedAttribute

from src import utils
from src.schemas.user import CreateUserSchema, UserSchema, CreateUserResponseSchema, UserPasswordUpdate, GetUserResponseSchema, UserProfileSchema
from src.models.roles import Users, Teams
from uuid import UUID
from src.database import get_db
from src.utils import hash_password, verify_password

app = FastAPI()

class Token(BaseModel):
    access_token: InstrumentedAttribute[str]
    token_type: str
    token_expires: Optional[datetime]

class TokenData(BaseModel):
    user: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

@app.post("/users/register", response_model=CreateUserResponseSchema)
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    # Check if the email or username already exists
    if db.query(Users).filter(Users.email == user.email).first() or db.query(Users).filter(Users.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    # Hash the password and create the user
    hashed_password = hash_password(user.password)
    new_user = Users(username=user.username, email=user.email, password=hashed_password, role=user.role.USER.value, is_active=user.is_active)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# might need to add a param: expires_delta=access_token_expires
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
    return encoded_jwt

# might need to have a param: form_data: OAuth2PasswordRequestForm = Depends()
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": form_data.username},
    )
    return access_token


def authenticate_user(token: str):
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")])

        exp_time = payload.get("exp")
        if exp_time is None or exp_time < datetime.now().timestamp():
            # self.activeSessionsEntityManager.delete_many({"username": username})
            # recreating this code on top w/o entity manager
            raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")

        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=400, detail="Incorrect user")
        token_data = TokenData(user=username)
        return token_data

        # Check if the username exists in the active sessions
        # session = self.activeSessionsEntityManager.find_one({"username": username})
        # if not session:
        #     raise HTTPException(status_code=401, detail="User session not found.")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")

@app.post("/users/login", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials.",
        )
    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)

    return {"message": "Welcome Mother*ucker"}
    #return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    token = authenticate_user(token)

    if not token:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
    user = db.query(Users).filter(Users.username == token.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
    return user

@app.get("users/me", response_model=UserProfileSchema)
def get_my_account(current_user: Users = Depends(get_current_user)):
    return current_user

@app.get("/users/{user_id}", response_model=GetUserResponseSchema)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@app.get("/users/{user_id}", response_model=GetUserResponseSchema)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@app.get("/users/{username}", response_model=GetUserResponseSchema)
def get_user_by_username(username: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

@app.get("users/teams", response_model=List[str])
def get_user_teams(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    teams = db.query(Teams).filter(Teams.members.any(id=current_user.id)).all()
    return [team.name for team in teams]

@app.put("users/update-password")
def update_password(password_data: UserPasswordUpdate, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(password_data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_user.password = hash_password(password_data.new_password)
    db.commit()
    db.refresh(current_user)
    return {"Updated Password Successfully!": datetime.now()}

if __name__ == "__main__":
    uvicorn.run("src.routes.users:app" , host="127.0.0.1", port=8000, reload=True)