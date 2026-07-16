from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.promocode import Promocode
from schemas.promocode import PromocodeCreate, PromocodeInfo


class CRUDPromocode(CRUDBase[Promocode, PromocodeCreate, PromocodeInfo]):
    """CRUD для пользовательских промокодов."""

    async def get_code(
        self,
        session: AsyncSession,
        code: str
    ) -> Promocode | None:
        """Получить промокод по его коду."""
        result = await session.execute(
            select(Promocode).where(Promocode.code == code)
        )
        promocode = result.scalars().first()
        return promocode

    async def create_promo(
            self,
            session: AsyncSession,
            obj_in: PromocodeCreate,
            user_id: int) -> Promocode:
        """Создание промокода для конкретного пользователя."""
        promocode = Promocode(
            user_id=user_id,
            code=obj_in.code,
            is_active=obj_in.is_active,
            usage_limit=obj_in.usage_limit,
            purpose=obj_in.purpose,
            target_user_ids=obj_in.target_user_ids,
            end_date=datetime.fromisoformat(obj_in.end_date) if obj_in.end_date else None
        )
        session.add(promocode)
        await session.commit()
        await session.refresh(promocode)
        return promocode

promocode_crud = CRUDPromocode(Promocode)
