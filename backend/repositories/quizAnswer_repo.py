from sqlmodel import Session, select
from models.quizAnswer_model import QuizAnswer
from schemas.quizAnswer_schema import QuizAnswerCreate


def get_quiz_answers_by_attempt(session: Session, attempt_id: int):
    return session.exec(
        select(QuizAnswer).where(QuizAnswer.attempt_id == attempt_id)
    ).all()


def get_quiz_answer_by_question(session: Session, question_id: int, attempt_id: int):
    return session.exec(
        select(QuizAnswer).where(
            QuizAnswer.question_id == question_id, QuizAnswer.attempt_id == attempt_id
        )
    ).first()


def create_quiz_answer(
    session: Session,
    question_id: int,
    attempt_id: int,
    is_correct: bool,
    difficulty: str,
):
    quiz_answer = QuizAnswer(
        is_correct=is_correct,
        difficulty_at_time=difficulty,
        attempt_id=attempt_id,
        question_id=question_id,
    )
    quiz_answer.question_id = question_id
    quiz_answer.attempt_id = attempt_id
    session.add(quiz_answer)
    session.commit()
    session.refresh(quiz_answer)
    return quiz_answer
