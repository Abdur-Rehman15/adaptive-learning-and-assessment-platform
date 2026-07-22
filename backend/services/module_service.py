from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.module_schema import ModuleCreate, ModuleUpdate, ModuleUpdateOrder
import repositories.module_repo as module_repo
import repositories.course_repo as course_repo
from middleware.notification_decorator import notify


def get_course_modules(session: Session, course_id: int):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course doesn't exist")
    return module_repo.get_course_modules(session, course_id)


@notify(
    type="module_creation",
    message="Module successfully added to Course ID {course_id}",
    user_id_pos=3,
)
def create_module(
    session: Session, course_id: int, module_in: ModuleCreate, creator_username: str
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course doesn't exist")
    if course.created_by != creator_username:
        raise HTTPException(
            403, "you are not allowed to create a module in this course"
        )
    result = module_repo.create_module(session, course_id, module_in)
    if result:
        result.course_id = course_id
    return result


@notify(
    type="module_update",
    message="Module ID {module_id} has been modified",
    user_id_pos=4,
)
def update_module(
    session: Session,
    course_id: int,
    module_id: int,
    updated_module: ModuleUpdate,
    creator_username: str,
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course doesn't exist")
    if course.created_by != creator_username:
        raise HTTPException(
            403, "you are not allowed to update a module in this course"
        )
    module = module_repo.get_module_by_id(session, module_id)
    if not module:
        raise HTTPException(404, "module doesn't exist")

    result = module_repo.update_module(session, module_id, updated_module)
    if result:
        result.module_id = module.id
    return result


def update_modules_order(
    session: Session, course_id: int, updated_order: list[ModuleUpdateOrder]
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course doesn't exist")
    course_modules = module_repo.get_course_modules(session, course_id)
    valid_ids = {module.id for module in course_modules}
    for item in updated_order:
        if item.module_id not in valid_ids:
            raise HTTPException(400, "module id doesnt belong to this course")

    return module_repo.update_modules_order(session, course_id, updated_order)


def delete_module(
    session: Session, course_id: int, module_id: int, creator_username: str
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course doesn't exist")
    if course.created_by != creator_username:
        raise HTTPException(
            403, "you are not allowed to delete a module in this course"
        )
    module = module_repo.get_module_by_id(session, module_id)
    if not module:
        raise HTTPException(404, "module doesn't exist")

    return module_repo.delete_module(session, module_id)
