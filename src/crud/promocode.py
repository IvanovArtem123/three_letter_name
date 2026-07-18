from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.promocode import Promocode
from schemas.promocode import PromocodeCreate, PromocodeInfo


class CRUDPromocode(CRUDBase[Promocode, PromocodeCreate, PromocodeInfo]):
    '''CRUD для пользовательских промокодов.'''

    async def get_promocode_by_code(
        self,
        session: AsyncSession,
        code: str
    ) -> Promocode | None:
        '''Получить промокод по его коду.'''
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
        '''Создание промокода для конкретного пользователя.'''
        promocode = Promocode(
            code=obj_in.code,
            is_active=obj_in.is_active,
            is_activated=False,
            purpose=obj_in.purpose,
            end_date=obj_in.end_date,
            used_count=0,
            usage_limit=obj_in.usage_limit,
            sub_level=obj_in.sub_level,
            user_id=user_id,
            target_user_ids=obj_in.target_user_ids
        )
        session.add(promocode)
        await session.commit()
        await session.refresh(promocode)
        return promocode

    async def activate_gift_promo(
        self,
        session: AsyncSession,
        promocode: Promocode,
        sub_id: int
    ) -> Promocode:
        promocode.is_activated = True
        promocode.used_count += 1
        promocode.sub_id = sub_id
        session.add(promocode)
        await session.commit()
        await session.refresh(promocode)
        return promocode


promocode_crud = CRUDPromocode(Promocode)
