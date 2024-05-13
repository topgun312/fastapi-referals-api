from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from redis import asyncio as aioredis

from src.api_work.router import router as api_router
from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead
from src.config import REDIS_HOST, REDIS_PORT
from src.referal.router import router as referal_router
from src.tasks.router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Функция для запуска redis для кеширования при запуске приложения и закрытия redis при его остановке
    """
    print("starting db session")
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()
    print("shutdown db session")


app = FastAPI(title="Referals", lifespan=lifespan)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(referal_router)
app.include_router(task_router)
app.include_router(api_router)
