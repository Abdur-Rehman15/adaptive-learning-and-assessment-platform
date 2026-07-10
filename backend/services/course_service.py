from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.course_schema import CourseCreate, CourseUpdate
import repositories.course_repo as course_repo


def get_creator_courses(session: Session, creator_username: str):
    return course_repo.get_courses_by_username(session, creator_username)


def get_all_courses(session: Session):
    return course_repo.get_all_courses(session)


def create_course(session: Session, creator_username: str, course_in: CourseCreate):
    return course_repo.create_course(session, creator_username, course_in)


def update_course(
    session: Session,
    course_id: int,
    creator_username: str,
    updated_course: CourseUpdate,
):
    course = course_repo.get_course_by_id(session, course_id)

    if not course:
        raise HTTPException(404, "course not found with this ID")
    if course.created_by != creator_username:
        raise HTTPException(403, "you are not allowed to updated this course")

    return course_repo.update_course(session, course_id, updated_course)


def delete_course(
    session: Session,
    course_id: int,
    creator_username: str,
):
    course = course_repo.get_course_by_id(session, course_id)

    if not course:
        raise HTTPException(404, "course not found with this ID")
    if course.created_by != creator_username:
        raise HTTPException(403, "you are not allowed to delete this course")

    return course_repo.delete_course(session, course_id)
