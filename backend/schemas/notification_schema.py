from sqlmodel import SQLModel, Field
from datetime import datetime


class NotificationBase(SQLModel):
    type: str = Field(
        min_length=10,
        nullable=False,
        description="Notification type title length should be atleast 10 characters",
    )
    message: str = Field(
        min_length=20,
        nullable=False,
        description="notification msg length should be atleast 20 characters",
    )
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class NotificationCreate(SQLModel):
    type: str
    message: str


class NotificationUpdate(SQLModel):
    is_read: bool


class NotificationResponse(SQLModel):
    id: int
    type: str
    message: str
    is_read: bool
    created_at: datetime
