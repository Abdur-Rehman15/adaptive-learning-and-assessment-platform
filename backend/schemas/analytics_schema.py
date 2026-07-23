from pydantic import BaseModel, Field


class LearnerOverviewResponse(BaseModel):
    course_id: int
    progress_percent: float = Field(
        ge=0.0,
        le=100.0,
        description="progress percentage should be in between 0 and 100",
    )
    average_quiz_score: float = Field(
        ge=0.0, le=100.0, description="avg quiz score should be in between 0 and 100"
    )
    weakest_topics: list[str]


class ScoreTrendPoint(BaseModel):
    attempt_id: int
    module_title: str
    final_score: float = Field(
        ge=0.0, le=100.0, description="final score should be in between 0 and 100"
    )


class InstructorModuleMetric(BaseModel):
    module_id: int
    title: str
    learners: int = Field(ge=0)
    completion_rate: float = Field(ge=0.0, le=100.0)
    average_score: float = Field(ge=0.0, le=100.0)


class InstructorLearnerMetric(BaseModel):
    user_id: int
    username: str
    progress_percent: float = Field(ge=0.0, le=100.0)
    score: float = Field(ge=0.0, le=100.0)
    status: str


class InstructorDashboardResponse(BaseModel):
    total_enrolled_learners: int = Field(ge=0)
    course_average_progress: float = Field(
        ge=0.0,
        le=100.0,
        description="course avg progress should be in between 0 and 100",
    )
    completion_rate_percent: float = Field(
        ge=0.0,
        le=100.0,
        description="completion rate percentage should be in between 0 and 100",
    )
    course_average_quiz_score: float = Field(
        ge=0.0,
        le=100.0,
        description="average quiz score across all completed attempts in the course",
    )
    modules: list[InstructorModuleMetric] = Field(default_factory=list)
    learners: list[InstructorLearnerMetric] = Field(default_factory=list)
