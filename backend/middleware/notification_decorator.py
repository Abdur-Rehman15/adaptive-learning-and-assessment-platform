import inspect
import services.notification_service as notification_service
from schemas.notification_schema import NotificationCreate
from functools import wraps
from models.user_model import User
from sqlmodel import select


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
                if isinstance(user_id, str):
                    user = session.exec(select(User).where(User.username == user_id)).first()
                    user_id = user.id if user else None

                if isinstance(user_id, int):
                    try:
                        sig = inspect.signature(original_func)
                        bound_args = sig.bind(*args, **kwargs)
                        bound_args.apply_defaults()
                        context = {**bound_args.arguments}
                    except Exception:
                        context = {**kwargs}

                    if result:
                        if isinstance(result, dict):
                            context.update(result)
                            for k, v in result.items():
                                if hasattr(v, "__dict__"):
                                    context.update(
                                        {
                                            key: val
                                            for key, val in v.__dict__.items()
                                            if not key.startswith("_")
                                        }
                                    )
                        elif hasattr(result, "__dict__"):
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

