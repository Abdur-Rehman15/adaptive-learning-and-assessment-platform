from sqlmodel import Field, Relationship
from schemas.quizAnswer_schema import QuizAnswerBase


class QuizAnswer(QuizAnswerBase, table=True):
  id: int | None=Field(default=None, primary_key=True)
  attempt_id: int | None=Field(default=None, foreign_key="quizattempt.id")
  question_id: int | None=Field(default=None, foreign_key="question.id")
