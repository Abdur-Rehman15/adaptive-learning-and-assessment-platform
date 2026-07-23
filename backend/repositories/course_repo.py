from sqlmodel import Session, select
from models.course_model import Course
from schemas.course_schema import CourseCreate, CourseUpdate
import repositories.module_repo as module_repo


def get_course_by_id(session: Session, course_id: int):
    return session.get(Course, course_id)


def get_courses_by_username(session: Session, username: str):
    statement = select(Course).where(Course.created_by == username)
    return session.exec(statement).all()


def get_all_courses(session: Session):
    return session.exec(select(Course)).all()


def create_course(session: Session, creator_username: str, course_in: CourseCreate):
    db_course = Course.model_validate(course_in)
    db_course.created_by = creator_username
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


def update_course(session: Session, course_id: int, updated_course: CourseUpdate):
    course = get_course_by_id(session, course_id)
    if course:
        db_course = updated_course.model_dump(exclude_unset=True)
        for k, v in db_course.items():
            setattr(course, k, v)
        session.add(course)
        session.commit()
        session.refresh(course)

    return course


def delete_course(session: Session, course_id: int):
    course = get_course_by_id(session, course_id)
    if course:
        modules = module_repo.get_course_modules(session, course_id)
        for module in modules:
            if module.id is not None:
                module_repo.delete_module(session, module.id, commit=False)

        session.delete(course)
        session.commit()
