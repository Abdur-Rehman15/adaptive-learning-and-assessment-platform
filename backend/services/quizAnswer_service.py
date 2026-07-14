from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.quizAnswer_schema import QuizAnswerCreate
import repositories.question_repo as question_repo
import repositories.quizAnswer_repo as quizAnswer_repo
import repositories.quizAttempt_repo as quizAttempt_repo
import repositories.question_repo as question_repo
import services.quizAttempt_service as quizAttempt_service


def get_quiz_answers_by_attempt(session: Session, attempt_id: int):
    answers = quizAnswer_repo.get_quiz_answers_by_attempt(session, attempt_id)
    if not answers:
        raise HTTPException(404, "quiz answers not found with this attempt ID")
    return answers


def create_quiz_answer(
    session: Session, question_id: int, attempt_id: int, answer_in: QuizAnswerCreate
):
    question = question_repo.get_question_by_id(session, question_id)
    if not question:
        raise HTTPException(404, "question not found with this ID")
    quiz_attempt = quizAttempt_repo.get_quiz_attempt_by_id(session, attempt_id)
    if not quiz_attempt:
        raise HTTPException(404, "quiz attempt not found with this ID")
    if quiz_attempt.completed_at is not None:
        raise HTTPException(400, "this quiz attempt is already completed")
    if question.module_id != quiz_attempt.module_id:
        raise HTTPException(400, "this attempt doesn't belong to this question")
    quiz_answer = quizAnswer_repo.get_quiz_answer_by_question(
        session, question_id, attempt_id
    )
    if quiz_answer:
        raise HTTPException(400, "this question has already been answered")
    if answer_in.chosen_option.strip() not in question.options:
        raise HTTPException(400, "chosen option is different than given options")
    is_correct = question.correct_option.strip() == answer_in.chosen_option.strip()
    difficulty = question.difficulty

    current_answer = quizAnswer_repo.create_quiz_answer(
        session, question_id, attempt_id, is_correct, difficulty
    )

    next_question = quizAttempt_service.adaptive_engine_next_question(
        session, quiz_attempt, question.module_id
    )

    return {"answer": current_answer, "next_question": next_question}
