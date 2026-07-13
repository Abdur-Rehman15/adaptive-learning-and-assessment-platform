from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.enrollment_schema import EnrollmentCreate, EnrollmentUpdate
import repositories.enrollment_repo as enrollment_repo
import repositories.user_repo as user_repo
import repositories.course_repo as course_repo


def get_student_enrollments(session: Session, user_id: int):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, "student not found with this ID")

    return enrollment_repo.get_enrollments_by_student_id(session, user_id)


def create_enrollment(
    session: Session, course_id: int, user_id: int, enrollment_in: EnrollmentCreate
):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, "student not found with this ID")
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course not found with this ID")
    enrollments = get_student_enrollments(session, user.id)
    existing_course_ids = {e.course_id for e in enrollments}
    if course.id in existing_course_ids:
        raise HTTPException(400, "student already enrolled in this course")

    return enrollment_repo.create_enrollment(session, user_id, course_id, enrollment_in)


def update_enrollment(
    session: Session, enrollment_id: int, updated_enrollment: EnrollmentUpdate
):
    enrollment = enrollment_repo.get_enrollment_by_id(session, enrollment_id)
    if not enrollment:
        raise HTTPException(404, "enrollment not found with this ID")
    return enrollment_repo.update_enrollment(session, enrollment_id, updated_enrollment)


def unenroll_course(session: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_enrollment_by_id(session, enrollment_id)
    if not enrollment:
        raise HTTPException(404, "enrollment not found with this ID")
    enrollment_repo.unenroll_course(session, enrollment_id)
