from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserUpdate
import repositories.user_repo as user_repo
from models.user_model import User


def create_user(session: Session, user_in: UserCreate):
    existing_user = user_repo.get_user_by_username(session, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists"
        )
    return user_repo.create_user(session, user_in)


def update_user(session: Session, user_id: int, updated_user: UserUpdate):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    return user_repo.update_user(session, user_id, updated_user)


def get_user_by_id(session: Session, user_id: int):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user with this ID doesn't exist",
        )
    return user


def delete_user(session: Session, user_id: int):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user doesn't exist"
        )
    user_repo.delete_user(session, user_id)
