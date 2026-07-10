from fastapi import status, APIRouter, Depends
from schemas.course_schema import CourseCreate, CourseResponse, CourseUpdate
from database.database import SessionDep
from models.user_model import User
import services.course_service as course_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/courses/me", response_model=list[CourseResponse], status_code=status.HTTP_200_OK
)
def get_creator_courses(
    session: SessionDep, current_user: User = Depends(verify_role(["admin"]))
):
    return course_service.get_creator_courses(session, current_user.username)


@router.get(
    "/courses", response_model=list[CourseResponse], status_code=status.HTTP_200_OK
)
def get_all_courses(session: SessionDep):
    return course_service.get_all_courses(session)


@router.post(
    "/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED
)
def create_course(
    course_in: CourseCreate,
    session: SessionDep,
    current_user: User = Depends(verify_role(["admin"])),
):
    return course_service.create_course(session, current_user.username, course_in)


@router.patch(
    "/courses/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK
)
def update_course(
    session: SessionDep,
    course_id: int,
    updated_course: CourseUpdate,
    current_user: User = Depends(verify_role(["admin"])),
):
    return course_service.update_course(
        session, course_id, current_user.username, updated_course
    )


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    session: SessionDep,
    course_id: int,
    current_user: User = Depends(verify_role(["admin"])),
):
    return course_service.delete_course(session, course_id, current_user.username)
