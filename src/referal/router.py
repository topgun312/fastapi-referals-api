import hashlib

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.database import get_async_session
from src.referal.models import ReferalCode
from src.referal.schemas import ReferalCodeCreate


router = APIRouter(
    prefix="/referals",
    tags=["referals"],
)


@router.get("/users/me")
def protected_route(user: User = Depends(current_user)) -> str:
    """
    Функция-эндпоинт для получения авторизованного пользователя
    """
    return f"Hello {user.username}"


@router.post("/create_referal_code", response_model=None)
async def create_referal_code(
    operation_new: ReferalCodeCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> dict[str, str] | HTTPException:
    """
    Функция-эндпоинт для создания реферального кода
    """
    if user:
        try:
            await session.execute(
                insert(ReferalCode).values(**operation_new.dict(), user_id=user.id)
            )
            await session.commit()
            return {"status": "Реферальный код создан"}
        except Exception:
            raise HTTPException(
                status_code=422,
                detail={
                    "status": "error",
                    "details": "Ошибка при введении данных при создании кода или код уже существует",
                },
            )
    else:
        return {"status": "Авторизуйтесь пожалуйста"}


@router.delete("/delete_referal_code", response_model=None)
async def delete_referal_code(
    ref_cod: str, session: AsyncSession = Depends(get_async_session)
) -> dict[str, str] | HTTPException:
    """
    Функция-эндпоинт для удаления реферального кода
    """
    try:
        await session.execute(delete(ReferalCode).filter(ReferalCode.code == ref_cod))
        await session.commit()
        return {"status": "Реферальный код удален"}
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "details": "Введен несуществующий код!"},
        )


@router.post("/register_referal", response_model=None)
async def register_referal(
    new_user: UserCreate,
    referalcode=None,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str] | HTTPException:
    """
    Функция-эндпоинт для регистрации пользователя по реферальному коду
    """
    try:

        ref_code = await session.execute(
            select(ReferalCode).filter(ReferalCode.code == referalcode)
        )
        user_id = ref_code.scalar().user_id
        data_dict = new_user.dict()
        password = data_dict.pop("password")
        hash_object = hashlib.md5(password.encode())
        data_dict["hashed_password"] = hash_object.hexdigest()
        reg_referal = insert(User).values(**data_dict, referer_by=user_id)
        await session.execute(reg_referal)
        await session.commit()
        return {"status": "Пользователь по реферальному коду зарегистрирован"}

    except Exception:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "details": "Введите корректные данные"},
        )


@router.get("/referal_info", response_model=None)
@cache(expire=3600)
async def get_referals(
    referer_id: int, session: AsyncSession = Depends(get_async_session)
) -> str | HTTPException:
    """
    Функция-эндпоинт для получения информации о рефералах по id пользователя
    """
    try:
        ref_list = []
        user = await session.execute(select(User).filter(User.id == referer_id))
        referals = await session.execute(
            select(User).filter(User.referer_by == referer_id)
        )
        user_res = user.scalar()
        referals_res = referals.scalars()
        for r in referals_res:
            ref_list.append(r.username)
        return (
            f'Список рефералов пользователя {user_res.username}: {", ".join(ref_list)}'
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "details": "Введите корректный id реферера"},
        )
