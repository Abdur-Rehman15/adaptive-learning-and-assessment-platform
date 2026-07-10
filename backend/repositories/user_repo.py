from sqlmodel import Session, select
from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate
from security.security import hash_password


def get_user_by_id(session: Session, user_id: int):
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def create_user(session: Session, user_in: UserCreate):
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        role=user_in.role,
        hashed_password=hash_password(user_in.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, updated_user: UserUpdate):
    user = get_user_by_id(session, user_id)
    db_user = updated_user.model_dump(exclude_unset=True)
    if "password" in db_user:
        db_user["hashed_password"] = db_user.pop("password")
    for k, v in db_user.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def delete_user(session: Session, user_id: int):
    db_user = get_user_by_id(session, user_id)
    session.delete(db_user)
    session.commit()
