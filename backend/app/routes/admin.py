from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.security import valid_admin_credentials

router = APIRouter(prefix="/api/admin", tags=["Админка"])


class AdminLogin(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=300)


@router.post("/login")
def login(credentials: AdminLogin):
    if not valid_admin_credentials(credentials.username, credentials.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный логин или пароль")
    return {"authenticated": True}
