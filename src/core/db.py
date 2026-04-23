from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker)
from sqlalchemy.orm import declarative_base, declared_attr
from collections.abc import AsyncIterator

from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """Возвращает асинхронную сессию БД для зависимостей FastAPI."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except (HTTPException, StarletteHTTPException) as e:
            await session.rollback()
            raise e
