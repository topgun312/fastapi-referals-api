import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(async_client: AsyncClient) -> None:
    """
    Тесрирование регистрации пользователя
    """
    response = await async_client.post(
        "/auth/register",
        json={
            "username": "username_test",
            "email": "email_test@gmail.com",
            "password": "password_test",
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["username"] == "username_test"
    assert response.json()["email"] == "email_test@gmail.com"


@pytest.mark.asyncio
async def test_login(async_client: AsyncClient) -> None:
    """
    Тестирование авторизации пользователя
    """
    response = await async_client.post(
        "/auth/jwt/login",
        data={
            "username": "email_test@gmail.com",
            "password": "password_test",
        },
    )
    assert response.status_code == 204
