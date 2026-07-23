from fastapi import status, APIRouter, Depends
from schemas.quizAnswer_schema import (
    QuizAnswerCreate,
    QuizAnswerResponse,
    QuizAnswerSubmissionResponse,
)
from database.database import SessionDep
import services.quizAnswer_service as quizAnswer_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/quiz-attempts/{attempt_id}/answers",
    response_model=list[QuizAnswerResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_role(["user"]))],
)
def get_quiz_answers_by_attempt(session: SessionDep, attempt_id: int):
    return quizAnswer_service.get_quiz_answers_by_attempt(session, attempt_id)


@router.post(
    "/quiz-attempts/{question_id}/answers/{attempt_id}",
    response_model=QuizAnswerSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_role(["user"]))],
)
def create_quiz_answer(
    session: SessionDep,
    question_id: int,
    attempt_id: int,
    answer_in: QuizAnswerCreate,
    curr_user=Depends(verify_role(["user"])),
):
    return quizAnswer_service.create_quiz_answer(
        session, question_id, attempt_id, answer_in, curr_user.id
    )
