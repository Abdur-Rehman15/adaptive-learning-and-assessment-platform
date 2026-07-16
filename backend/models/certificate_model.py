from sqlmodel import Field
from schemas.certificate_schema import CertificateBase


class Certificate(CertificateBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    course_id: int | None = Field(
        default=None, foreign_key="course.id", ondelete="CASCADE"
    )
