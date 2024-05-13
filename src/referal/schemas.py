import random
import string
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing_extensions import LiteralString


def generate_referal_code() -> LiteralString:
    """
    Функция для автоматической генерации кода
    :return:
    """
    code_length = 10
    letters = string.ascii_letters + string.digits
    result = "".join(random.choice(letters) for _ in range(code_length))
    return result


class ReferalCodeCreate(BaseModel):
    """
    Схема для создания реферального кода
    """

    code: str = generate_referal_code()


class ReferalCodeRead(BaseModel):
    """
    Схема для чтения реферального кода
    """

    model_config = ConfigDict(extra="allow")

    id: int
    code: str
    created_at: datetime
    user_id: int
