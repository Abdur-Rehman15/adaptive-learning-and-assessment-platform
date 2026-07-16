from fastapi import status, APIRouter, Depends
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from database.database import SessionDep
from models.user_model import User
from security.security import get_current_user
import services.user_service as user_service  # Import the new service layer
from middleware.verifyRole import verify_role

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: SessionDep):
    return user_service.create_user(session, user_in)


@router.patch("/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    updated_user: UserUpdate,
    session: SessionDep,
    current_user=Depends(verify_role(["admin", "user"])),
):
    return user_service.update_user(session, current_user.id, updated_user)


@router.get("/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(session: SessionDep, current_user=Depends(verify_role(["admin", "user"]))):
    return user_service.get_user_by_id(session, current_user.id)


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(session: SessionDep, current_user=Depends(verify_role(["admin", "user"]))):
    user_service.delete_user(session, current_user.id)
