import secrets

from fastapi import Header, HTTPException, status

from app.config import settings


def require_admin(x_admin_token: str = Header(default="")) -> None:
    """Читать данные может любой, менять только тот, у кого есть токен."""
    if not secrets.compare_digest(x_admin_token, settings.admin_token):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный токен администратора")
