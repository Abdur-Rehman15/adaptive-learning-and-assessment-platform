import services.notification_service as notification_service
from schemas.notification_schema import NotificationCreate
from functools import wraps


def notify(type: str, message: str, user_id_pos: int = 2, session_pos: int = 0):
    def original(original_func):
        @wraps(original_func)
        def wrapper(*args, **kwargs):
            result = original_func(*args, **kwargs)
            session = kwargs.get("session") or (
                args[session_pos] if len(args) > session_pos else None
            )
            user_id = kwargs.get("user_id") or (
                args[user_id_pos] if len(args) > user_id_pos else None
            )

            if session and user_id:
                context = {**kwargs}
                if result and hasattr(result, "__dict__"):
                    context.update(
                        {
                            k: v
                            for k, v in result.__dict__.items()
                            if not k.startswith("_")
                        }
                    )
                try:
                    formatted_message = message.format(*args, **context)
                except Exception:
                    formatted_message = message

                notification_in = NotificationCreate(
                    type=type, message=formatted_message
                )
                notification_service.create_in_app_notification(
                    session, user_id, notification_in
                )

            return result

        return wrapper

    return original
