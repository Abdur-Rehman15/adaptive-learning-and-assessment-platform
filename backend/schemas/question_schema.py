from enum import Enum
from sqlmodel import SQLModel
from typing import List
from pydantic import model_validator, Field


class QuestionType(str, Enum):
    MCQ = "multiple_choice"
    TF = "true_false"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionBase(SQLModel):
    question_type: QuestionType = QuestionType.MCQ
    text: str = Field(
        min_length=20,
        description="question text length should be atleast 15 characters",
    )
    topic: str = Field(
        min_length=3,
        description="question text length should be atleast 3 characters",
    )
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    options: List[str]
    correct_option: str


class QuestionCreate(QuestionBase):

    @model_validator(mode="after")
    def validate_creation_payload(self) -> "QuestionCreate":
        if self.question_type == QuestionType.TF:
            self.options = ["True", "False"]
            if self.correct_option not in ["True", "False"]:
                raise ValueError(
                    "For True/False questions, correct_option must be 'True' or 'False'"
                )

        elif self.question_type == QuestionType.MCQ:
            if len(self.options) < 2:
                raise ValueError(
                    "Multiple choice questions must have at least 2 options"
                )
            if self.correct_option not in self.options:
                raise ValueError(
                    "correct_option must exactly match one of the items in the options list"
                )

        return self


class QuestionResponse(QuestionBase):
    id: int
    module_id: int


class QuestionUpdate(SQLModel):
    question_type: QuestionType | None = None
    text: str | None = None
    topic: str | None = None
    difficulty: DifficultyLevel | None = None
    options: list[str] | None = None
    correct_option: str | None = None

    @model_validator(mode="after")
    def validate_update_payload(self) -> "QuestionUpdate":
        if self.question_type == QuestionType.TF and self.correct_option:
            self.options = ["True", "False"]
            if self.correct_option not in ["True", "False"]:
                raise ValueError(
                    "For True/False updates, correct_option must be 'True' or 'False'"
                )
        return self
