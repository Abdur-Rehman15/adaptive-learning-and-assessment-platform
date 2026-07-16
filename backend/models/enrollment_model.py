from sqlmodel import Field, Relationship
from schemas.enrollment_schema import EnrollmentBase


class Enrollment(EnrollmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    course_id: int | None = Field(
        default=None, foreign_key="course.id", ondelete="CASCADE"
    )
