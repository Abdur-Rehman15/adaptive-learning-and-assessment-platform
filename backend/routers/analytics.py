from fastapi import APIRouter, Depends, status
from database.database import SessionDep
from middleware.verifyRole import verify_role
from schemas.analytics_schema import (
    LearnerOverviewResponse,
    ScoreTrendPoint,
    InstructorDashboardResponse,
)
import services.analytics_service as analytics_service

router = APIRouter()


@router.get(
    "/courses/{course_id}/learner-summary",
    response_model=LearnerOverviewResponse,
    status_code=status.HTTP_200_OK,
)
def get_learner_summary(
    session: SessionDep, course_id: int, curr_user=Depends(verify_role(["user"]))
):
    return analytics_service.get_learner_course_overview(
        session, curr_user.id, course_id
    )


@router.get(
    "/courses/{course_id}/score-trends",
    response_model=list[ScoreTrendPoint],
    status_code=status.HTTP_200_OK,
)
def get_score_trends(
    course_id: int,
    session: SessionDep,
    curr_user=Depends(verify_role(["user"])),
):
    return analytics_service.get_learner_score_trends(session, curr_user.id, course_id)


@router.get(
    "/courses/{course_id}/instructor-dashboard",
    response_model=InstructorDashboardResponse,
    status_code=status.HTTP_200_OK,
)
def get_instructor_dashboard(
    course_id: int,
    session: SessionDep,
    curr_user = Depends(verify_role(["admin"]))
):
    return analytics_service.get_instructor_course_analytics(session, course_id, curr_user.username)
