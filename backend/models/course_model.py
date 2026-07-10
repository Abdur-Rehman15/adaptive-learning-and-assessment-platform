from sqlmodel import Field, Relationship
from schemas.course_schema import CourseBase


class Course(CourseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_by: str | None = Field(default=None)
