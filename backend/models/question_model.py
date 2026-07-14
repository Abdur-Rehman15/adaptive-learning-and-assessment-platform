from typing import List
from sqlmodel import Field
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String
from schemas.question_schema import QuestionBase


class Question(QuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="module.id")
    options: List[str] = Field(sa_column=Column(ARRAY(String), nullable=False))
