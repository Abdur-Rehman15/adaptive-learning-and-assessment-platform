from fastapi import HTTPException
from sqlmodel import Session, select, func
from models.quizAttempt_model import QuizAttempt
from models.question_model import Question
from models.quizAnswer_model import QuizAnswer
from models.module_model import Module
from models.enrollment_model import Enrollment
import repositories.module_repo as module_repo
import repositories.enrollment_repo as enrollment_repo


def get_learner_course_overview(session: Session, user_id: int, course_id: int):
    enrollments = enrollment_repo.get_enrollments_by_student_id(session, user_id)
    if not enrollments:
        raise HTTPException(404, "student not enrolled in any course")
    modules = module_repo.get_course_modules(session, course_id)
    module_ids = {m.id for m in modules}

    attempts = session.exec(
        select(QuizAttempt).where(
            QuizAttempt.user_id == user_id, QuizAttempt.module_id.in_(module_ids)
        )
    ).all()

    scores = [a.final_score for a in attempts if a.final_score is not None]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    attempt_ids = [a.id for a in attempts]
    wrong_answers = session.exec(
        select(Question.topic, func.count(QuizAnswer.id))
        .join(QuizAnswer, QuizAnswer.question_id == Question.id)
        .where(QuizAnswer.attempt_id.in_(attempt_ids), QuizAnswer.is_correct == False)
        .group_by(Question.topic)
    ).all()

    sorted_weak_topics = [topic for topic, count in sorted(wrong_answers, key=lambda x: x[1], reverse=True)]

    return {
        "course_id": course_id,
        "progress_percent": enrollments.progress_percent,
        "average_quiz_score": avg_score,
        "weakest_topics": sorted_weak_topics[:3]
    }


def get_learner_score_trends(session: Session, user_id: int, course_id: int):
    
    modules = session.exec(select(Module).where(Module.course_id == course_id)).all()
    if not modules:
        return []
    
    module_map = {m.id: m.title for m in modules}
    
    statement = (
        select(QuizAttempt)
        .where(
            QuizAttempt.user_id == user_id,
            QuizAttempt.module_id.in_(list(module_map.keys())),
            QuizAttempt.completed_at != None
        )
        .order_by(QuizAttempt.completed_at.asc())
    )
    attempts = session.exec(statement).all()
    
    return [
        {
            "attempt_id": a.id,
            "module_title": module_map.get(a.module_id, "Unknown Module"),
            "final_score": a.final_score
        }
        for a in attempts
    ]


def get_instructor_course_analytics(session: Session, course_id: int):
    enrollments = session.exec(
        select(Enrollment).where(Enrollment.course_id == course_id)
    ).all()
    
    total_learners = len(enrollments)
    if total_learners == 0:
        return {
            "total_enrolled_learners": 0,
            "course_average_progress": 0.0,
            "completion_rate_percent": 0.0
        }
        
    total_progress = sum(e.progress_percent for e in enrollments)
    avg_progress = round(total_progress / total_learners, 2)
    
    completed_count = sum(1 for e in enrollments if e.status == "Completed")
    completion_rate = round((completed_count / total_learners) * 100, 2)
    
    return {
        "total_enrolled_learners": total_learners,
        "course_average_progress": avg_progress,
        "completion_rate_percent": completion_rate
    }
