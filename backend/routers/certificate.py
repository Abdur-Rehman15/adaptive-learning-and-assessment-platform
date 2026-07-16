from fastapi import status, APIRouter, Depends
from database.database import SessionDep
from middleware.verifyRole import verify_role
import services.certificate_service as certificate_service
from schemas.certificate_schema import CertificateResponse

router = APIRouter()


@router.get(
    "/certificates/download/{course_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "Returns the generated course certificate as a PDF file attachment download.",
        }
    },
)
def download_certificate(
    session: SessionDep, course_id: int, curr_user=Depends(verify_role(["user"]))
):
    return certificate_service.download_certificate(
        session, curr_user.id, curr_user.username, course_id
    )


@router.get(
    "/certificates/verify/{verification_code}",
    response_model=CertificateResponse,
    status_code=status.HTTP_200_OK,
)
def verify_certificate(session: SessionDep, verification_code: int):
    return certificate_service.verify_certificate_by_code(session, verification_code)
