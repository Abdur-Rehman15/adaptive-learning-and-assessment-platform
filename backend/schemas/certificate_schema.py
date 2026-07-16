from sqlmodel import SQLModel
from datetime import datetime


class CertificateBase(SQLModel):
    issued_at: datetime
    verification_code: int


class CertificateCreate(CertificateBase):
    pass


class CertificateResponse(SQLModel):
    user_id: int
    course_id: int
    issued_at: datetime
    verification_code: int
