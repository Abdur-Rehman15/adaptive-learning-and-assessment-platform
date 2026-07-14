from fastapi import status, APIRouter, Depends
from schemas.quizAttempt_schema import QuizAttemptResponse, QuizStartResponse
from database.database import SessionDep
import services.quizAttempt_service as quizAttempt_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/modules/{module_id}/quiz-attempts",
    response_model=QuizAttemptResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_role(["user"]))],
)
def get_module_quiz_attempt(session: SessionDep, module_id: int):
    return quizAttempt_service.get_module_quiz_attempt(session, module_id)


@router.post(
    "/modules/{module_id}/quiz-attempts/start",
    response_model=QuizStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_or_resume_quiz(
    session: SessionDep, module_id: int, curr_user=Depends(verify_role(["user"]))
):
    return quizAttempt_service.start_or_resume_quiz(session, module_id, curr_user.id)


@router.post(
    "/modules/{module_id}/quiz-attempts/retry",
    response_model=QuizStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def retry_quiz(
    session: SessionDep, module_id: int, curr_user=Depends(verify_role(["user"]))
):
    return quizAttempt_service.retry_quiz(session, module_id, curr_user.id)


@router.post(
    "/modules/{module_id}/quiz-attempts/submit",
    status_code=status.HTTP_200_OK,
)
def submit_quiz(session: SessionDep, module_id: int, curr_user=Depends(verify_role(["user"]))):
    return quizAttempt_service.submit_quiz(session, module_id, curr_user.id)
