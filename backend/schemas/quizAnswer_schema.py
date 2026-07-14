from sqlmodel import SQLModel
from pydantic import model_validator
from schemas.question_schema import QuestionResponse


class QuizAnswerBase(SQLModel):
    is_correct: bool
    difficulty_at_time: str

    @model_validator(mode="after")
    def validate_difficulty(self):
        if self.difficulty_at_time not in ("easy", "medium", "hard"):
            raise ValueError("difficulty can be easy, medium, or hard only")
        return self


class QuizAnswerResponse(QuizAnswerBase):
    id: int
    question_id: int
    attempt_id: int


class QuizAnswerCreate(SQLModel):
    chosen_option: str


class QuizAnswerSubmissionResponse(SQLModel):
    answer: QuizAnswerResponse
    next_question: QuestionResponse | None = None
