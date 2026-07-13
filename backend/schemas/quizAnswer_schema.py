from sqlmodel import SQLModel
from pydantic import model_validator


class QuizAnswerBase(SQLModel):
    is_correct: bool
    difficulty_at_time: str

    @model_validator(mode="after")
    def validate_difficulty(self):
        if self.difficulty_at_time not in ("easy", "medium", "difficult"):
            raise ValueError("difficulty can be easy, medium, or difficult only")


class QuizAnswerResponse(QuizAnswerBase):
    id: int
    question_id: int
    attempt_id: int


class QuizAnswerCreate(SQLModel):
    chosen_option: str
