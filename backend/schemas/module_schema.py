from sqlmodel import SQLModel, Field
from pydantic import HttpUrl, field_validator


class ModuleBase(SQLModel):
    title: str = Field(
        min_length=10, description="module title length should be atleast 10 characters"
    )
    order: int = Field(
        gt=0,
        unique=True,
        description="order number cannot be less than 1 and it will be unique",
    )
    content_url: str

    field_validator("content_url", mode="after")
    @classmethod
    def validate_url(cls, v: str) -> str:
        try:
            cleaned_url = v.strip()
            HttpUrl(cleaned_url)
        except Exception:
            raise ValueError("content url must be a valid link")
        return cleaned_url


class ModuleCreate(ModuleBase):
    pass


class ModuleResponse(ModuleBase):
    id: int
    course_id: int


class ModuleUpdate(SQLModel):
    title: str | None = None
    content_url: str | None = None


class ModuleUpdateOrder(SQLModel):
    module_id: int | None = None
    order: int | None = None
