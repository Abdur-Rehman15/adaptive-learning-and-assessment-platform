from sqlmodel import Field, Relationship
from schemas.notification_schema import NotificationBase
from datetime import datetime
import models.notification_model as notification_model


class Notification(NotificationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now().date())
    user: "User" = Relationship(back_populates="notifications")

