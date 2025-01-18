import os
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import PyJWTError
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Users
from src.routes.users import TokenData, oauth2_scheme


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

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    token = authenticate_user(token)

    if not token:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
    user = db.query(Users).filter(Users.username == token.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
    return user