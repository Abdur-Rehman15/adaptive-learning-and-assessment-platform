from sqlmodel import SQLModel
from pydantic import Field


class CourseBase(SQLModel):
    title: str = Field(
        min_length=10, description="course title should be 10 characters length atleast"
    )
    description: str = Field(
        min_length=200,
        max_length=1000,
        description="course description characters length should be in between 200 and 1000 characters",
    )


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_by: str


class CourseUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
