from fastapi import HTTPException
from sqlmodel import Session, select, func
from models import Enrollment, QuizAttempt, QuizAnswer, Question, Module
from schemas.analytics_schema import LearnerOverviewResponse, ScoreTrendPoint, InstructorDashboardResponse


