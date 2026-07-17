from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.question_schema import QuestionCreate, QuestionUpdate
import repositories.question_repo as question_repo
import repositories.module_repo as module_repo
import repositories.course_repo as course_repo
from middleware.notification_decorator import notify


def get_question_by_id(session: Session, question_id: int):
    question = question_repo.get_question_by_id(session, question_id)
    if not question:
        raise HTTPException(404, "question not found with this ID")
    return question


def get_module_questions(session: Session, module_id: int):
    module = module_repo.get_module_by_id(session, module_id)
    if not module:
        raise HTTPException(404, "module not found")
    return question_repo.get_module_questions(session, module_id)


@notify(
    type="question_creation",
    message="A new question was successfully added to module ID {module_id}.",
)
def create_question(
    session: Session, module_id: int, question_in: QuestionCreate, creator_username: str
):
    module = module_repo.get_module_by_id(session, module_id)
    if not module:
        raise HTTPException(404, "module not found")

    course = course_repo.get_course_by_id(session, module.course_id)
    if not course or course.created_by != creator_username:
        raise HTTPException(
            403, "you are not allowed to create a question in this module"
        )
    new_question = question_repo.create_question(session, module_id, question_in)
    new_question.module_id = module.id
    return new_question


@notify(type="question_update", message="Question ID {question_id} has been modified.")
def update_question(
    session: Session,
    question_id: int,
    updated_question: QuestionUpdate,
    creator_username: str,
):
    question = get_question_by_id(session, question_id)
    module = module_repo.get_module_by_id(session, question.module_id)
    if not module:
        raise HTTPException(404, "module not found")

    course = course_repo.get_course_by_id(session, module.course_id)
    if not course or course.created_by != creator_username:
        raise HTTPException(403, "you are not allowed to update this question")

    updated_question = question_repo.update_question(
        session, question_id, updated_question
    )
    updated_question.question_id = question.id
    return updated_question


def delete_question(session: Session, question_id: int, creator_username: str):
    question = get_question_by_id(session, question_id)
    module = module_repo.get_module_by_id(session, question.module_id)
    if not module:
        raise HTTPException(404, "module not found")

    course = course_repo.get_course_by_id(session, module.course_id)
    if not course or course.created_by != creator_username:
        raise HTTPException(403, "you are not allowed to delete this question")

    question_repo.delete_question(session, question_id)
