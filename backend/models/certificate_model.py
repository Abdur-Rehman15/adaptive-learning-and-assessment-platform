from sqlmodel import Field, Relationship
from schemas.certificate_schema import CertificateBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user_model import User
    from models.course_model import Course


class Certificate(CertificateBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    course_id: int | None = Field(
        default=None, foreign_key="course.id", ondelete="CASCADE"
    )
    user: "User" = Relationship(back_populates="certificates")
    course: "Course" = Relationship(back_populates="certificates")


