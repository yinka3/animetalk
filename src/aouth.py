import os

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException
from jose import jwt, JWTError
from pydantic import BaseModel
import subprocess


sec_key = subprocess.check_output(["openssl", "rand", "-hex", "32"]).decode().strip()
ALGORITHM = "HS256"
class TokenData(BaseModel):
    user: Optional[str] = None
    email: Optional[str] = None

# might need to add a param: expires_delta=access_token_expires
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, sec_key, algorithm=ALGORITHM)
    return encoded_jwt

# might need to have a param: form_data: OAuth2PasswordRequestForm = Depends()
# def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     # access_token_expires = timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
#     access_token = create_access_token(
#         data={"sub": form_data.username},
#     )
#     return access_token


def authenticate_user(token: str):
    try:
        payload = jwt.decode(token, sec_key, algorithms=[ALGORITHM])

        exp_time = payload.get("exp")
        if exp_time is None or exp_time < datetime.now().timestamp():
            # self.activeSessionsEntityManager.delete_many({"username": username})
            # recreating this code on top w/o entity manager
            raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")

        username: str = payload.get("user")
        email: str = payload.get("email")
        if not username:
            raise HTTPException(status_code=400, detail="Incorrect user")
        token_data = TokenData(user=username, email=email)
        return token_data

        # Check if the username exists in the active sessions
        # session = self.activeSessionsEntityManager.find_one({"username": username})
        # if not session:
        #     raise HTTPException(status_code=401, detail="User session not found.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Authentication failed, invalid or expired token.")
