from fastapi import status, APIRouter, Depends
from schemas.module_schema import (
    ModuleCreate,
    ModuleResponse,
    ModuleUpdate,
    ModuleUpdateOrder,
)
from database.database import SessionDep
from models.user_model import User
from models.module_model import Module
import services.module_service as module_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/courses/{course_id}/modules",
    response_model=list[ModuleResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_role(["admin", "user"]))],
)
def get_course_modules(
    session: SessionDep,
    course_id: int,
):
    return module_service.get_course_modules(session, course_id)


@router.post(
    "/courses/{course_id}/modules",
    response_model=ModuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_module(
    session: SessionDep,
    course_id: int,
    module_in: ModuleCreate,
    current_user: User = Depends(verify_role(["admin"])),
):
    return module_service.create_module(
        session, course_id, module_in, current_user.username
    )


@router.patch(
    "/courses/{course_id}/modules/{module_id}",
    response_model=ModuleResponse,
    status_code=status.HTTP_200_OK,
)
def update_module(
    session: SessionDep,
    course_id: int,
    module_id: int,
    updated_module: ModuleUpdate,
    current_user: User = Depends(verify_role(["admin"])),
):
    return module_service.update_module(
        session, course_id, module_id, updated_module, current_user.username
    )


@router.patch(
    "/courses/{course_id}/modules",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_role(["admin"]))],
)
def update_modules_order(
    session: SessionDep, course_id: int, updated_list: list[ModuleUpdateOrder]
):
    module_service.update_modules_order(session, course_id, updated_list)
    return None


@router.delete(
    "/courses/{course_id}/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_module(
    session: SessionDep,
    course_id: int,
    module_id: int,
    current_user: User = Depends(verify_role(["admin"])),
):
    module_service.delete_module(session, course_id, module_id, current_user.username)
