from fastapi import HTTPException
from sqlmodel import Session
import repositories.module_repo as module_repo
import repositories.enrollment_repo as enrollment_repo
import repositories.analytics_repo as analytics_repo
import repositories.course_repo as course_repo
import repositories.user_repo as user_repo
import services.enrollment_service as enrollment_service


def get_learner_course_overview(session: Session, user_id: int, course_id: int):
    student_enrollments = enrollment_service.get_student_enrollments(session, user_id)

    enrollment = next(
        (e for e in student_enrollments if e.course_id == course_id), None
    )
    if not enrollment:
        raise HTTPException(404, "student not enrolled in this course")

    modules = module_repo.get_course_modules(session, course_id)
    module_ids = {m.id for m in modules}

    attempts_result = analytics_repo.get_module_attempts(session, user_id, module_ids)

    if hasattr(attempts_result, "all"):
        attempts = attempts_result.all()
    elif isinstance(attempts_result, list):
        attempts = attempts_result
    else:
        attempts = []

    scores = [
        a.final_score
        for a in attempts
        if a and getattr(a, "final_score", None) is not None
    ]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    attempt_ids = [a.id for a in attempts if a]
    wrong_answers = (
        analytics_repo.get_wrong_answers(session, attempt_ids) if attempt_ids else []
    )

    sorted_weak_topics = [
        topic
        for topic, count in sorted(wrong_answers, key=lambda x: x[1], reverse=True)
    ]

    return {
        "course_id": course_id,
        "progress_percent": enrollment.progress_percent,
        "average_quiz_score": avg_score,
        "weakest_topics": sorted_weak_topics[:3],
    }


def get_learner_score_trends(session: Session, user_id: int, course_id: int):

    modules = module_repo.get_course_modules(session, course_id)
    if not modules:
        return []

    module_map = {m.id: m.title for m in modules}

    attempts = analytics_repo.get_module_attempts_for_trends(
        session, user_id, module_map
    )

    return [
        {
            "attempt_id": a.id,
            "module_title": module_map.get(a.module_id, "Unknown Module"),
            "final_score": a.final_score,
        }
        for a in attempts
    ]


def __average_score(scores: list[float]) -> float:
    return round(sum(scores) / len(scores), 2) if scores else 0.0


def __build_empty_module_metrics(modules):
    return [
        {
            "module_id": module.id,
            "title": module.title,
            "learners": 0,
            "completion_rate": 0.0,
            "average_score": 0.0,
        }
        for module in modules
    ]


def get_instructor_course_analytics(
    session: Session, course_id: int, instructor_username: str
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course not found with this ID")
    if course.created_by != instructor_username:
        raise HTTPException(403, "you are not allowed to access this course analytics")

    modules = module_repo.get_course_modules(session, course_id)
    module_ids = {module.id for module in modules}
    enrollments = enrollment_repo.get_course_enrollments(session, course_id)
    completed_attempts = analytics_repo.get_completed_attempts_for_modules(
        session, module_ids
    )

    total_learners = len(enrollments)
    if total_learners == 0:
        return {
            "total_enrolled_learners": 0,
            "course_average_progress": 0.0,
            "completion_rate_percent": 0.0,
            "course_average_quiz_score": 0.0,
            "modules": __build_empty_module_metrics(modules),
            "learners": [],
        }

    total_progress = sum(enrollment.progress_percent for enrollment in enrollments)
    avg_progress = round(total_progress / total_learners, 2)

    completed_count = sum(
        1 for enrollment in enrollments if enrollment.status == "Completed"
    )
    completion_rate = round((completed_count / total_learners) * 100, 2)

    all_scores = [attempt.final_score for attempt in completed_attempts]
    course_average_quiz_score = __average_score(all_scores)

    learners = []
    for enrollment in enrollments:
        user = user_repo.get_user_by_id(session, enrollment.user_id)
        user_attempts = [
            attempt
            for attempt in completed_attempts
            if attempt.user_id == enrollment.user_id
        ]
        user_scores = [attempt.final_score for attempt in user_attempts]

        learners.append(
            {
                "user_id": enrollment.user_id,
                "username": user.username if user else f"Learner {enrollment.user_id}",
                "progress_percent": enrollment.progress_percent,
                "score": __average_score(user_scores),
                "status": enrollment.status,
            }
        )

    module_metrics = []
    for module in modules:
        module_attempts = [
            attempt for attempt in completed_attempts if attempt.module_id == module.id
        ]
        completed_user_ids = {attempt.user_id for attempt in module_attempts}
        module_scores = [attempt.final_score for attempt in module_attempts]

        module_metrics.append(
            {
                "module_id": module.id,
                "title": module.title,
                "learners": len(completed_user_ids),
                "completion_rate": round(
                    (len(completed_user_ids) / total_learners) * 100, 2
                ),
                "average_score": __average_score(module_scores),
            }
        )

    return {
        "total_enrolled_learners": total_learners,
        "course_average_progress": avg_progress,
        "completion_rate_percent": completion_rate,
        "course_average_quiz_score": course_average_quiz_score,
        "modules": module_metrics,
        "learners": learners,
    }
