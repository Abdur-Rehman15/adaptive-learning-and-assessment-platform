from sqlmodel import Session, select
from models.module_model import Module
from schemas.module_schema import ModuleCreate, ModuleUpdate, ModuleUpdateOrder


def get_module_by_id(session: Session, module_id: int):
    return session.exec(select(Module).where(Module.id == module_id)).first()


def get_course_modules(session: Session, course_id: int):
    return session.exec(select(Module).where(Module.course_id == course_id)).all()


def create_module(session: Session, course_id: int, module_in: ModuleCreate):
    course_module = Module.model_validate(module_in)
    course_module.course_id = course_id
    session.add(course_module)
    session.commit()
    session.refresh(course_module)
    return course_module


def update_module(session: Session, module_id: int, updated_module: ModuleUpdate):
    module = get_module_by_id(session, module_id)
    updated = updated_module.model_dump(exclude_unset=True)
    for k, v in updated.items():
        setattr(module, k, v)
    session.add(module)
    session.commit()
    session.refresh(module)
    return module


def update_modules_order(
    session: Session, course_id: int, order_data: list[ModuleUpdateOrder]
):
    modules = get_course_modules(session, course_id)
    module_map = {m.id: m for m in modules}
    for item in order_data:
        module_map[item.module_id].order = item.order

    session.commit()


def delete_module(session: Session, module_id: int):
    module = get_module_by_id(session, module_id)
    session.delete(module)
    session.commit()
