from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.enrollment_schema import EnrollmentCreate, EnrollmentUpdate
from models.certificate_model import Certificate
import repositories.enrollment_repo as enrollment_repo
import repositories.user_repo as user_repo
import repositories.course_repo as course_repo
import repositories.module_repo as module_repo
import repositories.quizAttempt_repo as quizAttempt_repo
import services.certificate_service as certificate_service
from datetime import datetime
import random


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


def __calculate_enrollment_progress(
    session: Session,
    user_id: int,
    course_id: int,
):
    enrollments = enrollment_repo.get_enrollments_by_student_id(session, user_id)
    if not enrollments:
        raise HTTPException(400, "student is not enrolled in any course")
    course_ids = {e.course_id for e in enrollments}
    if course_id not in course_ids:
        raise HTTPException(400, "course ID not enrolled by this student")
    modules = module_repo.get_course_modules(session, course_id)
    if not modules:
        raise HTTPException(400, "this course has no modules")

    course_module_ids = {m.id for m in modules}
    all_user_attempts = quizAttempt_repo.get_all_quiz_attempts_by_user(session, user_id)
    completed_module_ids = {
        attempt.module_id
        for attempt in all_user_attempts
        if attempt.module_id in course_module_ids
        and attempt.completed_at is not None
        and attempt.final_score is not None
    }

    return round((len(completed_module_ids) / len(modules)) * 100, 2)


def update_enrollment_progress(
    session: Session, enrollment_id: int, user_id: int, course_id: int
):
    enrollment = enrollment_repo.get_enrollment_by_id(session, enrollment_id)
    if not enrollment:
        raise HTTPException(404, "enrollment not found with this ID")

    new_progress = __calculate_enrollment_progress(session, user_id, course_id)
    new_status = enrollment.status

    if new_progress >= 100:
        new_status = "Completed"
        certificate_in = Certificate(
            issued_at=datetime.now().date(), verification_code=random.randint(0, 9999)
        )
        certificate_service.create_certificate(
            session, user_id, course_id, certificate_in
        )
        
    updated = EnrollmentUpdate(progress_percent=new_progress, status=new_status)
    return enrollment_repo.update_enrollment(session, enrollment_id, updated)


def unenroll_course(session: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_enrollment_by_id(session, enrollment_id)
    if not enrollment:
        raise HTTPException(404, "enrollment not found with this ID")
    enrollment_repo.unenroll_course(session, enrollment_id)
