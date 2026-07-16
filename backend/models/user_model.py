from sqlmodel import Field, Relationship
from schemas.user_schema import UserBase
import models.enrollment_model as enrollment_model
import models.quizAttempt_model as quizAttempt_model
import models.notification_model as notification_model
import models.certificate_model as certificate_model


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    
    enrollments: list["enrollment_model.Enrollment"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    quiz_attempts: list["quizAttempt_model.QuizAttempt"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    notifications: list["notification_model.Notification"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    certificates: list["certificate_model.Certificate"] = Relationship(
        back_populates="user", cascade_delete=True
    )
