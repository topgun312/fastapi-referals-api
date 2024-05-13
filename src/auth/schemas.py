from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr


class UserRead(schemas.BaseUser[int]):
    """
    Схема для чтения данных пользователя
    """

    model_config = ConfigDict(extra="allow")

    id: int
    email: str
    username: str
    registered_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    referer_by: int


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания данных пользователя
    """

    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
