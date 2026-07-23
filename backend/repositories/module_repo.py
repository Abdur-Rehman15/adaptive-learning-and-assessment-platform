from sqlmodel import Session, select
from models.module_model import Module
from models.question_model import Question
from models.quizAttempt_model import QuizAttempt
from models.quizAnswer_model import QuizAnswer
from schemas.module_schema import ModuleCreate, ModuleUpdate, ModuleUpdateOrder


def get_module_by_id(session: Session, module_id: int):
    return session.exec(select(Module).where(Module.id == module_id)).first()


def get_course_modules(session: Session, course_id: int):
    return session.exec(select(Module).where(Module.course_id == course_id)).all()


def _delete_module_dependencies(session: Session, module_id: int):
    attempts = session.exec(
        select(QuizAttempt).where(QuizAttempt.module_id == module_id)
    ).all()

    for attempt in attempts:
        answers = session.exec(
            select(QuizAnswer).where(QuizAnswer.attempt_id == attempt.id)
        ).all()
        for answer in answers:
            session.delete(answer)
        session.delete(attempt)

    questions = session.exec(
        select(Question).where(Question.module_id == module_id)
    ).all()
    for question in questions:
        session.delete(question)


def create_module(
    session: Session,
    course_id: int,
    module_in: ModuleCreate,
):
    course_module = Module.model_validate(module_in)
    course_module.course_id = course_id
    session.add(course_module)
    session.commit()
    session.refresh(course_module)
    return course_module


def update_module(session: Session, module_id: int, updated_module: ModuleUpdate):
    module = get_module_by_id(session, module_id)
    updated = updated_module.model_dump(exclude_unset=True)
    for k, v in updated.items():
        setattr(module, k, v)
    session.add(module)
    session.commit()
    session.refresh(module)
    return module


def update_modules_order(
    session: Session, course_id: int, order_data: list[ModuleUpdateOrder]
):
    modules = get_course_modules(session, course_id)
    module_map = {m.id: m for m in modules}
    for item in order_data:
        module_map[item.module_id].order = item.order

    session.commit()


def delete_module(session: Session, module_id: int, *, commit: bool = True):
    module = get_module_by_id(session, module_id)
    if not module:
        return None

    _delete_module_dependencies(session, module_id)
    session.delete(module)
    if commit:
        session.commit()
    return module
