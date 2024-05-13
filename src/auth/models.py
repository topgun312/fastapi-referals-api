from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя
    """

    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    referer_by: int = Column(Integer, default=0, nullable=False)
    referalcode = relationship("ReferalCode", backref="referalcode", uselist=False)
