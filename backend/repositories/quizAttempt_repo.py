from sqlmodel import Session, select
from models.quizAttempt_model import QuizAttempt
from datetime import datetime


def get_quiz_attempt_by_module(session: Session, module_id: int):
    return session.exec(
        select(QuizAttempt).where(QuizAttempt.module_id == module_id)
    ).first()


def start_or_resume_quiz(session: Session, module_id: int, user_id: int):
    db_quiz_attempt = get_quiz_attempt_by_module(session, module_id)
    if db_quiz_attempt:
        return db_quiz_attempt

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


def submit_quiz_attempt(session: Session, module_id: int, final_score:float):
    db_quiz = get_quiz_attempt_by_module(session, module_id)
    db_quiz.completed_at = datetime.now()
    db_quiz.final_score = final_score
    session.add(db_quiz)
    session.commit()
    session.refresh(db_quiz)
    return db_quiz
