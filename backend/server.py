from fastapi import FastAPI
from routers import users, tasks, auth
from sqlmodel import SQLModel
from database.database import engine
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)