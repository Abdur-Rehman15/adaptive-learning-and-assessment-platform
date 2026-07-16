from pydantic import BaseModel


class LearnerOverviewResponse(BaseModel):
    course_id: int
    progress_percent: float
    average_quiz_score: float
    weakest_topics: list[str]


class ScoreTrendPoint(BaseModel):
    attempt_id: int
    module_title: str
    final_score: float


class InstructorDashboardResponse(BaseModel):
    total_enrolled_learners: int
    course_average_progress: float
    completion_rate_percent: float
