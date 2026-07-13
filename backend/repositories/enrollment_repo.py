from sqlmodel import Session, select
from models.enrollment_model import Enrollment
from schemas.enrollment_schema import EnrollmentCreate, EnrollmentUpdate


def get_enrollment_by_id(session: Session, enroll_id: int):
    return session.exec(select(Enrollment).where(Enrollment.id == enroll_id)).first()


def get_enrollments_by_student_id(session: Session, student_id: int):
    return session.exec(
        select(Enrollment).where(Enrollment.user_id == student_id)
    ).all()


def create_enrollment(session: Session, user_id: int, course_id: int, enrollment_in: EnrollmentCreate):
    db_enrollment = Enrollment.model_validate(enrollment_in)
    db_enrollment.user_id = user_id
    db_enrollment.course_id = course_id
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment


def update_enrollment(
    session: Session, enrollment_id: int, updated_enrollment: EnrollmentUpdate
):
    db_enrollment = get_enrollment_by_id(session, enrollment_id)
    updated = updated_enrollment.model_dump(exclude_unset=True)
    for k, v in updated.items():
        setattr(db_enrollment, k, v)
    session.add(db_enrollment)
    session.commit()
    session.refresh(db_enrollment)
    return db_enrollment


def unenroll_course(session: Session, enrollment_id: int):
    db_enrollment = get_enrollment_by_id(session, enrollment_id)
    session.delete(db_enrollment)
    session.commit()