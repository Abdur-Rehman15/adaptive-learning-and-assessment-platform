from fastapi import FastAPI
from sqlmodel import SQLModel
from database.database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import user, auth, course

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
