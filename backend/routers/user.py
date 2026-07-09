from fastapi import HTTPException, status, APIRouter, Depends
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
import repositories.user_repo as user_repo
from database.database import SessionDep
from models.user_model import User
from security.security import get_current_user

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: SessionDep):
    user = user_repo.get_user_by_username(session, user_in.username)
    if user:
        raise HTTPException(400, "username already exists")

    return user_repo.create_user(session, user_in)


@router.patch("/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    updated_user: UserUpdate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    user = user_repo.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(404, "user not found")
    return user_repo.update_user(session, current_user.id, updated_user)


@router.get("/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(session: SessionDep, current_user: User = Depends(get_current_user)):
    user = user_repo.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(400, "user with this ID doesn't exist")

    return user


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: SessionDep, current_user: User = Depends(get_current_user)):
    user = user_repo.get_user_by_id(session, current_user.id)
    if not user:
        raise HTTPException(404, "user doesn't exist")

    user_repo.delete_user(session, current_user.id)
