from sqlalchemy import Column, String

from .base import BaseModel


class Panel(BaseModel):
    """Модель панели."""

    __tablename__ = 'panels'

    path = Column(String(150), nullable=False)
    domain = Column(String(150), nullable=False)
    login = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    country = Column(String(150), nullable=False)
