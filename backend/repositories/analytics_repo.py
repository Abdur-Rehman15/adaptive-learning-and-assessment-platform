from fastapi import HTTPException
from sqlmodel import Session, select, func
from models.quizAttempt_model import QuizAttempt
from models.quizAnswer_model import QuizAnswer
from models.question_model import Question


def get_wrong_answers(session: Session, attempt_ids):
    return session.exec(
        select(Question.topic, func.count(QuizAnswer.id))
        .join(QuizAnswer, QuizAnswer.question_id == Question.id)
        .where(QuizAnswer.attempt_id.in_(attempt_ids), QuizAnswer.is_correct == False)
        .group_by(Question.topic)
    ).all()


def get_module_attempts(session: Session, user_id: int, module_ids):
    session.exec(
        select(QuizAttempt).where(
            QuizAttempt.user_id == user_id, QuizAttempt.module_id.in_(module_ids)
        )
    ).all()


def get_module_attempts_for_trends(session: Session, user_id: int, module_map):
    statement = (
        select(QuizAttempt)
        .where(
            QuizAttempt.user_id == user_id,
            QuizAttempt.module_id.in_(list(module_map.keys())),
            QuizAttempt.completed_at != None,
        )
        .order_by(QuizAttempt.completed_at.asc())
    )
    return session.exec(statement).all()
