from sqlmodel import Session, select
from models.notification_model import Notification
from schemas.notification_schema import NotificationCreate, NotificationUpdate


def get_notification_by_id(session: Session, notification_id: int):
    return session.exec(
        select(Notification).where(Notification.id == notification_id)
    ).first()


def create_notification(
    session: Session, user_id: int, notification_in: NotificationCreate
):
    db_notification = Notification.model_validate(notification_in)
    db_notification.user_id = user_id
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification


def get_unread_notifications(session: Session, user_id: int):
    statement = select(Notification).where(
        Notification.user_id == user_id, Notification.is_read == False
    )
    return session.exec(statement).all()


def read_notification(
    session: Session, notification_id: int, updated_notification: NotificationUpdate
):
    db_notification = get_notification_by_id(session, notification_id)
    updated = updated_notification.model_dump()
    for k, v in updated.items():
        setattr(db_notification, k, v)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification
