from sqlmodel import Session, select
from models.question_model import Question
from schemas.question_schema import QuestionCreate, QuestionUpdate


def get_question_by_id(session: Session, question_id: int):
    return session.exec(select(Question).where(Question.id == question_id)).first()


def get_module_questions(session: Session, module_id: int):
    return session.exec(select(Question).where(Question.module_id == module_id)).all()


def get_module_questions_by_difficulty(
    session: Session, module_id: int, difficulty: str
):
    return session.exec(
        select(Question).where(
            Question.module_id == module_id and Question.difficulty == difficulty
        )
    ).all()


def create_question(
    session: Session,
    module_id: int,
    question_in: QuestionCreate,
):
    module_question = Question.model_validate(
        question_in, update={"module_id": module_id}
    )
    session.add(module_question)
    session.commit()
    session.refresh(module_question)
    return module_question


def update_question(
    session: Session, question_id: int, updated_question: QuestionUpdate
):
    question = get_question_by_id(session, question_id)
    updated = updated_question.model_dump(exclude_unset=True)
    for k, v in updated.items():
        setattr(question, k, v)
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def delete_question(session: Session, question_id: int):
    question = get_question_by_id(session, question_id)
    session.delete(question)
    session.commit()
