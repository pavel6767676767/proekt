import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import settings

admin_basic = HTTPBasic(auto_error=False)


def valid_admin_credentials(username: str, password: str) -> bool:
    if not settings.admin_password:
        return False
    return secrets.compare_digest(username, settings.admin_username) and secrets.compare_digest(password, settings.admin_password)


def require_admin(credentials: HTTPBasicCredentials | None = Depends(admin_basic)) -> None:
    """Чтение открыто, изменение данных доступно только администратору."""
    if not settings.admin_password:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Админка не настроена: задайте ADMIN_PASSWORD")
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Требуется вход администратора", headers={"WWW-Authenticate": "Basic"})
    if not valid_admin_credentials(credentials.username, credentials.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный логин или пароль", headers={"WWW-Authenticate": "Basic"})
