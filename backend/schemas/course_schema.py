from sqlmodel import SQLModel


class CourseBase(SQLModel):
    title: str
    description: str


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_by: str


class CourseUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
