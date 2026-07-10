from sqlmodel import SQLModel


class ModuleBase(SQLModel):
    title: str
    order: int
    content_url: str


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
