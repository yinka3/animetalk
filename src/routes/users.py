import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.user import CreateUserSchema, UserSchema, CreateUserResponseSchema, UserPasswordUpdateResponse, UserPasswordUpdate, GetUserResponseSchema, UserProfileSchema
from src.models.roles import Users, Teams
from uuid import UUID
from src.database import get_db
from src.utils import hash_password, verify_password

app = FastAPI()

@app.post("/users/", response_model=CreateUserResponseSchema)
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

@app.put("/update-password", response_model=UserPasswordUpdateResponse)
def update_password(password_data: UserPasswordUpdate, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    db.refresh(current_user)
    return current_user

if __name__ == "__main__":
    uvicorn.run("src.routes.users:app" , host="127.0.0.1", port=8000, reload=True)