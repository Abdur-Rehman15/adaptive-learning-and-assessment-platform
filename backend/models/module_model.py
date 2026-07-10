from sqlmodel import Field, Relationship
from schemas.module_schema import ModuleBase

class Module(ModuleBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  course_id: int | None = Field(default=None, foreign_key="course.id")
  title: str
  order: int
  content_url: str