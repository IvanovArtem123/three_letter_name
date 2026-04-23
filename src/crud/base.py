from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
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
    ) -> ModelType:
        """Создать объект из схемы `obj_in` и вернуть его."""
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновление объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> None:
        await session.delete(db_obj)
        await session.commit()
