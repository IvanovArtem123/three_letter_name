from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый CRUD класс."""

    def __init__(self, model: type[ModelType]) -> None:
        """Сохранить класс ORM-модели, с которой работает CRUD."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Вернуть объект по ID или None."""
        return await session.get(self.model, obj_id)

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> ModelType:
        """Создать объект из схемы `obj_in` и вернуть его."""
        obj_in_data = obj_in.model_dump()
        if user_id is not None:
            obj_in_data['user_id'] = user_id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
