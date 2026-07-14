import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Session, select
from models.quizAnswer_model import QuizAnswer
from models.quizAttempt_model import QuizAttempt
import repositories.user_repo as user_repo
import repositories.quizAttempt_repo as quizAttempt_repo
import repositories.module_repo as module_repo
import repositories.question_repo as question_repo
import repositories.quizAnswer_repo as quizAnswer_repo
import services.quizAnswer_service as quizAnswer_service
import services.enrollment_service as enrollment_service


def __calculate_final_score(attempted_answers: list[QuizAnswer]):

    weights = {"easy": 1.0, "medium": 2.0, "hard": 3.0}

    total_points = 0.0
    earned_points = 0.0

    for ans in attempted_answers:
        difficulty = (
            ans.difficulty_at_time.lower() if ans.difficulty_at_time else "medium"
        )

        weight = weights.get(difficulty, 1.0)
        total_points += weight

        if ans.is_correct is True:
            earned_points += weight

    if total_points == 0.0:
        return 0.0

    return round((earned_points / total_points) * 100, 2)


def adaptive_engine_next_question(
    session: Session, quiz_attempt: QuizAttempt, module_id: int
):
    attempted_answers = quizAnswer_repo.get_quiz_answers_by_attempt(
        session, quiz_attempt.id
    )
    attempted_answers = sorted(attempted_answers, key=lambda ans: ans.id)

    difficulty = "medium"
    last_difficulty = None
    second_last_difficulty = None
    last_correctness = None
    second_last_correctness = None

    if attempted_answers:
        last_difficulty = (
            attempted_answers[-1].difficulty_at_time.lower()
            if len(attempted_answers) >= 1
            else None
        )
        second_last_difficulty = (
            attempted_answers[-2].difficulty_at_time.lower()
            if len(attempted_answers) >= 2
            else None
        )

        last_correctness = (
            attempted_answers[-1].is_correct if len(attempted_answers) >= 1 else None
        )
        second_last_correctness = (
            attempted_answers[-2].is_correct if len(attempted_answers) >= 2 else None
        )

        if second_last_difficulty is None and last_correctness is True:
            difficulty = "hard"

        elif second_last_correctness is True and last_correctness is True:
            if last_difficulty == "easy":
                difficulty = "medium"
            elif last_difficulty == "medium":
                difficulty = "hard"
            elif last_difficulty == "hard":
                difficulty = "hard"

        elif last_correctness is False:
            if last_difficulty == "hard":
                difficulty = "medium"
            else:
                difficulty = "easy"

    questions = question_repo.get_module_questions_by_difficulty(
        session, module_id, difficulty
    )
    answered_ids = {ans.question_id for ans in attempted_answers}
    available_questions = [q for q in questions if q.id not in answered_ids]
    selected_question = (
        random.choice(available_questions) if available_questions else None
    )

    if selected_question is None:
        all_questions = question_repo.get_module_questions(session, module_id)
        fallback = [q for q in all_questions if q.id not in answered_ids]
        selected_question = random.choice(fallback) if fallback else None

    return selected_question


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

    attempt = quizAttempt_repo.get_latest_user_quiz_attempt_by_module(
        session, module_id, user_id
    )

    if attempt:
        if attempt.completed_at is not None:
            raise HTTPException(
                400, "this quiz is already completed. you can retry instead"
            )

        next_question = adaptive_engine_next_question(session, attempt, module_id)
        return {"attempt": attempt, "next_question": next_question}

    new_attempt = quizAttempt_repo.start_or_resume_quiz(session, module_id, user_id)
    next_question = adaptive_engine_next_question(session, new_attempt, module_id)
    return {"attempt": new_attempt, "next_question": next_question}


def retry_quiz(session: Session, module_id: int, user_id: int):
    user = user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(404, "user not found")

    attempt = quizAttempt_repo.get_latest_user_quiz_attempt_by_module(
        session, module_id, user_id
    )

    if not attempt:
        raise HTTPException(400, "this quiz was never started. you can not retry this")
    if attempt.completed_at is None:
        raise HTTPException(
            400, "this quiz is already in progress. complete unfinished quiz first"
        )
    if attempt.final_score >= 80.0:
        raise HTTPException(
            400, "you have already passed this course with atleast 80 score or higher"
        )

    new_attempt = quizAttempt_repo.create_new_quiz_attempt(session, module_id, user_id)
    next_question = adaptive_engine_next_question(session, new_attempt, module_id)
    return {"attempt": new_attempt, "next_question": next_question}


def submit_quiz(session: Session, module_id: int, user_id: int):
    attempt = quizAttempt_repo.get_latest_user_quiz_attempt_by_module(
        session, module_id, user_id
    )

    if not attempt:
        raise HTTPException(404, "active quiz attempt not found to submit")
    if attempt.completed_at is not None:
        raise HTTPException(
            400, "This quiz attempt has already been submitted and completed."
        )

    attempted_answers = quizAnswer_service.get_quiz_answers_by_attempt(
        session, attempt.id
    )
    questions = question_repo.get_module_questions(session, module_id)
    if len(attempted_answers) < len(questions):
        raise HTTPException(400, "attempt all the questions first")

    final_score = __calculate_final_score(attempted_answers)
    result = quizAttempt_repo.submit_quiz_attempt(session, attempt.id, final_score)

    student_enrollments = enrollment_service.get_student_enrollments(session, user_id)
    db_module = module_repo.get_module_by_id(session, module_id)

    if db_module:
        target_enrollment = next(
            (e for e in student_enrollments if e.course_id == db_module.course_id),
            None,
        )
        if target_enrollment:
            enrollment_service.update_enrollment_progress(
                session, target_enrollment.id, user_id, db_module.course_id
            )

    return result
