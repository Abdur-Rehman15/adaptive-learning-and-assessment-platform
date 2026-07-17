from sqlmodel import Field, Relationship
from schemas.quizAttempt_schema import QuizAttemptBase
import models.quizAttempt_model as quizAttempt_model


class QuizAttempt(QuizAttemptBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    module_id: int | None = Field(default=None, foreign_key="module.id")
    user: "User" = Relationship(back_populates="quiz_attempts")

