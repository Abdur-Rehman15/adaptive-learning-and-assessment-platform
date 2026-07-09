from sqlmodel import Field, Relationship
from schemas.user_schema import UserBase
# from models import task_model

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    # tasks: list["task_model.Task"] = Relationship(back_populates="user")