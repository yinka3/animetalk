import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.user import CreateUserSchema, UserSchema, CreateUserResponseSchema
from src.models.roles import Users
from uuid import UUID
from src.database import get_db
from src.utils import hash_password

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

@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

if __name__ == "__main__":
    uvicorn.run("src.routes.users:app" , host="127.0.0.1", port=8000, reload=True)