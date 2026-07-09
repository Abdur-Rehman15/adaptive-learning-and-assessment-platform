import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from models.user_model import User
from sqlmodel import Session, select
from database.database import get_session
from fastapi import Depends, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRES_IN_MINUTES = int(os.getenv("EXPIRES_IN_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.now() + timedelta(minutes=EXPIRES_IN_MINUTES),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except JWTError:
        return None


def authenticate_user(session: Session, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "invalid token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(401, "invalid token")

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(401, "user not found")

    return user