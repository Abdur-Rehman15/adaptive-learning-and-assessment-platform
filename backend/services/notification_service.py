from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.notification_schema import NotificationCreate
import repositories.notification_repo as notification_repo


def create_in_app_notification(
    session: Session, user_id: int, notification_in: NotificationCreate
):
    return notification_repo.create_notification(session, user_id, notification_in)


def get_unread_notifications(session: Session, user_id: int):
    return notification_repo.get_unread_notifications(session, user_id)


def read_notification(session: Session, user_id: int, notification_id: int):
    notification = notification_repo.get_notification_by_id(session, notification_id)
    if not notification:
        raise HTTPException(404, "notification not found")
    user_notifications = get_unread_notifications(session, user_id)
    notification_ids = {n.id for n in user_notifications}
    if notification_id not in notification_ids:
        raise HTTPException(
            403, "you are not allowed to modify notifications other than yours"
        )
    return notification_repo.read_notification(session, notification_id)
