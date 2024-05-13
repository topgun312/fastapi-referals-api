from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String

from src.database import Base


class ReferalCode(Base):
    """
    Модель реферального кода
    """

    __tablename__ = "referalcodes"
    id: int = Column(Integer, primary_key=True)
    code: str = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user_id: int = Column(ForeignKey("users.id"), unique=True, nullable=False)
