from fastapi import FastAPI
from sqlmodel import SQLModel
from database.database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    user,
    auth,
    course,
    module,
    question,
    enrollment,
    quizAttempt,
    quizAnswer,
    analytics
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(module.router)
app.include_router(question.router)
app.include_router(enrollment.router)
app.include_router(quizAttempt.router)
app.include_router(quizAnswer.router)
app.include_router(analytics.router)