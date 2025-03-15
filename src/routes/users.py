from datetime import datetime, timedelta
from typing import Optional, List

import uvicorn
import src.aouth as aouth
from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.utils import UserRole, verify_password, hash_password
from src.schemas.user import CreateUserSchema, CreateUserResponseSchema, UserPasswordUpdate, GetUserResponseSchema, UserProfileSchema
from src.models.roles import Users, Teams
from uuid import UUID
from src.database import get_db


app = FastAPI()

# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     token_expires: Optional[datetime]




oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    token = aouth.authenticate_user(token)

    if not token:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
    user = db.query(Users).filter(Users.username == token.user).first()

    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
    return user

@app.post("/users/register", response_model=CreateUserResponseSchema)
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    # Check if the email or username already exists
    if db.query(Users).filter(Users.email == user.email).first() or db.query(Users).filter(Users.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    # Hash the password and create the user
    hashed_password = hash_password(user.password)

    new_user = Users(username=user.username, email=user.email, password=hashed_password, is_active=user.is_active)

    new_user.role = UserRole.USER
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bad password",
        )
    access_token = aouth.create_access_token(data={"user": user.username, "email": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)

    user.is_active = True
    db.commit()
    db.refresh(user)

    return {"message": "Welcome Mother*ucker", "access_token": access_token, "token_type": "bearer"}

@app.post("/users/logout")
def logout(response: Response, user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    user.is_active = False  # Mark user as inactive
    db.commit()
    db.refresh(user)

    # Remove the token from cookies
    response.delete_cookie("access_token")

    return {"message": "GoodBye Mother*ucker."}


@app.get("/users/me", response_model=UserProfileSchema)
def get_my_account(current_user: Users = Depends(get_current_user)):
    return current_user

@app.get("/users/id/{user_id}", response_model=GetUserResponseSchema)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@app.get("/users/username/{username}", response_model=GetUserResponseSchema)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

@app.get("/users/teams", response_model=List[str])
def get_user_teams(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    teams = db.query(Teams).filter(Teams.members.any(id=current_user.id)).all()
    return [team.name for team in teams]

@app.put("/users/update-password")
def update_password(password_data: UserPasswordUpdate, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    old_password = password_data.old_password
    if not verify_password(old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    new_password = password_data.new_password
    current_user.password = hash_password(new_password)
    db.commit()
    db.refresh(current_user)
    return {"Updated Password Successfully!": datetime.now()}

if __name__ == "__main__":
    uvicorn.run("src.routes.users:app" , host="127.0.0.1", port=8000, reload=True, log_level="debug")