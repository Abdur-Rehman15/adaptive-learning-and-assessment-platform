from sqlmodel import Field, Relationship
from schemas.quizAttempt_schema import QuizAttemptBase


class QuizAttempt(QuizAttemptBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    module_id: int | None = Field(default=None, foreign_key="module.id")
