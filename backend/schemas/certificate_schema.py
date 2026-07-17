from sqlmodel import SQLModel
from datetime import datetime
from pydantic import Field


class CertificateBase(SQLModel):
    issued_at: datetime
    verification_code: int = Field(
        ge=1000, le=9999, description="verification code should be 4 digits length"
    )


class CertificateCreate(CertificateBase):
    pass


class CertificateResponse(SQLModel):
    user_id: int
    course_id: int
    issued_at: datetime
    verification_code: int
