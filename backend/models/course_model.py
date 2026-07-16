from sqlmodel import Field, Relationship
from schemas.course_schema import CourseBase
import models.module_model as module_model
import models.enrollment_model as enrollment_model
import models.certificate_model as certificate_model


class Course(CourseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_by: str | None = Field(default=None)
    modules: list["module_model.Module"] = Relationship(
        back_populates="course", cascade_delete=True
    )
    enrollments: list["enrollment_model.Enrollment"] = Relationship(
        back_populates="course", cascade_delete=True
    )
    certificates: list["certificate_model.Certificate"] = Relationship(
        back_populates="course", cascade_delete=True
    )
