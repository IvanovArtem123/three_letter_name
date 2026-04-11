from sqlalchemy import Column, String

from core.db import Base


class Panel(Base):
    """Модель панели."""

    __tablename__ = 'panels'
    path = Column(String(150), nullable=False)
    domain = Column(String(150), nullable=False)
    login = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    country = Column(String(150), nullable=False)
