from sqlmodel import SQLModel, Field


class EnrollmentBase(SQLModel):
    status: str = Field(default="In progress")
    progress_percent: float = Field(default=0.0, ge=0.0, le=100.0)


class EnrollmentCreate(SQLModel):
    pass


class EnrollmentResponse(EnrollmentBase):
    user_id: int


class EnrollmentUpdate(SQLModel):
    status: str | None = None
    progress_percent: float | None = None
