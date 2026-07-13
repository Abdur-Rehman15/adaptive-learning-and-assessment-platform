from fastapi import HTTPException
from sqlalchemy.orm import Session
import repositories.user_repo as user_repo
import repositories.quizAttempt_repo as quizAttempt_repo
import repositories.module_repo as module_repo


def get_module_quiz_attempt(session: Session, module_id: int):
    attempt = quizAttempt_repo.get_quiz_attempt_by_module(session, module_id)
    if not attempt:
        raise HTTPException(404, "no quiz attempt found")

    return attempt


def start_or_resume_quiz(session: Session, module_id: int, user_id: int):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, "user not found")
    module = module_repo.get_module_by_id(session, module_id)
    if not module:
        raise HTTPException(404, "module not found")
    attempt = quizAttempt_repo.get_quiz_attempt_by_module(session, module_id)
    if attempt:
        if user.id != attempt.user_id:
            raise HTTPException(400, "user doesn't belong to this quiz")
        return attempt

    return quizAttempt_repo.start_or_resume_quiz(session, module_id, user_id)


def submit_quiz(session: Session, module_id: int, final_score: float):
    attempt = get_module_quiz_attempt(session, module_id)
    if not attempt:
        raise HTTPException(404, "quiz attempt not found")

    return quizAttempt_repo.submit_quiz_attempt(session, module_id, final_score)
