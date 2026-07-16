from sqlmodel import SQLModel, Field
from pydantic import EmailStr, model_validator


class UserBase(SQLModel):
    username: str = Field(min_length=5)
    email: EmailStr
    role: str

    @model_validator(mode="after")
    def verify_role(self):
        if self.role not in ("admin", "user"):
            raise ValueError("role can be user or admin only")
        return self


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserResponse(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
