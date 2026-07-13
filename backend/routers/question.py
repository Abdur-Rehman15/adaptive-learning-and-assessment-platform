from fastapi import status, APIRouter, Depends
from schemas.question_schema import QuestionCreate, QuestionUpdate, QuestionResponse
from database.database import SessionDep
import services.question_service as question_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/modules/{module_id}/questions",
    response_model=list[QuestionResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_role(["admin", "user"]))],
)
def get_module_questions(session: SessionDep, module_id: int):
    return question_service.get_module_questions(session, module_id)


@router.post(
    "/modules/{module_id}/questions",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    session: SessionDep,
    module_id: int,
    question_in: QuestionCreate,
    current_user=Depends(verify_role(["admin"])),
):
    return question_service.create_question(
        session, module_id, question_in, current_user.username
    )


@router.patch(
    "/questions/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
def update_question(
    session: SessionDep,
    question_id: int,
    updated_question: QuestionUpdate,
    current_user=Depends(verify_role(["admin"])),
):
    return question_service.update_question(
        session, question_id, updated_question, current_user.username
    )


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    session: SessionDep,
    question_id: int,
    current_user=Depends(verify_role(["admin"])),
):
    question_service.delete_question(session, question_id, current_user.username)
