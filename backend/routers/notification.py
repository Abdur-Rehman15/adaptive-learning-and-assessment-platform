from fastapi import status, APIRouter, Depends
from schemas.notification_schema import NotificationUpdate, NotificationResponse
from database.database import SessionDep
import services.notification_service as notification_service
from middleware.verifyRole import verify_role

router = APIRouter()


@router.get(
    "/notifications",
    response_model=list[NotificationResponse],
    status_code=status.HTTP_200_OK,
)
def get_unread_notifications(
    session: SessionDep, curr_user=Depends(verify_role(["user"]))
):
    return notification_service.get_unread_notifications(session, curr_user.id)


@router.patch(
    "/notification/{notification_id}/read",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
def read_notification(
    session: SessionDep, notification_id: int, curr_user=Depends(verify_role(["user"]))
):
    return notification_service.read_notification(
        session, curr_user.id, notification_id
    )
