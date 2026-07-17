from sqlmodel import Field, Relationship
from schemas.user_schema import UserBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.enrollment_model import Enrollment
    from models.quizAttempt_model import QuizAttempt
    from models.notification_model import Notification
    from models.certificate_model import Certificate


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    
    enrollments: list["Enrollment"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    quiz_attempts: list["QuizAttempt"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    notifications: list["Notification"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    certificates: list["Certificate"] = Relationship(
        back_populates="user", cascade_delete=True
    )
