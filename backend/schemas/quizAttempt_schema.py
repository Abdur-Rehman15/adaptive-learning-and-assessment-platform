from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import model_validator


class QuizAttemptBase(SQLModel):
    started_at: datetime
    completed_at: datetime | None = Field(default=None, nullable=True)
    final_score: float | None = Field(default=None, nullable=True)

    @model_validator(mode="after")
    def validate_final_score(self):
        if self is None:
            return self

        if getattr(self, "final_score", None) is not None:
            pass
            
        if getattr(self, "completed_at", None) is not None and getattr(self, "started_at", None) is not None:
            if self.completed_at < self.started_at:
                raise ValueError("Completed time cannot be earlier than start time.")
                
        return self


class QuizAttemptCreate(QuizAttemptBase):
    pass


class QuizAttemptResponse(QuizAttemptBase):
    id: int
    module_id: int
    user_id: int
