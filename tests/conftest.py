import asyncio
from asyncio import AbstractEventLoop
from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from main import app
from src.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
)
from src.database import Base, get_async_session


DATABASE_URl_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


engine_test = create_async_engine(DATABASE_URl_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция-генератор для создания асинхронной сессии для тестовой БД
    """
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database() -> AsyncGenerator:
    """
    Функция для создания тестовой БД перед запуском тестов и удаления после окончания тестирования
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator[AbstractEventLoop, Any, None]:
    """
    Функция для работы с асинхронными функциями
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Функция для создания асинхронного тестового клиента
    """
    async with AsyncClient(app=app, base_url="http://test.io") as async_client:
        yield async_client
