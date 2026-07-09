from fastapi import HTTPException, status, APIRouter, Depends
from database.database import SessionDep, get_session
from fastapi.security import OAuth2PasswordRequestForm
from security.security import authenticate_user, create_token
from sqlmodel import Session

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "invalid username or password")

    token = create_token(user.username)
    return {"access_token": token, "token_type": "bearer"}