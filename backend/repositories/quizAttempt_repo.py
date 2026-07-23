from sqlmodel import Session, select
from models.quizAttempt_model import QuizAttempt
from datetime import datetime


def get_quiz_attempt_by_id(session: Session, attempt_id: int):
    return session.exec(select(QuizAttempt).where(QuizAttempt.id == attempt_id)).first()


def get_quiz_attempt_by_module(session: Session, module_id: int):
    return session.exec(
        select(QuizAttempt).where(QuizAttempt.module_id == module_id)
    ).first()


def get_latest_user_quiz_attempt_by_module(
    session: Session, module_id: int, user_id: int
):
    return session.exec(
        select(QuizAttempt)
        .where(QuizAttempt.module_id == module_id, QuizAttempt.user_id == user_id)
        .order_by(QuizAttempt.id.desc())
    ).first()


def get_all_quiz_attempts_by_user(session: Session, user_id: int):
    return session.exec(select(QuizAttempt).where(QuizAttempt.user_id == user_id)).all()


def start_or_resume_quiz(session: Session, module_id: int, user_id: int):
    existing_attempt = get_latest_user_quiz_attempt_by_module(
        session, module_id, user_id
    )
    if existing_attempt and existing_attempt.completed_at is None:
        return existing_attempt

    new_attempt = QuizAttempt(
        started_at=datetime.now(),
        completed_at=None,
        final_score=None,
        user_id=user_id,
        module_id=module_id,
    )
    session.add(new_attempt)
    session.commit()
    session.refresh(new_attempt)
    return new_attempt


def create_new_quiz_attempt(session: Session, module_id: int, user_id: int):
    new_attempt = QuizAttempt(
        started_at=datetime.now(),
        completed_at=None,
        final_score=None,
        user_id=user_id,
        module_id=module_id,
    )
    session.add(new_attempt)
    session.commit()
    session.refresh(new_attempt)
    return new_attempt


def submit_quiz_attempt(session: Session, attempt_id: int, final_score: float):
    db_quiz = session.get(QuizAttempt, attempt_id)
    if not db_quiz:
        return None

    db_quiz.completed_at = datetime.now()
    db_quiz.final_score = final_score

    session.add(db_quiz)
    session.commit()
    session.refresh(db_quiz)
    return db_quiz
