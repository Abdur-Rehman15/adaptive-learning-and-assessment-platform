from sqlmodel import create_engine, Session
from fastapi import Depends
from typing import Annotated
import os
from dotenv import load_dotenv

from models.user_model import User
from models.course_model import Course
from models.module_model import Module
from models.question_model import Question
from models.quizAttempt_model import QuizAttempt
from models.quizAnswer_model import QuizAnswer
from models.enrollment_model import Enrollment
from models.certificate_model import Certificate
from models.notification_model import Notification

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_session():
  with Session(engine) as session:
    yield session

SessionDep = Annotated[Session, Depends(get_session)]