import asyncio
from typing import Any, Coroutine

import aiohttp
from fastapi import APIRouter, HTTPException

from src.config import API_KEY

router = APIRouter(prefix="/api", tags=["api_work"])


async def request(session, email: str) -> Coroutine | Any:
    async with session.get(
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEY}"
    ) as response:
        return await response.text()


async def email_verify_task(email: str) -> dict[str, Any]:
    """
    Функция для верификации email-адреса на сайте emailhunter.co
    """
    async with aiohttp.ClientSession() as session:
        try:
            task = request(session, email)
            result = await asyncio.gather(task)
            for res in result:
                return {
                    "status": res["data"]["status"],
                    "result": res["data"]["result"],
                    "email": res["data"]["email"],
                }
        except Exception:
            raise HTTPException(
                status_code=400,
                detail={"status": "error", "details": "Введен некорректный email!"},
            )


@router.get("/email_verify/")
async def main(email: str) -> None:
    """
    Функция-эндпоинт для верификации email-адреса
    :param email:
    """
    await email_verify_task(email)
    print("Email проверен!")
