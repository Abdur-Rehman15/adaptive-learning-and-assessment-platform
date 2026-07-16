from sqlmodel import SQLModel
from datetime import datetime


class NotificationBase(SQLModel):
    type: str
    message: str
    is_read: bool
    created_at: datetime


class NotificationCreate(SQLModel):
    type: str
    message: str


class NotificationUpdate(SQLModel):
    is_read: bool


class NotificationResponse(SQLModel):
    type: str
    message: str
    is_read: bool
    created_at: datetime
