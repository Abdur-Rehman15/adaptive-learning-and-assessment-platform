from fastapi import status, APIRouter, Depends
from schemas.enrollment_schema import (
    EnrollmentCreate,
    EnrollmentResponse,
)
from database.database import SessionDep
import services.enrollment_service as enrollment_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/enrollments/me",
    response_model=list[EnrollmentResponse],
    status_code=status.HTTP_200_OK,
)
def get_student_enrollments(
    session: SessionDep, curr_user=Depends(verify_role(["user"]))
):
    return enrollment_service.get_student_enrollments(session, curr_user.id)


@router.post(
    "/enroll/{course_id}",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_enrollment(
    session: SessionDep,
    course_id: int,
    enrollment_in: EnrollmentCreate,
    curr_user=Depends(verify_role(["user"])),
):
    return enrollment_service.create_enrollment(
        session, course_id, curr_user.id, enrollment_in
    )


@router.delete(
    "/unenroll/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_role(["admin"]))],
)
def unenroll_course(session: SessionDep, enrollment_id: int):
    return enrollment_service.unenroll_course(session, enrollment_id)
