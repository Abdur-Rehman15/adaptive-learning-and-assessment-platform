from fastapi import Depends, HTTPException, status
from security.security import get_current_user
from models.user_model import User


def verify_role(allowed_roles: list[str]):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(403, "no access to this resource")
        return current_user

    return dependency
