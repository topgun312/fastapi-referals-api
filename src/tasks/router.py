from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session
from src.referal.models import ReferalCode
from src.tasks.tasks import send_email_report_referal_code


router = APIRouter(
    prefix="/report",
    tags=["tasks"],
)


@router.get("/get_email_referal_code", response_model=None)
@cache(expire=3600)
async def get_referal_code_report(
    email: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
) -> dict[str, str | None | int] | HTTPException:
    """
    Функция-эндпоинт для получения реферального кода на электронную почту по email пользователя
    """
    try:
        user_rc = await session.execute(select(User).filter(User.email == email))
        user_id = user_rc.scalar().id
        code = await session.execute(
            select(ReferalCode).filter(ReferalCode.user_id == user_id)
        )
        ref_code = code.scalar().code
        send_email_report_referal_code.delay(user.username, ref_code)
        return {"status": 200, "data": "Письмо отправлено", "details": None}
    except Exception:
        return HTTPException(
            status_code=400,
            detail={"status": "error", "details": "Введите корректный email"},
        )
