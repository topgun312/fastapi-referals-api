from typing import Any, AsyncGenerator

from fastapi import Depends
from fastapi_users.models import UserProtocol
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[UserProtocol, Any], Any]:
    """
    Функция для создани связи между полтзователем и БД
    """
    yield SQLAlchemyUserDatabase(session, User)
