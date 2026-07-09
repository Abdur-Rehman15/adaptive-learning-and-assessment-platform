from sqlmodel import SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    username: str
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None